package com.neutronbinary.percipience.actions

import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.actionSystem.CommonDataKeys
import com.intellij.openapi.progress.ProgressIndicator
import com.intellij.openapi.progress.ProgressManager
import com.intellij.openapi.progress.Task
import com.intellij.openapi.ui.Messages
import com.neutronbinary.percipience.services.ExecutionResult
import com.neutronbinary.percipience.services.PercipienceExecutionService
import kotlinx.coroutines.runBlocking

class RunReflexionCriticAction : AnAction() {
    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return
        val execService = PercipienceExecutionService.getInstance(project)
        val virtualFile = e.getData(CommonDataKeys.VIRTUAL_FILE)
        val targetPath = virtualFile?.path

        ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Running Swarm Self-Reflection Critic...", false) {
            private var result: ExecutionResult? = null

            override fun run(indicator: ProgressIndicator) {
                indicator.isIndeterminate = true
                indicator.text = "Executing .nb/bin/percipience swarm reflexion..."
                result = runBlocking {
                    execService.runSwarmReflexion(targetPath)
                }
            }

            override fun onSuccess() {
                val res = result ?: return
                if (res.success) {
                    Messages.showInfoMessage(
                        project,
                        "Swarm Self-Reflection Critic Verification Passed!\n\n${res.stdout}",
                        "Swarm Reflexion Critic Passed"
                    )
                } else {
                    Messages.showErrorDialog(
                        project,
                        "Swarm Reflexion Critique Flagged Violations:\n\n${res.stderr.ifEmpty { res.stdout }}",
                        "Swarm Reflexion Critic Violated"
                    )
                }
            }

            override fun onThrowable(error: Throwable) {
                Messages.showErrorDialog(
                    project,
                    "Reflexion Critic Error:\n\n${error.message}",
                    "Swarm Reflexion Error"
                )
            }
        })
    }
}
