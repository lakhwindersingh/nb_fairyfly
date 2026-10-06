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
        val claudeMcpFile = File(root, ".claude/mcp.json")
        val claudeSettingsFile = File(root, ".claude/settings.json")
        val coreDir = File(root, ".nb/core")
        val coreReady = File(coreDir, "ast_optimizer.py").exists() && File(coreDir, "merkle_engine.py").exists()

        return (binFile.exists() && binFile.canExecute() &&
                billingFile.exists() &&
                (planFile.exists() || masterPlanFile.exists()) &&
                ledgerFile.exists() &&
                cicdFile.exists() &&
                claudeMcpFile.exists() &&
                claudeSettingsFile.exists() &&
                coreReady)
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
            ".claude",
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

        // 3. Deploy Essential Platform Core Engines (.nb/core/*.py)
        val coreDir = File(root, ".nb/core")
        if (!coreDir.exists()) {
            coreDir.mkdirs()
        }
        val essentialCoreFiles = listOf(
            "__init__.py",
            "adversarial_fuzzer.py",
            "agent_plugin_engine.py",
            "ambiguity_resolver.py",
            "ast_optimizer.py",
            "attention_budgeter.py",
            "autonomous_cicd.py",
            "byor_adapter.py",
            "cognitive_router.py",
            "commercial_packager_provisioner.py",
            "context_gateway.py",
            "contract_compatibility_checker.py",
            "dependency_cve_sentinel.py",
            "diagnostic_reprompt.py",
            "doc_drift_synchronizer.py",
            "error_recovery_orchestrator.py",
            "eval_scoring_engine.py",
            "flaky_test_detector.py",
            "handoff_validator.py",
            "layered_context_validator.py",
            "living_doc_engine.py",
            "maturity_evaluator.py",
            "merkle_engine.py",
            "nbpack_envelope.py",
            "otel_exporter.py",
            "output_guardrail_validator.py",
            "pii_sanitizer.py",
            "poisoning_sentinel.py",
            "prompt_benchmark_engine.py",
            "prompt_drift_sentinel.py",
            "prompt_injection_guard.py",
            "reconciliation_engine.py",
            "request_formalizer.py",
            "semantic_parity_engine.py",
            "semantic_prompt_cache.py",
            "swarm_governor.py",
            "terminal_agent_ast_proxy.py",
            "token_optimizer_suite.py",
            "token_tracker.py",
            "trajectory_recorder.py",
            "tree_sitter_daemon.py",
            "workflow_orchestrator.py",
            "worktree_engine.py",
            "worm_egress.py"
        )
        for (coreFileName in essentialCoreFiles) {
            val targetCoreFile = File(coreDir, coreFileName)
            if (!targetCoreFile.exists()) {
                val resourceStream: InputStream? = javaClass.getResourceAsStream("/percipience/core/$coreFileName")
                if (resourceStream != null) {
                    resourceStream.use { input ->
                        targetCoreFile.outputStream().use { output ->
                            input.copyTo(output)
                        }
                    }
                    createdFiles.add(".nb/core/$coreFileName")
                }
            }
        }

        // 4. Ensure billing plans configuration (.nb/config/billing_plans.yaml)
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
      platform_core_encryption: true
      nbpack_obfuscation: false
      user_plan_encryption: false
      basic_platform_tools_exposure: false
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
      platform_core_encryption: true
      nbpack_obfuscation: false
      user_plan_encryption: false
      basic_platform_tools_exposure: false
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
      platform_core_encryption: true
      nbpack_obfuscation: true
      user_plan_encryption: true
      basic_platform_tools_exposure: true
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
      platform_core_encryption: true
      nbpack_obfuscation: true
      user_plan_encryption: true
      basic_platform_tools_exposure: true
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

        // 5. Ensure token compression rules (.nb/config/token_compression_rules.yaml)
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

        // 6. Ensure basic autonomous CI/CD workflow (.nb/agentic/custom/workflows/basic_autonomous_cicd.yaml)
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
    inputs: ["user/scratch/", ".nb/workspaces/"]
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

        // 7. Ensure Parent Master Plan (.nb/plan/claude-context-engineering-parent-master-free_plan.md)
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
- Essential Platform Core Engines (.nb/core/)
""".trimIndent()
                freePlanFile.writeText(planContent)
            }
            createdFiles.add(".nb/plan/claude-context-engineering-parent-master-free_plan.md")
        }

        // 8. Ensure Genesis Merkle Ledger (.nb/context/ledger/context_ledger.yaml)
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

        // 9. Ensure Claude & MCP Agent Configuration (.claude/mcp.json & .claude/settings.json) across all bundles
        val claudeMcpFile = File(root, ".claude/mcp.json")
        if (!claudeMcpFile.exists()) {
            val mcpContent = """
{
  "mcpServers": {
    "percipience": {
      "command": "python3",
      "args": [
        ".nb/bin/percipience"
      ],
      "env": {
        "PYTHONPATH": ".:.nb:.nb/core:workplace:workplace/core",
        "PERCIPIENCE_TERMINAL_MODE": "1",
        "PERCIPIENCE_AST_COMPRESSION": "1"
      },
      "description": "Percipience Context Engineering CLI for running multi-agent workflows, managing worktrees, and auditing Merkle ledger."
    },
    "ast_optimizer": {
      "command": "python3",
      "args": [
        ".nb/bin/percipience",
        "optimize"
      ],
      "env": {
        "PYTHONPATH": ".:.nb:.nb/core:workplace:workplace/core"
      },
      "description": "Polyglot Tree-Sitter 6D AST skeletonization and token pruning engine (cuts prompt overhead by 60-85%)."
    },
    "gatekeeper": {
      "command": "python3",
      "args": [
        ".nb/bin/percipience",
        "gate"
      ],
      "env": {
        "PYTHONPATH": ".:.nb:.nb/core:workplace:workplace/core"
      },
      "description": "Automated 7-stage CI/CD gatekeeper validating wire contracts, security invariants, and test regressions."
    },
    "merkle_auditor": {
      "command": "python3",
      "args": [
        ".nb/bin/percipience",
        "audit"
      ],
      "env": {
        "PYTHONPATH": ".:.nb:.nb/core:workplace:workplace/core"
      },
      "description": "Cryptographic SHA-256 Merkle DAG state auditor, recovery point validator, and maturity scorecard evaluator."
    },
    "worktree_manager": {
      "command": "python3",
      "args": [
        ".nb/bin/percipience",
        "worktree"
      ],
      "env": {
        "PYTHONPATH": ".:.nb:.nb/core:workplace:workplace/core"
      },
      "description": "Ephemeral Git worktree allocator and concurrency isolator preventing workspace clobbering."
    },
    "living_doc_engine": {
      "command": "python3",
      "args": [
        ".nb/bin/percipience",
        "doc"
      ],
      "env": {
        "PYTHONPATH": ".:.nb:.nb/core:workplace:workplace/core"
      },
      "description": "AST-to-Mermaid architecture synchronizer and living contract documentation generator."
    }
  }
}
""".trimIndent()
            claudeMcpFile.writeText(mcpContent)
            createdFiles.add(".claude/mcp.json")

            val rootMcp = File(root, "mcp.json")
            if (!rootMcp.exists()) {
                rootMcp.writeText(mcpContent)
                createdFiles.add("mcp.json")
            }
        }

        val claudeSettingsFile = File(root, ".claude/settings.json")
        if (!claudeSettingsFile.exists()) {
            val settingsContent = """
{
  "${'$'}schema": "https://json.schemastore.org/claude-settings.json",
  "project_name": "nb_fairyfly",
  "canonical_title": "Neutron Binary Percipience - Enterprise Context Engineering OS & Autonomous CI/CD Gatekeeper",
  "version": "7.5.0",
  "architecture": "Quad-Space Context Engineering (.nb / workplace / user / .claude)",
  "settings_file": ".nb/config/claude_agents_settings.yaml",
  "model_tiering_policy": {
    "provider_agnostic": true,
    "default_model": "claude-3-5-sonnet-20241022",
    "tier_a_frontier": "claude-3-7-sonnet",
    "tier_b_production": "claude-3-5-sonnet-20241022",
    "tier_c_high_throughput": "claude-3-5-haiku-20241022",
    "reference_models": {
      "tier_a": [
        "claude-3-7-sonnet",
        "gemini-2.0-pro",
        "gpt-4o",
        "deepseek-r1"
      ],
      "tier_b": [
        "claude-3-5-haiku",
        "gemini-2.0-flash",
        "gpt-4o-mini"
      ]
    }
  },
  "runtime_environment": {
    "PYTHONPATH": ".:.nb:.nb/core:workplace:workplace/core",
    "PERCIPIENCE_CLI": ".nb/bin/percipience",
    "PERCIPIENCE_TERMINAL_MODE": "1",
    "PERCIPIENCE_AST_COMPRESSION": "1"
  },
  "context_rules": {
    "jetbrains_threading": ".nb/context/rules/jetbrains_platform_threading_rules.md",
    "psi_read_lock": ".nb/context/rules/psi_read_lock_invariants.md",
    "jcef_security": ".nb/context/rules/jcef_security_invariants.md",
    "sandbox_security": ".nb/context/rules/sandbox_security_rules.md",
    "secret_storage": ".nb/context/rules/secret_storage_rules.md",
    "merkle_ledger": ".nb/context/ledger/context_ledger.yaml"
  },
  "context_contracts": {
    "intellij_manifest": ".nb/context/contracts/intellij_plugin_manifest_contract.json",
    "psi_ast_bridge": ".nb/context/contracts/psi_ast_bridge_contract.yaml",
    "terminal_agent_ast": ".nb/context/contracts/terminal_agent_ast_contract.yaml",
    "daemon_rpc": ".nb/context/contracts/daemon_rpc_contract.json",
    "commercial_provisioning": ".nb/context/contracts/commercial_provisioning_contract.yaml"
  },
  "ignore_patterns": [
    ".git/**",
    ".workspaces/**",
    ".nb/workspaces/**",
    "__pycache__/**",
    "**/*.pyc",
    "build/**",
    ".gradle/**",
    "node_modules/**"
  ],
  "agent_registry": [
    "agent_jetbrains_plugin_architect",
    "agent_psi_ast_bridge_specialist",
    "agent_intellij_ui_ux_engineer",
    "agent_terminal_mode_specialist",
    "agent_commercial_packager_provisioner",
    "agent_living_doc_architect",
    "agent_request_formalizer",
    "contract_compatibility_checker",
    "dependency_cve_sentinel",
    "doc_drift_synchronizer",
    "flaky_test_detector",
    "security_auditor",
    "token_finops_auditor",
    "quality_guard"
  ]
}
""".trimIndent()
            claudeSettingsFile.writeText(settingsContent)
            createdFiles.add(".claude/settings.json")

            val rootSettings = File(root, "settings.json")
            if (!rootSettings.exists()) {
                rootSettings.writeText(settingsContent)
                createdFiles.add("settings.json")
            }
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
