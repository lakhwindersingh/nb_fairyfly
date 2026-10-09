"""
Test suite for Tier 3: Enterprise Tier Launch (Section 20.3 in TODO.md).

Validates:
- TODO-REV-15 / TODO-COMP-15: GitOps PR Bot, rich status cards, ephemeral previews, and slash commands.
- TODO-REV-16 / TODO-COMP-09: Hybrid Sparse-Dense Vector RAG Code Retrieval alongside AST Pruning.
- TODO-REV-18: Conventional-to-Quad-Space Repository Migrator (Analysis, Execution, Rollback).
- TODO-REV-19: Interactive Onboarding Setup Wizard (Scaffolding, MCP provisioning, Genesis Ledger).
"""

import os
import sys
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timezone

from workplace.core.gitops_pr_bot import GitOpsPRBot, SlashCommandResult
from workplace.core.vector_retrieval_engine import (
    HybridVectorRetrievalEngine,
    DeterministicCodeEmbedder,
    CodeChunk
)
from workplace.core.repository_migrator import (
    ConventionalRepositoryMigrator,
    MigrationAnalysisReport
)
from workplace.core.onboarding_wizard import (
    InteractiveOnboardingWizard,
    OnboardingConfig,
    OnboardingResult
)


class TestGitOpsPRBot(unittest.TestCase):
    """Unit tests for GitOps PR Bot (TODO-REV-15 / TODO-COMP-15)."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.bot = GitOpsPRBot(repo_root=Path(self.temp_dir))

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_format_status_card_contents(self):
        card = self.bot.format_status_card(
            pr_id="84",
            branch="feat/decentralized-agents",
            commit_sha="c0ffee123456",
            status="PASS",
            test_results={"passed": 292, "failed": 0, "skipped": 1, "total": 293},
            ast_savings={"tokens_saved": 85000, "gross_savings_usd": 0.255, "reduction_pct": 71.2},
            merkle_seal={"block_id": 204, "block_hash": "hash_sec_204", "merkle_root": "root_204"},
            security_verdict="CLEAN",
            collapsible_logs="All 292 tests passed cleanly."
        )

        self.assertIn("Percipience Context Engineering OS & CI/CD Gatekeeper", card)
        self.assertIn("feat/decentralized-agents", card)
        self.assertIn("#84", card)
        self.assertIn("85,000", card)
        self.assertIn("-71.2% Context Drift", card)
        self.assertIn("https://pr-84-c0ffee1.preview.percipience.internal", card)
        self.assertIn("<details>", card)
        self.assertIn("All 292 tests passed cleanly.", card)
        self.assertIn("/re-heal", card)
        self.assertIn("/rollback", card)

    def test_slash_command_dispatcher(self):
        # 1. /verify
        res_v = self.bot.handle_slash_command("/verify", pr_id="10", actor="alice")
        self.assertEqual(res_v.status, "SUCCESS")
        self.assertEqual(res_v.action_executed, "verify-gate")
        self.assertIn("Gatekeeper Verification Re-Run", res_v.reply_markdown)

        # 2. /rollback
        res_rb = self.bot.handle_slash_command("/rollback RP_STABLE_01", pr_id="10", actor="bob")
        self.assertEqual(res_rb.status, "SUCCESS")
        self.assertIn("RP_STABLE_01", res_rb.action_executed)
        self.assertIn("RP_STABLE_01", res_rb.reply_markdown)

        # 3. /preview
        res_p = self.bot.handle_slash_command("/preview", pr_id="10", actor="charlie")
        self.assertEqual(res_p.status, "SUCCESS")
        self.assertEqual(res_p.action_executed, "preview-deploy")
        self.assertIn("preview.percipience.internal", res_p.reply_markdown)

        # 4. /re-heal
        res_rh = self.bot.handle_slash_command("/re-heal", pr_id="10", actor="dave")
        self.assertEqual(res_rh.status, "SUCCESS")
        self.assertEqual(res_rh.action_executed, "re-heal")

        # 5. /help
        res_h = self.bot.handle_slash_command("/help", pr_id="10", actor="eve")
        self.assertEqual(res_h.status, "SUCCESS")
        self.assertIn("Supported commands", res_h.reply_markdown)

        # 6. Invalid command
        res_inv = self.bot.handle_slash_command("/nonexistent_cmd", pr_id="10")
        self.assertEqual(res_inv.status, "IGNORED")

        # Verify audit log was recorded
        audit_file = Path(self.temp_dir) / ".nb" / "context" / "ledger" / "gitops_bot_audit.jsonl"
        self.assertTrue(audit_file.exists())
        lines = audit_file.read_text(encoding="utf-8").strip().splitlines()
        self.assertGreaterEqual(len(lines), 5)

    def test_deploy_bot_manifest(self):
        manifest = self.bot.deploy_bot()
        self.assertEqual(manifest["status"], "DEPLOYED")
        wf_path = Path(manifest["workflow_file"])
        self.assertTrue(wf_path.exists())
        content = wf_path.read_text(encoding="utf-8")
        self.assertIn("Percipience GitOps PR Gatekeeper Bot", content)


class TestHybridVectorRetrievalEngine(unittest.TestCase):
    """Unit tests for Hybrid Vector RAG Retrieval Engine (TODO-REV-16 / TODO-COMP-09)."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.repo_root = Path(self.temp_dir)
        # Create sample files
        code_dir = self.repo_root / "workplace" / "core"
        code_dir.mkdir(parents=True, exist_ok=True)

        sample_py = (
            "class AuthenticationGatekeeper:\n"
            "    '''Enforces enterprise OIDC and SAML identity checks.'''\n"
            "    def verify_token(self, token: str) -> bool:\n"
            "        if not token:\n"
            "            return False\n"
            "        return token.startswith('bearer_sec_')\n\n"
            "def calculate_finops_savings(gross: float, rate: float = 0.15) -> float:\n"
            "    '''Calculates 15% revenue share fee for customer retained savings.'''\n"
            "    return gross * rate\n"
        )
        (code_dir / "auth_gate.py").write_text(sample_py, encoding="utf-8")

        self.engine = HybridVectorRetrievalEngine(repo_root=self.repo_root)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_embedder_normalization(self):
        embedder = DeterministicCodeEmbedder(dimension=64)
        v1 = embedder.embed_text("AuthenticationGatekeeper verify_token OIDC")
        self.assertEqual(len(v1), 64)
        # Magnitude should be ~1.0
        norm = sum(x * x for x in v1) ** 0.5
        self.assertAlmostEqual(norm, 1.0, places=4)

    def test_indexing_and_hybrid_search(self):
        idx_res = self.engine.index_codebase()
        self.assertEqual(idx_res["status"], "INDEXED")
        self.assertGreaterEqual(idx_res["indexed_chunks"], 2)

        # Search for authentication
        results = self.engine.search("enterprise OIDC authentication token", top_k=2)
        self.assertGreaterEqual(len(results), 1)
        top = results[0]
        self.assertIn("auth_gate.py", top.chunk.file_path)
        self.assertGreater(top.combined_score, 0.0)

        # Search for finops savings
        f_results = self.engine.search("finops savings revenue share fee", top_k=2)
        self.assertGreaterEqual(len(f_results), 1)
        f_top = f_results[0]
        self.assertTrue(
            "calculate_finops_savings" in f_top.chunk.symbol_name or
            "auth_gate.py" in f_top.chunk.file_path
        )

        # Verify prompt context envelope formatting
        ctx = self.engine.format_prompt_context(results, use_ast_skeletons=True)
        self.assertIn("### 🔍 Retrieved Codebase Context", ctx)
        self.assertIn("auth_gate.py", ctx)

    def test_persistence_and_reload(self):
        self.engine.index_codebase()
        meta_file = Path(self.temp_dir) / ".nb" / "context" / "vector_index" / "vector_index_meta.json"
        self.assertTrue(meta_file.exists())

        # Create new engine instance loading from disk
        engine2 = HybridVectorRetrievalEngine(repo_root=self.repo_root)
        self.assertGreater(len(engine2.chunks), 0)


