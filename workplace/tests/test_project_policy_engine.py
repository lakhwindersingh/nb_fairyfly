"""
Unit and Integration Test Suite for Minute Project Control & Policy Configuration (CAP-41 / Section 18.2):
- TODO-PRT-04: Granular Context Engineering Tuning Sliders (Attention Slicing, Cognitive Routing, AST Pruning)
- TODO-PRT-05: PR Gate & Self-Healing SLA Policies (Diagnostic re-prompts 1-5, Flaky quarantine variance, Wire contract rules)
"""

import sys
import shutil
import tempfile
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "workplace") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "workplace"))

from core.project_policy_engine import (
    ProjectPolicyManager,
    ProjectPolicy,
    AttentionSlicingPolicy,
    CognitiveRoutingPolicy,
    ASTPruningPolicy,
    SelfHealingSLAPolicy,
    WireContractRule
)


@pytest.fixture
def temp_policy_mgr():
    temp_dir = Path(tempfile.mkdtemp(prefix="nb_policy_test_"))
    mgr = ProjectPolicyManager(policy_dir=temp_dir)
    yield mgr, temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


class TestProjectPolicyEngineSection18_2:

    def test_01_default_policy_creation_and_validation(self, temp_policy_mgr):
        mgr, _ = temp_policy_mgr
        policy = mgr.get_policy("tenant_fintech", "proj_quantum")

        # 1. Attention quotas baseline
        att = policy.attention
        assert att.persona_invariants_pct == 15.0
        assert att.contracts_schemas_pct == 25.0
        assert att.ast_codebase_pct == 35.0
        assert att.memory_trajectories_pct == 10.0
        assert att.reserved_output_pct == 15.0
        assert (att.persona_invariants_pct + att.contracts_schemas_pct + att.ast_codebase_pct + att.memory_trajectories_pct + att.reserved_output_pct) == 100.0

        # 2. Cognitive routing baseline
        rout = policy.routing
        assert rout.tier_a_threshold == 0.70
        assert "wire_contract_compat" in rout.custom_tier_a_tasks

        # 3. SLA baseline
        sla = policy.healing_sla
        assert sla.max_diagnostic_reprompts == 3
        assert sla.flaky_quarantine_variance_threshold == 0.15
        assert sla.wire_contract_breaking_rule == WireContractRule.STRICT_BLOCK

        # 4. Validation error checks
        with pytest.raises(ValueError, match="must sum to 100.0%"):
            bad_att = AttentionSlicingPolicy(persona_invariants_pct=50.0)
            bad_att.validate()

        with pytest.raises(ValueError, match="between 0.0 and 1.0"):
            bad_rout = CognitiveRoutingPolicy(tier_a_threshold=1.5)
            bad_rout.validate()

        with pytest.raises(ValueError, match="between 1 and 5 turns"):
            bad_sla = SelfHealingSLAPolicy(max_diagnostic_reprompts=7)
            bad_sla.validate()

    def test_02_policy_persistence_and_update(self, temp_policy_mgr):
        mgr, temp_dir = temp_policy_mgr
        t_id = "tenant_enterprise"
        p_id = "proj_algo_trading"

        # Update policy with customized slider values
        updated = mgr.update_policy(
            tenant_id=t_id,
            project_id=p_id,
            patch_data={
                "attention": {
                    "persona_invariants_pct": 20.0,
                    "contracts_schemas_pct": 20.0,
                    "ast_codebase_pct": 30.0,
                    "memory_trajectories_pct": 10.0,
                    "reserved_output_pct": 20.0
                },
                "routing": {
                    "tier_a_threshold": 0.85,
                    "custom_tier_a_tasks": ["custom_critical_audit"]
                },
                "healing_sla": {
                    "max_diagnostic_reprompts": 4,
                    "flaky_quarantine_variance_threshold": 0.20,
                    "wire_contract_breaking_rule": "ALLOW_ADDITIVE_WARN"
                }
            },
            user_id="lead_alice"
        )

        assert updated.version == 2
        assert updated.updated_by == "lead_alice"
        assert updated.attention.persona_invariants_pct == 20.0
        assert updated.routing.tier_a_threshold == 0.85
        assert updated.healing_sla.max_diagnostic_reprompts == 4
        assert updated.healing_sla.flaky_quarantine_variance_threshold == 0.20
        assert updated.healing_sla.wire_contract_breaking_rule == WireContractRule.ALLOW_ADDITIVE_WARN

        # Verify disk persistence file exists
        persisted_file = temp_dir / f"{t_id}_{p_id}.yaml"
        assert persisted_file.exists()

        # Create new manager pointing to same folder, verify roundtrip load
        mgr2 = ProjectPolicyManager(policy_dir=temp_dir)
        loaded = mgr2.get_policy(t_id, p_id)
        assert loaded.version == 2
        assert loaded.attention.persona_invariants_pct == 20.0
        assert loaded.healing_sla.wire_contract_breaking_rule == WireContractRule.ALLOW_ADDITIVE_WARN

    def test_03_attention_slicing_with_dynamic_quotas(self, temp_policy_mgr):
        mgr, _ = temp_policy_mgr
        t_id = "tenant_corp"
        p_id = "proj_finops"

        # Custom ratio: 10% persona, 30% contracts, 40% codebase, 10% memory, 10% reserved
        mgr.update_policy(
            tenant_id=t_id,
            project_id=p_id,
            patch_data={
                "attention": {
                    "persona_invariants_pct": 10.0,
                    "contracts_schemas_pct": 30.0,
                    "ast_codebase_pct": 40.0,
                    "memory_trajectories_pct": 10.0,
                    "reserved_output_pct": 10.0
                }
            }
        )

        sections = {
            "persona_invariants": "System Invariant: Do not breach SEC Rule 17a-4.",
            "contracts_schemas": "Contract: OrderPlacement(symbol: str, qty: int, price: float) " * 50,
            "ast_codebase": "def execute_order(sym, qty): pass\n" * 300,
            "memory_trajectories": "Turn 1: Success\nTurn 2: Success\n" * 50
        }

        res = mgr.slice_context_with_project_policy(
            tenant_id=t_id,
            project_id=p_id,
            sections=sections,
            max_total_tokens=1000
        )

        assert res["max_total_tokens"] == 1000
        assert res["reserved_output_tokens"] == 100  # 10% of 1000
        assert res["headroom_pct"] == 10.0
        # Persona invariant must NOT be sliced
        assert "System Invariant: Do not breach SEC Rule 17a-4." in res["sections"]["persona_invariants"]
        # Codebase should have been trimmed to fit 40% (400 tokens)
        assert "[SLICED_BY_PROJECT_POLICY]" in res["sections"]["ast_codebase"]

    def test_04_cognitive_routing_with_project_rules(self, temp_policy_mgr):
        mgr, _ = temp_policy_mgr
        t_id = "tenant_ai"
        p_id = "proj_nlp"

        # Project with high Tier A bar (0.90) and custom task routing
        mgr.update_policy(
            tenant_id=t_id,
            project_id=p_id,
            patch_data={
                "routing": {
                    "tier_a_threshold": 0.90,
                    "custom_tier_a_tasks": ["nlp_pipeline_design"],
                    "custom_tier_b_tasks": ["heavy_batch_indexing"]
                }
            }
        )

        # 1. Custom Tier A task
        res1 = mgr.route_cognitive_task_with_project_policy(t_id, p_id, "nlp_pipeline_design")
        assert res1["assigned_tier"] == "Tier_A"
        assert res1["cost_discount_pct"] == 0.0

        # 2. Custom Tier B task
        res2 = mgr.route_cognitive_task_with_project_policy(t_id, p_id, "heavy_batch_indexing")
        assert res2["assigned_tier"] == "Tier_B"
        assert res2["cost_discount_pct"] == 90.0

        # 3. Complexity score below project threshold (0.80 < 0.90) -> Tier B
        res3 = mgr.route_cognitive_task_with_project_policy(
            t_id, p_id, "complex_algorithm_analysis", complexity_score=0.80
        )
        assert res3["assigned_tier"] == "Tier_B"

        # 4. Complexity score above threshold (0.95 >= 0.90) -> Tier A
        res4 = mgr.route_cognitive_task_with_project_policy(
            t_id, p_id, "complex_algorithm_analysis", complexity_score=0.95
        )
        assert res4["assigned_tier"] == "Tier_A"

    def test_05_pr_gate_and_self_healing_sla(self, temp_policy_mgr):
        mgr, _ = temp_policy_mgr
        t_id = "tenant_sec"
        p_id = "proj_vault"

        # Setup SLA: 3 reprompts, 15% flaky variance threshold, STRICT_BLOCK
        mgr.update_policy(
            tenant_id=t_id,
            project_id=p_id,
            patch_data={
                "healing_sla": {
                    "max_diagnostic_reprompts": 3,
                    "flaky_quarantine_variance_threshold": 0.15,
                    "wire_contract_breaking_rule": "STRICT_BLOCK"
                }
            }
        )

        # Test history:
        # test_a: 1 failure out of 10 runs (10% fail rate <= 15% threshold -> Quarantined as flaky)
        # test_b: 0 failures out of 10 runs (Pass)
        # test_c: 4 failures out of 10 runs (40% fail rate > 15% threshold -> Deterministic failure)
        test_history_flaky_only = [
            {"test_id": "test_auth_latency", "runs": 10, "failures": 1},
            {"test_id": "test_order_matching", "runs": 10, "failures": 0}
        ]

        # Case 1: Only flaky test within variance threshold -> Should quarantine and PASS gate
        res1 = mgr.evaluate_pr_gate(
            tenant_id=t_id,
            project_id=p_id,
            test_run_history=test_history_flaky_only,
            current_heal_turn=0
        )
        assert res1["gate_decision"] == "PASS"
        assert res1["recommended_action"] == "PROCEED_MERGE"
        assert len(res1["test_audit"]["quarantined_flaky_tests"]) == 1
        assert res1["test_audit"]["quarantined_flaky_tests"][0]["test_id"] == "test_auth_latency"

        # Case 2: Deterministic test failure on turn 1 -> Retry diagnostic reprompt
        test_history_with_hard_failure = [
            {"test_id": "test_auth_latency", "runs": 10, "failures": 1},
            {"test_id": "test_crypto_keygen", "runs": 10, "failures": 4}
        ]
        res2 = mgr.evaluate_pr_gate(
            tenant_id=t_id,
            project_id=p_id,
            test_run_history=test_history_with_hard_failure,
            current_heal_turn=1
        )
        assert res2["gate_decision"] == "FAIL"
        assert res2["recommended_action"] == "DIAGNOSTIC_REPROMPT_TURN_2"
        assert res2["healing_sla"]["can_retry"] is True

        # Case 3: Breaching max diagnostic reprompts (turn 3 of 3) -> Trigger automated rollback
        res3 = mgr.evaluate_pr_gate(
            tenant_id=t_id,
            project_id=p_id,
            test_run_history=test_history_with_hard_failure,
            current_heal_turn=3
        )
        assert res3["gate_decision"] == "FAIL"
        assert res3["recommended_action"] == "TRIGGER_AUTOMATED_ROLLBACK"
        assert res3["healing_sla"]["can_retry"] is False

        # Case 4: Wire contract breaking change with STRICT_BLOCK vs ALLOW_ADDITIVE_WARN
        base_contract = {
            "title": "TradingAPI",
            "properties": {"order_id": {"type": "string"}, "price": {"type": "number"}},
            "required": ["order_id", "price"]
        }
        broken_contract = {
            "title": "TradingAPI",
            "properties": {"order_id": {"type": "string"}},  # 'price' deleted
            "required": ["order_id"]
        }

        res4_blocked = mgr.evaluate_pr_gate(
            tenant_id=t_id,
            project_id=p_id,
            test_run_history=test_history_flaky_only,
            base_contract=base_contract,
            head_contract=broken_contract,
            current_heal_turn=0
        )
        assert res4_blocked["gate_decision"] == "FAIL"
        assert res4_blocked["contract_audit"]["status"] == "BLOCKED"
        assert len(res4_blocked["contract_audit"]["violations"]) > 0

        # Now change policy to ALLOW_ADDITIVE_WARN
        mgr.update_policy(
            tenant_id=t_id,
            project_id=p_id,
            patch_data={"healing_sla": {"wire_contract_breaking_rule": "ALLOW_ADDITIVE_WARN"}}
        )
        res4_warned = mgr.evaluate_pr_gate(
            tenant_id=t_id,
            project_id=p_id,
            test_run_history=test_history_flaky_only,
            base_contract=base_contract,
            head_contract=broken_contract,
            current_heal_turn=0
        )
        assert res4_warned["contract_audit"]["status"] == "WARNING_ALLOWED"
        assert res4_warned["gate_decision"] == "PASS"
