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

class RunSwarmDagAction : AnAction() {
    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return
        val execService = PercipienceExecutionService.getInstance(project)

        ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Executing Swarm Wave...", false) {
            private var result: ExecutionResult? = null

            override fun run(indicator: ProgressIndicator) {
                indicator.isIndeterminate = true
                indicator.text = "Executing .nb/bin/percipience swarm dag --action exec..."
                result = runBlocking {
                    execService.runSwarmDag("exec")
                }
            }

            override fun onSuccess() {
                val res = result ?: return
                if (res.success) {
                    Messages.showInfoMessage(
                        project,
                        "Swarm Wave Execution Completed Successfully!\n\n${res.stdout}",
                        "Swarm DAG Execution"
                    )
                } else {
                    Messages.showErrorDialog(
                        project,
                        "Swarm Wave Execution Failed:\n\n${res.stderr.ifEmpty { res.stdout }}",
                        "Swarm Wave Failed"
                    )
                }
            }

            override fun onThrowable(error: Throwable) {
                Messages.showErrorDialog(
                    project,
                    "Swarm DAG Error:\n\n${error.message}",
                    "Swarm Error"
                )
            }
        })
    }
}
