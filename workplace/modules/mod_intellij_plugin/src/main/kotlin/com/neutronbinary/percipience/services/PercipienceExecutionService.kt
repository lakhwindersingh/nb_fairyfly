package com.neutronbinary.percipience.services

import com.intellij.openapi.components.Service
import com.intellij.openapi.project.Project
import com.intellij.openapi.vfs.VirtualFileManager
import com.neutronbinary.percipience.bootstrap.WorkspaceBootstrapper
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.BufferedReader
import java.io.File
import java.io.InputStreamReader

data class ExecutionResult(
    val exitCode: Int,
    val stdout: String,
    val stderr: String,
    val command: String,
    val success: Boolean
)

@Service(Service.Level.PROJECT)
class PercipienceExecutionService(private val project: Project) {

    companion object {
        fun getInstance(project: Project): PercipienceExecutionService {
            return project.getService(PercipienceExecutionService::class.java)
        }
    }

    @Volatile
    private var cachedPythonExecutable: String? = null

    private fun testPythonCandidate(executablePath: String, requireYaml: Boolean): Boolean {
        return try {
            val testCode = if (requireYaml) {
                "import yaml, json, sys; sys.exit(0)"
            } else {
                "import json, sys; sys.exit(0)"
            }
            val pb = ProcessBuilder(executablePath, "-c", testCode)
            pb.redirectErrorStream(true)
            val process = pb.start()
            val finished = process.waitFor(1200, java.util.concurrent.TimeUnit.MILLISECONDS)
            finished && process.exitValue() == 0
        } catch (_: Exception) {
            false
        }
    }

    fun findPythonExecutable(): String {
        cachedPythonExecutable?.let { cached ->
            val f = File(cached)
            if ((f.exists() && f.canExecute()) || cached == "python3") {
                return cached
            }
        }

        val basePath = project.basePath
        val candidatePaths = mutableListOf<String>()

        // 1. Virtual environments in current project root
        if (basePath != null) {
            val root = File(basePath)
            listOf(
                File(root, ".venv/bin/python3"),
                File(root, ".venv/bin/python"),
                File(root, "venv/bin/python3"),
                File(root, "venv/bin/python"),
                File(root, ".env/bin/python3"),
                File(root, ".env/bin/python"),
                File(root, "env/bin/python3"),
                File(root, "env/bin/python")
            ).forEach { if (it.exists() && it.canExecute()) candidatePaths.add(it.absolutePath) }
        }

        // 2. Known Framework and system Python installations on macOS/Linux/Unix
        val userHome = System.getProperty("user.home") ?: ""
        val knownSystemCandidates = listOf(
            "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3",
            "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3",
            "/Library/Frameworks/Python.framework/Versions/3.10/bin/python3",
            "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3",
            "/Library/Frameworks/Python.framework/Versions/Current/bin/python3",
            "/usr/bin/python3",
            "/usr/local/bin/python3",
            "/opt/homebrew/bin/python3",
            "$userHome/.pyenv/shims/python3",
            "$userHome/.pyenv/shims/python",
            "$userHome/miniconda3/bin/python3",
            "$userHome/anaconda3/bin/python3",
            "python3",
            "python"
        )
        candidatePaths.addAll(knownSystemCandidates)

        // Pass 1: Prioritize an interpreter that has 'yaml' (PyYAML) installed
        for (cand in candidatePaths) {
            val f = File(cand)
            val exists = f.exists() && f.canExecute()
            val isCommand = cand == "python3" || cand == "python"
            if (exists || isCommand) {
                if (testPythonCandidate(cand, requireYaml = true)) {
                    cachedPythonExecutable = cand
                    return cand
                }
            }
        }

        // Pass 2: Fallback to any working python3/python interpreter
        for (cand in candidatePaths) {
            val f = File(cand)
            val exists = f.exists() && f.canExecute()
            val isCommand = cand == "python3" || cand == "python"
            if (exists || isCommand) {
                if (testPythonCandidate(cand, requireYaml = false)) {
                    cachedPythonExecutable = cand
                    return cand
                }
            }
        }

        val fallback = "python3"
        cachedPythonExecutable = fallback
        return fallback
    }

    fun getPercipienceBinary(): File {
        val basePath = project.basePath ?: throw IllegalStateException("Project base path is null")
        val root = File(basePath)
        val bin = File(root, ".nb/bin/percipience")
        if (!bin.exists()) {
            WorkspaceBootstrapper.bootstrapWorkspace(basePath)
        }
        if (!bin.canExecute()) {
            bin.setExecutable(true, false)
        }
        return bin
    }

