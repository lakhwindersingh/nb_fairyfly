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
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
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
from core.cognitive_router import CognitiveRouter
from core.flaky_test_detector import FlakyTestDetector
from core.contract_compatibility_checker import ContractCompatibilityChecker
from core.dependency_cve_sentinel import DependencyCVESentinel
from core.doc_drift_synchronizer import DocDriftSynchronizer

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
        chain_ok, logs = MerkleEngine.verify_chain(REPO_ROOT)
        self.assertTrue(chain_ok, f"Merkle chain check failed: {logs}")

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



    def test_13_layerable_nbpack_compilation_and_enclave_consumption(self):
        """Test compilation of layerable domain plan into sealed .nbpack and zero-disk RAM enclave consumption."""
        saas_plan = REPO_ROOT / ".nb" / "plan" / "claude-context-engineering-saas-portal-domain-plan.md"
        self.assertTrue(saas_plan.exists(), "SaaS Portal domain plan must exist")

        out_pack = REPO_ROOT / ".workspaces" / "test_saas_layer.nbpack"
        
        # 1. Compile layerable plan into sealed binary envelope
        compiled_pack = NBPackEnvelope.compile_layer_pack(REPO_ROOT, saas_plan, out_pack)
        self.assertTrue(compiled_pack.exists())
        self.assertGreater(compiled_pack.stat().st_size, 500)

        # 2. Verify binary header seal
        with open(compiled_pack, "rb") as bf:
            header = bf.read(len(NBPackEnvelope.MAGIC_HEADER))
            self.assertEqual(header, NBPackEnvelope.MAGIC_HEADER)

        # 3. Apply encrypted layer strictly in RAM enclave
        res = NBPackEnvelope.apply_layer_pack(REPO_ROOT, compiled_pack, in_memory=True)
        self.assertEqual(res["status"], "APPLIED")
        self.assertEqual(res["storage_mode"], "RAM_ENCLAVE")
        self.assertGreaterEqual(res["components_loaded"], 3)
        self.assertIsNotNone(res["merkle_block_id"])
        self.assertIsNotNone(res["merkle_block_hash"])

        # 4. Verify in-memory residency and zero disk leaks
        mounted = NBPackEnvelope.list_mounted_layers()
        self.assertIn(res["layer_id"], mounted)
        self.assertGreater(mounted[res["layer_id"]], 0)

        # 5. Verify Merkle chain cryptographic continuity
        chain_ok, logs = MerkleEngine.verify_chain(REPO_ROOT)
        self.assertTrue(chain_ok, f"Merkle verification failed: {logs}")


    def test_14_atomic_ledger_and_pid_probing(self):
        """Test Phase 1 Reliability: Atomic temporary file replacement & active PID-probing lease eviction."""
        test_file = REPO_ROOT / ".workspaces" / "test_atomic.json"
        data = {"key": "value", "integrity": "verified"}
        checksum = MerkleEngine.atomic_write_data(test_file, data)
        self.assertTrue(test_file.exists())
        self.assertGreater(len(checksum), 32)
        
        # Test active PID probing in WorktreeEngine
        lease = WorktreeEngine.acquire(REPO_ROOT, "agent_test_pid_probe", ttl_seconds=60)
        self.assertEqual(lease["pid"], os.getpid())
        leases = WorktreeEngine.list_leases(REPO_ROOT)
        matching = [l for l in leases if l["agent_id"] == "agent_test_pid_probe"]
        self.assertTrue(len(matching) > 0)
        self.assertTrue(matching[0]["pid_alive"])
        
        # Simulate dead PID eviction
        lease_file = WorktreeEngine._lease_file(REPO_ROOT)
        with open(lease_file, "r") as lf:
            all_l = json.load(lf)
        all_l["agent_test_dead_proc"] = {
            "agent_id": "agent_test_dead_proc",
            "branch": "wt_branch_test_dead",
            "path": str(REPO_ROOT / ".workspaces" / "wt_dead"),
            "pid": 99999999,  # Non-existent dead PID
            "acquired_at": int(time.time()),
            "expires_at": int(time.time()) + 3600,
            "status": "ACTIVE"
        }
        with open(lease_file, "w") as lf:
            json.dump(all_l, lf, indent=2)

        evicted = WorktreeEngine.reclaim_stale_leases(REPO_ROOT)
        self.assertIn("agent_test_dead_proc", evicted)
        
        # Cleanup test lease
        WorktreeEngine.release(REPO_ROOT, "agent_test_pid_probe")

    def test_15_ast_caching_and_epoch_checkpointing(self):
        """Test Phase 2 Scalability: Content-addressable AST caching & rolling epoch checkpointing."""
        code = """export class FinOpsAuditor {
  private threshold: number = 5000;
  public audit(tokens: number): boolean {
    return tokens > this.threshold;
  }
}"""
        # 1. First AST pruning pass (Cache Miss)
        p1, s1 = ASTOptimizer.prune_source(code, "typescript", use_cache=True)
        self.assertFalse(s1["cache_hit"])
        
        # 2. Second AST pruning pass with identical code (Cache Hit, 0ms)
        p2, s2 = ASTOptimizer.prune_source(code, "typescript", use_cache=True)
        self.assertTrue(s2["cache_hit"])
        self.assertEqual(p1, p2)
        
        # 3. Epoch checkpointing test
        ledger_path = REPO_ROOT / "context" / "ledger" / "context_ledger.yaml"
        self.assertTrue(ledger_path.exists())
        # Retain active window of 100 blocks, archive older
        res = MerkleEngine.checkpoint_epoch(REPO_ROOT, retain_active_blocks=100)
        self.assertIn(res["status"], ["CHECKPOINTED", "SKIPPED"])
        
        # Verify chain continuity across archive + active blocks
        chain_ok, logs = MerkleEngine.verify_chain(REPO_ROOT)
        self.assertTrue(chain_ok, f"Merkle chain break: {logs}")

    def test_16_cognitive_tier_routing_and_wire_contracts(self):
        """Test Phase 2 Model Dispatcher & Phase 1 Wire Contract Runtime Gate."""
        # 1. Cognitive Tier Routing
        d1 = CognitiveRouter.dispatch("ast_parsing", requested_model="claude-3-7-sonnet")
        self.assertEqual(d1["assigned_tier"], "Tier_B")
        self.assertTrue(d1["downgraded_from_tier_a"])
        self.assertEqual(d1["cost_discount_pct"], 90.0)

        d2 = CognitiveRouter.dispatch("wire_contract_compat")
        self.assertEqual(d2["assigned_tier"], "Tier_A")
        self.assertFalse(d2["downgraded_from_tier_a"])
        
        # 2. Wire Contract Schema Validation
        contract_res = LayeredContextValidator.validate_wire_contracts(REPO_ROOT)
        self.assertTrue(contract_res["valid"])
        self.assertGreaterEqual(len(contract_res["contracts"]), 3)

        # 3. Runtime Event Payload Validation
        billing_schema = {
            "required": ["tenant_id", "event_type", "tokens_saved"],
            "properties": {
                "tenant_id": {"type": "string"},
                "event_type": {"type": "string"},
                "tokens_saved": {"type": "integer"}
            }
        }
        valid_payload = {"tenant_id": "cust_123", "event_type": "pr_gate_verified", "tokens_saved": 450}
        ok, errs = LayeredContextValidator.validate_sample_payload(billing_schema, valid_payload)
        self.assertTrue(ok)
        self.assertEqual(len(errs), 0)

        invalid_payload = {"tenant_id": "cust_123", "tokens_saved": "not_an_int"}
        bad_ok, bad_errs = LayeredContextValidator.validate_sample_payload(billing_schema, invalid_payload)
        self.assertFalse(bad_ok)
        self.assertGreaterEqual(len(bad_errs), 1)

    def test_17_autonomous_cicd_specialist_plugins(self):
        """Test Phase 3 Specialist Plugins: Flaky Test, Contract Evolution, CVE Sentinel, Doc Drift."""
        # 1. Flaky Test Detection & Quarantine
        flaky_res = FlakyTestDetector.audit_test_stability(
            REPO_ROOT,
            test_id="test_mod_portal_async_worker",
            runs=3,
            simulated_failure_rate=0.33
        )
        self.assertTrue(flaky_res["is_flaky"])
        self.assertEqual(flaky_res["action"], "QUARANTINED")
        q_file = REPO_ROOT / "user" / "hitl" / "flaky_quarantine.yaml"
        self.assertTrue(q_file.exists())

        # 2. Wire Contract Compatibility Checker (SemVer)
        base_c = {
            "title": "V1",
            "required": ["id", "amount"],
            "properties": {"id": {"type": "string"}, "amount": {"type": "number"}}
        }
        # Compatible addition: new optional field
        head_compat = {
            "title": "V1.1",
            "required": ["id", "amount"],
            "properties": {"id": {"type": "string"}, "amount": {"type": "number"}, "currency": {"type": "string"}}
        }
        c_res1 = ContractCompatibilityChecker.check_compatibility(base_c, head_compat)
        self.assertTrue(c_res1["is_compatible"])

        # Breaking removal: required 'amount' removed
        head_breaking = {
            "title": "V2_BROKEN",
            "required": ["id"],
            "properties": {"id": {"type": "string"}}
        }
        c_res2 = ContractCompatibilityChecker.check_compatibility(base_c, head_breaking)
        self.assertFalse(c_res2["is_compatible"])
        self.assertIn("REMOVED_REQUIRED_FIELD", c_res2["breaking_changes"][0])

        # 3. Supply-Chain CVE Sentinel
        clean_code = "import os\nimport sys\n"
        dirty_code = "import os\nimport event-stream\n"
        vuln_res = DependencyCVESentinel.audit_source_imports(dirty_code)
        self.assertFalse(vuln_res["clean"])
        self.assertEqual(vuln_res["violations"][0]["package"], "event-stream")

        # 4. Doc Drift Synchronizer
        exports = ["calculateRisk", "executeTrade", "orphanedFunction"]
        docs = "# API Docs\nUse `calculateRisk` and `executeTrade` to manage assets."
        drift_res = DocDriftSynchronizer.audit_doc_coverage(exports, docs)
        self.assertEqual(drift_res["documented_count"], 2)
        self.assertIn("orphanedFunction", drift_res["missing_symbols"])
        self.assertEqual(drift_res["status"], "DRIFT_DETECTED")

if __name__ == "__main__":
    unittest.main(verbosity=2)
