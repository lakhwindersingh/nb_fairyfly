#!/usr/bin/env python3
"""
Comprehensive Automated Test Suite for Percipience Play 3:
- Enterprise Context Engineering OS (play_3_enterprise_context_engineering_os_plan.md)
- Cloud SaaS Portal & Corporate Platform (play_3_corp_site_saas_portal_plan.md)
"""

import os
import sys
import unittest
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "workplace"))

from core.ast_optimizer import ASTOptimizer
from core.merkle_engine import MerkleEngine
from core.poisoning_sentinel import PoisoningSentinel
from core.maturity_evaluator import MaturityEvaluator
from core.nbpack_envelope import NBPackEnvelope
from core.worktree_engine import WorktreeEngine
from core.byor_adapter import BYORAdapter
from core.layered_context_validator import LayeredContextValidator

class TestPlay3Subsystems(unittest.TestCase):

    def test_01_ast_optimizer(self):
        """Test structural AST pruning and token reduction metrics."""
        ts_code = """export function calculateRisk(portfolio: any): number {
  const alpha = 0.05;
  const beta = 1.12;
  return alpha * beta;
}"""
        pruned, stats = ASTOptimizer.prune_source(ts_code, "typescript")
        self.assertIn("calculateRisk", pruned)
        self.assertIn("...", pruned)
        self.assertGreater(stats["reduction_percentage"], 0.0)

    def test_02_merkle_engine(self):
        """Test cryptographic Merkle hash calculation and ledger continuity."""
        chain_ok, logs = MerkleEngine.verify_chain(REPO_ROOT)
        self.assertTrue(chain_ok, f"Merkle chain failed verification: {logs}")
        self.assertGreaterEqual(len(logs), 2)

    def test_03_poisoning_sentinel(self):
        """Test detection of hardcoded secrets and malicious dependencies."""
        bad_code = 'const apiKey = "api_key_12345678901234567890";'
        violations = PoisoningSentinel.scan_content_for_poisoning(bad_code, "test_file.ts")
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0]["type"], "SECRET_LEAK")

    def test_04_surgical_rollback(self):
        """Test surgical rollback execution isolating single module."""
        ok = PoisoningSentinel.execute_surgical_rollback(REPO_ROOT, "mod_observability_usage", "RP_PLAY3_BOOTSTRAP_001")
        self.assertTrue(ok)

    def test_05_maturity_evaluator(self):
        """Test 6-dimensional context maturity score calculation."""
        scores = MaturityEvaluator.evaluate_workspace(REPO_ROOT)
        self.assertGreaterEqual(scores["composite_score"], 0.88)
        self.assertEqual(scores["status"], "ENTERPRISE GRADE")

    def test_06_nbpack_packaging_and_hydration(self):
        """Test .nbpack compilation, signature seal, and zero-disk in-memory hydration."""
        out_pack = REPO_ROOT / ".workspaces" / "test_bundle.nbpack"
        compiled_file = NBPackEnvelope.compile_package(REPO_ROOT, out_pack, include_spaces=["context/contracts"])
        self.assertTrue(compiled_file.exists())
        
        # Hydrate strictly in memory
        payload = NBPackEnvelope.hydrate_in_memory(compiled_file)
        self.assertIsInstance(payload, dict)
        self.assertGreater(len(payload), 0)

    def test_07_worktree_engine(self):
        """Test subagent worktree lease acquire, list, and release."""
        agent_id = "test_subagent_suite_01"
        lease = WorktreeEngine.acquire(REPO_ROOT, agent_id, ttl_seconds=300)
        self.assertEqual(lease["agent_id"], agent_id)
        
        leases = WorktreeEngine.list_leases(REPO_ROOT)
        agent_ids = [l["agent_id"] for l in leases]
        self.assertIn(agent_id, agent_ids)

        released = WorktreeEngine.release(REPO_ROOT, agent_id)
        self.assertTrue(released)

    def test_08_byor_adapter(self):
        """Test BYOR multi-VCS connection, webhook validation, and commit status."""
        conn = BYORAdapter.connect_repository(
            REPO_ROOT,
            remote_url="git@gitlab.internal.enterprise:core/ledger.git",
            webhook_provider="gitlab"
        )
        self.assertEqual(conn["status"], "CONNECTED")

        # Test commit status formatter
        status_payload = BYORAdapter.format_commit_status("gitlab", "abc1234", "PASS", "Audit passed", "https://percipience.corp")
        self.assertEqual(status_payload["state"], "success")

    def test_09_layered_context_validator(self):
        """Test 3-tier precedence hierarchy validation."""
        val_res = LayeredContextValidator.validate_layered_hierarchy(REPO_ROOT)
        self.assertTrue(val_res["overall_valid"])
        self.assertEqual(val_res["tier1_invariants"], "VALID")

if __name__ == "__main__":
    unittest.main(verbosity=2)
