package com.neutronbinary.percipience.startup

import com.intellij.notification.Notification
import com.intellij.notification.NotificationAction
import com.intellij.notification.NotificationGroupManager
import com.intellij.notification.NotificationType
import com.intellij.openapi.project.Project
import com.intellij.openapi.startup.ProjectActivity
import com.neutronbinary.percipience.bootstrap.WorkspaceBootstrapper
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class PercipienceProjectStartupActivity : ProjectActivity {

    override suspend fun execute(project: Project) {
        val basePath = project.basePath ?: return

        val isConfigured = withContext(Dispatchers.IO) {
            WorkspaceBootstrapper.isWorkspaceConfigured(basePath)
        }

        if (!isConfigured) {
            promptWorkspaceInitialization(project, basePath)
        }
    }

    companion object {
        fun promptWorkspaceInitialization(project: Project, basePath: String) {
            val title = "Percipience Context Engineering OS"
            val content = "No Percipience workspace configuration detected. Initialize this workspace with the Free Community Tier (AST token pruning, Merkle ledger, and basic CI/CD)?"

            val notification = try {
                NotificationGroupManager.getInstance()
                    .getNotificationGroup("Percipience Notifications")
                    .createNotification(title, content, NotificationType.INFORMATION)
            } catch (e: Exception) {
                Notification("Percipience Notifications", title, content, NotificationType.INFORMATION)
            }

            notification.addAction(NotificationAction.createSimpleExpiring("🚀 Initialize Free Workspace") {
                val res = WorkspaceBootstrapper.bootstrapWorkspace(basePath)
                val successTitle = "Percipience Workspace Initialized"
                val successContent = "Bootstrapped ${res.createdFiles.size} configuration and binary files for Free Community Tier. Percipience CLI (.nb/bin/percipience) and basic CI/CD are now ready in the workspace."

                val successNotification = try {
                    NotificationGroupManager.getInstance()
                        .getNotificationGroup("Percipience Notifications")
                        .createNotification(successTitle, successContent, NotificationType.INFORMATION)
                } catch (e: Exception) {
                    Notification("Percipience Notifications", successTitle, successContent, NotificationType.INFORMATION)
                }
                successNotification.notify(project)
            })

            notification.addAction(NotificationAction.createSimpleExpiring("Dismiss") {
                notification.expire()
            })

            notification.notify(project)
        }
    }
}
