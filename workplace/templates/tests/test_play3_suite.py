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
from core.token_tracker import TokenTracker
from core.agent_plugin_engine import AgentPluginEngine
from core.autonomous_cicd import (
    SelfSustainingEngine,
    AutonomousHealer,
    SelfImprovingEngine,
    AutonomousCICDOrchestrator
)

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

    def test_10_token_tracker(self):
        """Test token savings capture, 15% rev-share metering, and report generation."""
        evt = TokenTracker.record_event(
            repo_root=REPO_ROOT,
            file_path="workplace/core/test_sample.py",
            uncompressed_tokens=1000,
            pruned_tokens=400,
            session_or_pr="test_suite_run"
        )
        self.assertEqual(evt["tokens_saved"], 600)
        self.assertEqual(evt["reduction_percentage"], 60.0)
        self.assertAlmostEqual(evt["gross_savings_usd"], 0.0018, places=4)
        self.assertAlmostEqual(evt["rev_share_fee_usd"], 0.00027, places=5)
        self.assertAlmostEqual(evt["net_savings_usd"], 0.00153, places=5)

        # Verify report generation
        md = TokenTracker.generate_markdown_report(REPO_ROOT)
        self.assertIn("Percipience Context Token Savings & Rev-Share Metering Report", md)
        self.assertIn("15.0%", md)


    def test_11_autonomous_cicd_self_healing_and_sustain(self):
        """Test Autonomous CI/CD Triad: Self-Sustaining, Self-Recovering, Self-Improving."""
        # 1. Self-Sustaining pass
        sustain_res = SelfSustainingEngine.execute_maintenance(REPO_ROOT)
        self.assertEqual(sustain_res["status"], "SUSTAINED")
        self.assertTrue(sustain_res["merkle_continuous"])

        # 2. Autonomous Healer diagnostic routine
        heal_res = AutonomousHealer.diagnose_and_heal(REPO_ROOT, target_module="mod_portal_marketing")
        self.assertTrue(heal_res["healed"])
        self.assertLessEqual(heal_res["attempts"], 3)
        self.assertIn(heal_res["action_taken"], ["AUTO_PATCH_VERIFIED_AND_SEALED", "SURGICAL_MODULE_ROLLBACK_EXECUTED"])

        # 3. Self-Improving feedback optimization
        improve_res = SelfImprovingEngine.analyze_and_optimize(REPO_ROOT)
        self.assertIn("current_avg_reduction_pct", improve_res)
        self.assertTrue((REPO_ROOT / "context" / "ledger" / "self_improving_ledger.yaml").exists())

        # 4. End-to-end Autonomous CI/CD Orchestrator pipeline
        pipeline_res = AutonomousCICDOrchestrator.run_autonomous_pipeline(REPO_ROOT, auto_heal=True, optimize=True)
        self.assertEqual(pipeline_res["status"], "SUCCESS")
        self.assertIn("run_id", pipeline_res)
        self.assertIn("merkle_seal", pipeline_res["stages"])

    def test_12_agent_plugin_lifecycle_and_workflow_integration(self):
        """Test Custom Agent Plugin registration, workflow integration, worktree execution, Merkle seal, and surgical rollback."""
        # 1. Scaffold and register agent from template
        agent_name = "test_perf_guard"
        reg_res = AgentPluginEngine.create_agent(
            workspace_root=REPO_ROOT,
            name=agent_name,
            template_type="cicd_quality",
            role="Performance & Latency Guard",
            model="claude-3-5-sonnet-20241022",
            allowed_modules=["workplace/core", "workplace/modules/mod_portal_marketing"],
            target_workflow="wf_pr_gatekeeper"
        )
        self.assertEqual(reg_res["status"], "REGISTERED")
        self.assertEqual(reg_res["agent_id"], "agent_test_perf_guard")
        self.assertTrue((REPO_ROOT / reg_res["manifest_path"]).exists())
        self.assertIsNotNone(reg_res["merkle_block"])
        self.assertIsNotNone(reg_res["recovery_point"])

        # 2. Integrate into workflow DAG
        integ_res = AgentPluginEngine.integrate_into_workflow(
            workspace_root=REPO_ROOT,
            agent_id="agent_test_perf_guard",
            workflow_id="wf_pr_gatekeeper",
            after_step_id="step_contract_compat"
        )
        self.assertEqual(integ_res["status"], "INTEGRATED")
        self.assertEqual(integ_res["step_id"], "step_test_perf_guard")
        self.assertIsNotNone(integ_res["merkle_block_id"])

        # 3. List agents and verify discovery & workflow binding
        agents = AgentPluginEngine.list_agents(REPO_ROOT)
        matched = [a for a in agents if a["agent_id"] == "agent_test_perf_guard"]
        self.assertTrue(len(matched) > 0)
        self.assertEqual(matched[0]["category"], "cicd_quality")
        self.assertTrue(any(w["workflow_id"] == "wf_pr_gatekeeper" for w in matched[0]["workflow_bindings"]))

        # 4. Execute task in sandboxed worktree with Merkle seal
        exec_res = AgentPluginEngine.execute_agent_task(
            workspace_root=REPO_ROOT,
            agent_id="agent_test_perf_guard",
            task_description="Verify AST complexity in mod_portal_marketing",
            target_module="mod_portal_marketing",
            auto_rollback_on_failure=True
        )
        self.assertEqual(exec_res["status"], "SUCCESS")
        self.assertIsNotNone(exec_res["merkle_block_id"])
        self.assertIsNotNone(exec_res["recovery_point_id"])

        # 5. Surgical Rollback capability
        rb_res = AgentPluginEngine.rollback_agent(
            workspace_root=REPO_ROOT,
            agent_id="agent_test_perf_guard",
            target_module="mod_portal_marketing",
            target_point="RP_PLAY3_BOOTSTRAP_001"
        )
        self.assertEqual(rb_res["status"], "ROLLED_BACK")
        self.assertIsNotNone(rb_res["merkle_block_id"])

        # 6. Verify Merkle chain continuity holds
        chain_verified = MerkleEngine.verify_chain(REPO_ROOT)
        self.assertTrue(chain_verified)

        # 7. Cleanup test artifacts
        test_file = REPO_ROOT / reg_res["manifest_path"]
        if test_file.exists():
            test_file.unlink()
        wf_file = REPO_ROOT / "agentic" / "workflows" / "pr_gatekeeper.yaml"
        if wf_file.exists():
            import yaml
            with open(wf_file, "r", encoding="utf-8") as f:
                d = yaml.safe_load(f)
            d["steps"] = [s for s in d.get("steps", []) if s.get("id") != "step_test_perf_guard"]
            with open(wf_file, "w", encoding="utf-8") as f:
                yaml.dump(d, f, sort_keys=False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
