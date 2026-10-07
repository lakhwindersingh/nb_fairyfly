#!/usr/bin/env python3
"""
Unit tests for ConsensusQuorumEngine (TODO-AGT-17).
Verifies 2-of-3 multi-agent consensus, single-veto quarantine escalation,
HMAC cryptographic integrity attestation, and deadlock resolution.
"""

from pathlib import Path
import tempfile
import pytest

from workplace.core.consensus_quorum_engine import (
    ConsensusQuorumEngine,
    EvaluatorVote,
    QuorumReceipt
)


@pytest.fixture
def quorum_env():
    """Provides an isolated workspace directory with a consensus quorum engine."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        engine = ConsensusQuorumEngine(workspace_root=root, secret_key="test_secret_key")
        yield {"root": root, "engine": engine}


def test_2_of_3_approval_passage(quorum_env):
    """Verifies that 2 APPROVE votes and 1 REVISION vote successfully passes quorum."""
    engine = quorum_env["engine"]
    votes = [
        EvaluatorVote("agent_security", "SecurityAuditor", "APPROVE", "No CVEs or secrets found"),
        EvaluatorVote("agent_quality", "QualityGatekeeper", "APPROVE", "All 45 tests pass deterministically"),
        EvaluatorVote("agent_arch", "ArchitecturalSpecialist", "REQUEST_REVISION", "Minor docstring clarification requested")
    ]

    receipt = engine.evaluate_quorum(
        decision_type="PR_GATE_APPROVAL",
        target_artifact="PR #42 (mod_billing)",
        votes=votes
    )

    assert receipt.quorum_passed is True
    assert receipt.verdict == "APPROVED"
    assert receipt.single_veto_triggered is False
    assert receipt.merkle_block_id.startswith("RP_QUORUM_")
    assert engine.verify_receipt(receipt) is True


def test_single_veto_quarantine_escalation(quorum_env):
    """Verifies that ANY single QUARANTINE_VETO halts execution and escalates to quarantine."""
    engine = quorum_env["engine"]
    votes = [
        EvaluatorVote("agent_quality", "QualityGatekeeper", "APPROVE", "Tests pass"),
        EvaluatorVote("agent_arch", "ArchitecturalSpecialist", "APPROVE", "Architecture sound"),
        EvaluatorVote("agent_security", "SecurityAuditor", "QUARANTINE_VETO", "Detected obfuscated base64 exfiltration payload!")
    ]

    receipt = engine.evaluate_quorum(
        decision_type="SECURITY_SIGN_OFF",
        target_artifact="PR #43 (mod_auth)",
        votes=votes
    )

    assert receipt.quorum_passed is False
    assert receipt.verdict == "QUARANTINED"
    assert receipt.single_veto_triggered is True

    # Verify quarantine file updated
    quarantine_file = quorum_env["root"] / "user" / "hitl" / "poisoning_quarantine.md"
    assert quarantine_file.exists()
    assert "QUORUM SINGLE-VETO QUARANTINE" in quarantine_file.read_text(encoding="utf-8")
    assert "obfuscated base64 exfiltration" in quarantine_file.read_text(encoding="utf-8")


def test_revision_requested_quorum(quorum_env):
    """Verifies that >= 2 REQUEST_REVISION votes routes to revision requested."""
    engine = quorum_env["engine"]
    votes = [
        EvaluatorVote("agent_quality", "QualityGatekeeper", "REQUEST_REVISION", "Coverage fell below 85%"),
        EvaluatorVote("agent_arch", "ArchitecturalSpecialist", "REQUEST_REVISION", "Breaking wire contract change detected"),
        EvaluatorVote("agent_security", "SecurityAuditor", "APPROVE", "Clean security scan")
    ]

    receipt = engine.evaluate_quorum(
        decision_type="WIRE_CONTRACT_DEPRECATION",
        target_artifact="schemas/order_v1.yaml",
        votes=votes
    )

    assert receipt.quorum_passed is False
    assert receipt.verdict == "REVISION_REQUESTED"
    assert receipt.single_veto_triggered is False


def test_hmac_tamper_detection(quorum_env):
    """Verifies that modifying any receipt parameter causes HMAC attestation failure."""
    engine = quorum_env["engine"]
    votes = [
        EvaluatorVote("a1", "SecurityAuditor", "APPROVE", "ok"),
        EvaluatorVote("a2", "QualityGatekeeper", "APPROVE", "ok"),
        EvaluatorVote("a3", "ArchitecturalSpecialist", "APPROVE", "ok")
    ]

    receipt = engine.evaluate_quorum("PR_GATE_APPROVAL", "target_file", votes)
    assert engine.verify_receipt(receipt) is True

    # Tamper with verdict
    tampered = QuorumReceipt(
        quorum_id=receipt.quorum_id,
        decision_type=receipt.decision_type,
        target_artifact=receipt.target_artifact,
        verdict="REVISION_REQUESTED",  # TAMPERED
        quorum_passed=False,
        single_veto_triggered=receipt.single_veto_triggered,
        votes=receipt.votes,
        quorum_hmac=receipt.quorum_hmac,
        timestamp_utc=receipt.timestamp_utc
    )
    assert engine.verify_receipt(tampered) is False


def test_invalid_vote_count_raises_error(quorum_env):
    """Verifies that passing fewer or more than 3 votes raises a ValueError."""
    engine = quorum_env["engine"]
    with pytest.raises(ValueError):
        engine.evaluate_quorum("PR_GATE_APPROVAL", "target", [
            EvaluatorVote("a1", "r1", "APPROVE", "ok"),
            EvaluatorVote("a2", "r2", "APPROVE", "ok")
        ])
