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

class RunGatekeeperAction : AnAction() {
    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return
        val execService = PercipienceExecutionService.getInstance(project)

        ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Running Percipience PR Gatekeeper...", false) {
            private var result: ExecutionResult? = null

            override fun run(indicator: ProgressIndicator) {
                indicator.isIndeterminate = true
                indicator.text = "Executing .nb/bin/percipience gate across 7 verification stages..."
                result = runBlocking {
                    execService.runGatekeeper()
                }
            }

            override fun onSuccess() {
                val res = result ?: return
                if (res.success) {
                    Messages.showInfoMessage(
                        project,
                        "Percipience Gatekeeper passed all 7 verification stages successfully!\n\n${res.stdout.takeLast(500)}",
                        "Percipience Gatekeeper Passed"
                    )
                } else {
                    Messages.showErrorDialog(
                        project,
                        "Percipience Gatekeeper encountered errors:\n\n${res.stderr.ifEmpty { res.stdout }.takeLast(800)}",
                        "Gatekeeper Failed"
                    )
                }
            }

            override fun onThrowable(error: Throwable) {
                Messages.showErrorDialog(
                    project,
                    "Gatekeeper Execution Error:\n\n${error.message}",
                    "Gatekeeper Error"
                )
            }
        })
    }
}
