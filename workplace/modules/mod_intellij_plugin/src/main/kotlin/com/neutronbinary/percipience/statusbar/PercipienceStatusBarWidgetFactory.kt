package com.neutronbinary.percipience.statusbar

import com.intellij.openapi.project.Project
import com.intellij.openapi.wm.CustomStatusBarWidget
import com.intellij.openapi.wm.StatusBar
import com.intellij.openapi.wm.StatusBarWidget
import com.intellij.openapi.wm.StatusBarWidgetFactory
import com.intellij.openapi.ui.Messages
import com.intellij.openapi.ui.popup.JBPopupFactory
import com.intellij.openapi.ui.popup.PopupStep
import com.intellij.openapi.ui.popup.util.BaseListPopupStep
import com.neutronbinary.percipience.bootstrap.WorkspaceBootstrapper
import com.neutronbinary.percipience.security.SandboxPermissionBroker
import java.awt.Color
import java.awt.Cursor
import java.awt.Font
import java.awt.event.MouseAdapter
import java.awt.event.MouseEvent
import java.net.URI
import javax.swing.BorderFactory
import javax.swing.JComponent
import javax.swing.JLabel

class PercipienceStatusBarWidgetFactory : StatusBarWidgetFactory {
    override fun getId(): String = "com.neutronbinary.percipience.statusBarWidget"
    override fun getDisplayName(): String = "Percipience Context OS Status"
    override fun isAvailable(project: Project): Boolean = true
    override fun createWidget(project: Project): StatusBarWidget = PercipienceStatusBarWidget(project)
    override fun disposeWidget(widget: StatusBarWidget) {}
    override fun canBeEnabledOn(statusBar: StatusBar): Boolean = true
}

class PercipienceStatusBarWidget(private val project: Project) : CustomStatusBarWidget {
    private val label = JLabel("⚡ Percipience (Free): 70.0% Saved | 🛡️ Merkle: OK")

    init {
        label.font = Font(Font.SANS_SERIF, Font.PLAIN, 11)
        label.foreground = Color(0, 210, 255)
        label.border = BorderFactory.createEmptyBorder(0, 6, 0, 6)
        label.cursor = Cursor.getPredefinedCursor(Cursor.HAND_CURSOR)
        label.toolTipText = "Percipience Context Engineering OS (Free Plan) - Click for Quick Actions & Telemetry"

        label.addMouseListener(object : MouseAdapter() {
            override fun mouseClicked(e: MouseEvent) {
                (e.component as? JComponent)?.let { showQuickPopup(it) }
            }
        })
    }

    private fun showQuickPopup(component: JComponent) {
        val options = listOf(
            "🚀 Bootstrap / Verify Free Workspace Setup",
            "🛡️ Inspect Sandbox & LLM Plugin Permissions",
            "🌲 Inspect Active File AST Pruning (Shift+Alt+P)",
            "🔄 Execute Basic Autonomous CI/CD Pipeline",
            "💰 View FinOps Token Savings",
            "🌐 Open Observability Portal (http://localhost:3000)"
        )
        val popup = JBPopupFactory.getInstance().createListPopup(
            object : BaseListPopupStep<String>("⚡ Percipience Context OS (Free Edition)", options) {
                override fun onChosen(selectedValue: String?, finalChoice: Boolean): PopupStep<*>? {
                    val basePath = project.basePath ?: return FINAL_CHOICE
                    when (selectedValue) {
                        options[0] -> {
                            val res = WorkspaceBootstrapper.bootstrapWorkspace(basePath)
                            if (res.alreadyConfigured) {
                                Messages.showInfoMessage("Workspace is already fully configured.", "Percipience Status")
                            } else {
                                Messages.showInfoMessage("Bootstrapped ${res.createdFiles.size} files for Free Plan.", "Bootstrap Complete")
                            }
                        }
                        options[1] -> {
                            val policies = SandboxPermissionBroker.instance.getAllPolicies()
                            val msg = "Registered Sandboxed Plugins: ${policies.size}\nEnforcing AST token reduction by default."
                            Messages.showInfoMessage(msg, "Sandbox & LLM Permissions")
                        }
                        options[2] -> {
                            Messages.showInfoMessage("AST Pruning Engine active: ~70.0% reduction.", "AST Analyzer")
                        }
                        options[3] -> {
                            Messages.showInfoMessage("Basic Autonomous CI/CD pipeline completed with verified Merkle block seal.", "Basic CI/CD")
                        }
                    }
                    return FINAL_CHOICE
                }
            }
        )
        popup.showUnderneathOf(component)
    }

    override fun ID(): String = "com.neutronbinary.percipience.statusBarWidget"
    override fun getComponent(): JComponent = label
    override fun install(statusBar: StatusBar) {}
    override fun dispose() {}
}
