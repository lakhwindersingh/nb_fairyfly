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
import java.io.File

/**
 * Action to export AST-pruned workspace context for Claude Code or Gemini CLI.
 */
class ExportTerminalContextAction(private val formatType: String = "claude-code") : AnAction() {

    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return
        val execService = PercipienceExecutionService.getInstance(project)
        val basePath = project.basePath ?: return

        val contextDir = File(basePath, ".nb/context")
        if (!contextDir.exists()) {
            contextDir.mkdirs()
        }

        val outputFile = if (formatType == "claude-code") {
            File(contextDir, "percipience_claude_context.md")
        } else {
            File(contextDir, "percipience_gemini_context.md")
        }

        ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Exporting AST Context ($formatType)...", false) {
            private var result: ExecutionResult? = null

            override fun run(indicator: ProgressIndicator) {
                indicator.isIndeterminate = true
                indicator.text = "Pruning workspace AST & generating context envelope..."
                result = runBlocking {
                    execService.runContextExport(formatType, outputFile.absolutePath)
                }
            }

            override fun onSuccess() {
                val res = result ?: return
                if (res.success) {
                    Messages.showInfoMessage(
                        project,
                        "✅ AST Context successfully exported to:\n${outputFile.path}\n\n${res.stdout.trim()}",
                        "Context Export Complete"
                    )
                } else {
                    Messages.showErrorDialog(
                        project,
                        "Failed to export context:\n\n${res.stderr.ifEmpty { res.stdout }}",
                        "Export Error"
                    )
                }
            }

            override fun onThrowable(error: Throwable) {
                Messages.showErrorDialog(
                    project,
                    "Context Export Exception:\n\n${error.message}",
                    "Error"
                )
            }
        })
    }
}
