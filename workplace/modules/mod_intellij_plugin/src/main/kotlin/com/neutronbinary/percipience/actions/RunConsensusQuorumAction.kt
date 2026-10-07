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

class RunConsensusQuorumAction : AnAction() {
    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return
        val execService = PercipienceExecutionService.getInstance(project)

        val proposal = Messages.showInputDialog(
            project,
            "Enter governance proposal or PR title for multi-model consensus voting:",
            "Swarm Consensus Quorum",
            Messages.getQuestionIcon(),
            "PR Gate Approval",
            null
        ) ?: return

        ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Verifying Multi-Model Consensus...", false) {
            private var result: ExecutionResult? = null

            override fun run(indicator: ProgressIndicator) {
                indicator.isIndeterminate = true
                indicator.text = "Executing .nb/bin/percipience swarm consensus --proposal \"$proposal\"..."
                result = runBlocking {
                    execService.runSwarmConsensus(proposal)
                }
            }

            override fun onSuccess() {
                val res = result ?: return
                if (res.success) {
                    Messages.showInfoMessage(
                        project,
                        "Multi-Model Consensus Quorum Attested!\n\n${res.stdout}",
                        "Consensus Quorum Passed"
                    )
                } else {
                    Messages.showErrorDialog(
                        project,
                        "Consensus Quorum Quorum Failed:\n\n${res.stderr.ifEmpty { res.stdout }}",
                        "Consensus Quorum Rejected"
                    )
                }
            }

            override fun onThrowable(error: Throwable) {
                Messages.showErrorDialog(
                    project,
                    "Consensus Quorum Error:\n\n${error.message}",
                    "Consensus Error"
                )
            }
        })
    }
}
