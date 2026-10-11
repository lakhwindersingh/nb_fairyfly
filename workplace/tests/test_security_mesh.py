"""
Unit and integration test suite for the Percipience Security Mesh.
Tests multi-tenant ReBAC, WebAuthn Passkeys, RFC 6238 TOTP MFA,
Bloom Filter token revocation, NIST SP 800-38G FPE dynamic masking,
Four-Eyes dual control, and portal HTTP request handler security endpoints.
"""

import time
import json
import base64
import secrets
from pathlib import Path
from io import BytesIO
from unittest.mock import MagicMock

import pytest

from workplace.core.security_mesh_engine import (
    SecurityMeshEngine,
    ReBACTuple,
    AdaptiveRiskEngine,
    WebAuthnPasskeyEngine,
    TOTPAuthenticationEngine,
    FormatPreservingEncryption,
    PIISanitizerMesh,
    MaskingStyle,
    FourEyesController,
    ActionStatus,
    BloomRevocationFilter,
)
from workplace.portal.core.request_handler import PortalRequestHandler
from workplace.portal.core.state import CLIENT_SESSIONS, DEMO_CLIENT, GLOBAL_SECURITY_MESH


REPO_ROOT = Path(__file__).resolve().parents[2]


class DummyPortalHandler(PortalRequestHandler):
    """Mock handler for testing request handler methods directly."""
    def __init__(self, method="GET", path="/", body=None, headers=None):
        self.command = method
        self.path = path
        self.headers = headers or {}
        raw_body = json.dumps(body).encode("utf-8") if isinstance(body, dict) else (body or b"")
        self.rfile = BytesIO(raw_body)
        self.wfile = BytesIO()
        self.headers = headers or {}
        if "Content-Length" not in self.headers and raw_body:
            self.headers["Content-Length"] = str(len(raw_body))
        self.client_address = ("127.0.0.1", 54321)
        self.response_status = 200
        self.response_headers = {}

    def send_response(self, code, message=None):
        self.response_status = code

    def send_header(self, keyword, value):
        self.response_headers[keyword] = value

    def end_headers(self):
        pass

    def get_json_response(self):
        raw = self.wfile.getvalue()
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))


# =========================================================================
# 1. ReBAC & Multi-Tenant Hierarchy Tests
# =========================================================================

def test_rebac_tuple_evaluation():
    engine = SecurityMeshEngine()
    tup = ReBACTuple(
        tenant_id="tenant_acme",
        entity_type="project",
        entity_id="proj_001",
        relation="owner",
        subject_type="user",
        subject_id="alice"
    )
    engine.add_rebac_tuple(tup)

    # Direct match
    assert engine.check_rebac_relation(
        "tenant_acme", "project", "proj_001", "owner", "user", "alice"
    ) is True

    # Ownership implies viewer and editor
    assert engine.check_rebac_relation(
        "tenant_acme", "project", "proj_001", "viewer", "user", "alice"
    ) is True
    assert engine.check_rebac_relation(
        "tenant_acme", "project", "proj_001", "editor", "user", "alice"
    ) is True

    # Cross-tenant boundary isolation
    assert engine.check_rebac_relation(
        "tenant_hacker", "project", "proj_001", "owner", "user", "alice"
    ) is False

    # Unrelated user
    assert engine.check_rebac_relation(
        "tenant_acme", "project", "proj_001", "owner", "user", "eve"
    ) is False


# =========================================================================
# 2. Adaptive Risk Engine & Impossible Travel
# =========================================================================

