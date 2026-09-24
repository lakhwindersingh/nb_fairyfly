package com.neutronbinary.percipience.ledger

import java.io.File
import java.text.DecimalFormat

data class TokenSavingsSummary(
    val totalEvents: Int = 0,
    val totalUncompressedTokens: Long = 0,
    val totalPrunedTokens: Long = 0,
    val totalTokensSaved: Long = 0,
    val averageReductionPct: Double = 0.0,
    val totalGrossSavingsUsd: Double = 0.0,
    val totalRevShareFeeUsd: Double = 0.0,
    val totalNetSavingsUsd: Double = 0.0,
    val lastUpdated: String = "",
    val exists: Boolean = false
) {
    fun formatTokensSaved(): String {
        return when {
            totalTokensSaved >= 1_000_000 -> "%.1fM".format(totalTokensSaved / 1_000_000.0)
            totalTokensSaved >= 1_000 -> "%.1fk".format(totalTokensSaved / 1_000.0)
            else -> "$totalTokensSaved"
        }
    }

    fun formatReductionPct(): String {
        return "%.1f%%".format(averageReductionPct)
    }

    fun formatGrossSavingsUsd(): String {
        return "$%.4f".format(totalGrossSavingsUsd)
    }

    fun formatNetSavingsUsd(): String {
        return "$%.4f".format(totalNetSavingsUsd)
    }
}

data class MerkleLedgerSummary(
    val merkleBlockHeight: Int = 0,
    val activeRecoveryPoint: String = "RP_GENESIS_000",
    val overallMaturityScore: Double = 0.99,
    val quarantinedTestsCount: Int = 0,
    val activePoisoningIncidents: Int = 0,
    val continuityVerified: Boolean = true,
    val tier: String = "plan_free",
    val lastAuditTimestamp: String = "",
    val exists: Boolean = false
)

data class TierInfo(
    val tierId: String = "plan_free",
    val tierName: String = "Free Community Tier",
    val includedSeats: Int = 1,
    val includedWorktrees: Int = 1,
    val includedAuditsMonthly: Int = 500,
    val canPackNbpack: Boolean = false,
    val canCreateCustomAgents: Boolean = false,
    val canUseWorktrees: Boolean = false,
    val canUseDriftReconciliation: Boolean = false,
    val canUseSwarmOrchestrator: Boolean = false,
    val canUsePrivateVpc: Boolean = false,
    val canUseWormEgress: Boolean = false,
    val exposeBasicPlatformTools: Boolean = false
) {
    fun formatQuota(): String {
        val seats = if (includedSeats < 0) "Unlimited Seats" else "$includedSeats Seat${if (includedSeats > 1) "s" else ""}"
        val wts = if (includedWorktrees < 0) "Unlimited Worktrees" else "$includedWorktrees Worktree${if (includedWorktrees > 1) "s" else ""}"
        val audits = if (includedAuditsMonthly < 0) "Unlimited Audits" else "$includedAuditsMonthly Audits/mo"
        return "$seats | $wts | $audits"
    }
}

data class WorkspaceMetrics(
    val tokenSavings: TokenSavingsSummary,
    val merkleLedger: MerkleLedgerSummary,
    val tierInfo: TierInfo = TierInfo()
)

object WorkspaceLedgerReader {

    fun readWorkspaceMetrics(projectBasePath: String?): WorkspaceMetrics {
        val root = if (!projectBasePath.isNullOrBlank()) File(projectBasePath) else null
        val tokenSavings = readTokenSavings(root)
        val merkleLedger = readMerkleLedger(root)
        val tierInfo = resolveTier(root)
        return WorkspaceMetrics(tokenSavings, merkleLedger, tierInfo)
    }

    private fun findLedgerFile(root: File?, relativePaths: List<String>): File? {
        if (root == null || !root.exists()) return null
        for (rel in relativePaths) {
            val f = File(root, rel)
            if (f.exists() && f.isFile) return f
        }
        return null
    }

