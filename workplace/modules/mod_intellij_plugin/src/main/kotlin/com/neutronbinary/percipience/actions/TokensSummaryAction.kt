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

class TokensSummaryAction : AnAction() {
    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return
        val execService = PercipienceExecutionService.getInstance(project)

        ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Loading Percipience Token Savings...", false) {
            private var result: ExecutionResult? = null

            override fun run(indicator: ProgressIndicator) {
                indicator.isIndeterminate = true
                indicator.text = "Reading token savings and FinOps ledger events..."
                result = runBlocking {
                    execService.runTokensSummary()
                }
            }

            override fun onSuccess() {
                val res = result ?: return
                if (res.success) {
                    Messages.showInfoMessage(
                        project,
                        res.stdout,
                        "Percipience Token Savings & FinOps"
                    )
                } else {
                    Messages.showErrorDialog(
                        project,
                        "Failed to load token savings:\n\n${res.stderr.ifEmpty { res.stdout }}",
                        "Error"
                    )
                }
            }

            override fun onThrowable(error: Throwable) {
                Messages.showErrorDialog(
                    project,
                    "Error loading summary:\n\n${error.message}",
                    "Error"
                )
            }
        })
    }
}
