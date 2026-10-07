#!/usr/bin/env python3
"""
Unit tests for HITLCheckpointManager (TODO-AGT-18).
Verifies milestone checkpoint creation, Markdown card rendering,
interactive human resolution (approve/reject), and automated timeout policy handling.
"""

from datetime import datetime, timezone, timedelta
from pathlib import Path
import tempfile
import pytest

from workplace.core.hitl_checkpoint_manager import (
    HITLCheckpointManager,
    BlastRadiusInfo,
    HITLCheckpoint
)


@pytest.fixture
def hitl_env():
    """Initializes an isolated HITL checkpoint manager environment."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        spool = root / "milestones"
        manager = HITLCheckpointManager(workspace_root=root, spool_dir=spool)
        yield {"root": root, "spool": spool, "manager": manager}


def test_create_checkpoint(hitl_env):
    """Verifies that creating a checkpoint generates valid JSON and Markdown cards."""
    mgr = hitl_env["manager"]
    chk = mgr.create_checkpoint(
        milestone_type="ARCH_DESIGN_APPROVAL",
        title="Payment Gateway Integration Architecture",
        description="Review proposed microservice boundary and token vault schema.",
        diff_preview="--- a/schema.py\n+++ b/schema.py\n@@ ...\n+class PaymentVault: pass",
        blast_radius=BlastRadiusInfo(affected_modules=["mod_tenant_billing"], symbols_modified=12, breaking_changes=False),
        selectable_options=["APPROVE", "REJECT", "MODIFY"],
        timeout_seconds=7200,
        timeout_action="AUTO_PAUSE"
    )

    assert chk.status == "PENDING"
    assert chk.checkpoint_id.startswith("chk_")
    assert (hitl_env["spool"] / f"{chk.checkpoint_id}.json").exists()
    assert (hitl_env["spool"] / f"{chk.checkpoint_id}.md").exists()

    md_content = (hitl_env["spool"] / f"{chk.checkpoint_id}.md").read_text(encoding="utf-8")
    assert "Payment Gateway Integration" in md_content
    assert "Blast Radius & Impact Analysis" in md_content
    assert "PaymentVault" in md_content


def test_list_and_get_checkpoints(hitl_env):
    """Verifies retrieval and filtering of pending checkpoints."""
    mgr = hitl_env["manager"]
    chk1 = mgr.create_checkpoint("SCHEMA_EVOLUTION_RFC", "Schema A", "Desc A")
    chk2 = mgr.create_checkpoint("UI_WIREFRAME_SIGN_OFF", "UI B", "Desc B")

    all_chks = mgr.list_checkpoints()
    assert len(all_chks) == 2

    retrieved = mgr.get_checkpoint(chk1.checkpoint_id)
    assert retrieved is not None
    assert retrieved.title == "Schema A"


def test_resolve_checkpoint_approve(hitl_env):
    """Verifies human operator approval updates status and resolution metadata."""
    mgr = hitl_env["manager"]
    chk = mgr.create_checkpoint("PRODUCTION_DEPLOY_APPROVAL", "Deploy v2.1", "Ready for prod")

    resolved = mgr.resolve_checkpoint(
        checkpoint_id=chk.checkpoint_id,
        decision="APPROVE",
        reason="Load testing passed, SLO verified",
        resolver="lead_architect@enterprise.com"
    )

    assert resolved.status == "APPROVED"
    assert resolved.resolution is not None
    assert resolved.resolution.decision == "APPROVE"
    assert resolved.resolution.resolver == "lead_architect@enterprise.com"

    # Reload from disk
    reloaded = mgr.get_checkpoint(chk.checkpoint_id)
    assert reloaded.status == "APPROVED"
    assert reloaded.resolution.decision == "APPROVE"


def test_resolve_checkpoint_reject(hitl_env):
    """Verifies human operator rejection."""
    mgr = hitl_env["manager"]
    chk = mgr.create_checkpoint("SECURITY_POLICY_OVERRIDE", "Allow Shell Exec", "Unsafe request")

    resolved = mgr.resolve_checkpoint(
        checkpoint_id=chk.checkpoint_id,
        decision="REJECT",
        reason="Security violation: arbitrary shell exec forbidden",
        resolver="security_auditor"
    )

    assert resolved.status == "REJECTED"
    assert resolved.resolution.decision == "REJECT"


def test_invalid_decision_raises_error(hitl_env):
    """Verifies that non-permitted decision choices raise a ValueError."""
    mgr = hitl_env["manager"]
    chk = mgr.create_checkpoint("ARCH_DESIGN_APPROVAL", "Title", "Desc")

    with pytest.raises(ValueError):
        mgr.resolve_checkpoint(chk.checkpoint_id, decision="INVALID_CHOICE")


def test_check_and_handle_timeouts(hitl_env):
    """Verifies automated timeout transition for expired checkpoints."""
    mgr = hitl_env["manager"]
    chk = mgr.create_checkpoint(
        milestone_type="ARCH_DESIGN_APPROVAL",
        title="Expiring Checkpoint",
        description="Should expire quickly",
        timeout_seconds=60,
        timeout_action="AUTO_PAUSE"
    )

    # Manually backdate created_at timestamp
    past_time = (datetime.now(timezone.utc) - timedelta(seconds=120)).isoformat()
    chk.created_at = past_time
    json_file = hitl_env["spool"] / f"{chk.checkpoint_id}.json"
    json_file.write_text(pytest.importorskip("json").dumps(chk.to_dict(), indent=2), encoding="utf-8")

    timed_out_list = mgr.check_and_handle_timeouts()
    assert len(timed_out_list) == 1
    assert timed_out_list[0].checkpoint_id == chk.checkpoint_id
    assert timed_out_list[0].status == "TIMED_OUT"
    assert "TIMEOUT_AUTO_PAUSE" in timed_out_list[0].resolution.decision
