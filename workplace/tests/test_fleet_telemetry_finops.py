"""
Test suite for Workstation & Node Fleet Telemetry (Section 18.3)
and Consolidated Fleet Monitoring & FinOps Dashboard (Section 18.4).

Validates:
- FleetAgentDaemon machine identity, worktree introspection, task tracking, and FinOps savings.
- FleetManager registration, heartbeat, telemetry ingestion, liveness evaluation, and persistence.
- FinOps rollup calculation: $ gross, 15% Percipience fee, 85% customer net, and leaderboards.
- Consolidated task progress tracking across fleet nodes.
"""

import json
import os
import shutil
import tempfile
import time
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock

from workplace.core.fleet_agent import (
    FleetAgentDaemon,
    MachineIdentity,
    WorkspaceTelemetry,
    TaskProgress,
    TokenFinOps,
    NodeTelemetry,
    HeartbeatPayload
)
from workplace.core.fleet_manager import FleetManager


class TestFleetAgentDaemon(unittest.TestCase):
    """Unit tests for background FleetAgentDaemon (TODO-PRT-06)."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.workspace_path = (Path(self.test_dir) / "test_workspace").resolve()
        self.workspace_path.mkdir(parents=True)
        # Initialize a git repo in test workspace
        os.system(f"git -C {self.workspace_path} init -q")
        os.system(f"git -C {self.workspace_path} config user.email 'test@percipience.internal'")
        os.system(f"git -C {self.workspace_path} config user.name 'Test Runner'")
        (self.workspace_path / "README.md").write_text("# Test Workspace\n", encoding="utf-8")
        os.system(f"git -C {self.workspace_path} add README.md && git -C {self.workspace_path} commit -q -m 'Initial commit'")

        self.agent = FleetAgentDaemon(
            workspace_root=self.workspace_path,
            org_id="tenant_omega",
            project_id="proj_alpha",
            machine_id="test_node_001"
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_collect_machine_identity(self):
        identity = self.agent.get_machine_identity()
        self.assertIsInstance(identity, MachineIdentity)
        self.assertEqual(identity.machine_id, "test_node_001")
        self.assertTrue(len(identity.hostname) > 0)
        self.assertTrue(len(identity.os_name) > 0)
        self.assertEqual(identity.agent_version, "1.0.0")

    def test_collect_workspace_telemetry(self):
        telemetry = self.agent.get_workspace_telemetry()
        self.assertIsInstance(telemetry, WorkspaceTelemetry)
        self.assertEqual(telemetry.workspace_path, str(self.workspace_path))
        self.assertEqual(telemetry.git_branch, "main" if telemetry.git_branch == "main" else telemetry.git_branch)
        self.assertFalse(telemetry.uncommitted_changes)

        # Make worktree dirty
        (self.workspace_path / "dirty.txt").write_text("modified", encoding="utf-8")
        telemetry_dirty = self.agent.get_workspace_telemetry()
        self.assertTrue(telemetry_dirty.uncommitted_changes)

    def test_task_lifecycle_tracking(self):
        task = self.agent.update_task_progress(
            task_id="task_001",
            task_name="Build Auth Module",
            progress_pct=25.0,
            step_status="Compiling AST",
            eta_seconds=45
        )
        self.assertEqual(task.task_id, "task_001")
        self.assertEqual(task.progress_pct, 25.0)
        self.assertEqual(task.step_status, "Compiling AST")
        self.assertEqual(self.agent.current_task.task_id, "task_001")

        # Advance progress
        updated = self.agent.update_task_progress(
            task_id="task_001",
            task_name="Build Auth Module",
            progress_pct=85.0,
            step_status="Running Unit Tests",
            eta_seconds=10
        )
        self.assertEqual(updated.progress_pct, 85.0)
        self.assertEqual(updated.started_at, task.started_at)  # started_at preserved

    def test_finops_token_savings_accounting(self):
        finops = self.agent.get_token_finops()
        self.assertIsInstance(finops, TokenFinOps)
        self.assertGreater(finops.tokens_saved, 0)
        self.assertGreater(finops.gross_savings_usd, 0.0)

        # Revenue share validation: 15% fee, 85% customer net
        expected_fee = round(finops.gross_savings_usd * 0.15, 4)
        expected_net = round(finops.gross_savings_usd * 0.85, 4)
        self.assertAlmostEqual(finops.fee_usd, expected_fee, places=3)
        self.assertAlmostEqual(finops.net_savings_usd, expected_net, places=3)
        self.assertAlmostEqual(finops.fee_usd + finops.net_savings_usd, finops.gross_savings_usd, places=3)

    def test_collect_telemetry_and_heartbeat(self):
        hb = self.agent.collect_heartbeat(health_status="HEALTHY")
        self.assertIsInstance(hb, HeartbeatPayload)
        self.assertEqual(hb.machine_id, "test_node_001")
        self.assertEqual(hb.health_status, "HEALTHY")
        self.assertEqual(hb.org_id, "tenant_omega")
        self.assertEqual(hb.project_id, "proj_alpha")

        node_telem = self.agent.collect_telemetry(health_status="HEALTHY")
        self.assertIsInstance(node_telem, NodeTelemetry)
        self.assertEqual(node_telem.machine.machine_id, "test_node_001")
        self.assertEqual(node_telem.workspace.workspace_path, str(self.workspace_path))

    @patch("urllib.request.urlopen")
    def test_transmit_heartbeat_and_telemetry(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        self.assertTrue(self.agent.transmit_heartbeat("http://127.0.0.1:3000", auth_token="tok_123"))
        self.assertTrue(self.agent.transmit_telemetry("http://127.0.0.1:3000", auth_token="tok_123"))
        self.assertEqual(mock_urlopen.call_count, 2)


class TestFleetManager(unittest.TestCase):
    """Unit tests for FleetManager & Consolidated Monitoring (TODO-PRT-07, 08, 09, 10)."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.storage_file = Path(self.test_dir) / "fleet_registry.json"
        self.manager = FleetManager(storage_path=self.storage_file)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_ingest_heartbeat_and_list_machines(self):
        heartbeat = {
            "machine_id": "mac_node_01",
            "hostname": "macbook-pro.local",
            "health_status": "HEALTHY",
            "org_id": "tenant_enterprise",
            "project_id": "proj_market_pulse",
            "active_task": "Running Fuzzer",
            "progress_pct": 65.0,
            "tokens_saved": 500000
        }
        res = self.manager.ingest_heartbeat(heartbeat)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["machine_id"], "mac_node_01")

        machines = self.manager.list_machines(project_id="proj_market_pulse")
        self.assertEqual(len(machines), 1)
        self.assertEqual(machines[0]["machine_id"], "mac_node_01")
        self.assertEqual(machines[0]["health_status"], "HEALTHY")
        self.assertEqual(machines[0]["finops"]["tokens_saved"], 500000)
        # Gross = (500000 / 1000) * 0.003 = $1.50
        self.assertAlmostEqual(machines[0]["finops"]["gross_savings_usd"], 1.50, places=2)
        # Fee = 15% of 1.50 = 0.225
        self.assertAlmostEqual(machines[0]["finops"]["fee_usd"], 0.225, places=3)
        # Net = 85% of 1.50 = 1.275
        self.assertAlmostEqual(machines[0]["finops"]["net_savings_usd"], 1.275, places=3)

    def test_evaluate_liveness_timeout(self):
        heartbeat = {
            "machine_id": "mac_node_timeout",
            "hostname": "workstation-old",
            "org_id": "tenant_1",
            "project_id": "proj_1"
        }
        self.manager.ingest_heartbeat(heartbeat)
        self.assertEqual(self.manager.machines["mac_node_timeout"]["health_status"], "HEALTHY")

        # Manually backdate the last_seen_utc timestamp by 120 seconds to simulate inactivity
        past_time = (datetime.now(timezone.utc) - timedelta(seconds=120)).isoformat()
        self.manager.machines["mac_node_timeout"]["last_seen_utc"] = past_time
        self.manager.evaluate_liveness()
        self.assertEqual(self.manager.machines["mac_node_timeout"]["health_status"], "OFFLINE")

    def test_finops_rollup_and_leaderboards(self):
        # Clear seeded defaults to test exact numbers
        self.manager.machines.clear()

        # Register Node 1: $10.00 gross savings (3,333,333 tokens)
        self.manager.ingest_telemetry({
            "machine": {
                "machine_id": "node_heavy",
                "hostname": "build-box-01",
                "os_name": "Linux",
                "os_version": "Debian 12",
                "user_id": "agent_ci"
            },
            "workspace": {
                "workspace_path": "/workspace/analytics",
                "active_worktree": "primary",
                "git_branch": "main",
                "git_commit": "aabbcc112233",
                "uncommitted_changes": False
            },
            "task": {
                "task_id": "t_01",
                "task_name": "ETL Ingestion",
                "progress_pct": 80.0,
                "step_status": "Batch Processing",
                "started_at": datetime.now(timezone.utc).isoformat(),
                "eta_seconds": 60,
                "is_stuck": False
            },
            "finops": {
                "input_tokens": 1000000,
                "output_tokens": 500000,
                "tokens_saved": 3333333,
                "gross_savings_usd": 10.00,
                "fee_usd": 1.50,
                "net_savings_usd": 8.50
            },
            "health_status": "HEALTHY",
            "org_id": "enterprise_corp",
            "project_id": "proj_analytics"
        })

        # Register Node 2: $2.00 gross savings (666,667 tokens)
        self.manager.ingest_telemetry({
            "machine": {
                "machine_id": "node_light",
                "hostname": "laptop-02",
                "os_name": "macOS",
                "os_version": "Darwin 24.1",
                "user_id": "developer_bob"
            },
            "workspace": {
                "workspace_path": "/Users/bob/frontend",
                "active_worktree": "wt_frontend",
                "git_branch": "feature/ui",
                "git_commit": "ccddeeff4455",
                "uncommitted_changes": True
            },
            "task": {
                "task_id": "t_02",
                "task_name": "React Build",
                "progress_pct": 40.0,
                "step_status": "Bundling Webpack",
                "started_at": datetime.now(timezone.utc).isoformat(),
                "eta_seconds": 30,
                "is_stuck": False
            },
            "finops": {
                "input_tokens": 200000,
                "output_tokens": 100000,
                "tokens_saved": 666667,
                "gross_savings_usd": 2.00,
                "fee_usd": 0.30,
                "net_savings_usd": 1.70
            },
            "health_status": "HEALTHY",
            "org_id": "enterprise_corp",
            "project_id": "proj_frontend"
        })

        rollup = self.manager.get_finops_rollup()
        summary = rollup["summary"]
        self.assertEqual(summary["total_machines_count"], 2)
        self.assertEqual(summary["active_machines_count"], 2)
        self.assertEqual(summary["total_tokens_saved"], 4000000)
        self.assertAlmostEqual(summary["enterprise_gross_savings_usd"], 12.00, places=2)
        # 15% Percipience Rev-Share fee: $1.80
        self.assertAlmostEqual(summary["percipience_rev_share_fee_usd"], 1.80, places=2)
        # 85% Customer Net: $10.20
        self.assertAlmostEqual(summary["customer_net_retained_usd"], 10.20, places=2)

        # Leaderboard checks
        self.assertEqual(len(rollup["machine_leaderboard"]), 2)
        self.assertEqual(rollup["machine_leaderboard"][0]["machine_id"], "node_heavy")
        self.assertEqual(rollup["machine_leaderboard"][0]["gross_savings_usd"], 10.00)

        self.assertEqual(len(rollup["project_leaderboard"]), 2)
        self.assertEqual(rollup["project_leaderboard"][0]["project_id"], "proj_analytics")
        self.assertEqual(rollup["project_leaderboard"][0]["gross_savings_usd"], 10.00)

        # Active tasks
        tasks = self.manager.get_active_tasks()
        self.assertEqual(len(tasks), 2)
        task_ids = {t["task_id"] for t in tasks}
        self.assertIn("t_01", task_ids)
        self.assertIn("t_02", task_ids)

    def test_persistence_across_instances(self):
        self.manager.ingest_heartbeat({
            "machine_id": "node_persist_1",
            "hostname": "node-persisted",
            "tokens_saved": 1500000
        })

        # Load from same file with new instance
        new_manager = FleetManager(storage_path=self.storage_file)
        machines = new_manager.list_machines()
        node = next((m for m in machines if m["machine_id"] == "node_persist_1"), None)
        self.assertIsNotNone(node)
        self.assertEqual(node["hostname"], "node-persisted")
        self.assertEqual(node["finops"]["tokens_saved"], 1500000)

    def test_simulate_pulse_and_reset(self):
        res = self.manager.simulate_pulse(delta_tokens=50000, advance_task=True)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["action"], "SIMULATION_PULSE")
        machine = res["machine"]
        self.assertGreater(machine["finops"]["tokens_saved"], 0)
        self.assertEqual(machine["health_status"], "HEALTHY")

        reset_res = self.manager.reset_fleet()
        self.assertEqual(reset_res["status"], "SUCCESS")
        self.assertEqual(reset_res["action"], "RESET_BASELINE")
        self.assertGreater(reset_res["machines_count"], 0)




