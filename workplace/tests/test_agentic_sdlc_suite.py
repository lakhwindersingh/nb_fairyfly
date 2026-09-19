"""
Unit and Integration Test Suite for Percipience Autonomous Agentic SDLC Modules (Section 17.2)
Tests:
- TODO-AGT-06: Quad-Space boundary cleanup & declarative facades in agentic/runtime/
- TODO-AGT-07: Parallel Fan-Out / Fan-In Barrier Synchronization in WorkflowOrchestrator
- TODO-AGT-08: Fine-Grained Error Taxonomy & Adaptive Recovery Playbooks
- TODO-AGT-09: Prompt SemVer, Manifest Integrity & PromptDriftSentinel Golden Suite
- TODO-AGT-10: Hierarchical Swarm Governance & Authority Trees
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "workplace") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "workplace"))
if str(REPO_ROOT / ".nb") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / ".nb"))

import pytest
import time

# Core Engines
from core.workflow_orchestrator import WorkflowOrchestrator
from core.error_recovery_orchestrator import (
    ErrorRecoveryOrchestrator,
    ErrorCategory,
    ErrorDiagnostic
)
from core.prompt_drift_sentinel import PromptDriftSentinel
from core.swarm_governor import SwarmGovernor, AuthorityLevel

# Agentic Runtime Facades
import agentic.runtime.cognitive_router as agt_cog_router
import agentic.runtime.concurrency.worktree_manager as agt_wt_mgr
import agentic.runtime.concurrency.atomic_gate_merger as agt_gate_merger
import agentic.runtime.finops.token_budget_enforcer as agt_finops_budget
import agentic.runtime.finops.token_savings_meter as agt_finops_meter
import agentic.runtime.packaging.envelope_hydrator as agt_env_hydrator
import agentic.runtime.packaging.plan_pack_compiler as agt_pack_compiler
import agentic.runtime.recovery.ledger_chain_verifier as agt_ledger_verif
import agentic.runtime.recovery.surgical_rollback_manager as agt_rollback_mgr


class TestAgenticRuntimeFacades:
    """Verifies that agentic/runtime/ exports proper facades to workplace/core/."""

    def test_cognitive_router_facade(self):
        assert hasattr(agt_cog_router, "CognitiveRouter")
        res = agt_cog_router.CognitiveRouter.dispatch("ast_parsing")
        assert res["assigned_tier"] == "Tier_B"

    def test_concurrency_facades(self):
        assert hasattr(agt_wt_mgr, "WorktreeEngine")
        assert hasattr(agt_wt_mgr, "is_pid_alive")
        assert hasattr(agt_gate_merger, "WorktreeEngine")
        assert hasattr(agt_gate_merger, "AutonomousCICDOrchestrator")

    def test_finops_facades(self):
        assert hasattr(agt_finops_budget, "TokenTracker")
        assert hasattr(agt_finops_meter, "TokenTracker")
        assert hasattr(agt_finops_meter, "UnifiedTokenOptimizer")

    def test_packaging_facades(self):
        assert hasattr(agt_env_hydrator, "NBPackEnvelope")
        assert hasattr(agt_pack_compiler, "NBPackEnvelope")

    def test_recovery_facades(self):
        assert hasattr(agt_ledger_verif, "MerkleEngine")
        assert hasattr(agt_rollback_mgr, "AutonomousHealer")


class TestWorkflowOrchestrator:
    """Verifies parallel fan-out and fan-in barrier synchronization in workflow DAGs."""

    def test_parallel_fan_out_execution(self):
        # Construct workflow with 3 parallel steps and 1 dependent barrier step
        workflow_def = {
            "workflow_id": "wf_test_parallel",
            "steps": [
                {
                    "id": "step_ast_prune",
                    "name": "AST Symbol Pruning",
                    "parallel_group": "group_parallel_scanners",
                    "executor": "mock_ast_prune"
                },
                {
                    "id": "step_cve_scan",
                    "name": "CVE Supply-Chain Scan",
                    "parallel_group": "group_parallel_scanners",
                    "executor": "mock_cve_scan"
                },
                {
                    "id": "step_lint",
                    "name": "Style Linting",
                    "parallel_group": "group_parallel_scanners",
                    "executor": "mock_lint"
                },
                {
                    "id": "step_barrier_join",
                    "name": "PR Merge Verification",
                    "depends_on": ["step_ast_prune", "step_cve_scan", "step_lint"],
                    "executor": "mock_barrier_join"
                }
            ]
        }

        call_log = []

        def mock_executor(step, context):
            sid = step["id"]
            call_log.append(sid)
            time.sleep(0.01)  # small work simulation
            return {"status": "SUCCESS", "message": f"{sid} done"}

        executors = {
            "mock_ast_prune": mock_executor,
            "mock_cve_scan": mock_executor,
            "mock_lint": mock_executor,
            "mock_barrier_join": mock_executor
        }

        res = WorkflowOrchestrator.execute_workflow(workflow_def, executors, max_workers=3)
        assert res["status"] == "COMPLETED"
        assert res["step_count"] == 4
        assert set(call_log[:3]) == {"step_ast_prune", "step_cve_scan", "step_lint"}
        assert call_log[3] == "step_barrier_join"

    def test_deadlock_detection(self):
        # Circular dependency
        circular_def = {
            "workflow_id": "wf_deadlock",
            "steps": [
                {"id": "step_a", "depends_on": ["step_b"]},
                {"id": "step_b", "depends_on": ["step_a"]}
            ]
        }
        res = WorkflowOrchestrator.execute_workflow(circular_def)
        assert res["status"] == "DEADLOCK_OR_UNRESOLVED_DEPENDENCY"
        assert set(res["unresolved_steps"]) == {"step_a", "step_b"}


class TestErrorRecoveryOrchestrator:
    """Verifies error classification into four pillars and playbook execution."""

    def test_transient_error_classification_and_backoff(self):
        diag = ErrorRecoveryOrchestrator.classify_error("HTTP 429: OpenAI Rate limit reached. Try again later.")
        assert diag.category == ErrorCategory.TRANSIENT
        
        playbook = ErrorRecoveryOrchestrator.execute_recovery_playbook(diag, retry_count=1, max_retries=3)
        assert playbook["action_taken"] == "EXPONENTIAL_BACKOFF_RETRY"
        assert playbook["status"] == "RETRY_SCHEDULED"
        assert playbook["next_retry"] == 2

    def test_structural_error_classification_and_ast_repair(self):
        diag = ErrorRecoveryOrchestrator.classify_error("SyntaxError: unexpected token ':' at line 42", stack_trace="ast_parse_error")
        assert diag.category == ErrorCategory.STRUCTURAL

        playbook = ErrorRecoveryOrchestrator.execute_recovery_playbook(diag)
        assert playbook["action_taken"] == "SYNTHESIZE_AST_DIAGNOSTIC_REPROMPT"
        assert playbook["status"] == "HEALING_DISPATCHED"

    def test_invariant_contract_error_classification(self):
        diag = ErrorRecoveryOrchestrator.classify_error("Breaking change detected: wire contract incompatible with v1.0.0")
        assert diag.category == ErrorCategory.INVARIANT

        playbook = ErrorRecoveryOrchestrator.execute_recovery_playbook(diag)
        assert playbook["action_taken"] == "TRIGGER_DUAL_RECONCILIATION_EVOLVE"
        assert playbook["status"] == "SPEC_DELTA_GENERATED"

    def test_hallucinatory_error_classification_and_quarantine(self):
        diag = ErrorRecoveryOrchestrator.classify_error("Poisoning detected: secret leaked sk-ant-api03-1234567890abcdef")
        assert diag.category == ErrorCategory.HALLUCINATORY

        playbook = ErrorRecoveryOrchestrator.execute_recovery_playbook(diag, module_id="mod_tenant_billing")
        assert playbook["action_taken"] == "ISOLATE_QUARANTINE_AND_SURGICAL_ROLLBACK"
        assert playbook["status"] == "QUARANTINED_AND_ROLLED_BACK"


class TestPromptDriftSentinel:
    """Verifies prompt manifest verification and golden evaluation suite."""

    def test_prompt_manifest_audit(self):
        audit_res = PromptDriftSentinel.audit_prompt_integrity()
        assert audit_res["status"] == "PASSED"
        assert audit_res["total_prompts"] >= 6
        assert audit_res["verified_count"] == audit_res["total_prompts"]
        assert audit_res["integrity_pure"] is True

    def test_golden_eval_suite(self):
        eval_res = PromptDriftSentinel.run_golden_eval_suite()
        assert eval_res["eval_suite_status"] == "PASSED"
        assert eval_res["results"]["system_prompt"]["passed"] is True
        assert eval_res["results"]["derivation_prompt"]["passed"] is True


class TestSwarmGovernor:
    """Verifies authority level hierarchy, action permissions, and anti-usurpation spawning defense."""

    def test_authority_tiers(self):
        orch = SwarmGovernor.get_agent_authority("lead_architect")
        assert orch["authority_level"] == AuthorityLevel.ORCHESTRATOR
        assert orch["can_merge_pr"] is True

        worker = SwarmGovernor.get_agent_authority("agent_tester")
        assert worker["authority_level"] == AuthorityLevel.SPECIALIST_WORKER
        assert worker["can_merge_pr"] is False
        assert worker["can_edit_code"] is True

        sentinel = SwarmGovernor.get_agent_authority("security_auditor")
        assert sentinel["authority_level"] == AuthorityLevel.GATEKEEPER_SENTINEL
        assert sentinel["can_veto"] is True

    def test_action_authorization(self):
        # Specialist worker cannot seal genesis or merge PR
        auth_seal = SwarmGovernor.authorize_action("agent_tester", "SEAL_MERKLE_GENESIS")
        assert auth_seal["authorized"] is False

        # Lead architect can merge PR
        auth_merge = SwarmGovernor.authorize_action("lead_architect", "MERGE_PR_GATE")
        assert auth_merge["authorized"] is True

        # Gatekeeper sentinel cannot author code
        auth_edit = SwarmGovernor.authorize_action("security_auditor", "EDIT_MODULE_CODE")
        assert auth_edit["authorized"] is False
        assert auth_edit["status"] == "DENIED_ROLE_CONFLICT"

    def test_anti_usurpation_spawn_defense(self):
        # Specialist worker cannot spawn an Orchestrator
        spawn_usurp = SwarmGovernor.intercept_spawn(parent_id="agent_tester", child_id="lead_architect")
        assert spawn_usurp["allowed"] is False
        assert spawn_usurp["status"] == "ROLE_USURPATION_BLOCKED"

        # Orchestrator can spawn a Specialist worker
        spawn_valid = SwarmGovernor.intercept_spawn(parent_id="lead_architect", child_id="agent_tester")
        assert spawn_valid["allowed"] is True
        assert spawn_valid["status"] == "SPAWN_PERMITTED"

        # Exceeding swarm depth
        spawn_deep = SwarmGovernor.intercept_spawn(parent_id="lead_architect", child_id="agent_tester", current_depth=2)
        assert spawn_deep["allowed"] is False
        assert spawn_deep["status"] == "RECURSION_DEPTH_EXCEEDED"
