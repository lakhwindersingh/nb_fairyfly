"""
Test suite for Section 21.2: Distributed Multi-Container Swarm Fleet & Transport (DEWS)
Governed by workplace/docs/proposals/rfc_containerized_worktree_swarms.md (CAP-48 to CAP-52).

Validates:
- TODO-DEWS-04: Enterprise Swarm Fleet Dispatch API & Endpoints
- TODO-DEWS-05: Distributed Worktree Coordinator with Live Redis 7.x Redlock
- TODO-DEWS-06: Topological Consolidation & 3-Way Merge Agent Plugin
- TODO-DEWS-07: Percipience CLI Remote Dispatch Subcommand
- TODO-DEWS-08: Portal Fleet Telemetry & Swarm Dashboard Tab
"""

import os
import sys
import json
import time
import uuid
import shutil
import tempfile
import threading
import subprocess
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
for p in [REPO_ROOT, REPO_ROOT / ".nb", REPO_ROOT / ".nb" / "core", REPO_ROOT / "workplace", REPO_ROOT / "workplace" / "core"]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.worktree_engine import RedisRedlockBackend, WorktreeEngine
from core.swarm_fleet_dispatcher import SwarmFleetDispatcher, WorkerSlot, SwarmJobRecord
from core.consolidation_synthesizer import ConsolidationSynthesizer, ConsolidationReceipt
from core.git_bundle_transport import GitBundleTransport


class TestRedisRedlockCoordinator:
    """Validates TODO-DEWS-05: RedisRedlockBackend distributed synchronization."""

    def test_redlock_acquire_and_release(self):
        backend = RedisRedlockBackend()
        res_name = f"test_resource_{uuid.uuid4().hex[:6]}"
        token = backend.acquire_lock(res_name, ttl_ms=5000)
        assert token is not None
        assert token.startswith(f"redlock_{res_name}")

        # Mutual exclusion: second acquisition fails
        token2 = backend.acquire_lock(res_name, ttl_ms=5000)
        assert token2 is None

        # Introspection
        leases = backend.get_active_leases()
        res_leases = [l for l in leases if l["resource_key"] == res_name]
        assert len(res_leases) == 1
        assert res_leases[0]["remaining_ttl_ms"] > 0

        # Release with correct token
        released = backend.release_lock(res_name, token)
        assert released is True

        # Now available again
        token3 = backend.acquire_lock(res_name, ttl_ms=5000)
        assert token3 is not None
        backend.release_lock(res_name, token3)

    def test_redlock_lease_renewal_heartbeat(self):
        backend = RedisRedlockBackend()
        res_name = f"test_renew_{uuid.uuid4().hex[:6]}"
        token = backend.acquire_lock(res_name, ttl_ms=2000)
        assert token is not None

        # Heartbeat renewal
        renewed = backend.renew_lease(res_name, token, ttl_ms=4000)
        assert renewed is True

        # Renewal with invalid token fails
        invalid_renew = backend.renew_lease(res_name, "bogus_token", ttl_ms=4000)
        assert invalid_renew is False

        backend.release_lock(res_name, token)

    def test_redlock_ttl_auto_eviction(self):
        backend = RedisRedlockBackend()
        res_name = f"test_ttl_{uuid.uuid4().hex[:6]}"
        token = backend.acquire_lock(res_name, ttl_ms=50) # 50ms TTL
        assert token is not None

        time.sleep(0.08) # Wait for TTL expiry
        backend.purge_expired_leases()

        # Should be evictable / re-acquirable
        token_after = backend.acquire_lock(res_name, ttl_ms=1000)
        assert token_after is not None
        backend.release_lock(res_name, token_after)


