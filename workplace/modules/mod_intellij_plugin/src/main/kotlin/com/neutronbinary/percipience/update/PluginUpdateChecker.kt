package com.neutronbinary.percipience.update

import java.io.File
import java.io.InputStream
import java.util.zip.ZipFile

/**
 * Installed / candidate plugin version manifest, mirroring the canonical
 * Python engine `plugin_update_resolver.py`.
 */
data class PluginVersionInfo(
    val pluginVersion: String = "0.0.0",
    val platformVersion: String = "7.5.0",
    val tier: String = "plan_free",
    val channel: String = "stable",
    val manifestSchema: Int = PluginUpdateChecker.MANIFEST_SCHEMA,
    val releasedAt: String? = null
)

data class UpgradeCandidate(
    val version: PluginVersionInfo,
    val path: String,
    val kind: String,
    val source: String
) {
    val pluginVersion: String get() = version.pluginVersion
}

data class UpgradeCheckResult(
    val currentVersion: String,
    val appliedRuntimeVersion: String?,
    val candidates: List<UpgradeCandidate>,
    val selected: UpgradeCandidate?
) {
    val upgradeAvailable: Boolean get() = selected != null
}

data class UpgradeResult(
    val status: String,
    val pluginVersion: String,
    val previousVersion: String?,
    val tier: String,
    val source: String,
    val filesUpgraded: Int
)

/**
 * Offline, local-file-system-only plugin auto-upgrade resolver.
 *
 * Discovers locally-available Percipience plugin / runtime updates, compares
 * semantic versions against the currently installed plugin, and materializes a
 * newer candidate's payload into the workspace `.nb/` tree. No network access.
 */
object PluginUpdateChecker {

    const val MANIFEST_SCHEMA = 1
    const val MANIFEST_FILENAME = "version.json"
    const val EMBEDDED_MANIFEST_RESOURCE = "/percipience/version.json"
    const val RUNTIME_VERSION_RELPATH = ".nb/config/runtime_version.json"

    private val ARCHIVE_MANIFEST_PATHS = listOf("percipience/version.json", "version.json")

    /** Payload directory (inside a candidate archive / staged dir) -> workspace dest. */
    private val PAYLOAD_MAP = mapOf(
        "core" to ".nb/core",
        "bin" to ".nb/bin",
        "config" to ".nb/config",
        "workflows" to ".nb/agentic/custom/workflows",
        "hooks" to ".nb/git_hooks",
        "scripts" to ".nb/scripts",
        "plan" to ".nb/plan"
    )

    // ------------------------------------------------------------------ //
    // Semver
    // ------------------------------------------------------------------ //

    fun parseSemver(version: String?): List<Int> {
        if (version.isNullOrBlank()) return listOf(0, 0, 0)
        val core = version.trim().removePrefix("v").removePrefix("V")
            .substringBefore("-").substringBefore("+")
        val parts = core.split(".").map { chunk ->
            chunk.filter { it.isDigit() }.toIntOrNull() ?: 0
        }.toMutableList()
        while (parts.size < 3) parts.add(0)
        return parts.take(3)
    }

    fun isNewer(candidate: String?, current: String?): Boolean {
        val a = parseSemver(candidate)
        val b = parseSemver(current)
        for (i in 0 until 3) {
            if (a[i] != b[i]) return a[i] > b[i]
        }
        return false
    }

    // ------------------------------------------------------------------ //
    // Minimal JSON field extraction (no external dependency)
    // ------------------------------------------------------------------ //

    private fun jsonString(text: String, key: String): String? =
        Regex("\"" + Regex.escape(key) + "\"\\s*:\\s*\"([^\"]*)\"").find(text)?.groupValues?.get(1)

    private fun jsonInt(text: String, key: String): Int? =
        Regex("\"" + Regex.escape(key) + "\"\\s*:\\s*(-?\\d+)").find(text)?.groupValues?.get(1)?.toIntOrNull()

    private fun parseManifest(text: String): PluginVersionInfo? {
        val version = jsonString(text, "plugin_version") ?: return null
        return PluginVersionInfo(
            pluginVersion = version,
            platformVersion = jsonString(text, "platform_version") ?: "7.5.0",
            tier = jsonString(text, "tier") ?: "plan_free",
            channel = jsonString(text, "channel") ?: "stable",
            manifestSchema = jsonInt(text, "manifest_schema") ?: MANIFEST_SCHEMA,
            releasedAt = jsonString(text, "released_at")
        )
    }

    // ------------------------------------------------------------------ //
    // Installed / applied version
    // ------------------------------------------------------------------ //

