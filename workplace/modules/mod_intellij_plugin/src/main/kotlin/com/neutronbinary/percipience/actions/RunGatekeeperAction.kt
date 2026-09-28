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

class RunGatekeeperAction : AnAction() {
    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return
        val execService = PercipienceExecutionService.getInstance(project)

        ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Running Percipience PR Gatekeeper...", false) {
            override fun run(indicator: ProgressIndicator) {
                indicator.isIndeterminate = true
                indicator.text = "Executing .nb/bin/percipience gate across 7 verification stages..."

                val result = runBlocking {
                    execService.runGatekeeper()
                }

                ApplicationManager.getApplication().invokeLater {
                    if (result.success) {
                        Messages.showInfoMessage(
                            project,
                            "Percipience Gatekeeper passed all 7 verification stages successfully!\n\n${result.stdout.takeLast(500)}",
                            "Percipience Gatekeeper Passed"
                        )
                    } else {
                        Messages.showErrorDialog(
                            project,
                            "Percipience Gatekeeper encountered errors:\n\n${result.stderr.ifEmpty { result.stdout }.takeLast(800)}",
                            "Gatekeeper Failed"
                        )
                    }
                }
            }
        })
    }
}
