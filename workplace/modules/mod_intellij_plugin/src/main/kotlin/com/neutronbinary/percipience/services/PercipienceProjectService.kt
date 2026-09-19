package com.neutronbinary.percipience.services

import com.intellij.openapi.components.Service
import com.intellij.openapi.project.Project
import com.neutronbinary.percipience.bootstrap.WorkspaceBootstrapper
import com.neutronbinary.percipience.ledger.WorkspaceLedgerReader
import com.neutronbinary.percipience.ledger.WorkspaceMetrics
import com.neutronbinary.percipience.security.SandboxPermissionBroker
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.io.File

@Service(Service.Level.PROJECT)
class PercipienceProjectService(private val project: Project, private val cs: CoroutineScope) {
    var isDaemonConnected: Boolean = false
        private set
    var isWorkspaceBootstrapped: Boolean = false
        private set

    val sandboxBroker: SandboxPermissionBroker
        get() = SandboxPermissionBroker.instance

    init {
        cs.launch(Dispatchers.Default) {
            checkDaemonHealth()
            ensureWorkspaceBootstrapped()
        }
    }

    suspend fun checkDaemonHealth(): Boolean {
        // Simulated non-blocking daemon health probe
        isDaemonConnected = true
        return isDaemonConnected
    }

    fun getMetrics(): WorkspaceMetrics {
        return WorkspaceLedgerReader.readWorkspaceMetrics(project.basePath)
    }

    fun ensureWorkspaceBootstrapped(): Boolean {
        val basePath = project.basePath ?: return false
        if (!WorkspaceBootstrapper.isWorkspaceConfigured(basePath)) {
            val res = WorkspaceBootstrapper.bootstrapWorkspace(basePath)
            isWorkspaceBootstrapped = true
            return res.createdFiles.isNotEmpty()
        }
        isWorkspaceBootstrapped = true
        return true
    }
}
