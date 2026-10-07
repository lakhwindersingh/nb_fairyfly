"""
Unit and Integration Test Suite for Portal Observability Dashboard & Secure Client Space:
- Public unauthenticated zones (health, comparatives, otel traces, evals, cache)
- Secure client authentication (login, session validation, logout)
- Protected client space endpoints (project details, finops invoices, WORM audit, surgical rollback)
- Multi-tenant hierarchy, PostgreSQL RLS schema generator, and automated KMS sealed enclave endpoints (CAP-40 / Section 18.1)
"""

import sys
import json
import threading
import time
from pathlib import Path
from http.client import HTTPConnection
from urllib.parse import urlencode

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "workplace") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "workplace"))

import pytest
from http.server import HTTPServer
from portal.server import PortalRequestHandler, CLIENT_SESSIONS


@pytest.fixture(scope="module")
def portal_server():
    """Spins up a lightweight ephemeral instance of PortalRequestHandler."""
    server = HTTPServer(("127.0.0.1", 0), PortalRequestHandler)
    port = server.server_port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.1)
    yield f"127.0.0.1:{port}"
    server.shutdown()


def test_public_observability_endpoints(portal_server):
    conn = HTTPConnection(portal_server)

    # 1. Health
    conn.request("GET", "/api/health")
    res = conn.getresponse()
    assert res.status == 200
    data = json.loads(res.read().decode("utf-8"))
    assert data["status"] == "HEALTHY"

    # 2. OpenTelemetry traces
    conn.request("GET", "/api/observability/otel-traces")
    res = conn.getresponse()
    assert res.status == 200
    otel_data = json.loads(res.read().decode("utf-8"))
    assert "spans" in otel_data
    assert len(otel_data["spans"]) >= 2
    assert "w3c_traceparent" in otel_data["spans"][0]["context"]

    # 3. Quantitative Evals
    conn.request("GET", "/api/observability/evals")
    res = conn.getresponse()
    assert res.status == 200
    eval_data = json.loads(res.read().decode("utf-8"))
    assert eval_data["composite_geval_score"] >= 0.90
    assert eval_data["rubrics"]["faithfulness"] >= 0.90

    # 4. Semantic Cache
    conn.request("GET", "/api/observability/semantic-cache")
    res = conn.getresponse()
    assert res.status == 200
    cache_data = json.loads(res.read().decode("utf-8"))
    assert "hits" in cache_data


def test_secure_client_space_unauthorized_rejection(portal_server):
    conn = HTTPConnection(portal_server)

    # Attempting to access client endpoints without token
    conn.request("GET", "/api/client/project-details")
    res = conn.getresponse()
    assert res.status == 401

    conn.request("GET", "/api/client/finops-invoices")
    res = conn.getresponse()
    assert res.status == 401

    conn.request("GET", "/api/client/worm-audit")
    res = conn.getresponse()
    assert res.status == 401


