package com.neutronbinary.percipience.actions

import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.application.ApplicationManager
import com.intellij.openapi.progress.ProgressIndicator
import com.intellij.openapi.progress.ProgressManager
import com.intellij.openapi.progress.Task
import com.intellij.openapi.ui.Messages
import com.neutronbinary.percipience.services.PercipienceExecutionService
import kotlinx.coroutines.runBlocking

class RunMerkleAuditAction : AnAction() {
    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return
        val execService = PercipienceExecutionService.getInstance(project)

        ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Auditing Percipience Merkle Ledger...", false) {
            override fun run(indicator: ProgressIndicator) {
                indicator.isIndeterminate = true
                indicator.text = "Verifying cryptographic SHA-256 state continuity & maturity..."

                val result = runBlocking {
                    execService.runMerkleAudit(enforceMerkleChain = true, minMaturity = 0.85)
                }

                ApplicationManager.getApplication().invokeLater {
                    if (result.success) {
                        Messages.showInfoMessage(
                            project,
                            "Merkle Chain audit passed successfully!\n\n${result.stdout.takeLast(500)}",
                            "Merkle Audit Passed"
                        )
                    } else {
                        Messages.showErrorDialog(
                            project,
                            "Merkle Chain audit failed:\n\n${result.stderr.ifEmpty { result.stdout }.takeLast(800)}",
                            "Merkle Audit Failed"
                        )
                    }
                }
            }
        })
    }
}
