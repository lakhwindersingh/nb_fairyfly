"""
Unit and Integration Test Suite for SaaS Portal Commercial Packager, Multi-Tier Provisioner & Entitlement Engine (CAP-42)
Tests:
- GET /api/commercial/tiers (all 4 tier specifications and feature entitlements)
- GET /api/commercial/entitlements (tenant quota audits)
- GET /api/commercial/packages (bundled distribution packages)
- POST /api/commercial/package (on-demand commercial packaging & Merkle sealing)
- POST /api/commercial/provision (multi-target IDE and SaaS runtime provisioning)
- POST /api/commercial/verify-permission (zero-trust RBAC permission evaluation)
- HTML UI rendering for Commercial Provisioner console tab and navigation
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
from portal.server import PortalRequestHandler


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


def test_commercial_tiers_endpoint(portal_server):
    """Verifies GET /api/commercial/tiers returns all 4 commercial tier specifications."""
    conn = HTTPConnection(portal_server)
    conn.request("GET", "/api/commercial/tiers")
    res = conn.getresponse()
    assert res.status == 200
    data = json.loads(res.read().decode("utf-8"))
    assert data["status"] == "SUCCESS"
    assert "tiers" in data
    tiers = data["tiers"]
    assert "plan_free" in tiers
    assert "plan_team" in tiers
    assert "plan_business" in tiers
    assert "plan_enterprise" in tiers

    # Check Free Community Tier
    free = tiers["plan_free"]
    assert free["base_price_monthly_usd"] == 0
    assert free["included_seats"] == 1
    assert free["rules"]["allow_worm_egress"] is False
    assert free["rules"]["allow_nbpack_compilation"] is False

    # Check Enterprise Dedicated Tier
    ent = tiers["plan_enterprise"]
    assert ent["base_price_monthly_usd"] == 9999
    assert ent["included_seats"] == -1
    assert ent["rules"]["allow_worm_egress"] is True
    assert ent["rules"]["allow_nbpack_compilation"] is True


def test_commercial_entitlements_endpoint(portal_server):
    """Verifies GET /api/commercial/entitlements audits tenant billing quotas."""
    conn = HTTPConnection(portal_server)
    conn.request("GET", "/api/commercial/entitlements?tenant_id=tenant_acme_fintech")
    res = conn.getresponse()
    assert res.status == 200
    data = json.loads(res.read().decode("utf-8"))
    assert data["status"] == "SUCCESS"
    assert "entitlements" in data
    ent = data["entitlements"]
    assert ent["tenant_id"] == "tenant_acme_fintech"
    assert ent["tier"] == "plan_enterprise"
    assert ent["included_seats"] == -1
    assert ent["included_concurrent_worktrees"] == -1


def test_commercial_packages_endpoint(portal_server):
    """Verifies GET /api/commercial/packages lists compiled packages and bundles."""
    conn = HTTPConnection(portal_server)
    conn.request("GET", "/api/commercial/packages")
    res = conn.getresponse()
    assert res.status == 200
    data = json.loads(res.read().decode("utf-8"))
    assert data["status"] == "SUCCESS"
    assert "packages" in data
    assert isinstance(data["packages"], list)


def test_commercial_package_on_demand_endpoint(portal_server, tmp_path):
    """Verifies POST /api/commercial/package assembles and seals a tier bundle."""
    conn = HTTPConnection(portal_server)
    payload = json.dumps({
        "tier": "plan_team",
        "tenant_id": "tenant_test_pod",
        "output_dir": str(tmp_path / "test_pkg_team")
    })
    conn.request("POST", "/api/commercial/package", body=payload, headers={"Content-Type": "application/json"})
    res = conn.getresponse()
    assert res.status == 200
    data = json.loads(res.read().decode("utf-8"))
    assert data["status"] == "SUCCESS"
    pkg = data["package_result"]
    assert pkg["tier"] == "plan_team"
    assert pkg["bundled_files_count"] > 0
    assert "merkle_root" in pkg
    assert "license_id" in pkg
    assert Path(pkg["output_directory"]).exists()


def test_commercial_provision_endpoint(portal_server):
    """Verifies POST /api/commercial/provision mints cryptographic license and provisions targets."""
    conn = HTTPConnection(portal_server)
    payload = json.dumps({
        "tenant_id": "tenant_acme_fintech",
        "tier": "plan_enterprise",
        "target": "saas_portal_gateway"
    })
    conn.request("POST", "/api/commercial/provision", body=payload, headers={"Content-Type": "application/json"})
    res = conn.getresponse()
    assert res.status == 200
    data = json.loads(res.read().decode("utf-8"))
    assert data["status"] == "SUCCESS"
    prov = data["provision_result"]
    assert prov["tenant_id"] == "tenant_acme_fintech"
    assert prov["tier"] == "plan_enterprise"
    assert "license_token" in prov
    assert "saas_portal_gateway" in prov["targets"]


def test_commercial_verify_permission_endpoint(portal_server):
    """Verifies POST /api/commercial/verify-permission evaluates zero-trust RBAC policies."""
    conn = HTTPConnection(portal_server)

    # 1. Enterprise tenant requesting WORM egress -> PERMITTED
    payload_ent = json.dumps({
        "tenant_id": "tenant_acme_fintech",
        "action": "allow_worm_egress"
    })
    conn.request("POST", "/api/commercial/verify-permission", body=payload_ent, headers={"Content-Type": "application/json"})
    res_ent = conn.getresponse()
    assert res_ent.status == 200
    data_ent = json.loads(res_ent.read().decode("utf-8"))
    assert data_ent["verification"]["permitted"] is True

    # 2. Community tenant requesting WORM egress -> DENIED
    payload_comm = json.dumps({
        "tenant_id": "tenant_community_default",
        "action": "allow_worm_egress"
    })
    conn.request("POST", "/api/commercial/verify-permission", body=payload_comm, headers={"Content-Type": "application/json"})
    res_comm = conn.getresponse()
    assert res_comm.status == 200
    data_comm = json.loads(res_comm.read().decode("utf-8"))
    assert data_comm["verification"]["permitted"] is False


def test_portal_html_contains_commercial_provisioner_ui(portal_server):
    """Verifies GET / returns HTML containing the Commercial Package Provisioner console tab."""
    conn = HTTPConnection(portal_server)
    conn.request("GET", "/")
    res = conn.getresponse()
    assert res.status == 200
    html = res.read().decode("utf-8")
    assert "commercialNavBtn" in html
    assert "Commercial Provisioner" in html
    assert 'id="commercial-provisioner"' in html
    assert "packageCommercialTier" in html
    assert "provisionCommercialTarget" in html
    assert "verifyCommercialPermission" in html