def test_adaptive_risk_impossible_travel():
    # London (51.5074, -0.1278) to Tokyo (35.6762, 139.6503) is ~9,560 km
    lon_lat, lon_lon = 51.5074, -0.1278
    tok_lat, tok_lon = 35.6762, 139.6503

    now = time.time()
    # Logged in 10 minutes ago in London
    last_login = {
        "lat": lon_lat,
        "lon": lon_lon,
        "timestamp": now - 600,
        "device_fingerprint": "dev_trusted_mac"
    }

    # Attempt login from Tokyo 10 min later -> velocity ~ 57,000 km/h (impossible)
    score, reasons = AdaptiveRiskEngine.calculate_risk(
        ip="142.250.190.46",
        current_lat=tok_lat,
        current_lon=tok_lon,
        current_ts=now,
        device_fingerprint="dev_trusted_mac",
        last_login=last_login
    )

    assert score >= 0.65
    assert any("Impossible travel detected" in r for r in reasons)


def test_adaptive_risk_low_velocity_clean():
    now = time.time()
    last_login = {
        "lat": 40.7128,
        "lon": -74.0060,
        "timestamp": now - 3600,
        "device_fingerprint": "dev_trusted_mac"
    }

    score, reasons = AdaptiveRiskEngine.calculate_risk(
        ip="192.168.1.100",
        current_lat=40.7128,
        current_lon=-74.0060,
        current_ts=now,
        device_fingerprint="dev_trusted_mac",
        last_login=last_login
    )

    assert score == 0.0
    assert len(reasons) == 0


# =========================================================================
# 3. WebAuthn / FIDO2 Passkeys Engine
# =========================================================================

def test_webauthn_registration_and_authentication():
    engine = WebAuthnPasskeyEngine()
    # 1. Registration
    reg_opts = engine.generate_registration_options("user_alice", "tenant_acme")
    challenge = reg_opts["challenge"]
    assert len(challenge) > 20

    # Verify registration
    cred_id = "cred_yubikey_5_nfc_001"
    pub_key = secrets.token_hex(32)
    assert engine.verify_registration(challenge, cred_id, pub_key, "Alice YubiKey") is True
    assert cred_id in engine.credentials

    # 2. Authentication
    auth_opts = engine.generate_authentication_options("user_alice", "tenant_acme")
    auth_challenge = auth_opts["challenge"]
    assert any(c["id"] == cred_id for c in auth_opts["allowCredentials"])

    # Successful authentication
    assert engine.verify_authentication(auth_challenge, cred_id, "hash", counter=1) is True

    # Replay attack with non-increasing counter must fail
    auth_opts_2 = engine.generate_authentication_options("user_alice", "tenant_acme")
    assert engine.verify_authentication(auth_opts_2["challenge"], cred_id, "hash", counter=1) is False


# =========================================================================
# 4. RFC 6238 TOTP Engine & Backup Codes
# =========================================================================

def test_totp_generation_and_validation():
    secret = TOTPAuthenticationEngine.generate_secret()
    assert len(secret) >= 16

    code = TOTPAuthenticationEngine.get_totp(secret)
    assert len(code) == 6
    assert code.isdigit()

    # Valid code verifies
    assert TOTPAuthenticationEngine.verify_totp(secret, code) is True

    # Invalid code fails
    assert TOTPAuthenticationEngine.verify_totp(secret, "999999" if code != "999999" else "000000") is False

    # Backup codes
    plain, hashed = TOTPAuthenticationEngine.generate_backup_codes(4)
    assert len(plain) == 4
    assert len(hashed) == 4
    assert "-" in plain[0]


# =========================================================================
# 5. Continuous Zero-Trust Bloom Revocation Filter
# =========================================================================

def test_bloom_revocation_submillisecond():
    bloom = BloomRevocationFilter()
    token = "nb_sess_test_bloom_token_999"

    assert bloom.is_revoked(token) is False

    # Revoke
    bloom.revoke(token)
    assert bloom.is_revoked(token) is True

    # Measure lookup latency across 100 iterations (must average < 1000 microseconds)
    start_t = time.perf_counter()
    for _ in range(100):
        bloom.is_revoked(token)
    elapsed_us = ((time.perf_counter() - start_t) / 100) * 1_000_000
    assert elapsed_us < 1000.0  # Well within sub-millisecond SLA


# =========================================================================
# 6. NIST SP 800-38G FPE & PII Dynamic Masking
# =========================================================================

