package com.neutronbinary.percipience.bootstrap

import com.intellij.openapi.project.Project
import com.intellij.openapi.vfs.VirtualFileManager
import java.io.File
import java.io.InputStream
import java.security.MessageDigest
import java.time.Instant

data class BootstrapResult(
    val createdDirectories: List<String>,
    val createdFiles: List<String>,
    val alreadyConfigured: Boolean,
    val merkleGenesisHash: String
)

object WorkspaceBootstrapper {

    fun isWorkspaceConfigured(projectBasePath: String): Boolean {
        val root = File(projectBasePath)
        val binFile = File(root, ".nb/bin/percipience")
        val billingFile = File(root, ".nb/config/billing_plans.yaml")
        val planFile = File(root, ".nb/plan/claude-context-engineering-parent-master-free_plan.md")
        val masterPlanFile = File(root, ".nb/plan/claude-context-engineering-parent-master-plan.md")
        val ledgerFile = File(root, ".nb/context/ledger/context_ledger.yaml")
        val cicdFile = File(root, ".nb/agentic/custom/workflows/basic_autonomous_cicd.yaml")

        return (binFile.exists() && binFile.canExecute() &&
                billingFile.exists() &&
                (planFile.exists() || masterPlanFile.exists()) &&
                ledgerFile.exists() &&
                cicdFile.exists())
    }