class TestSwarmFleetDispatcher:
    """Validates TODO-DEWS-04: SwarmFleetDispatcher slot management and job execution."""

    def test_worker_slots_initialization(self):
        dispatcher = SwarmFleetDispatcher(REPO_ROOT)
        status = dispatcher.get_fleet_status()
        assert status["status"] == "HEALTHY"
        assert status["worker_slots_total"] == 5
        assert status["worker_slots_idle"] >= 0
        assert "worker_slots" in status
        assert len(status["worker_slots"]) == 5

    def test_job_dispatch_lifecycle_mock_mode(self):
        dispatcher = SwarmFleetDispatcher(REPO_ROOT)
        plan_file = REPO_ROOT / ".nb" / "plan" / "test" / "concise.md"

        job_data = dispatcher.dispatch_job(
            plan_path=str(plan_file),
            agent_id="agent_unit_worker",
            target_module="workplace/core",
            prompt="Unit test dispatch",
            mock_mode=True
        )

        assert job_data["status"] == "SUCCESS"
        assert job_data["job_id"].startswith("job_dews_")
        assert job_data["worker_slot_id"] is not None
        assert job_data["result_bundle_path"] is not None
        assert job_data["result_bundle_sha256"] is not None
        assert job_data["exit_code"] == 0

        # Verify persisted in job store
        fetched = dispatcher.get_job_status(job_data["job_id"])
        assert fetched is not None
        assert fetched["job_id"] == job_data["job_id"]

        # Verify result bundle readable
        bundle_tuple = dispatcher.get_job_bundle(job_data["job_id"])
        assert bundle_tuple is not None
        filename, bundle_bytes = bundle_tuple
        assert filename.endswith(".bundle")
        assert len(bundle_bytes) > 0

    def test_fleet_status_telemetry(self):
        dispatcher = SwarmFleetDispatcher(REPO_ROOT)
        status = dispatcher.get_fleet_status()
        assert status["status"] == "HEALTHY"
        assert "jobs_summary" in status
        assert "finops_rollup" in status
        assert status["finops_rollup"]["total_tokens_burned"] >= 0


class TestConsolidationSynthesizer:
    """Validates TODO-DEWS-06: Topological Consolidation & 3-Way Merge Agent Plugin."""

    def test_consolidation_agent_manifest_exists(self):
        manifest_path = REPO_ROOT / ".nb" / "agentic" / "custom" / "agents" / "agent_consolidation_synthesizer.yaml"
        assert manifest_path.exists(), "Consolidation Synthesizer agent manifest missing"
        text = manifest_path.read_text(encoding="utf-8")
        assert "agent_consolidation_synthesizer" in text
        assert "Consolidation & 3-Way Merge" in text

    def test_consolidation_mock_merge_cycle(self):
        synthesizer = ConsolidationSynthesizer(REPO_ROOT)
        receipt = synthesizer.consolidate_branches(
            branches=["worker/slot_01_billing", "worker/slot_02_portal"],
            target_integration_branch="integration/test_wave"
        )

        assert receipt.status == "SUCCESS"
        assert receipt.consolidated_branch == "integration/test_wave"
        assert len(receipt.merged_branches) == 2
        assert receipt.merkle_block_id is not None
        assert receipt.merkle_block_id is not None
        assert receipt.consolidated_bundle_path is not None