def test_fpe_structure_preservation():
    fpe = FormatPreservingEncryption()
    ssn = "123-45-6789"
    cipher = fpe.encrypt_structured(ssn, "SSN")
    assert len(cipher) == len(ssn)
    assert cipher[3] == "-" and cipher[6] == "-"
    assert cipher != ssn


def test_pii_masking_styles():
    mesh = PIISanitizerMesh()
    email = "sarah.connor@cyberdyne.com"
    tax_id = "948-21-5038"

    assert mesh.mask_field(email, MaskingStyle.EMAIL_MASK).startswith("s***@")
    assert mesh.mask_field(tax_id, MaskingStyle.PARTIAL_TRAILING_FOUR) == "***-**-5038"
    assert mesh.mask_field(tax_id, MaskingStyle.FULL_REDACTED) == "[REDACTED_PII]"
    assert mesh.mask_field(tax_id, MaskingStyle.PLAINTEXT_AUTHORIZED) == tax_id


def test_pii_streaming_scrubber():
    mesh = PIISanitizerMesh()
    raw_prompt = "User alice@bank.com with TIN 123-45-6789 used API key nb_sec_1234567890abcdef."
    scrubbed = mesh.scrub_text(raw_prompt)
    assert "[SCRUBBED_EMAIL]" in scrubbed
    assert "[SCRUBBED_TIN]" in scrubbed
    assert "[SCRUBBED_API_KEY]" in scrubbed
    assert "alice@bank.com" not in scrubbed
    assert "123-45-6789" not in scrubbed


# =========================================================================
# 7. Four-Eyes Multi-Signature Dual Control State Machine
# =========================================================================

def test_four_eyes_controller():
    controller = FourEyesController()
    # Propose
    act = controller.propose_action(
        tenant_id="tenant_acme",
        action_type="SURGICAL_ROLLBACK",
        target_resource="mod_auth",
        initiator_id="alice",
        initiator_sig="sig_alice_ed25519"
    )
    assert act.status == ActionStatus.PENDING_APPROVAL

    # Self-approval violation
    ok, err = controller.approve_action(act.action_id, approver_id="alice", approver_sig="sig_alice")
    assert ok is False
    assert "Distinct individuals" in err or "Four-Eyes Violation" in err

    # Distinct approver
    ok, msg = controller.approve_action(act.action_id, approver_id="bob", approver_sig="sig_bob_ed25519")
    assert ok is True
    assert act.status == ActionStatus.MERKLE_SEALED
    assert act.merkle_leaf_hash is not None


# =========================================================================
# 8. Portal HTTP Handler Security Endpoints
# =========================================================================

def test_portal_security_mesh_status():
    handler = DummyPortalHandler(method="GET", path="/api/security-mesh/status")
    handler.do_GET()
    assert handler.response_status == 200
    res = handler.get_json_response()
    assert res["status"] == "OPERATIONAL"
    assert res["bloom_filter"]["sub_millisecond_eval"] is True
    assert res["pii_vault"]["standard"] == "NIST SP 800-38G FF1"


def test_portal_rebac_check_endpoint():
    handler = DummyPortalHandler(method="GET", path="/api/security/rebac/check?tenant_id=tenant_acme_fintech&entity_type=project&entity_id=proj_fairyfly_core_9921&relation=owner&subject_type=user&subject_id=user_super_alice")
    handler.do_GET()
    assert handler.response_status == 200
    res = handler.get_json_response()
    assert res["allowed"] is True


