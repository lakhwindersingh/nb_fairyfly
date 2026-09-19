package com.neutronbinary.percipience.actions

import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.ui.Messages
import com.neutronbinary.percipience.security.SandboxPermissionBroker

class ManageSandboxPermissionsAction : AnAction() {

    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return
        val broker = SandboxPermissionBroker.instance
        val policies = broker.getAllPolicies()

        val sb = StringBuilder()
        sb.append("Percipience IDE Sandbox Permission Registry\n")
        sb.append("===========================================\n\n")
        sb.append("Enforcing AST Token Reduction (60%-80% Pruned Skeletons) on sandboxed LLM plugins.\n\n")

        policies.values.forEach { policy ->
            sb.append("• Plugin: ${policy.pluginName} (${policy.pluginId})\n")
            sb.append("  - Sandboxed: ${policy.isSandboxed}\n")
            sb.append("  - Default Read: ${policy.defaultReadLevel}\n")
            sb.append("  - Token Pruning Enforced: ${policy.enforceTokenPruning}\n")
            sb.append("  - Direct Write: ${policy.canWriteDirect}\n\n")
        }

        Messages.showInfoMessage(
            project,
            sb.toString(),
            "Sandbox & Agent Permissions"
        )
    }
}
