"""
Unit and Integration Test Suite for Percipience Autonomous SDLC Section 17.3 Modules
Tests:
- TODO-AGT-11: Adversarial Red-Team & Mutation Fuzzing Engine (AdversarialFuzzer)
- TODO-AGT-12: Context Attention Slicing & Token Budgeting Engine (AttentionBudgeter)
- TODO-AGT-13: Static Prompt Prefix Pinning for KV Cache Optimization (PromptDriftSentinel)
- TODO-AGT-14: Structured Step-by-Step Trajectory Recording & Replay Engine (TrajectoryRecorder)
- TODO-AGT-15: Requirement Clarification & Ambiguity Resolution Engine (AmbiguityResolver)
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "workplace") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "workplace"))

import pytest
import json

from core.adversarial_fuzzer import AdversarialFuzzer
from core.attention_budgeter import AttentionBudgeter
from core.prompt_drift_sentinel import PromptDriftSentinel
from core.trajectory_recorder import TrajectoryRecorder
from core.ambiguity_resolver import AmbiguityResolver


class TestAdversarialFuzzer:
    """Verifies adversarial payload generation, schema mutation, and fuzz test resilience."""

    def test_payload_vector_generation(self):
        nums = AdversarialFuzzer.generate_fuzz_vectors("int", count=3)
        assert len(nums) == 3
        strs = AdversarialFuzzer.generate_fuzz_vectors("string", count=4)
        assert len(strs) == 4

    def test_schema_mutations(self):
        base_payload = {"user_id": 1234, "username": "alice", "active": True}
        mutations = AdversarialFuzzer.mutate_input_schema(base_payload)
        assert len(mutations) > 5

    def test_execute_fuzz_test_resilient(self):
        # Target function that validates inputs cleanly
        def safe_handler(payload):
            if not payload or "username" not in payload or payload["username"] is None:
                raise ValueError("Missing or null username")
            return f"Processed {payload['username']}"

        base_payload = {"user_id": 100, "username": "valid_user"}
        res = AdversarialFuzzer.execute_fuzz_test(safe_handler, base_payload)
        assert res["status"] == "RESILIENT"
        assert res["unhandled_panics_count"] == 0
        assert res["resilience_score"] == 1.0


class TestAttentionBudgeter:
    """Verifies declarative token quotas, invariant protection, and context slicing."""

    def test_token_estimation(self):
        text = "Hello world! This is a test."
        toks = AttentionBudgeter.estimate_tokens(text)
        assert toks > 0

    def test_context_slicing_and_budget_bounds(self):
        sections = {
            "persona_invariants": "System Invariant: Must follow Quad-Space.",
            "contracts_schemas": "openapi: 3.0.0\ninfo:\n  title: API Contract\n",
            "ast_codebase": "def huge_code_listing():\n" + ("    x = 1\n" * 500),
            "memory_trajectories": "Step 1: Analyzed issue.\n"
        }

        sliced = AttentionBudgeter.slice_context(sections, max_total_tokens=500)
        assert sliced["status"] == "SLICED_SUCCESSFULLY"
        assert sliced["total_used_tokens"] <= 500
        assert "System Invariant: Must follow Quad-Space." in sliced["assembled_prompt"]
        # Codebase should be bounded
        assert sliced["section_metrics"]["ast_codebase"]["trimmed_tokens"] > 0


class TestPromptPrefixPinning:
    """Verifies static prefix pinning for KV-cache optimization across all prompts."""

    def test_prefix_pinning_audit(self):
        audit = PromptDriftSentinel.audit_prefix_pinning_compliance()
        assert audit["status"] == "PASSED"
        assert audit["compliant_count"] == audit["total_prompts"]
        assert audit["non_compliant_count"] == 0


class TestTrajectoryRecorder:
    """Verifies structured ReAct trajectory logging, disk serialization, and replay."""

    def test_trajectory_lifecycle(self, tmp_path):
        traj = TrajectoryRecorder.create_trajectory(
            session_id="sess_test_101",
            agent_id="agent_living_doc_architect",
            goal="Synchronize architecture diagrams"
        )
        assert traj["status"] == "RECORDING"

        TrajectoryRecorder.append_step(
            trajectory=traj,
            thought="Inspect current docs in workplace/docs/",
            action="list_dir",
            action_input={"path": "workplace/docs"},
            observation={"files_count": 33},
            reflection="Docs directory populated."
        )

        saved_file = TrajectoryRecorder.save_trajectory(traj)
        assert saved_file.exists()

        # Replay trajectory
        replay_res = TrajectoryRecorder.replay_trajectory(traj["trajectory_id"])
        assert replay_res["replay_status"] == "REPLAY_VERIFIED"
        assert replay_res["is_deterministic"] is True
        assert replay_res["total_steps"] == 1


class TestAmbiguityResolver:
    """Verifies requirement entropy scoring, vague term detection, and clarification RFCs."""

    def test_ambiguity_scoring_vague_input(self):
        vague_text = "Make the portal faster and more modern with a simple clean look."
        report = AmbiguityResolver.evaluate_ambiguity(vague_text)
        assert report["is_ambiguous"] is True
        assert len(report["vague_terms_found"]) >= 2
        assert len(report["clarification_questions"]) > 0

    def test_ambiguity_scoring_precise_input(self):
        precise_text = (
            "Implement POST /api/v1/auth/token endpoint accepting { email: string, password_hash: string }. "
            "Return 200 OK with JSON { token: string, expires_in: int } or 401 Unauthorized with error schema. "
            "Enforce rate limit of 100 RPS."
        )
        report = AmbiguityResolver.evaluate_ambiguity(precise_text)
        assert report["is_ambiguous"] is False
        assert report["ambiguity_score"] < 0.35

    def test_generate_clarification_rfc(self, tmp_path):
        vague_text = "Add standard auth."
        rfc_file = AmbiguityResolver.generate_clarification_rfc(
            requirement_id="REQ-9912",
            requirement_text=vague_text,
            out_dir=tmp_path
        )
        assert rfc_file.exists()
        content = rfc_file.read_text(encoding="utf-8")
        assert "REQ-9912" in content
        assert "Detected Ambiguity Factors" in content
        assert "Required Clarification Questions" in content