    suspend fun executeCommand(
        subcommand: String,
        args: List<String> = emptyList(),
        onOutput: ((String) -> Unit)? = null
    ): ExecutionResult = withContext(Dispatchers.IO) {
        val basePath = project.basePath ?: return@withContext ExecutionResult(
            exitCode = 1,
            stdout = "",
            stderr = "No project base path found",
            command = subcommand,
            success = false
        )

        val bin = getPercipienceBinary()
        val python = findPythonExecutable()

        val fullCommand = mutableListOf<String>()
        fullCommand.add(python)
        fullCommand.add(bin.absolutePath)
        fullCommand.add(subcommand)
        fullCommand.addAll(args)

        val pb = ProcessBuilder(fullCommand)
        pb.directory(File(basePath))
        pb.redirectErrorStream(false)

        val env = pb.environment()
        env["PERCIPIENCE_ROOT"] = basePath
        env["PERCIPIENCE_CLI_HEADLESS"] = "1"
        env["PYTHONUNBUFFERED"] = "1"

        return@withContext try {
            val process = pb.start()

            val stdoutBuilder = StringBuilder()
            val stderrBuilder = StringBuilder()

            val stdoutReader = BufferedReader(InputStreamReader(process.inputStream))
            val stderrReader = BufferedReader(InputStreamReader(process.errorStream))

            val stdoutThread = Thread {
                stdoutReader.lineSequence().forEach { line ->
                    stdoutBuilder.append(line).append("\n")
                    onOutput?.invoke(line)
                }
            }
            val stderrThread = Thread {
                stderrReader.lineSequence().forEach { line ->
                    stderrBuilder.append(line).append("\n")
                }
            }

            stdoutThread.start()
            stderrThread.start()

            val exitCode = process.waitFor()
            stdoutThread.join(2000)
            stderrThread.join(2000)

            // Refresh VFS to reflect newly created / updated files in IDE
            VirtualFileManager.getInstance().asyncRefresh(null)

            ExecutionResult(
                exitCode = exitCode,
                stdout = stdoutBuilder.toString().trim(),
                stderr = stderrBuilder.toString().trim(),
                command = fullCommand.joinToString(" "),
                success = (exitCode == 0)
            )
        } catch (ex: Exception) {
            ExecutionResult(
                exitCode = 1,
                stdout = "",
                stderr = "Failed to execute percipience: ${ex.message}",
                command = fullCommand.joinToString(" "),
                success = false
            )
        }
    }

    suspend fun runGatekeeper() = executeCommand("gate")

    suspend fun runMerkleAudit(enforceMerkleChain: Boolean = true, minMaturity: Double = 0.85) =
        executeCommand("audit", listOf("--min-maturity", minMaturity.toString()))

    suspend fun runBasicCicd() = executeCommand("cicd")

    suspend fun runValidateLayered() = executeCommand("layer", listOf("validate"))

    suspend fun runTokensSummary() = executeCommand("tokens", listOf("summary"))

    suspend fun runWorktreesList() = executeCommand("worktrees", listOf("list"))

    suspend fun runCustomAgent(agentName: String, taskDescription: String) =
        executeCommand("agent", listOf("run", agentName, "--task", taskDescription))

    suspend fun runDriftCheck() = executeCommand("drift", listOf("check"))

    suspend fun runLayerPack(domainPlanPath: String, outputPath: String) =
        executeCommand("layer", listOf("pack", domainPlanPath, "-o", outputPath))

    suspend fun runProvisionPortal(tier: String) =
        executeCommand("portal", listOf("provision", "--tier", tier))

    suspend fun runDriftReport() = executeCommand("drift", listOf("report"))

    suspend fun runSwarmInspect() = executeCommand("swarm", listOf("inspect"))

    suspend fun runVpcSync() = executeCommand("vpc", listOf("sync"))

    suspend fun runWormEgressAudit() = executeCommand("worm", listOf("audit"))

    suspend fun runAgentWrap(agentName: String, format: String) =
        executeCommand("terminal", listOf("wrap", agentName, "--format", format))

    suspend fun runContextExport(format: String, outputFile: String) =
        executeCommand("terminal", listOf("export", "--format", format, "-o", outputFile))
}
