"""
Unit and Integration Test Suite for Solution Management Simplification & Zero-Dial Invariants (Section 22):
- TODO-SIMP-01: Document Integral Invariants as Official Architecture Standards
- TODO-SIMP-02: Decommission UI Dials & Sliders in Web SaaS Portal
- TODO-SIMP-03: Collapse Project Policy Engine Schemas into 5-Point Control Surface
- TODO-SIMP-04: Simplify CLI Flags & Deprecate Redundant Tuning Options
- TODO-SIMP-05: Cleanse Static Rule Configurations in Workspace Repositories
- TODO-SIMP-06: Verification & End-to-End Regression Harness for Zero-Dial Architecture
"""

import sys
import json
import threading
import time
from pathlib import Path
from http.client import HTTPConnection
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "workplace") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "workplace"))

from http.server import HTTPServer
from portal.server import PortalRequestHandler
from core.project_policy_engine import (
    ProjectPolicy,
    ProjectPolicyManager,
    WireContractRule,
    AttentionSlicingPolicy,
    CognitiveRoutingPolicy,
    ASTPruningPolicy,
    SelfHealingSLAPolicy
)


@pytest.fixture(scope="module")
def portal_server():
    """Lightweight test server for portal endpoint verification."""
    server = HTTPServer(("127.0.0.1", 0), PortalRequestHandler)
    port = server.server_port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.1)
    yield f"127.0.0.1:{port}"
    server.shutdown()


def test_01_certified_invariants_and_control_surface():
    """Verifies that ProjectPolicy operates on the minimal 5-point surface with certified invariants."""
    policy = ProjectPolicy(
        tenant_id="tenant_acme",
        project_id="proj_simplification",
        environment="production",
        vcs_repository={"url": "https://github.com/acme/repo.git", "default_branch": "main"},
        hitl_quarantine_webhook="https://hooks.slack.com/services/test"
    )

    # 1. 5-point control surface verification
    assert policy.tenant_id == "tenant_acme"
    assert policy.project_id == "proj_simplification"
    assert policy.environment == "production"
    assert policy.vcs_repository["url"] == "https://github.com/acme/repo.git"
    assert policy.hitl_quarantine_webhook == "https://hooks.slack.com/services/test"

    # 2. Immutable/Invariant standards verified
    assert policy.attention.persona_invariants_pct == 15.0
    assert policy.attention.contracts_schemas_pct == 25.0
    assert policy.attention.ast_codebase_pct == 35.0
    assert policy.attention.memory_trajectories_pct == 10.0
    assert policy.attention.reserved_output_pct == 15.0

    assert policy.healing_sla.max_diagnostic_reprompts == 3
    assert policy.healing_sla.flaky_quarantine_variance_threshold == 0.15

    # 3. Certified invariants attestation dictionary
    invariants = policy.certified_invariants
    assert "attention_slicing" in invariants
    assert "15/25/35/10/15" in invariants["attention_slicing"]
    assert "ast_skeletonization" in invariants
    assert "self_healing_sla" in invariants
    assert invariants["wire_contract_rule"] == "STRICT_BLOCK"

    # 4. Serialization round-trip
    p_dict = policy.to_dict()
    assert "certified_invariants" in p_dict
    assert p_dict["environment"] == "production"

    reconstructed = ProjectPolicy.from_dict(p_dict)
    assert reconstructed.environment == "production"
    assert reconstructed.vcs_repository["url"] == "https://github.com/acme/repo.git"


def test_02_environment_mode_governance():
    """Verifies that Operational Environment Mode toggles strict vs non-blocking gate rules."""
    dev_policy = ProjectPolicy(
        tenant_id="tenant_dev",
        project_id="proj_dev",
        environment="development"
    )
    # Development mode adapts wire contract breaking rule
    assert dev_policy.environment == "development"
    assert dev_policy.certified_invariants["wire_contract_rule"] == "ALLOW_ADDITIVE_WARN"

    # Invalid environment rejected
    with pytest.raises(ValueError):
        invalid_policy = ProjectPolicy(
            tenant_id="t",
            project_id="p",
            environment="staging_invalid"
        )
        invalid_policy.validate()