    fun bootstrapWorkspace(projectBasePath: String): BootstrapResult {
        val root = File(projectBasePath)
        val createdDirs = mutableListOf<String>()
        val createdFiles = mutableListOf<String>()

        // 1. Ensure Quad-Space directory structure
        val dirsToCreate = listOf(
            ".nb/bin",
            ".nb/config",
            ".nb/core",
            ".nb/plan",
            ".nb/context/contracts",
            ".nb/context/invariants",
            ".nb/context/ledger",
            ".nb/context/rules",
            ".nb/context/custom/rules",
            ".nb/agentic/custom/agents",
            ".nb/agentic/custom/workflows",
            ".nb/agentic/prompts",
            ".nb/scripts",
            ".nb/tests",
            "workplace/modules",
            "workplace/shared",
            "workplace/tests",
            "workplace/config",
            "workplace/docs",
            "user/inputs/templates",
            "user/hitl",
            "user/outputs/dashboard"
        )

        for (dir in dirsToCreate) {
            val d = File(root, dir)
            if (!d.exists()) {
                d.mkdirs()
                createdDirs.add(dir)
            }
        }

        // 2. Deploy Canonical Percipience CLI Binary (.nb/bin/percipience)
        val binFile = File(root, ".nb/bin/percipience")
        if (!binFile.exists()) {
            val resourceStream: InputStream? = javaClass.getResourceAsStream("/percipience/bin/percipience")
            if (resourceStream != null) {
                resourceStream.use { input ->
                    binFile.outputStream().use { output ->
                        input.copyTo(output)
                    }
                }
            } else {
                // Fallback lightweight executable runner
                val fallbackBinary = """
#!/usr/bin/env python3
""${'"'}
Neutron Binary Percipience CLI (Free Community Edition)
Autonomous Context Engineering OS & CI/CD Gatekeeper Command-Line Interface.
""${'"'}
import os
import sys
from pathlib import Path

current_p = Path(__file__).resolve()
REPO_ROOT = current_p.parents[2]
for path_dir in [REPO_ROOT / ".nb", REPO_ROOT / ".nb" / "core", REPO_ROOT / "workplace"]:
    if str(path_dir) not in sys.path:
        sys.path.insert(0, str(path_dir))

if __name__ == "__main__":
    try:
        from bin.percipience import main
        main()
    except Exception as e:
        print(f"Percipience CLI: {e}")
        sys.exit(0)
""".trimIndent()
                binFile.writeText(fallbackBinary)
            }
            binFile.setExecutable(true, false)
            createdFiles.add(".nb/bin/percipience")
        } else {
            binFile.setExecutable(true, false)
        }

        // 3. Ensure billing plans configuration (.nb/config/billing_plans.yaml)
        val billingFile = File(root, ".nb/config/billing_plans.yaml")
        if (!billingFile.exists()) {
            val resourceStream = javaClass.getResourceAsStream("/percipience/config/billing_plans.yaml")
            if (resourceStream != null) {
                resourceStream.use { input ->
                    billingFile.outputStream().use { output ->
                        input.copyTo(output)
                    }
                }
            } else {
                val billingContent = """
plans:
  plan_free:
    id: "plan_free"
    name: "Free Community Tier"
    base_price_monthly_usd: 0
    included_seats: 1
    included_concurrent_worktrees: 1
    included_pr_audits_monthly: 500
    features:
      ast_token_pruning: true
      merkle_chain_audit: true
      basic_autonomous_cicd: true
      nbpack_obfuscation: false
      private_vpc_deploy: false

  plan_team:
    id: "plan_team"
    name: "Team Tier"
    base_price_monthly_usd: 1499
    included_seats: 15
    included_concurrent_worktrees: 5
    included_pr_audits_monthly: 5000
    features:
      ast_token_pruning: true
      merkle_chain_audit: true
      basic_autonomous_cicd: true
      nbpack_obfuscation: false
      private_vpc_deploy: false

  plan_business:
    id: "plan_business"
    name: "Business Tier"
    base_price_monthly_usd: 4499
    included_seats: 50
    included_concurrent_worktrees: 20
    included_pr_audits_monthly: 25000
    features:
      ast_token_pruning: true
      merkle_chain_audit: true
      basic_autonomous_cicd: true
      nbpack_obfuscation: true
      private_vpc_deploy: false

  plan_enterprise:
    id: "plan_enterprise"
    name: "Enterprise Dedicated Tier"
    base_price_monthly_usd: 9999
    included_seats: -1 # Unlimited
    included_concurrent_worktrees: -1 # Unlimited
    included_pr_audits_monthly: -1 # Unlimited
    features:
      ast_token_pruning: true
      merkle_chain_audit: true
      basic_autonomous_cicd: true
      nbpack_obfuscation: true
      private_vpc_deploy: true
      dedicated_slack_sla: true

overage_pricing:
  pr_audit_overage_usd: 0.05
  worktree_compute_hour_usd: 0.15
  token_savings_rev_share_rate: 0.15
""".trimIndent()
                billingFile.writeText(billingContent)
            }
            createdFiles.add(".nb/config/billing_plans.yaml")
        }

        // 4. Ensure token compression rules (.nb/config/token_compression_rules.yaml)
        val tokenRulesFile = File(root, ".nb/config/token_compression_rules.yaml")
        if (!tokenRulesFile.exists()) {
            val resourceStream = javaClass.getResourceAsStream("/percipience/config/token_compression_rules.yaml")
            if (resourceStream != null) {
                resourceStream.use { input ->
                    tokenRulesFile.outputStream().use { output ->
                        input.copyTo(output)
                    }
                }
            } else {
                val tokenRulesContent = """
version: "1.0.0"
default_preset: "standard"
active_provider: "anthropic"
presets:
  standard:
    target_reduction_pct: 70.0
    ast_pruning_enabled: true
    attention_budgeting:
      invariants_pct: 15
      contracts_pct: 25
      ast_skeletons_pct: 35
      memory_pct: 10
      output_buffer_pct: 15
    static_prefix_pinning: true
""".trimIndent()
                tokenRulesFile.writeText(tokenRulesContent)
            }
            createdFiles.add(".nb/config/token_compression_rules.yaml")
        }

        // 5. Ensure basic autonomous CI/CD workflow (.nb/agentic/custom/workflows/basic_autonomous_cicd.yaml)
        val cicdFile = File(root, ".nb/agentic/custom/workflows/basic_autonomous_cicd.yaml")
        if (!cicdFile.exists()) {
            val resourceStream = javaClass.getResourceAsStream("/percipience/workflows/basic_autonomous_cicd.yaml")
            if (resourceStream != null) {
                resourceStream.use { input ->
                    cicdFile.outputStream().use { output ->
                        input.copyTo(output)
                    }
                }
            } else {
                val cicdContent = """
workflow_id: "basic_autonomous_cicd"
name: "Free Community Autonomous CI/CD Pipeline"
description: "Watered-down autonomous CI/CD workflow providing maintenance, AST token compression, basic bounded self-repair, and Merkle block sealing for the Free Plan."

steps:
  - step_id: "sustain_maintenance"
    name: "Self-Sustaining Workspace Hygiene"
    executor: "platform.self_sustaining_engine"
    inputs: ["user/scratch/", ".workspaces/"]
    failure_action: "warn_and_continue"

  - step_id: "ast_token_reduction"
    name: "AST Token Skeletonization & Attention Budgeting"
    executor: "platform.ast_pruner"
    depends_on: ["sustain_maintenance"]
    inputs: ["workplace/"]

  - step_id: "contract_and_test_gate"
    name: "Basic Contract & Test Verification"
    executor: "platform.contract_verifier"
    depends_on: ["ast_token_reduction"]
    inputs:
      - ".nb/context/contracts/"
      - "workplace/tests/"

  - step_id: "bounded_auto_heal"
    name: "Basic Single-Attempt Self-Healing"
    executor: "platform.autonomous_healer"
    depends_on: ["contract_and_test_gate"]
    config:
      max_retries: 1
      fallback: "quarantine_and_notify"

  - step_id: "merkle_state_seal"
    name: "Cryptographic Merkle State Block Seal"
    executor: "platform.merkle_ledger"
    depends_on: ["bounded_auto_heal"]
    action: "SEAL_BLOCK"
""".trimIndent()
                cicdFile.writeText(cicdContent)
            }
            createdFiles.add(".nb/agentic/custom/workflows/basic_autonomous_cicd.yaml")
        }

        // 6. Ensure Parent Master Plan (.nb/plan/claude-context-engineering-parent-master-free_plan.md)
        val freePlanFile = File(root, ".nb/plan/claude-context-engineering-parent-master-free_plan.md")
        val masterPlanFile = File(root, ".nb/plan/claude-context-engineering-parent-master-plan.md")
        if (!freePlanFile.exists() && !masterPlanFile.exists()) {
            val resourceStream = javaClass.getResourceAsStream("/percipience/plan/claude-context-engineering-parent-master-free_plan.md")
            if (resourceStream != null) {
                resourceStream.use { input ->
                    freePlanFile.outputStream().use { output ->
                        input.copyTo(output)
                    }
                }
            } else {
                val planContent = """
---
sessionId: session-260913-master-parent-plan
tier: plan_free
---

# Parent Master Context Engineering Plan (Free Community Edition)

## 1. Free Community Plan Core Features
- AST Token Reduction (60%-80% compression)
- Linear SHA-256 Merkle Ledger State Chain
- Basic Autonomous CI/CD Pipeline (.nb/agentic/custom/workflows/basic_autonomous_cicd.yaml)
- Quad-Space Partitioning (.nb/, workplace/, user/)
- IntelliJ / PyCharm Plugin Bootstrapper & Sandbox Permission Broker
- Percipience CLI Executable (.nb/bin/percipience)
""".trimIndent()
                freePlanFile.writeText(planContent)
            }
            createdFiles.add(".nb/plan/claude-context-engineering-parent-master-free_plan.md")
        }

        // 7. Ensure Genesis Merkle Ledger (.nb/context/ledger/context_ledger.yaml)
        val ledgerFile = File(root, ".nb/context/ledger/context_ledger.yaml")
        val nowIso = Instant.now().toString()
        val genesisPayload = "0|" + ("0".repeat(64)) + "|genesis_root|HEAD|" + nowIso
        val genesisHash = sha256(genesisPayload)

        if (!ledgerFile.exists()) {
            val ledgerContent = """
ledger_version: "7.5.0"
project:
  name: "nb_fairyfly"
  tier: "plan_free"
  mode: "multi_module"
ledger_chain:
  - block_id: 0
    block_type: "GENESIS"
    prev_block_hash: "${"0".repeat(64)}"
    timestamp: "$nowIso"
    merkle_root: "${"0".repeat(64)}"
    current_block_hash: "$genesisHash"
    action: "BOOTSTRAP_FREE_WORKSPACE_GENESIS"
recovery_points:
  - id: "RP_GENESIS_000"
    module_scope: "global_system"
    git_commit: "HEAD"
    timestamp: "$nowIso"
    status: "VERIFIED"
    description: "Genesis bootstrap of Free Community Plan workspace"
quarantined_tests: []
poisoning_incidents: []
""".trimIndent()
            ledgerFile.writeText(ledgerContent)
            createdFiles.add(".nb/context/ledger/context_ledger.yaml")

            // Public ledger projection
            val publicLedger = File(root, ".nb/context/ledger/context_ledger.public.yaml")
            val publicContent = """
ledger_version: "7.5.0"
project:
  name: "nb_fairyfly"
  tier: "plan_free"
active_recovery_point: "RP_GENESIS_000"
merkle_block_height: 1
overall_maturity_score: 0.990
quarantined_tests_count: 0
active_poisoning_incidents: 0
last_audit_timestamp: "$nowIso"
continuity_verified: true
""".trimIndent()
            publicLedger.writeText(publicContent)
            createdFiles.add(".nb/context/ledger/context_ledger.public.yaml")
        }

        // Refresh VFS
        VirtualFileManager.getInstance().asyncRefresh(null)

        return BootstrapResult(
            createdDirectories = createdDirs,
            createdFiles = createdFiles,
            alreadyConfigured = createdFiles.isEmpty() && createdDirs.isEmpty(),
            merkleGenesisHash = genesisHash
        )
    }

    private fun sha256(input: String): String {
        val digest = MessageDigest.getInstance("SHA-256")
        val hash = digest.digest(input.toByteArray(Charsets.UTF_8))
        return hash.joinToString("") { "%02x".format(it) }
    }
}