def test_portal_auth_login_and_sub_ms_revocation():
    # 1. Login
    login_handler = DummyPortalHandler(method="POST", path="/api/auth/login", body={
        "client_id": "acme_corp_fintech",
        "api_key": "nb_sec_client_9948"
    })
    login_handler.do_POST()
    assert login_handler.response_status == 200
    login_res = login_handler.get_json_response()
    assert login_res["status"] == "AUTHENTICATED"
    token = login_res["session_token"]

    # 2. Access client project details with token
    client_handler = DummyPortalHandler(method="GET", path=f"/api/client/project-details?token={token}")
    client_handler.do_GET()
    assert client_handler.response_status == 200
    details = client_handler.get_json_response()
    assert details["pii_display_mode"] == "DYNAMIC_ROLE_MASKED"
    assert "@" in details["user_email"] and "*" in details["user_email"]

    # 3. Revoke token via Bloom filter
    revoke_handler = DummyPortalHandler(method="POST", path="/api/auth/revoke-token", body={"token": token})
    revoke_handler.do_POST()
    assert revoke_handler.response_status == 200
    rev_res = revoke_handler.get_json_response()
    assert rev_res["status"] == "REVOKED"
    assert rev_res["revocation_latency_us"] >= 0.0

    # 4. Immediate continuous Zero-Trust rejection
    post_revoke_handler = DummyPortalHandler(method="GET", path=f"/api/client/project-details?token={token}")
    post_revoke_handler.do_GET()
    assert post_revoke_handler.response_status == 401


def test_portal_webauthn_passkey_flow():
    # Generate options
    opt_handler = DummyPortalHandler(method="POST", path="/api/auth/webauthn/generate-options", body={
        "user_id": "user_super_alice",
        "tenant_id": "tenant_acme_fintech",
        "type": "authentication"
    })
    opt_handler.do_POST()
    assert opt_handler.response_status == 200
    opts = opt_handler.get_json_response()["options"]
    assert "challenge" in opts

    # Verify passkey
    ver_handler = DummyPortalHandler(method="POST", path="/api/auth/webauthn/verify", body={
        "challenge": opts["challenge"],
        "credential_id": "cred_fido2_apple_touchid_99",
        "counter": 15
    })
    ver_handler.do_POST()
    assert ver_handler.response_status == 200
    ver_res = ver_handler.get_json_response()
    assert ver_res["status"] == "AUTHENTICATED"
    assert ver_res["client"]["auth_factor"] == "FIDO2_WEBAUTHN_PASSKEY"


def test_portal_four_eyes_workflow():
    # 1. Propose action
    prop_handler = DummyPortalHandler(method="POST", path="/api/security/four-eyes/propose", body={
        "tenant_id": "tenant_acme_fintech",
        "action_type": "SURGICAL_ROLLBACK",
        "target_resource": "mod_auth",
        "initiator_id": "user_super_alice",
        "signature": "sig_ed25519_init_1a2b3c"
    })
    prop_handler.do_POST()
    assert prop_handler.response_status == 200
    act_id = prop_handler.get_json_response()["action_id"]

    # 2. Approve action
    appr_handler = DummyPortalHandler(method="POST", path="/api/security/four-eyes/approve", body={
        "action_id": act_id,
        "approver_id": "user_compliance_bob",
        "signature": "sig_ed25519_appr_4d5e6f"
    })
    appr_handler.do_POST()
    assert appr_handler.response_status == 200
    appr_res = appr_handler.get_json_response()
    assert appr_res["status"] == "APPROVED"
    assert appr_res["action_status"] == "MERKLE_SEALED"
    assert len(appr_res["merkle_leaf_hash"]) == 64


# =========================================================================
# 9. Schema Contracts Compatibility
# =========================================================================

def test_security_contracts_exist_and_valid():
    contracts_dir = REPO_ROOT / ".nb" / "context" / "contracts"
    expected = [
        "security_tenant_profile_contract.json",
        "security_rebac_policy_contract.json",
        "security_mfa_challenge_contract.json",
        "security_pii_vault_contract.json",
        "security_four_eyes_contract.json",
    ]
    for c_name in expected:
        c_path = contracts_dir / c_name
        assert c_path.exists(), f"Contract missing: {c_name}"
        data = json.loads(c_path.read_text(encoding="utf-8"))
        assert "$schema" in data
        assert "title" in data
        assert "properties" in data
