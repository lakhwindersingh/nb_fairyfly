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

class RunMerkleAuditAction : AnAction() {
    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return
        val execService = PercipienceExecutionService.getInstance(project)

        ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Auditing Percipience Merkle Ledger...", false) {
            private var result: ExecutionResult? = null

            override fun run(indicator: ProgressIndicator) {
                indicator.isIndeterminate = true
                indicator.text = "Verifying cryptographic SHA-256 state continuity & maturity..."
                result = runBlocking {
                    execService.runMerkleAudit(enforceMerkleChain = true, minMaturity = 0.85)
                }
            }

            override fun onSuccess() {
                val res = result ?: return
                if (res.success) {
                    Messages.showInfoMessage(
                        project,
                        "Merkle Chain audit passed successfully!\n\n${res.stdout.takeLast(500)}",
                        "Merkle Audit Passed"
                    )
                } else {
                    Messages.showErrorDialog(
                        project,
                        "Merkle Chain audit failed:\n\n${res.stderr.ifEmpty { res.stdout }.takeLast(800)}",
                        "Merkle Audit Failed"
                    )
                }
            }

            override fun onThrowable(error: Throwable) {
                Messages.showErrorDialog(
                    project,
                    "Merkle Audit Error:\n\n${error.message}",
                    "Audit Error"
                )
            }
        })
    }
}
