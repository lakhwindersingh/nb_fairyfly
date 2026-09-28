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

class RunCicdAction : AnAction() {
    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return
        val execService = PercipienceExecutionService.getInstance(project)

        ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Executing Basic Autonomous CI/CD...", false) {
            override fun run(indicator: ProgressIndicator) {
                indicator.isIndeterminate = true
                indicator.text = "Running hygiene, AST pruning, bounded TDD, and Merkle block sealing..."

                val result = runBlocking {
                    execService.runBasicCicd()
                }

                ApplicationManager.getApplication().invokeLater {
                    if (result.success) {
                        Messages.showInfoMessage(
                            project,
                            "Basic Autonomous CI/CD completed successfully!\n\n${result.stdout.takeLast(500)}",
                            "Autonomous CI/CD Success"
                        )
                    } else {
                        Messages.showErrorDialog(
                            project,
                            "Basic Autonomous CI/CD encountered issues:\n\n${result.stderr.ifEmpty { result.stdout }.takeLast(800)}",
                            "Autonomous CI/CD Failure"
                        )
                    }
                }
            }
        })
    }
}
