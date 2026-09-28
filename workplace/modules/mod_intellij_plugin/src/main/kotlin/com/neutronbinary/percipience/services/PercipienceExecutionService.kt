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

    fun findPythonExecutable(): String {
        val basePath = project.basePath
        if (basePath != null) {
            val root = File(basePath)
            val venvCandidates = listOf(
                File(root, ".venv/bin/python3"),
                File(root, ".venv/bin/python"),
                File(root, "venv/bin/python3"),
                File(root, "venv/bin/python"),
                File(root, ".env/bin/python3")
            )
            for (c in venvCandidates) {
                if (c.exists() && c.canExecute()) {
                    return c.absolutePath
                }
            }
        }

        // Check system python3 candidates
        val systemCandidates = listOf(
            "/opt/homebrew/bin/python3",
            "/usr/local/bin/python3",
            "/usr/bin/python3",
            "python3",
            "python"
        )
        for (c in systemCandidates) {
            val f = File(c)
            if (f.exists() && f.canExecute()) {
                return f.absolutePath
            }
        }
        return "python3"
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
        pb.environment()["PYTHONUNBUFFERED"] = "1"
        pb.environment()["PYTHONPATH"] = "${File(basePath, ".nb").absolutePath}:${File(basePath, ".nb/core").absolutePath}:${File(basePath, "workplace").absolutePath}"

        val stdoutSb = StringBuilder()
        val stderrSb = StringBuilder()

        try {
            val process = pb.start()

            val stdoutReader = BufferedReader(InputStreamReader(process.inputStream))
            val stderrReader = BufferedReader(InputStreamReader(process.errorStream))

            var line: String?
            while (stdoutReader.readLine().also { line = it } != null) {
                val l = line ?: ""
                stdoutSb.appendLine(l)
                onOutput?.invoke(l)
            }

            while (stderrReader.readLine().also { line = it } != null) {
                val l = line ?: ""
                stderrSb.appendLine(l)
                onOutput?.invoke("[STDERR] $l")
            }

            val exitCode = process.waitFor()
            VirtualFileManager.getInstance().asyncRefresh(null)

            ExecutionResult(
                exitCode = exitCode,
                stdout = stdoutSb.toString().trim(),
                stderr = stderrSb.toString().trim(),
                command = fullCommand.joinToString(" "),
                success = exitCode == 0
            )
        } catch (e: Exception) {
            ExecutionResult(
                exitCode = 1,
                stdout = stdoutSb.toString().trim(),
                stderr = e.message ?: "Unknown process execution error",
                command = fullCommand.joinToString(" "),
                success = false
            )
        }
    }

    suspend fun runGatekeeper(onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("gate", emptyList(), onOutput)
    }

    suspend fun runMerkleAudit(
        enforceMerkleChain: Boolean = true,
        minMaturity: Double = 0.85,
        onOutput: ((String) -> Unit)? = null
    ): ExecutionResult {
        val args = mutableListOf<String>()
        if (enforceMerkleChain) {
            args.add("--enforce-merkle-chain")
        }
        args.add("--min-maturity")
        args.add(minMaturity.toString())
        return executeCommand("audit", args, onOutput)
    }

    suspend fun runBasicCicd(onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("cicd", listOf("run"), onOutput)
    }

    suspend fun runValidateLayered(onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("validate", listOf("--layered"), onOutput)
    }

    suspend fun runTokensSummary(onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("tokens", listOf("summary"), onOutput)
    }

    suspend fun runTerminalStatus(onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("terminal", listOf("status"), onOutput)
    }

    suspend fun runWorktreeList(onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("worktree", listOf("list"), onOutput)
    }

    suspend fun runAgentList(onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("agent", listOf("list"), onOutput)
    }

    suspend fun runDriftCheck(onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("drift", listOf("check"), onOutput)
    }

    suspend fun runDriftReport(onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("drift", listOf("report"), onOutput)
    }

    suspend fun runLayerPack(planPath: String, outputPath: String, onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("layer", listOf("pack", "--plan", planPath, "--output", outputPath), onOutput)
    }

    suspend fun runProvisionPortal(target: String = "all", onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("provision", listOf("--target", target), onOutput)
    }

    suspend fun runSwarmAudit(onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("swarm", listOf("audit"), onOutput)
    }

    suspend fun runEgressList(onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("egress", listOf("list"), onOutput)
    }

    suspend fun runRepoStatus(onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("repo", listOf("status"), onOutput)
    }

    suspend fun runContextExport(format: String = "claude-code", outputPath: String? = null, onOutput: ((String) -> Unit)? = null): ExecutionResult {
        val args = mutableListOf("export", "--format", format)
        if (outputPath != null) {
            args.add("--output")
            args.add(outputPath)
        }
        return executeCommand("context", args, onOutput)
    }

    suspend fun runAgentWrap(agent: String = "claude", format: String? = null, onOutput: ((String) -> Unit)? = null): ExecutionResult {
        val args = mutableListOf("wrap", "--agent", agent)
        if (format != null) {
            args.add("--format")
            args.add(format)
        }
        return executeCommand("terminal", args, onOutput)
    }

    suspend fun runTerminalHook(shell: String = "zsh", onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("terminal", listOf("hook", "--shell", shell), onOutput)
    }
}