    fun installedVersionInfo(): PluginVersionInfo {
        try {
            val stream: InputStream? = javaClass.getResourceAsStream(EMBEDDED_MANIFEST_RESOURCE)
            if (stream != null) {
                val text = stream.bufferedReader(Charsets.UTF_8).use { it.readText() }
                parseManifest(text)?.let { return it }
            }
        } catch (_: Exception) {
        }
        return PluginVersionInfo(pluginVersion = "0.0.0")
    }

    fun appliedRuntimeVersion(projectBasePath: String?): String? {
        if (projectBasePath.isNullOrBlank()) return null
        val marker = File(projectBasePath, RUNTIME_VERSION_RELPATH)
        if (!marker.isFile) return null
        return try {
            jsonString(marker.readText(Charsets.UTF_8), "plugin_version")
        } catch (_: Exception) {
            null
        }
    }

    // ------------------------------------------------------------------ //
    // Discovery
    // ------------------------------------------------------------------ //

    fun defaultUpdateDirs(projectBasePath: String, env: Map<String, String> = System.getenv()): List<File> {
        val dirs = mutableListOf<File>()
        env["PERCIPIENCE_UPDATE_DIR"]?.split(File.pathSeparatorChar)?.forEach { part ->
            if (part.isNotBlank()) dirs.add(File(part.trim()))
        }
        val base = File(projectBasePath)
        dirs.add(File(base, ".nb/bundles"))
        dirs.add(File(base, ".nb/updates"))
        val home = env["HOME"] ?: System.getProperty("user.home") ?: ""
        if (home.isNotBlank()) dirs.add(File(home, ".percipience/updates"))
        return dirs
    }

    private fun readManifestFromDir(dir: File): PluginVersionInfo? {
        val candidates = listOf(
            File(dir, "percipience/$MANIFEST_FILENAME"),
            File(dir, MANIFEST_FILENAME)
        )
        for (f in candidates) {
            if (f.isFile) {
                try {
                    parseManifest(f.readText(Charsets.UTF_8))?.let { return it }
                } catch (_: Exception) {
                }
            }
        }
        return null
    }

    /**
     * Resolves the archive that actually carries the `percipience/` payload,
     * unwrapping the JetBrains distribution layout `<plugin>/lib/<plugin>.jar`
     * when required. Returns a caller-owned temp file to delete, or null.
     */
    private fun resolvePayloadArchive(archive: File): Pair<File, Boolean> {
        try {
            ZipFile(archive).use { zf ->
                val names = zf.entries().toList().map { it.name }
                val hasPayload = names.any { it.contains("percipience/") }
                if (hasPayload) return archive to false
                val innerJar = names.firstOrNull { it.lowercase().endsWith(".jar") }
                if (innerJar != null) {
                    val tmp = File.createTempFile("percipience_inner_", ".jar")
                    zf.getInputStream(zf.getEntry(innerJar)).use { input ->
                        tmp.outputStream().use { output -> input.copyTo(output) }
                    }
                    return tmp to true
                }
            }
        } catch (_: Exception) {
        }
        return archive to false
    }

    private fun readManifestFromArchive(archive: File): PluginVersionInfo? {
        if (!archive.isFile) return null
        val (resolved, isTemp) = resolvePayloadArchive(archive)
        try {
            ZipFile(resolved).use { zf ->
                for (rel in ARCHIVE_MANIFEST_PATHS) {
                    val entry = zf.getEntry(rel) ?: continue
                    try {
                        val text = zf.getInputStream(entry).bufferedReader(Charsets.UTF_8).use { it.readText() }
                        parseManifest(text)?.let { return it }
                    } catch (_: Exception) {
                    }
                }
            }
        } catch (_: Exception) {
        } finally {
            if (isTemp) resolved.delete()
        }
        return null
    }

    fun discoverLocalCandidates(
        projectBasePath: String,
        env: Map<String, String> = System.getenv()
    ): List<UpgradeCandidate> {
        val candidates = mutableListOf<UpgradeCandidate>()
        val seen = mutableSetOf<String>()

        fun add(file: File, source: String) {
            val info = (if (file.isDirectory) readManifestFromDir(file) else readManifestFromArchive(file))
                ?: return
            val key = "${info.pluginVersion}|${file.absolutePath}"
            if (!seen.add(key)) return
            candidates.add(
                UpgradeCandidate(
                    version = info,
                    path = file.absolutePath,
                    kind = if (file.isDirectory) "dir" else "archive",
                    source = source
                )
            )
        }

        for (dir in defaultUpdateDirs(projectBasePath, env)) {
            if (!dir.exists()) continue
            if (File(dir, MANIFEST_FILENAME).isFile || File(dir, "percipience/$MANIFEST_FILENAME").isFile) {
                add(dir, dir.absolutePath)
                continue
            }
            dir.listFiles()?.sortedBy { it.name }?.forEach { entry ->
                when {
                    entry.isDirectory -> add(entry, dir.absolutePath)
                    entry.isFile && (entry.name.endsWith(".jar") || entry.name.endsWith(".zip")) ->
                        add(entry, dir.absolutePath)
                }
            }
        }

        return candidates.sortedByDescending { parseSemver(it.pluginVersion).let { v -> v[0] * 1_000_000 + v[1] * 1_000 + v[2] } }
    }

