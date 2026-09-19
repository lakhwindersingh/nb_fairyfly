package com.neutronbinary.percipience.services

import com.intellij.openapi.components.Service
import com.intellij.openapi.project.Project
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.io.File

@Service(Service.Level.PROJECT)
class PercipienceProjectService(private val project: Project, private val cs: CoroutineScope) {
    var isDaemonConnected: Boolean = false
        private set

    init {
        cs.launch(Dispatchers.Default) {
            checkDaemonHealth()
        }
    }

    suspend fun checkDaemonHealth(): Boolean {
        // Simulated non-blocking daemon health probe
        isDaemonConnected = true
        return isDaemonConnected
    }
}
