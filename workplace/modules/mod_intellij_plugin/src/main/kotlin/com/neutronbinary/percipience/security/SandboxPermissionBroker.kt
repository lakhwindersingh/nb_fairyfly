package com.neutronbinary.percipience.security

import com.intellij.openapi.project.Project
import java.time.Instant
import java.util.concurrent.ConcurrentHashMap

enum class AccessLevel {
    READ_PRUNED_AST,   // Default: Returns AST-skeletonized code (60-80% token reduction)
    READ_RAW_SOURCE,   // Full raw file context (requires explicit grant)
    WRITE_SANDBOXED,   // Writes permitted only to ephemeral worktrees / scratch
    WRITE_DIRECT,      // Direct write to codebase
    DENIED             // Access blocked
}

data class PluginPermissionPolicy(
    val pluginId: String,
    val pluginName: String,
    val isSandboxed: Boolean,
    val defaultReadLevel: AccessLevel,
    val canWriteDirect: Boolean,
    val enforceTokenPruning: Boolean,
    val allowedPathPrefixes: List<String> = listOf("workplace/", "user/inputs/"),
    val restrictedPathPrefixes: List<String> = listOf(".nb/context/ledger/", ".nb/context/invariants/")
)

data class AccessRequestResult(
    val granted: Boolean,
    val effectiveAccessLevel: AccessLevel,
    val tokenPruned: Boolean,
    val reason: String,
    val timestamp: String = Instant.now().toString()
)

data class SandboxAuditRecord(
    val timestamp: String,
    val pluginId: String,
    val targetPath: String,
    val requestedLevel: AccessLevel,
    val effectiveLevel: AccessLevel,
    val granted: Boolean,
    val reason: String
)

class SandboxPermissionBroker private constructor() {

    private val policies = ConcurrentHashMap<String, PluginPermissionPolicy>()
    private val auditLogs = mutableListOf<SandboxAuditRecord>()

    init {
        // Register known IDE LLM / AI plugins with safe defaults
        registerPolicy(
            PluginPermissionPolicy(
                pluginId = "com.intellij.ai",
                pluginName = "JetBrains AI Assistant",
                isSandboxed = true,
                defaultReadLevel = AccessLevel.READ_PRUNED_AST,
                canWriteDirect = false,
                enforceTokenPruning = true
            )
        )
        registerPolicy(
            PluginPermissionPolicy(
                pluginId = "com.github.copilot",
                pluginName = "GitHub Copilot",
                isSandboxed = true,
                defaultReadLevel = AccessLevel.READ_PRUNED_AST,
                canWriteDirect = false,
                enforceTokenPruning = true
            )
        )
        registerPolicy(
            PluginPermissionPolicy(
                pluginId = "com.sourcegraph.cody",
                pluginName = "Sourcegraph Cody",
                isSandboxed = true,
                defaultReadLevel = AccessLevel.READ_PRUNED_AST,
                canWriteDirect = false,
                enforceTokenPruning = true
            )
        )
        registerPolicy(
            PluginPermissionPolicy(
                pluginId = "com.continue.continue",
                pluginName = "Continue Agentic Extension",
                isSandboxed = true,
                defaultReadLevel = AccessLevel.READ_PRUNED_AST,
                canWriteDirect = true,
                enforceTokenPruning = true
            )
        )
        registerPolicy(
            PluginPermissionPolicy(
                pluginId = "local_agent_runner",
                pluginName = "Percipience Local Autonomous Agent",
                isSandboxed = false,
                defaultReadLevel = AccessLevel.READ_PRUNED_AST,
                canWriteDirect = true,
                enforceTokenPruning = true
            )
        )
    }

    companion object {
        val instance: SandboxPermissionBroker by lazy { SandboxPermissionBroker() }
    }

    fun registerPolicy(policy: PluginPermissionPolicy) {
        policies[policy.pluginId] = policy
    }

    fun getPolicy(pluginId: String): PluginPermissionPolicy {
        return policies[pluginId] ?: PluginPermissionPolicy(
            pluginId = pluginId,
            pluginName = "Unknown Sandboxed Plugin ($pluginId)",
            isSandboxed = true,
            defaultReadLevel = AccessLevel.READ_PRUNED_AST,
            canWriteDirect = false,
            enforceTokenPruning = true
        )
    }

    fun getAllPolicies(): Map<String, PluginPermissionPolicy> = policies.toMap()

    fun getAuditLogs(): List<SandboxAuditRecord> = synchronized(auditLogs) { auditLogs.toList() }

    fun checkAccess(
        pluginId: String,
        targetRelativePath: String,
        requestedLevel: AccessLevel
    ): AccessRequestResult {
        val policy = getPolicy(pluginId)
        val normalizedPath = targetRelativePath.replace("\\", "/")

        // 1. Check restricted paths (e.g., Merkle Ledger & Invariants cannot be modified)
        if (policy.restrictedPathPrefixes.any { normalizedPath.startsWith(it) }) {
            if (requestedLevel == AccessLevel.WRITE_DIRECT || requestedLevel == AccessLevel.WRITE_SANDBOXED) {
                val record = SandboxAuditRecord(
                    timestamp = Instant.now().toString(),
                    pluginId = pluginId,
                    targetPath = normalizedPath,
                    requestedLevel = requestedLevel,
                    effectiveLevel = AccessLevel.DENIED,
                    granted = false,
                    reason = "DENIED: Target path '$normalizedPath' is a protected Merkle ledger or platform invariant."
                )
                synchronized(auditLogs) { auditLogs.add(record) }
                return AccessRequestResult(
                    granted = false,
                    effectiveAccessLevel = AccessLevel.DENIED,
                    tokenPruned = false,
                    reason = record.reason
                )
            }
        }

        // 2. Determine effective read access level (enforcing token reduction for sandboxed LLMs)
        val effectiveLevel = when (requestedLevel) {
            AccessLevel.READ_RAW_SOURCE -> {
                if (policy.enforceTokenPruning && policy.isSandboxed) {
                    AccessLevel.READ_PRUNED_AST
                } else {
                    AccessLevel.READ_RAW_SOURCE
                }
            }
            AccessLevel.READ_PRUNED_AST -> AccessLevel.READ_PRUNED_AST
            AccessLevel.WRITE_DIRECT -> {
                if (policy.canWriteDirect) AccessLevel.WRITE_DIRECT else AccessLevel.WRITE_SANDBOXED
            }
            AccessLevel.WRITE_SANDBOXED -> AccessLevel.WRITE_SANDBOXED
            AccessLevel.DENIED -> AccessLevel.DENIED
        }

        val tokenPruned = (effectiveLevel == AccessLevel.READ_PRUNED_AST)
        val reason = if (tokenPruned && requestedLevel == AccessLevel.READ_RAW_SOURCE) {
            "GRANTED_WITH_TOKEN_PRUNING: Sandbox policy enforced AST token skeletonization (60-80% savings)."
        } else {
            "ACCESS_GRANTED: Effective level $effectiveLevel"
        }

        val record = SandboxAuditRecord(
            timestamp = Instant.now().toString(),
            pluginId = pluginId,
            targetPath = normalizedPath,
            requestedLevel = requestedLevel,
            effectiveLevel = effectiveLevel,
            granted = true,
            reason = reason
        )
        synchronized(auditLogs) { auditLogs.add(record) }

        return AccessRequestResult(
            granted = true,
            effectiveAccessLevel = effectiveLevel,
            tokenPruned = tokenPruned,
            reason = reason
        )
    }
}
