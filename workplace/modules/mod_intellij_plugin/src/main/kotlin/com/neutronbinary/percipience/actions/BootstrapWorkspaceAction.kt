package com.neutronbinary.percipience.actions

import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.ui.Messages
import com.neutronbinary.percipience.bootstrap.WorkspaceBootstrapper

class BootstrapWorkspaceAction : AnAction() {

    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return
        val basePath = project.basePath ?: return

        try {
            val result = WorkspaceBootstrapper.bootstrapWorkspace(basePath)
            if (result.alreadyConfigured) {
                Messages.showInfoMessage(
                    project,
                    "Percipience Free Workspace is already configured.\n" +
                    "• Master Plan: .nb/plan/claude-context-engineering-parent-master-plan.md\n" +
                    "• Merkle Ledger: .nb/context/ledger/context_ledger.yaml\n" +
                    "• Basic CI/CD: .nb/agentic/custom/workflows/basic_autonomous_cicd.yaml\n" +
                    "• Token Reduction: 70.0% AST skeletonization active",
                    "Percipience Workspace Status"
                )
            } else {
                Messages.showInfoMessage(
                    project,
                    "Successfully bootstrapped Percipience Free Community Workspace!\n\n" +
                    "Created Directories: ${result.createdDirectories.size}\n" +
                    "Created Files: ${result.createdFiles.size}\n" +
                    "Genesis Merkle Block: ${result.merkleGenesisHash.take(16)}...\n\n" +
                    "Capabilities Enabled:\n" +
                    "✔ AST Token Reduction (60%-80%)\n" +
                    "✔ Linear SHA-256 Merkle Chain\n" +
                    "✔ Basic Autonomous CI/CD Pipeline\n" +
                    "✔ Sandbox Source Permission Broker",
                    "Percipience Bootstrap Complete"
                )
            }
        } catch (ex: Exception) {
            Messages.showErrorDialog(
                project,
                "Error bootstrapping workspace: ${ex.message}",
                "Bootstrap Error"
            )
        }
    }
}