def test_03_legacy_policy_backward_compatibility():
    """Verifies that historical policy payloads containing decommissioned knobs deserialize cleanly."""
    legacy_payload = {
        "tenant_id": "tenant_legacy",
        "project_id": "proj_legacy",
        "version": 4,
        "attention": {
            "persona_invariants_pct": 20.0,
            "contracts_schemas_pct": 20.0,
            "ast_codebase_pct": 30.0,
            "memory_trajectories_pct": 10.0,
            "reserved_output_pct": 20.0
        },
        "healing_sla": {
            "max_diagnostic_reprompts": 4,
            "flaky_quarantine_variance_threshold": 0.25,
            "wire_contract_breaking_rule": "MANUAL_APPROVAL"
        }
    }

    policy = ProjectPolicy.from_dict(legacy_payload)
    assert policy.tenant_id == "tenant_legacy"
    assert policy.environment == "production"  # Defaults safely to production
    assert policy.version == 4
    assert policy.attention.persona_invariants_pct == 20.0
    assert policy.healing_sla.max_diagnostic_reprompts == 4
    assert "certified_invariants" in policy.to_dict()


def test_04_portal_ui_zero_dials_rendered(portal_server):
    """Verifies that Tab 14 in the SaaS Portal renders with zero manual range sliders."""
    conn = HTTPConnection(portal_server)
    conn.request("GET", "/")
    res = conn.getresponse()
    assert res.status == 200
    html = res.read().decode("utf-8")

    # 1. Assert all 8 manual range sliders are eliminated
    eliminated_sliders = [
        'id="sliderPersona"',
        'id="sliderContracts"',
        'id="sliderAst"',
        'id="sliderMemory"',
        'id="sliderOutput"',
        'id="sliderTierA"',
        'id="sliderReprompts"',
        'id="sliderFlaky"'
    ]
    for slider_id in eliminated_sliders:
        assert slider_id not in html, f"Decommissioned dial {slider_id} found in Portal UI!"

    # 2. Assert simplified 5-point control surface and verified invariants are present
    assert 'id="policyEnvironmentSelect"' in html
    assert 'id="policyHitlWebhook"' in html
    assert 'id="policyVcsUrl"' in html
    assert 'id="policyVcsBranch"' in html
    assert "Certified Architectural Standards (Zero-Dial Invariants)" in html
    assert "Tree-Sitter 6D AST Skeletonizer" in html
    assert "Self-Healing SLA (3-Turn Bound)" in html


def test_05_portal_policy_update_endpoint(portal_server):
    """Verifies that POST /api/project/policy/update accepts simplified payloads and returns certified invariants."""
    conn = HTTPConnection(portal_server)
    headers = {"Content-Type": "application/json"}

    update_payload = json.dumps({
        "tenant_id": "tenant_acme_fintech",
        "project_id": "proj_fairyfly_core_9921",
        "patch_data": {
            "environment": "development",
            "hitl_quarantine_webhook": "https://hooks.slack.com/services/alerts",
            "vcs_repository": {
                "url": "https://github.com/acme/simplified.git",
                "default_branch": "develop"
            }
        },
        "user_id": "user_architect"
    })

    conn.request("POST", "/api/project/policy/update", body=update_payload, headers=headers)
    res = conn.getresponse()
    assert res.status == 200
    data = json.loads(res.read().decode("utf-8"))

    assert data["status"] == "UPDATED"
    pol = data["policy"]
    assert pol["environment"] == "development"
    assert pol["vcs_repository"]["url"] == "https://github.com/acme/simplified.git"
    assert pol["hitl_quarantine_webhook"] == "https://hooks.slack.com/services/alerts"
    assert "certified_invariants" in pol
    assert pol["certified_invariants"]["wire_contract_rule"] == "ALLOW_ADDITIVE_WARN"


def test_06_invariants_documentation_standards_exist():
    """Verifies that all 4 formal invariant standard specification files exist and are populated."""
    docs = [
        REPO_ROOT / "workplace/docs/methodologies/attention_slicing_standard.md",
        REPO_ROOT / "workplace/docs/standards/ast_skeletonization_standard.md",
        REPO_ROOT / "workplace/docs/standards/self_healing_convergence_standard.md",
        REPO_ROOT / "workplace/docs/standards/swarm_graph_integrity_standard.md",
    ]

    for doc_path in docs:
        assert doc_path.exists(), f"Standard document missing: {doc_path}"
        content = doc_path.read_text(encoding="utf-8")
        assert len(content) > 300, f"Standard document {doc_path} has insufficient content"
        assert "RATIFIED ARCHITECTURAL STANDARD" in content