class TestRemoteAdminInterventions(unittest.TestCase):
    """
    Unit tests for Remote Machine Interventions & Governance Actions (TODO-PRT-11 / CAP-44).
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.storage_file = Path(self.temp_dir) / "fleet_registry.json"
        self.manager = FleetManager(storage_path=self.storage_file, workspace_root=Path(self.temp_dir))

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_emergency_pause_and_resume(self):
        # 1. Pause machine
        res_pause = self.manager.execute_remote_action(
            machine_id="node_mac_lakhwinder",
            action="pause",
            actor="lead_architect@enterprise.corp"
        )
        self.assertEqual(res_pause["status"], "SUCCESS")
        inv = res_pause["intervention"]
        self.assertEqual(inv["action"], "pause")
        self.assertEqual(inv["actor"], "lead_architect@enterprise.corp")
        self.assertEqual(res_pause["machine"]["health_status"], "PAUSED")
        self.assertTrue(res_pause["machine"]["active_task"]["is_paused"])
        self.assertEqual(res_pause["machine"]["active_task"]["step_status"], "PAUSED_BY_ADMIN")

        # 2. Resume machine
        res_resume = self.manager.execute_remote_action(
            machine_id="node_mac_lakhwinder",
            action="resume",
            actor="lead_architect@enterprise.corp"
        )
        self.assertEqual(res_resume["status"], "SUCCESS")
        self.assertEqual(res_resume["machine"]["health_status"], "HEALTHY")
        self.assertFalse(res_resume["machine"]["active_task"]["is_paused"])
        self.assertEqual(res_resume["machine"]["active_task"]["step_status"], "RESUMED_ACTIVE")

    def test_surgical_rollback_remote(self):
        res = self.manager.execute_remote_action(
            machine_id="node_mac_lakhwinder",
            action="surgical_rollback",
            params={"module_id": "mod_portal_marketing", "recovery_point": "RP_TEST_CHECKPOINT_042"},
            actor="secops@enterprise.corp"
        )
        self.assertEqual(res["status"], "SUCCESS")
        m = res["machine"]
        self.assertEqual(m["active_task"]["step_status"], "ROLLED_BACK_TO_RP_TEST_CHECKPOINT_042")
        self.assertEqual(m["last_rollback"]["recovery_point"], "RP_TEST_CHECKPOINT_042")
        self.assertEqual(m["last_rollback"]["module_id"], "mod_portal_marketing")

    def test_force_worktree_lease_eviction(self):
        res = self.manager.execute_remote_action(
            machine_id="node_mac_lakhwinder",
            action="evict_lease",
            params={"worktree": "wt_orphaned_01"},
            actor="ops@enterprise.corp"
        )
        self.assertEqual(res["status"], "SUCCESS")
        m = res["machine"]
        self.assertEqual(m["active_worktree"], "")
        self.assertFalse(m["uncommitted_changes"])
        self.assertEqual(m["active_task"]["step_status"], "LEASE_EVICTED")

    def test_flush_ast_cache_remote(self):
        cache_dir = Path(self.temp_dir) / ".scratch" / "ast_cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        (cache_dir / "cache_file_1.json").write_text("{}", encoding="utf-8")
        (cache_dir / "cache_file_2.json").write_text("{}", encoding="utf-8")

        res = self.manager.execute_remote_action(
            machine_id="node_mac_lakhwinder",
            action="flush_ast_cache",
            actor="admin@enterprise.internal"
        )
        self.assertEqual(res["status"], "SUCCESS")
        self.assertIn("ast_cache_flushed_at", res["machine"])
        # Cached files should have been wiped
        self.assertEqual(len(list(cache_dir.glob("*"))), 0)

    def test_interventions_audit_and_polling(self):
        self.manager.execute_remote_action(machine_id="node_mac_lakhwinder", action="pause")
        self.manager.execute_remote_action(machine_id="node_mac_lakhwinder", action="resume")

        audit = self.manager.get_interventions_audit(machine_id="node_mac_lakhwinder")
        self.assertGreaterEqual(len(audit), 2)
        actions = [a["action"] for a in audit]
        self.assertIn("pause", actions)
        self.assertIn("resume", actions)

        # Polling commands by daemon
        cmds = self.manager.poll_commands("node_mac_lakhwinder")
        self.assertEqual(len(cmds), 2)
        self.assertEqual(cmds[0]["action"], "pause")
        self.assertEqual(cmds[1]["action"], "resume")

        # Second poll should be empty
        empty_cmds = self.manager.poll_commands("node_mac_lakhwinder")
        self.assertEqual(len(empty_cmds), 0)

    def test_invalid_machine_and_action_handling(self):
        with self.assertRaises(ValueError):
            self.manager.execute_remote_action(machine_id="non_existent_node", action="pause")

        with self.assertRaises(ValueError):
            self.manager.execute_remote_action(machine_id="node_mac_lakhwinder", action="unsupported_action")


class TestEnterpriseQuarantineCentralCommand(unittest.TestCase):
    """
    Unit tests for Enterprise Security & Quarantine Central Command (TODO-PRT-12 / CAP-44).
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.workspace_root = Path(self.temp_dir)
        self.storage_file = self.workspace_root / "fleet_registry.json"

        # Mock hitl directory structure
        hitl_dir = self.workspace_root / "user" / "hitl"
        hitl_dir.mkdir(parents=True, exist_ok=True)

        # Mock injection quarantine
        inj_file = hitl_dir / "injection_quarantine.jsonl"
        inj_file.write_text(
            json.dumps({
                "timestamp": 1791313521.0,
                "verdict": "BLOCKED",
                "risk_score": 0.95,
                "source": "external_untrusted",
                "violations": [{"category": "DIRECT_JAILBREAK", "severity": "CRITICAL"}],
                "raw_payload_preview": "Ignore all instructions"
            }) + "\n",
            encoding="utf-8"
        )

        # Mock poisoning quarantine
        poison_file = hitl_dir / "poisoning_quarantine.md"
        poison_file.write_text(
            "### Incident: `Q_INC_TEST_POISON` (2026-10-09T01:00:00+00:00)\n"
            "- **Target Module**: `mod_observability_usage`\n"
            "- **Status**: `QUARANTINED`\n"
            "- **Violations**:\n  - [SECRET_LEAK] Exposed KMS Key\n",
            encoding="utf-8"
        )

        # Mock proposed spec delta
        delta_file = hitl_dir / "proposed_spec_delta.md"
        delta_file.write_text(
            "# Proposed Specification Delta RFC: DELTA_TEST_01\n"
            "- **Delta ID:** `DELTA_TEST_01`\n"
            "- **Source Module:** `mod_portal_marketing`\n"
            "- **Title:** Add Custom Header\n"
            "- **Status:** `AWAITING_HITL_REVIEW`\n"
            "- **Created At:** `2026-10-09T02:00:00+00:00`\n",
            encoding="utf-8"
        )

        self.manager = FleetManager(storage_path=self.storage_file, workspace_root=self.workspace_root)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_get_quarantine_command_center_consolidation(self):
        qc = self.manager.get_quarantine_command_center()
        self.assertIn("incidents", qc)
        self.assertIn("stats", qc)

        stats = qc["stats"]
        self.assertGreaterEqual(stats["total"], 3)
        self.assertGreaterEqual(stats["quarantined"], 3)
        self.assertEqual(stats["resolved"], 0)

        categories = {inc["category"] for inc in qc["incidents"]}
        self.assertIn("PROMPT_INJECTION", categories)
        self.assertIn("CONTEXT_POISONING", categories)
        self.assertIn("DEPENDENCY_CVE", categories)
        self.assertIn("SEMANTIC_DRIFT", categories)

    def test_resolve_quarantine_incident_with_merkle_seal(self):
        res = self.manager.resolve_quarantine_incident(
            incident_id="Q_INC_TEST_POISON",
            resolution="SURGICALLY_ROLLED_BACK",
            resolution_notes="Reverted to clean snapshot RP_001",
            actor="ciso@enterprise.corp"
        )
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["resolution"], "SURGICALLY_ROLLED_BACK")
        self.assertIn("merkle_seal", res)
        seal = res["merkle_seal"]
        self.assertIn("block_id", seal)
        self.assertIn("merkle_root", seal)

        # Verify resolution persisted in quarantine_resolutions.jsonl
        res_file = self.workspace_root / "user" / "hitl" / "quarantine_resolutions.jsonl"
        self.assertTrue(res_file.exists())
        lines = res_file.read_text(encoding="utf-8").strip().splitlines()
        self.assertEqual(len(lines), 1)
        record = json.loads(lines[0])
        self.assertEqual(record["incident_id"], "Q_INC_TEST_POISON")
        self.assertEqual(record["resolution"], "SURGICALLY_ROLLED_BACK")

        # Now verify get_quarantine_command_center reflects the resolution
        qc_after = self.manager.get_quarantine_command_center()
        self.assertEqual(qc_after["stats"]["resolved"], 1)
        resolved_inc = next((i for i in qc_after["incidents"] if i["incident_id"] == "Q_INC_TEST_POISON"), None)
        self.assertIsNotNone(resolved_inc)
        self.assertEqual(resolved_inc["status"], "RESOLVED")
        self.assertEqual(resolved_inc["resolution"], "SURGICALLY_ROLLED_BACK")

    def test_invalid_resolution_fails(self):
        with self.assertRaises(ValueError):
            self.manager.resolve_quarantine_incident(
                incident_id="Q_INC_TEST_POISON",
                resolution="INVALID_RESOLUTION_MODE"
            )