class TestPercipienceCLICommand:
    """Validates TODO-DEWS-07: Percipience CLI Remote Dispatch Subcommand."""

    def test_cli_swarm_dispatch_local_mock(self):
        res = subprocess.run([
            str(REPO_ROOT / ".nb" / "bin" / "percipience"),
            "swarm", "dispatch",
            "--remote", "local",
            "--plan", ".nb/plan/test/concise.md",
            "--target-module", "workplace",
            "--agent-id", "agent_cli_test",
            "--mock"
        ], capture_output=True, text=True, cwd=str(REPO_ROOT))

        assert res.returncode == 0
        assert "Initializing Distributed Swarm Fleet (DEWS) Remote Dispatch" in res.stdout
        assert "Remote Swarm Execution Succeeded" in res.stdout
        assert "Allocated Slot:" in res.stdout
        assert "Bundle SHA256:" in res.stdout

    def test_cli_swarm_dispatch_sync_back(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "dest_repo"
            dest.mkdir()
            subprocess.run(["git", "init"], cwd=dest, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Tester"], cwd=dest, check=True)
            subprocess.run(["git", "config", "user.email", "tester@test.com"], cwd=dest, check=True)
            (dest / "base.txt").write_text("Base initial content")
            subprocess.run(["git", "add", "."], cwd=dest, check=True)
            subprocess.run(["git", "commit", "-m", "Init"], cwd=dest, check=True)

            res = subprocess.run([
                str(REPO_ROOT / ".nb" / "bin" / "percipience"),
                "swarm", "dispatch",
                "--remote", "local",
                "--plan", ".nb/plan/test/concise.md",
                "--target-module", "workplace",
                "--agent-id", "agent_sync_worker",
                "--mock",
                "--sync-back", str(dest)
            ], capture_output=True, text=True, cwd=str(REPO_ROOT))

            assert res.returncode == 0
            assert "Extracting result bundle into sync-back destination:" in res.stdout
            assert "Sync-back verified: Branch" in res.stdout


class TestPortalServerEndpointsAndUI:
    """Validates TODO-DEWS-04 & TODO-DEWS-08: Portal server REST API and Dashboard Tab."""

    @pytest.fixture(scope="class")
    def portal_server(self):
        from workplace.portal.server import PortalRequestHandler
        server = ThreadingHTTPServer(("127.0.0.1", 9005), PortalRequestHandler)
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        time.sleep(0.5)
        yield "http://127.0.0.1:9005"
        server.shutdown()
        server.server_close()

    def test_api_swarm_fleet_status(self, portal_server):
        with urllib.request.urlopen(f"{portal_server}/api/swarm/fleet/status") as res:
            assert res.status == 200
            data = json.loads(res.read().decode())
            assert data["status"] == "HEALTHY"
            assert data["worker_slots_total"] == 5
            assert "worker_slots" in data
            assert len(data["worker_slots"]) == 5

    def test_api_swarm_fleet_dispatch_and_bundle_download(self, portal_server):
        payload = json.dumps({
            "plan_path": ".nb/plan/test/concise.md",
            "target_module": "workplace",
            "agent_id": "agent_api_runner",
            "mock": True
        }).encode()
        req = urllib.request.Request(
            f"{portal_server}/api/swarm/fleet/dispatch",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as res:
            assert res.status == 200
            data = json.loads(res.read().decode())
            assert data["status"] == "DISPATCHED"
            job_id = data["job_id"]
            assert job_id is not None

        # Query job status
        with urllib.request.urlopen(f"{portal_server}/api/swarm/fleet/jobs/{job_id}", timeout=10) as res:
            assert res.status == 200
            jdata = json.loads(res.read().decode())
            assert jdata["status"] == "SUCCESS"
            assert jdata["job"]["job_id"] == job_id

        # Download result bundle
        with urllib.request.urlopen(f"{portal_server}/api/swarm/fleet/jobs/{job_id}/bundle", timeout=10) as res:
            assert res.status == 200
            bundle_bytes = res.read()
            assert len(bundle_bytes) > 0
            assert res.headers.get("Content-Type") == "application/octet-stream"

    def test_api_swarm_fleet_consolidate(self, portal_server):
        payload = json.dumps({
            "branches": ["worker/slot_01", "worker/slot_02"],
            "target_branch": "integration/portal_wave"
        }).encode()
        req = urllib.request.Request(
            f"{portal_server}/api/swarm/fleet/consolidate",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as res:
            assert res.status == 200
            cdata = json.loads(res.read().decode())
            assert cdata["status"] == "SUCCESS"
            assert cdata["result"]["consolidated_branch"] == "integration/portal_wave"

    def test_portal_html_dashboard_tab_rendering(self, portal_server):
        with urllib.request.urlopen(f"{portal_server}/", timeout=10) as res:
            assert res.status == 200
            html = res.read().decode()
            # Verify nav button and tab section
            assert 'id="swarm-fleet"' in html
            assert "showTab('swarm-fleet')" in html
            assert "Distributed Multi-Container Swarm Fleet" in html
            assert "Multi-Container Worker Slots (DEWS Fleet)" in html
            assert "Live Redis 7.x Redlock Leases" in html
            assert "loadSwarmFleetTelemetry" in html
