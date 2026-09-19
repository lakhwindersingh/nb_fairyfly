package com.neutronbinary.percipience.toolwindow

import com.intellij.openapi.project.Project
import com.intellij.openapi.wm.ToolWindow
import com.intellij.openapi.wm.ToolWindowFactory
import com.intellij.ui.content.ContentFactory
import javax.swing.JPanel
import javax.swing.JLabel
import java.awt.BorderLayout

class PercipienceToolWindowFactory : ToolWindowFactory {
    override fun createToolWindowContent(project: Project, toolWindow: ToolWindow) {
        val panel = JPanel(BorderLayout())
        val label = JLabel("⚡ Percipience Context Engineering OS - Connected")
        panel.add(label, BorderLayout.NORTH)
        val content = ContentFactory.getInstance().createContent(panel, "Control Plane", false)
        toolWindow.contentManager.addContent(content)
    }
}
