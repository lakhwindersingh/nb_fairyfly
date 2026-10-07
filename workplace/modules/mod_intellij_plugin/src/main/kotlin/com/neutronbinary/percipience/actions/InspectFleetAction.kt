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

class InspectFleetAction : AnAction() {
    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return
        val execService = PercipienceExecutionService.getInstance(project)

        ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Inspecting Workstation & Node Fleet...", false) {
            private var result: ExecutionResult? = null

            override fun run(indicator: ProgressIndicator) {
                indicator.isIndeterminate = true
                indicator.text = "Executing .nb/bin/percipience swarm fleet --simulate-pulse..."
                result = runBlocking {
                    execService.runSwarmFleet(simulatePulse = true)
                }
            }

            override fun onSuccess() {
                val res = result ?: return
                if (res.success) {
                    Messages.showInfoMessage(
                        project,
                        "Workstation & Fleet Metrics:\n\n${res.stdout}",
                        "Percipience Fleet Status"
                    )
                } else {
                    Messages.showErrorDialog(
                        project,
                        "Fleet Inspection Failed:\n\n${res.stderr.ifEmpty { res.stdout }}",
                        "Fleet Inspection Failed"
                    )
                }
            }

            override fun onThrowable(error: Throwable) {
                Messages.showErrorDialog(
                    project,
                    "Fleet Inspection Error:\n\n${error.message}",
                    "Fleet Error"
                )
            }
        })
    }
}
