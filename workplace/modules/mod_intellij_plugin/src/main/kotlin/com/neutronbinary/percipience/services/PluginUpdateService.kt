package com.neutronbinary.percipience.services

import com.intellij.notification.Notification
import com.intellij.notification.NotificationAction
import com.intellij.notification.NotificationGroupManager
import com.intellij.notification.NotificationType
import com.intellij.openapi.components.Service
import com.intellij.openapi.project.Project
import com.intellij.openapi.vfs.VirtualFileManager
import com.neutronbinary.percipience.update.PluginUpdateChecker
import com.neutronbinary.percipience.update.UpgradeCandidate
import com.neutronbinary.percipience.update.UpgradeCheckResult
import com.neutronbinary.percipience.update.UpgradeResult
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

/**
 * Project service exposing offline, local-file-system based plugin auto-upgrade.
 * Mirrors the canonical Python engine `plugin_update_resolver.py`.
 */
@Service(Service.Level.PROJECT)
class PluginUpdateService(private val project: Project, private val cs: CoroutineScope) {

    companion object {
        fun getInstance(project: Project): PluginUpdateService =
            project.getService(PluginUpdateService::class.java)

        /** Auto-apply a discovered upgrade without prompting (opt-in via env). */
        fun isAutoUpgradeEnabled(): Boolean =
            System.getenv("PERCIPIENCE_AUTO_UPGRADE")?.trim() == "1"

        fun notify(project: Project, title: String, content: String, type: NotificationType, block: (Notification) -> Unit = {}) {
            val notification = try {
                NotificationGroupManager.getInstance()
                    .getNotificationGroup("Percipience Notifications")
                    .createNotification(title, content, type)
            } catch (_: Exception) {
                Notification("Percipience Notifications", title, content, type)
            }
            block(notification)
            notification.notify(project)
        }
    }

    /** Kicks off an asynchronous local file system upgrade check (fire-and-forget). */
    fun requestCheck() {
        cs.launch { checkAndNotify() }
    }

    suspend fun checkForUpdate(): UpgradeCheckResult {
        val basePath = project.basePath ?: return UpgradeCheckResult(
            currentVersion = PluginUpdateChecker.installedVersionInfo().pluginVersion,
            appliedRuntimeVersion = null,
            candidates = emptyList(),
            selected = null
        )
        return withContext(Dispatchers.IO) {
            PluginUpdateChecker.checkForUpgrade(basePath)
        }
    }

    suspend fun applyUpgrade(candidate: UpgradeCandidate): UpgradeResult {
        val basePath = project.basePath ?: return UpgradeResult(
            status = "SKIPPED",
            pluginVersion = candidate.pluginVersion,
            previousVersion = null,
            tier = candidate.version.tier,
            source = candidate.path,
            filesUpgraded = 0
        )
        return withContext(Dispatchers.IO) {
            val result = PluginUpdateChecker.applyRuntimeUpgrade(basePath, candidate)
            VirtualFileManager.getInstance().asyncRefresh(null)
            result
        }
    }

    /**
     * Scans the local file system for an upgrade. Auto-applies when
     * [isAutoUpgradeEnabled], otherwise surfaces an interactive prompt.
     */
    suspend fun checkAndNotify() {
        val report = checkForUpdate()
        val candidate = report.selected
        if (candidate == null) {
            notify(project, "Percipience Plugin Up To Date",
                "No newer Percipience plugin build was found on the local file system.\nInstalled: v${report.currentVersion}",
                NotificationType.INFORMATION)
            return
        }

        if (isAutoUpgradeEnabled()) {
            val result = applyUpgrade(candidate)
            notify(project, "Percipience Auto-Upgrade Applied",
                "Upgraded workspace runtime to v${result.pluginVersion} (was ${result.previousVersion ?: "unversioned"}).\n${result.filesUpgraded} files refreshed from local source.",
                NotificationType.INFORMATION)
            return
        }

        notify(project, "Percipience Plugin Upgrade Available",
            "A newer Percipience plugin build (v${candidate.pluginVersion}, tier ${candidate.version.tier}) was found locally.\nInstalled: v${report.currentVersion}\nSource: ${candidate.path}",
            NotificationType.INFORMATION) { notification ->
            notification.addAction(NotificationAction.createSimpleExpiring("⬆️ Upgrade Workspace Runtime") {
                com.intellij.openapi.application.ApplicationManager.getApplication().executeOnPooledThread {
                    val result = try {
                        PluginUpdateChecker.applyRuntimeUpgrade(project.basePath ?: return@executeOnPooledThread, candidate)
                    } catch (ex: Exception) {
                        notify(project, "Percipience Upgrade Failed", ex.message ?: "Unknown error", NotificationType.ERROR)
                        return@executeOnPooledThread
                    }
                    VirtualFileManager.getInstance().asyncRefresh(null)
                    notify(project, "Percipience Upgrade Applied",
                        "Workspace runtime upgraded to v${result.pluginVersion}.\n${result.filesUpgraded} files refreshed from ${result.source}.",
                        NotificationType.INFORMATION)
                }
            })
            notification.addAction(NotificationAction.createSimpleExpiring("Dismiss") { notification.expire() })
        }
    }
}