def test_client_authentication_flow(portal_server):
    conn = HTTPConnection(portal_server)

    # 1. Login
    login_payload = json.dumps({"client_id": "acme_corp_fintech", "api_key": "nb_sec_client_9948"})
    headers = {"Content-Type": "application/json"}
    conn.request("POST", "/api/auth/login", body=login_payload, headers=headers)
    res = conn.getresponse()
    assert res.status == 200
    login_data = json.loads(res.read().decode("utf-8"))
    assert login_data["status"] == "AUTHENTICATED"
    token = login_data["session_token"]
    assert token is not None

    # 2. Validate session
    conn.request("GET", f"/api/auth/session?token={token}")
    res = conn.getresponse()
    assert res.status == 200
    sess_data = json.loads(res.read().decode("utf-8"))
    assert sess_data["client"]["client_id"] == "acme_corp_fintech"

    # 3. Access protected client project details
    conn.request("GET", f"/api/client/project-details?token={token}")
    res = conn.getresponse()
    assert res.status == 200
    proj_data = json.loads(res.read().decode("utf-8"))
    assert proj_data["workspace_mode"] == "multi_module"
    assert "mod_auth" in proj_data["active_modules"]

    # 4. Access protected finops invoices
    conn.request("GET", f"/api/client/finops-invoices?token={token}")
    res = conn.getresponse()
    assert res.status == 200
    invoice_data = json.loads(res.read().decode("utf-8"))
    assert invoice_data["rev_share_rate_pct"] == 15.0
    assert len(invoice_data["itemized_lines"]) >= 3

    # 5. Access WORM compliance audit
    conn.request("GET", f"/api/client/worm-audit?token={token}")
    res = conn.getresponse()
    assert res.status == 200
    worm_data = json.loads(res.read().decode("utf-8"))
    assert worm_data["status"] == "COMPLIANT"

    # 6. Execute surgical rollback
    rollback_payload = json.dumps({"module_id": "mod_auth", "token": token})
    conn.request("POST", "/api/client/surgical-rollback", body=rollback_payload, headers=headers)
    res = conn.getresponse()
    assert res.status == 200
    rb_data = json.loads(res.read().decode("utf-8"))
    assert rb_data["status"] == "SUCCESS"
    assert rb_data["module_id"] == "mod_auth"

    # 7. Logout
    logout_payload = json.dumps({"token": token})
    conn.request("POST", "/api/auth/logout", body=logout_payload, headers=headers)
    res = conn.getresponse()
    assert res.status == 200

    # 8. Verify token revoked
    conn.request("GET", f"/api/client/project-details?token={token}")
    res = conn.getresponse()
    assert res.status == 401


def test_tenant_and_kms_portal_endpoints(portal_server):
    """Validates multi-tenant hierarchy, PostgreSQL RLS schema DDL, and KMS sealed enclave endpoints."""
    conn = HTTPConnection(portal_server)
    headers = {"Content-Type": "application/json"}

    # 1. Get Tenant Hierarchy
    conn.request("GET", "/api/tenant/hierarchy?tenant_id=tenant_acme_fintech")
    res = conn.getresponse()
    assert res.status == 200
    hier = json.loads(res.read().decode("utf-8"))
    assert hier["tenant"]["tenant_id"] == "tenant_acme_fintech"
    assert len(hier["projects"]) >= 1
    assert hier["projects"][0]["project"]["project_id"] == "proj_fairyfly_core_9921"

    # 2. Get PostgreSQL RLS DDL
    conn.request("GET", "/api/tenant/rls-schema")
    res = conn.getresponse()
    assert res.status == 200
    rls_data = json.loads(res.read().decode("utf-8"))
    assert rls_data["status"] == "SUCCESS"
    assert "ENABLE ROW LEVEL SECURITY" in rls_data["rls_schema_ddl"]
    assert "CREATE POLICY tenant_isolation_policy" in rls_data["rls_schema_ddl"]

    # 3. Seal In-Memory KMS Enclave (.nbpack)
    seal_payload = json.dumps({
        "tenant_id": "tenant_acme_fintech",
        "project_id": "proj_fairyfly_core_9921",
        "payload": {
            "prompt_system": "Act as an autonomous institutional trading risk agent.",
            "max_var_loss_usd": 50000.0
        }
    })
    conn.request("POST", "/api/kms/seal", body=seal_payload, headers=headers)
    res = conn.getresponse()
    assert res.status == 200
    seal_res = json.loads(res.read().decode("utf-8"))
    assert seal_res["status"] == "SUCCESS"
    bundle = seal_res["bundle"]
    assert bundle["envelope_format"] == "NBPACK_AES256_ED25519"
    assert bundle["merkle_seal"] is not None

    # 4. Mount In-Memory KMS Enclave
    mount_payload = json.dumps({
        "project_id": "proj_fairyfly_core_9921",
        "bundle": bundle
    })
    conn.request("POST", "/api/kms/mount", body=mount_payload, headers=headers)
    res = conn.getresponse()
    assert res.status == 200
    mount_res = json.loads(res.read().decode("utf-8"))
    assert mount_res["status"] == "SUCCESS"
    assert mount_res["unsealed_payload"]["max_var_loss_usd"] == 50000.0

    # 5. Check KMS Audit Log
    conn.request("GET", "/api/kms/audit")
    res = conn.getresponse()
    assert res.status == 200
    audit_res = json.loads(res.read().decode("utf-8"))
    assert audit_res["status"] == "SUCCESS"
    assert len(audit_res["audit_log"]) >= 2


