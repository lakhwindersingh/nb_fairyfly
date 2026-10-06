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

class ValidateLayerAction : AnAction() {
    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return
        val execService = PercipienceExecutionService.getInstance(project)

        ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Validating Layered Context...", false) {
            private var result: ExecutionResult? = null

            override fun run(indicator: ProgressIndicator) {
                indicator.isIndeterminate = true
                indicator.text = "Validating 3-Tier Layered Context & Custom Invariants..."
                result = runBlocking {
                    execService.runValidateLayered()
                }
            }

            override fun onSuccess() {
                val res = result ?: return
                if (res.success) {
                    Messages.showInfoMessage(
                        project,
                        "Layered Context is 100% compliant with platform invariants!\n\n${res.stdout}",
                        "Layered Context Validated"
                    )
                } else {
                    Messages.showErrorDialog(
                        project,
                        "Layered Context validation failed:\n\n${res.stderr.ifEmpty { res.stdout }}",
                        "Validation Failed"
                    )
                }
            }

            override fun onThrowable(error: Throwable) {
                Messages.showErrorDialog(
                    project,
                    "Validation Error:\n\n${error.message}",
                    "Validation Error"
                )
            }
        })
    }
}
