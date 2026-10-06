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
        env["PYTHONPATH"] = "${File(basePath, ".nb").absolutePath}:${File(basePath, ".nb/core").absolutePath}:${File(basePath, "workplace").absolutePath}"

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
                    onOutput?.invoke("[STDERR] $line")
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

    suspend fun runWorktreesList(onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return runWorktreeList(onOutput)
    }

    suspend fun runAgentList(onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("agent", listOf("list"), onOutput)
    }

    suspend fun runCustomAgent(agentName: String, taskDescription: String, onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("agent", listOf("run", agentName, "--task", taskDescription), onOutput)
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

    suspend fun runSwarmInspect(onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("swarm", listOf("inspect"), onOutput)
    }

    suspend fun runEgressList(onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("egress", listOf("list"), onOutput)
    }

    suspend fun runWormEgressAudit(onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("worm", listOf("audit"), onOutput)
    }

    suspend fun runRepoStatus(onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("repo", listOf("status"), onOutput)
    }

    suspend fun runVpcSync(onOutput: ((String) -> Unit)? = null): ExecutionResult {
        return executeCommand("vpc", listOf("sync"), onOutput)
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