class TestConventionalRepositoryMigrator(unittest.TestCase):
    """Unit tests for Conventional-to-Quad-Space Migrator (TODO-REV-18)."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.repo_root = Path(self.temp_dir)

        # Setup conventional python project
        src_dir = self.repo_root / "src" / "myapp"
        src_dir.mkdir(parents=True)
        (src_dir / "app.py").write_text("def run(): print('hello')", encoding="utf-8")

        test_dir = self.repo_root / "tests"
        test_dir.mkdir(parents=True)
        (test_dir / "test_app.py").write_text("def test_run(): assert True", encoding="utf-8")

        doc_dir = self.repo_root / "docs"
        doc_dir.mkdir(parents=True)
        (doc_dir / "spec.md").write_text("# Requirements Spec", encoding="utf-8")

        (self.repo_root / "pyproject.toml").write_text("[project]\nname = 'myapp'", encoding="utf-8")

        self.migrator = ConventionalRepositoryMigrator(repo_root=self.repo_root)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_analysis_report(self):
        rep = self.migrator.analyze_repository()
        self.assertEqual(rep.detected_project_type, "python_package")
        self.assertGreaterEqual(rep.total_files, 4)
        self.assertIn("workplace", rep.partition_counts)
        self.assertIn("user", rep.partition_counts)

    def test_migration_execution_and_rollback(self):
        rep = self.migrator.analyze_repository()
        res = self.migrator.execute_migration(report=rep, dry_run=False)
        self.assertEqual(res["status"], "MIGRATION_COMPLETED")
        self.assertGreaterEqual(res["files_migrated"], 3)

        # Verify Quad-Space directories created
        self.assertTrue((self.repo_root / "workplace").exists())
        self.assertTrue((self.repo_root / "user").exists())
        self.assertTrue((self.repo_root / ".nb").exists())

        # Verify genesis ledger
        ledger_path = self.repo_root / ".nb" / "context" / "ledger" / "context_ledger.yaml"
        self.assertTrue(ledger_path.exists())

        # Test rollback
        rb_res = self.migrator.rollback_migration()
        self.assertEqual(rb_res["status"], "ROLLBACK_SUCCESSFUL")
        self.assertGreaterEqual(rb_res["files_reverted"], 1)


class TestInteractiveOnboardingWizard(unittest.TestCase):
    """Unit tests for Interactive Onboarding Wizard (TODO-REV-19)."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.repo_root = Path(self.temp_dir)
        self.wizard = InteractiveOnboardingWizard(repo_root=self.repo_root)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_programmatic_onboarding(self):
        res = self.wizard.run_interactive(answers={
            "project_name": "fintech-microservice",
            "project_type": "microservice",
            "primary_language": "python",
            "tier": "enterprise",
            "selected_mcp_servers": ["filesystem", "git", "tradingview"],
            "install_git_hooks": True,
            "enable_token_metering": True
        })

        self.assertEqual(res.status, "INITIALIZED")
        self.assertEqual(res.config.tier, "enterprise")
        self.assertEqual(len(res.mcp_servers_configured), 3)

        # Verify provisioned assets
        self.assertTrue((self.repo_root / "mcp.json").exists())
        mcp_data = json.loads((self.repo_root / "mcp.json").read_text(encoding="utf-8"))
        self.assertIn("tradingview", mcp_data["mcpServers"])
        self.assertIn("filesystem", mcp_data["mcpServers"])

        self.assertTrue((self.repo_root / ".nb" / "context" / "ledger" / "context_ledger.yaml").exists())
        self.assertTrue((self.repo_root / "user" / "specs" / "mvs_initial_feature.yaml").exists())
        self.assertTrue((self.repo_root / ".nb" / "config" / "percipience_config.yaml").exists())
        self.assertTrue((self.repo_root / ".nb" / "hooks" / "pre-commit").exists())


if __name__ == "__main__":
    unittest.main()
