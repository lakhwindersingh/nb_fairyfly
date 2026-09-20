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

data class WorkspaceMetrics(
    val tokenSavings: TokenSavingsSummary,
    val merkleLedger: MerkleLedgerSummary
)

object WorkspaceLedgerReader {

    fun readWorkspaceMetrics(projectBasePath: String?): WorkspaceMetrics {
        val root = if (!projectBasePath.isNullOrBlank()) File(projectBasePath) else null
        val tokenSavings = readTokenSavings(root)
        val merkleLedger = readMerkleLedger(root)
        return WorkspaceMetrics(tokenSavings, merkleLedger)
    }

    private fun findLedgerFile(root: File?, relativePaths: List<String>): File? {
        if (root == null || !root.exists()) return null
        for (rel in relativePaths) {
            val f = File(root, rel)
            if (f.exists() && f.isFile) return f
        }
        return null
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