    fun selectUpgrade(currentVersion: String, candidates: List<UpgradeCandidate>): UpgradeCandidate? {
        return candidates
            .filter { it.version.manifestSchema == MANIFEST_SCHEMA && isNewer(it.pluginVersion, currentVersion) }
            .maxByOrNull { parseSemver(it.pluginVersion).let { v -> v[0] * 1_000_000 + v[1] * 1_000 + v[2] } }
    }

    fun checkForUpgrade(projectBasePath: String, env: Map<String, String> = System.getenv()): UpgradeCheckResult {
        val current = installedVersionInfo().pluginVersion
        val candidates = discoverLocalCandidates(projectBasePath, env)
        val selected = selectUpgrade(current, candidates)
        return UpgradeCheckResult(
            currentVersion = current,
            appliedRuntimeVersion = appliedRuntimeVersion(projectBasePath),
            candidates = candidates,
            selected = selected
        )
    }

    // ------------------------------------------------------------------ //
    // Apply
    // ------------------------------------------------------------------ //

    fun applyRuntimeUpgrade(projectBasePath: String, candidate: UpgradeCandidate): UpgradeResult {
        val root = File(projectBasePath)
        val previous = appliedRuntimeVersion(projectBasePath)
        val source = File(candidate.path)
        val upgraded = mutableListOf<String>()

        if (source.isDirectory) {
            for ((rootRel, destRel) in PAYLOAD_MAP) {
                val base = File(source, rootRel)
                if (!base.exists()) continue
                base.walkTopDown().forEach { f ->
                    if (f.isFile && !f.name.startsWith(".")) {
                        val rel = f.relativeTo(base).path
                        val dest = File(root, "$destRel/$rel")
                        dest.parentFile?.mkdirs()
                        f.copyTo(dest, overwrite = true)
                        if (rootRel in listOf("bin", "hooks", "scripts")) dest.setExecutable(true, false)
                        upgraded.add(dest.relativeTo(root).path)
                    }
                }
            }
        } else {
            val (resolved, isTemp) = resolvePayloadArchive(source)
            try {
                ZipFile(resolved).use { zf ->
                    for (entry in zf.entries()) {
                        val name = entry.name
                        if (name.endsWith("/")) continue
                        val idx = name.indexOf("percipience/")
                        if (idx == -1) continue
                        val rel = name.substring(idx + "percipience/".length)
                        val rootRel = rel.substringBefore("/")
                        val subRel = if (rel.contains("/")) rel.substringAfter("/") else rel
                        val destRel = PAYLOAD_MAP[rootRel] ?: continue
                        val dest = File(root, "$destRel/$subRel")
                        dest.parentFile?.mkdirs()
                        zf.getInputStream(entry).use { input ->
                            dest.outputStream().use { output -> input.copyTo(output) }
                        }
                        if (rootRel in listOf("bin", "hooks", "scripts")) dest.setExecutable(true, false)
                        upgraded.add(dest.relativeTo(root).path)
                    }
                }
            } finally {
                if (isTemp) resolved.delete()
            }
        }

        val marker = File(root, RUNTIME_VERSION_RELPATH)
        marker.parentFile?.mkdirs()
        val record = buildString {
            append("{\n")
            append("  \"plugin_version\": \"${candidate.pluginVersion}\",\n")
            append("  \"platform_version\": \"${candidate.version.platformVersion}\",\n")
            append("  \"tier\": \"${candidate.version.tier}\",\n")
            append("  \"channel\": \"${candidate.version.channel}\",\n")
            append("  \"applied_at\": \"${java.time.Instant.now()}\",\n")
            append("  \"source\": \"${candidate.path}\",\n")
            append("  \"source_kind\": \"${candidate.kind}\",\n")
            append("  \"previous_version\": ${previous?.let { "\"$it\"" } ?: "null"},\n")
            append("  \"files_upgraded\": ${upgraded.size}\n")
            append("}\n")
        }
        marker.writeText(record, Charsets.UTF_8)

        return UpgradeResult(
            status = "UPGRADED",
            pluginVersion = candidate.pluginVersion,
            previousVersion = previous,
            tier = candidate.version.tier,
            source = candidate.path,
            filesUpgraded = upgraded.size
        )
    }
}