    fun resolveTier(projectRoot: File?): TierInfo {
        var rawTier: String? = System.getenv("PERCIPIENCE_PLAN")
        var tenantName: String? = null

        // 1. Check license files
        val licenseFiles = listOf(
            ".nb/context/tenant_license.json",
            ".nb/tenant_license.json",
            "tenant_license.json",
            ".percipience_license.json",
            ".nb/context/PERCIPIENCE_LICENSE.json",
            ".nb/PERCIPIENCE_LICENSE.json",
            "workplace/modules/mod_intellij_plugin/src/main/resources/percipience/tenant_license.json"
        )
        val licFile = findLedgerFile(projectRoot, licenseFiles)
        if (licFile != null && licFile.exists()) {
            try {
                val text = licFile.readText(Charsets.UTF_8)
                val tierMatch = Regex("\"tier\"\\s*:\\s*\"([^\"]+)\"").find(text)
                if (tierMatch != null) {
                    rawTier = tierMatch.groupValues[1]
                }
                val nameMatch = Regex("\"tier_name\"\\s*:\\s*\"([^\"]+)\"").find(text)
                if (nameMatch != null) {
                    tenantName = nameMatch.groupValues[1]
                }
            } catch (ignored: Exception) {}
        }

        // 2. Check context_ledger.yaml if still not resolved
        if (rawTier.isNullOrBlank()) {
            val ledgerSummary = readMerkleLedger(projectRoot)
            if (ledgerSummary.exists && ledgerSummary.tier.isNotBlank()) {
                rawTier = ledgerSummary.tier
            }
        }

        val normalized = when (rawTier?.lowercase()?.trim()) {
            "team", "plan_team" -> "plan_team"
            "business", "plan_business" -> "plan_business"
            "enterprise", "plan_enterprise", "dedicated" -> "plan_enterprise"
            else -> "plan_free"
        }

        return when (normalized) {
            "plan_enterprise" -> TierInfo(
                tierId = "plan_enterprise",
                tierName = tenantName ?: "Enterprise Dedicated Tier",
                includedSeats = -1,
                includedWorktrees = -1,
                includedAuditsMonthly = -1,
                canPackNbpack = true,
                canCreateCustomAgents = true,
                canUseWorktrees = true,
                canUseDriftReconciliation = true,
                canUseSwarmOrchestrator = true,
                canUsePrivateVpc = true,
                canUseWormEgress = true,
                exposeBasicPlatformTools = true
            )
            "plan_business" -> TierInfo(
                tierId = "plan_business",
                tierName = tenantName ?: "Business Tier",
                includedSeats = 50,
                includedWorktrees = 20,
                includedAuditsMonthly = 25000,
                canPackNbpack = true,
                canCreateCustomAgents = true,
                canUseWorktrees = true,
                canUseDriftReconciliation = true,
                canUseSwarmOrchestrator = false,
                canUsePrivateVpc = false,
                canUseWormEgress = false,
                exposeBasicPlatformTools = true
            )
            "plan_team" -> TierInfo(
                tierId = "plan_team",
                tierName = tenantName ?: "Team Tier",
                includedSeats = 15,
                includedWorktrees = 5,
                includedAuditsMonthly = 5000,
                canPackNbpack = false,
                canCreateCustomAgents = true,
                canUseWorktrees = true,
                canUseDriftReconciliation = true,
                canUseSwarmOrchestrator = false,
                canUsePrivateVpc = false,
                canUseWormEgress = false,
                exposeBasicPlatformTools = false
            )
            else -> TierInfo(
                tierId = "plan_free",
                tierName = tenantName ?: "Free Community Tier",
                includedSeats = 1,
                includedWorktrees = 1,
                includedAuditsMonthly = 500,
                canPackNbpack = false,
                canCreateCustomAgents = false,
                canUseWorktrees = false,
                canUseDriftReconciliation = false,
                canUseSwarmOrchestrator = false,
                canUsePrivateVpc = false,
                canUseWormEgress = false,
                exposeBasicPlatformTools = false
            )
        }
    }

