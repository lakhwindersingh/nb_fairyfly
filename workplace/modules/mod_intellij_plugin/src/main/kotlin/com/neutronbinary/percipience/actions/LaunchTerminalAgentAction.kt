package com.neutronbinary.percipience.actions

import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.progress.ProgressIndicator
import com.intellij.openapi.progress.ProgressManager
import com.intellij.openapi.progress.Task
import com.intellij.openapi.ui.Messages
import com.neutronbinary.percipience.services.ExecutionResult
import com.neutronbinary.percipience.services.PercipienceExecutionService
import kotlinx.coroutines.runBlocking

/**
 * Action to wrap and initialize an AST-optimized terminal session
 * for Claude Code or Gemini CLI in IntelliJ IDEA / PyCharm.
 */
class LaunchTerminalAgentAction(private val agentName: String = "claude") : AnAction() {

    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return
        val execService = PercipienceExecutionService.getInstance(project)

        val format = if (agentName.contains("gemini", ignoreCase = true)) "gemini-cli" else "claude-code"

        ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Preparing AST Context for $agentName...", false) {
            private var result: ExecutionResult? = null

            override fun run(indicator: ProgressIndicator) {
                indicator.isIndeterminate = true
                indicator.text = "Slicing workspace AST & preparing terminal context wrapper..."
                result = runBlocking {
                    execService.runAgentWrap(agentName, format)
                }
            }

            override fun onSuccess() {
                val res = result ?: return
                if (res.success) {
                    Messages.showInfoMessage(
                        project,
                        "⚡ AST-Optimized Context Prepared for $agentName!\n\n" +
                                "${res.stdout.trim()}\n\n" +
                                "To run in Terminal tool window:\n" +
                                "  claude --append-system-prompt \"\$(cat .percipience_claude_context.md)\"\n" +
                                "or use shell hook: eval \"\$(./.nb/bin/percipience terminal hook)\"",
                        "Terminal Mode Agent Ready"
                    )
                } else {
                    Messages.showErrorDialog(
                        project,
                        "Failed to wrap terminal agent:\n\n${res.stderr.ifEmpty { res.stdout }}",
                        "Error"
                    )
                }
            }

            override fun onThrowable(error: Throwable) {
                Messages.showErrorDialog(
                    project,
                    "Terminal Agent Wrap Error:\n\n${error.message}",
                    "Error"
                )
            }
        })
    }
}
