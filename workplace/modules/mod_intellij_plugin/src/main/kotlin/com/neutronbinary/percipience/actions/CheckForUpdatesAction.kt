package com.neutronbinary.percipience.actions

import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.neutronbinary.percipience.services.PluginUpdateService

/**
 * Scans the local file system for a newer Percipience plugin / runtime build
 * and offers an in-place workspace upgrade (offline auto-upgrade).
 */
class CheckForUpdatesAction : AnAction() {

    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return
        PluginUpdateService.getInstance(project).requestCheck()
    }

    override fun update(e: AnActionEvent) {
        e.presentation.isEnabledAndVisible = e.project != null
    }
}
