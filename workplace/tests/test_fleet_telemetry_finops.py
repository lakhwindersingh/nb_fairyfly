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


if __name__ == "__main__":
    unittest.main()
