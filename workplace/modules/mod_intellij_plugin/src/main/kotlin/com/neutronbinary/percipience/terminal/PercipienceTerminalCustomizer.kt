package com.neutronbinary.percipience.terminal

import com.intellij.openapi.project.Project
import java.io.File

/**
 * Customizes local terminal environment options for IntelliJ / PyCharm terminal sessions.
 * Injects Percipience AST token optimization environment variables, shell hooks,
 * and project context paths so CLI agents (Claude Code, Gemini CLI, Aider)
 * automatically execute through the AST compression layer.
 */
class PercipienceTerminalCustomizer {

    companion object {
        const val ENV_TERMINAL_MODE = "PERCIPIENCE_TERMINAL_MODE"
        const val ENV_AST_COMPRESSION = "PERCIPIENCE_AST_COMPRESSION"
        const val ENV_PROJECT_ROOT = "PERCIPIENCE_PROJECT_ROOT"
        const val ENV_BIN_PATH = "PERCIPIENCE_BIN"

        /**
         * Returns custom environment variables to inject into terminal PTY sessions.
         */
        fun getCustomEnvironment(project: Project): Map<String, String> {
            val env = mutableMapOf<String, String>()
            val basePath = project.basePath ?: return env

            val root = File(basePath)
            val bin = File(root, ".nb/bin/percipience")

            env[ENV_TERMINAL_MODE] = "1"
            env[ENV_AST_COMPRESSION] = "1"
            env[ENV_PROJECT_ROOT] = root.absolutePath
            if (bin.exists()) {
                env[ENV_BIN_PATH] = bin.absolutePath
            }

            return env
        }

        /**
         * Returns the shell command string to initialize AST hooks in a terminal session.
         */
        fun getShellHookCommand(project: Project, agent: String = "claude"): String {
            val basePath = project.basePath ?: "."
            return "./.nb/bin/percipience agent wrap --agent $agent"
        }
    }
}