def test_project_policy_tuning_portal_endpoints(portal_server):
    """Validates Section 18.2 granular policy tuning & SLA evaluation endpoints."""
    conn = HTTPConnection(portal_server)
    headers = {"Content-Type": "application/json"}
    p_test_id = "proj_portal_policy_test_unique"

    # 1. GET project policy
    conn.request("GET", f"/api/project/policy?tenant_id=tenant_acme_fintech&project_id={p_test_id}")
    res = conn.getresponse()
    assert res.status == 200
    pol_data = json.loads(res.read().decode("utf-8"))
    assert pol_data["status"] == "SUCCESS"
    policy = pol_data["policy"]
    assert policy["attention"]["persona_invariants_pct"] == 15.0
    assert policy["healing_sla"]["max_diagnostic_reprompts"] == 3

    # 2. UPDATE project policy (tuning sliders)
    update_payload = json.dumps({
        "tenant_id": "tenant_acme_fintech",
        "project_id": p_test_id,
        "patch_data": {
            "attention": {
                "persona_invariants_pct": 20.0,
                "contracts_schemas_pct": 20.0,
                "ast_codebase_pct": 35.0,
                "memory_trajectories_pct": 10.0,
                "reserved_output_pct": 15.0
            },
            "healing_sla": {
                "max_diagnostic_reprompts": 5,
                "flaky_quarantine_variance_threshold": 0.20
            }
        },
        "user_id": "lead_alice"
    })
    conn.request("POST", "/api/project/policy/update", body=update_payload, headers=headers)
    res = conn.getresponse()
    assert res.status == 200
    up_res = json.loads(res.read().decode("utf-8"))
    assert up_res["status"] == "UPDATED"
    assert up_res["policy"]["version"] == 2
    assert up_res["policy"]["attention"]["persona_invariants_pct"] == 20.0
    assert up_res["policy"]["healing_sla"]["max_diagnostic_reprompts"] == 5

    # 3. Dynamic Attention Slicing with updated project quotas
    slice_payload = json.dumps({
        "tenant_id": "tenant_acme_fintech",
        "project_id": p_test_id,
        "sections": {
            "persona_invariants": "Security Rule: Non-overridable",
            "contracts_schemas": "API Schema Definition " * 30,
            "ast_codebase": "def process(): pass\n" * 200
        },
        "max_total_tokens": 1000
    })
    conn.request("POST", "/api/project/policy/slice-attention", body=slice_payload, headers=headers)
    res = conn.getresponse()
    assert res.status == 200
    slice_res = json.loads(res.read().decode("utf-8"))
    assert slice_res["status"] == "SUCCESS"
    assert slice_res["result"]["policy_version"] == 2
    assert "Security Rule: Non-overridable" in slice_res["result"]["sections"]["persona_invariants"]

    # 4. Evaluate PR Verification Gate
    pr_eval_payload = json.dumps({
        "tenant_id": "tenant_acme_fintech",
        "project_id": p_test_id,
        "test_run_history": [
            {"test_id": "test_flaky_socket", "runs": 10, "failures": 1},
            {"test_id": "test_core_engine", "runs": 10, "failures": 0}
        ],
        "current_heal_turn": 0
    })
    conn.request("POST", "/api/project/policy/evaluate-pr-gate", body=pr_eval_payload, headers=headers)
    res = conn.getresponse()
    assert res.status == 200
    pr_res = json.loads(res.read().decode("utf-8"))
    assert pr_res["status"] == "SUCCESS"
    assert pr_res["evaluation"]["gate_decision"] == "PASS"
    assert len(pr_res["evaluation"]["test_audit"]["quarantined_flaky_tests"]) == 1

    # Cleanup test file
    cleanup_path = REPO_ROOT / ".nb" / "config" / "policies" / f"tenant_acme_fintech_{p_test_id}.yaml"
    if cleanup_path.exists():
        cleanup_path.unlink()
