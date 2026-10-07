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

class MintCbacTokenAction : AnAction() {
    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return
        val execService = PercipienceExecutionService.getInstance(project)

        val agentId = Messages.showInputDialog(
            project,
            "Enter target agent ID to mint capability token for:",
            "Mint Swarm CBAC Token",
            Messages.getQuestionIcon(),
            "agent_sandbox_coder",
            null
        ) ?: return

        ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Minting HMAC Capability Token...", false) {
            private var result: ExecutionResult? = null

            override fun run(indicator: ProgressIndicator) {
                indicator.isIndeterminate = true
                indicator.text = "Executing .nb/bin/percipience swarm cbac..."
                result = runBlocking {
                    execService.runSwarmCbac(agentId = agentId)
                }
            }

            override fun onSuccess() {
                val res = result ?: return
                if (res.success) {
                    Messages.showInfoMessage(
                        project,
                        "HMAC-SHA256 Capability Token Minted Successfully:\n\n${res.stdout}",
                        "CBAC Token Minted"
                    )
                } else {
                    Messages.showErrorDialog(
                        project,
                        "Failed to mint CBAC token:\n\n${res.stderr.ifEmpty { res.stdout }}",
                        "CBAC Minting Failed"
                    )
                }
            }

            override fun onThrowable(error: Throwable) {
                Messages.showErrorDialog(
                    project,
                    "CBAC Error:\n\n${error.message}",
                    "CBAC Error"
                )
            }
        })
    }
}