class TestFleetDaemonRemoteExecution(unittest.TestCase):
    """
    Unit tests for daemon-side remote command handling in FleetAgentDaemon.
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.daemon = FleetAgentDaemon(workspace_root=Path(self.temp_dir))
        self.daemon.current_task = TaskProgress(
            task_id="t_active",
            task_name="Worker Derivation",
            progress_pct=50.0,
            step_status="ACTIVE_DERIVATION",
            started_at=datetime.now(timezone.utc).isoformat(),
            eta_seconds=30
        )

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_daemon_pause_and_resume_execution(self):
        # 1. Pause
        res_p = self.daemon.execute_remote_command({"action": "pause"})
        self.assertEqual(res_p["status"], "SUCCESS")
        self.assertEqual(self.daemon.current_task.step_status, "PAUSED_BY_ADMIN")

        # 2. Resume
        res_r = self.daemon.execute_remote_command({"action": "resume"})
        self.assertEqual(res_r["status"], "SUCCESS")
        self.assertEqual(self.daemon.current_task.step_status, "RESUMED_ACTIVE")

    def test_daemon_surgical_rollback_execution(self):
        res = self.daemon.execute_remote_command({
            "action": "surgical_rollback",
            "params": {"module_id": "mod_core", "recovery_point": "RP_SAFE_01"}
        })
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(self.daemon.current_task.step_status, "ROLLED_BACK_TO_RP_SAFE_01")

    def test_daemon_evict_lease_execution(self):
        res = self.daemon.execute_remote_command({
            "action": "evict_lease",
            "params": {"worktree": "wt_old"}
        })
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(self.daemon.current_task.step_status, "LEASE_EVICTED")

    def test_daemon_flush_ast_cache_execution(self):
        cache_dir = Path(self.temp_dir) / ".scratch" / "ast_cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        (cache_dir / "ast_sample.cache").write_text("DATA", encoding="utf-8")

        res = self.daemon.execute_remote_command({"action": "flush_ast_cache"})
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(len(list(cache_dir.glob("*"))), 0)



class TestFleetPortalRestAPI(unittest.TestCase):
    """
    Integration tests for Portal REST APIs for Remote Machine Interventions
    and Enterprise Quarantine Central Command (Section 18.5).
    """

    @classmethod
    def setUpClass(cls):
        from http.server import HTTPServer
        import threading
        from workplace.portal.server import PortalRequestHandler
        cls.server = HTTPServer(("127.0.0.1", 0), PortalRequestHandler)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def _http_request(self, method: str, path: str, payload: dict = None) -> tuple:
        from http.client import HTTPConnection
        conn = HTTPConnection("127.0.0.1", self.port, timeout=5)
        headers = {"Content-Type": "application/json"} if payload else {}
        body = json.dumps(payload) if payload else None
        conn.request(method, path, body=body, headers=headers)
        resp = conn.getresponse()
        data = resp.read().decode("utf-8")
        parsed = json.loads(data) if data else {}
        conn.close()
        return resp.status, parsed

    def test_api_fleet_action_post(self):
        # 1. Pause action
        status, body = self._http_request("POST", "/api/fleet/action", {
            "machine_id": "node_mac_lakhwinder",
            "action": "pause",
            "actor": "admin@enterprise.internal"
        })
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "SUCCESS")
        self.assertEqual(body["machine"]["health_status"], "PAUSED")

        # 2. Resume action
        status, body = self._http_request("POST", "/api/fleet/action", {
            "machine_id": "node_mac_lakhwinder",
            "action": "resume",
            "actor": "admin@enterprise.internal"
        })
        self.assertEqual(status, 200)
        self.assertEqual(body["machine"]["health_status"], "HEALTHY")

        # 3. Surgical rollback
        status, body = self._http_request("POST", "/api/fleet/action", {
            "machine_id": "node_mac_lakhwinder",
            "action": "surgical_rollback",
            "params": {"module_id": "workplace", "recovery_point": "RP_HTTP_TEST_01"}
        })
        self.assertEqual(status, 200)
        self.assertIn("RP_HTTP_TEST_01", body["machine"]["active_task"]["step_status"])

    def test_api_fleet_interventions_get(self):
        status, body = self._http_request("GET", "/api/fleet/interventions?limit=10")
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "SUCCESS")
        self.assertIn("interventions", body)
        self.assertGreaterEqual(body["count"], 1)

    def test_api_fleet_quarantine_get_and_resolve_post(self):
        # GET quarantine
        status, body = self._http_request("GET", "/api/fleet/quarantine")
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "SUCCESS")
        cc = body["command_center"]
        self.assertIn("incidents", cc)
        self.assertIn("stats", cc)

        # POST resolve
        status, body = self._http_request("POST", "/api/fleet/quarantine/resolve", {
            "incident_id": "CVE_BLOCK_cryptominer-lib_1.0.0",
            "resolution": "DISMISSED",
            "resolution_notes": "Blacklist confirmed and dependency purged",
            "actor": "secops@enterprise.corp"
        })
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "SUCCESS")
        self.assertIn("merkle_seal", body)
        self.assertEqual(body["resolution"], "DISMISSED")

    def test_api_fleet_commands_poll(self):
        # Action was triggered earlier, test polling commands
        status, body = self._http_request("GET", "/api/fleet/commands/poll?machine_id=node_mac_lakhwinder")
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "SUCCESS")
        self.assertIn("commands", body)

    def test_portal_html_script_syntax_and_showtab_hoisting(self):
        """Verify showTab is hoisted in <head> and all <script> blocks parse cleanly without SyntaxErrors."""
        import re, subprocess, shutil
        from workplace.portal.server import PORTAL_HTML

        # 1. Verify showTab and switchAdminView are hoisted in <head>
        head_part = PORTAL_HTML.split("</head>")[0]
        self.assertIn("function showTab(id)", head_part)
        self.assertIn("window.showTab = showTab", head_part)
        self.assertIn("function switchAdminView(viewId)", head_part)
        self.assertIn("window.switchAdminView = switchAdminView", head_part)

        # 2. Verify navigation button exists after <head>
        nav_idx = PORTAL_HTML.find("onclick=\"showTab('client')\"")
        head_idx = PORTAL_HTML.find("</head>")
        self.assertGreater(nav_idx, head_idx, "Client nav button must follow <head>")

        # 3. Validate JS syntax with node if node is available
        node_bin = shutil.which("node")
        if node_bin:
            scripts = re.findall(r'<script>(.*?)</script>', PORTAL_HTML, re.DOTALL)
            self.assertGreaterEqual(len(scripts), 2)
            for idx, script_content in enumerate(scripts):
                with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as tf:
                    tf.write(script_content)
                    tf_path = tf.name
                try:
                    res = subprocess.run([node_bin, "-c", tf_path], capture_output=True, text=True)
                    self.assertEqual(res.returncode, 0, f"Script block {idx} failed syntax check: {res.stderr}")
                finally:
                    if os.path.exists(tf_path):
                        os.unlink(tf_path)


if __name__ == "__main__":
    unittest.main()