    fun readTokenSavings(projectRoot: File?): TokenSavingsSummary {
        val file = findLedgerFile(
            projectRoot,
            listOf(
                ".nb/context/ledger/token_savings_ledger.yaml",
                "context/ledger/token_savings_ledger.yaml",
                ".nb/context/token_savings_ledger.yaml"
            )
        ) ?: return TokenSavingsSummary()

        try {
            val text = file.readText(Charsets.UTF_8)
            var totalEvents = 0
            var uncompressed = 0L
            var pruned = 0L
            var saved = 0L
            var avgReduction = 0.0
            var grossUsd = 0.0
            var revShareUsd = 0.0
            var netUsd = 0.0
            var lastUpdated = ""

            val lines = text.lines()
            for (line in lines) {
                val trimmed = line.trim()
                when {
                    trimmed.startsWith("total_events:") -> {
                        totalEvents = trimmed.substringAfter(":").trim().toIntOrNull() ?: 0
                    }
                    trimmed.startsWith("total_uncompressed_tokens:") -> {
                        uncompressed = trimmed.substringAfter(":").trim().toLongOrNull() ?: 0L
                    }
                    trimmed.startsWith("total_pruned_tokens:") -> {
                        pruned = trimmed.substringAfter(":").trim().toLongOrNull() ?: 0L
                    }
                    trimmed.startsWith("total_tokens_saved:") -> {
                        saved = trimmed.substringAfter(":").trim().toLongOrNull() ?: 0L
                    }
                    trimmed.startsWith("average_reduction_pct:") -> {
                        avgReduction = trimmed.substringAfter(":").trim().toDoubleOrNull() ?: 0.0
                    }
                    trimmed.startsWith("total_gross_savings_usd:") -> {
                        grossUsd = trimmed.substringAfter(":").trim().toDoubleOrNull() ?: 0.0
                    }
                    trimmed.startsWith("total_rev_share_fee_usd:") -> {
                        revShareUsd = trimmed.substringAfter(":").trim().toDoubleOrNull() ?: 0.0
                    }
                    trimmed.startsWith("total_net_savings_usd:") -> {
                        netUsd = trimmed.substringAfter(":").trim().toDoubleOrNull() ?: 0.0
                    }
                    trimmed.startsWith("last_updated:") -> {
                        lastUpdated = trimmed.substringAfter(":").trim().trim('\'', '"')
                    }
                }
            }

            // Fallback calculation if average reduction wasn't directly in summary
            if (avgReduction == 0.0 && uncompressed > 0) {
                avgReduction = (saved.toDouble() / uncompressed.toDouble()) * 100.0
            }

            return TokenSavingsSummary(
                totalEvents = totalEvents,
                totalUncompressedTokens = uncompressed,
                totalPrunedTokens = pruned,
                totalTokensSaved = saved,
                averageReductionPct = Math.round(avgReduction * 100.0) / 100.0,
                totalGrossSavingsUsd = grossUsd,
                totalRevShareFeeUsd = revShareUsd,
                totalNetSavingsUsd = netUsd,
                lastUpdated = lastUpdated,
                exists = true
            )
        } catch (e: Exception) {
            return TokenSavingsSummary()
        }
    }

    fun readMerkleLedger(projectRoot: File?): MerkleLedgerSummary {
        val file = findLedgerFile(
            projectRoot,
            listOf(
                ".nb/context/ledger/context_ledger.public.yaml",
                "context/ledger/context_ledger.public.yaml",
                ".nb/context/ledger/context_ledger.yaml",
                "context/ledger/context_ledger.yaml"
            )
        ) ?: return MerkleLedgerSummary()

        try {
            val text = file.readText(Charsets.UTF_8)
            var blockHeight = 0
            var rp = "RP_GENESIS_000"
            var score = 0.99
            var quarantined = 0
            var poisoning = 0
            var continuity = true
            var tier = "plan_free"
            var lastAudit = ""

            val lines = text.lines()
            for (line in lines) {
                val trimmed = line.trim()
                when {
                    trimmed.startsWith("merkle_block_height:") -> {
                        blockHeight = trimmed.substringAfter(":").trim().toIntOrNull() ?: 0
                    }
                    trimmed.startsWith("active_recovery_point:") -> {
                        rp = trimmed.substringAfter(":").trim().trim('\'', '"')
                    }
                    trimmed.startsWith("overall_maturity_score:") -> {
                        score = trimmed.substringAfter(":").trim().toDoubleOrNull() ?: 0.99
                    }
                    trimmed.startsWith("quarantined_tests_count:") -> {
                        quarantined = trimmed.substringAfter(":").trim().toIntOrNull() ?: 0
                    }
                    trimmed.startsWith("active_poisoning_incidents:") -> {
                        poisoning = trimmed.substringAfter(":").trim().toIntOrNull() ?: 0
                    }
                    trimmed.startsWith("continuity_verified:") -> {
                        continuity = trimmed.substringAfter(":").trim().toBooleanStrictOrNull() ?: true
                    }
                    trimmed.startsWith("tier:") -> {
                        tier = trimmed.substringAfter(":").trim().trim('\'', '"')
                    }
                    trimmed.startsWith("last_audit_timestamp:") -> {
                        lastAudit = trimmed.substringAfter(":").trim().trim('\'', '"')
                    }
                }
            }

            return MerkleLedgerSummary(
                merkleBlockHeight = blockHeight,
                activeRecoveryPoint = rp,
                overallMaturityScore = score,
                quarantinedTestsCount = quarantined,
                activePoisoningIncidents = poisoning,
                continuityVerified = continuity,
                tier = tier,
                lastAuditTimestamp = lastAudit,
                exists = true
            )
        } catch (e: Exception) {
            return MerkleLedgerSummary()
        }
    }
}
