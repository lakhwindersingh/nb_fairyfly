import socket
import getpass
#!/usr/bin/env python3
"""
Enterprise Fleet Coordinator & FinOps Aggregator (TODO-PRT-07, 08, 09, 10 / CAP-43)
Manages centralized workstation and runner node registry:
- Ingests node heartbeats & full telemetry packages
- Evaluates machine liveness and status transitions (HEALTHY, HEALING, OFFLINE, QUARANTINED)
- Aggregates Enterprise FinOps Rollups (Gross savings, 15% Rev-Share, 85% Customer Net, Leaderboards)
- Tracks real-time task progression, milestone ETAs, and stuck subagent alerts
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple


class FleetManager:
    """
    Central fleet control plane manager for distributed workstations and runner nodes.
    """

    HEARTBEAT_TIMEOUT_SECONDS = 60

    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = Path(
            storage_path or (Path(__file__).resolve().parent.parent.parent / ".nb" / "context" / "fleet" / "fleet_registry.json")
        ).resolve()
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.machines: Dict[str, Dict[str, Any]] = {}
        self.telemetry_history: Dict[str, List[Dict[str, Any]]] = {}
        self._load()

    def _load(self) -> None:
        """Loads registry from disk."""
        if not self.storage_path.exists():
            self._seed_default_fleet()
            self._save()
            return
        try:
            data = json.loads(self.storage_path.read_text(encoding="utf-8"))
            self.machines = data.get("machines", {})
            self.telemetry_history = data.get("telemetry_history", {})
        except Exception:
            self._seed_default_fleet()

    def _save(self) -> None:
        """Persists registry to disk."""
        payload = {
            "version": "1.0.0",
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "machines": self.machines,
            "telemetry_history": self.telemetry_history
        }
        self.storage_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _seed_default_fleet(self) -> None:
        """Seeds representative enterprise workstation fleet if uninitialized."""
        now = datetime.now(timezone.utc).isoformat()
        self.machines = {
            "node_mac_lakhwinder": {
                "machine_id": "node_mac_lakhwinder",
                "hostname": os.environ.get("PERCIPIENCE_FLEET_HOSTNAME", socket.gethostname() if "socket" in globals() else "macbook-pro.local"),
                "os_name": "macOS",
                "os_version": "Darwin 24.1.0",
                "user_id": os.environ.get("PERCIPIENCE_USER_ID", os.environ.get("USER", "lakhwinder")),
                "org_id": "org_enterprise",
                "project_id": "proj_fairyfly",
                "health_status": "HEALTHY",
                "last_seen_utc": now,
                "workspace_path": os.environ.get("PERCIPIENCE_WORKSPACE_PATH", str(Path.cwd())),
                "active_worktree": "wt_branch_worker_1",
                "git_branch": "feature/dews-fleet",
                "git_commit": "ce77d0d3c21c",
                "uncommitted_changes": False,
                "active_task": {
                    "task_id": "task_ast_pruning_01",
                    "task_name": "AST Pruning & Token Optimization",
                    "progress_pct": 85.0,
                    "step_status": "AST Skeletonization",
                    "eta_seconds": 15,
                    "is_stuck": False
                },
                "finops": {
                    "tokens_saved": 420000,
                    "gross_savings_usd": 1.2600,
                    "net_savings_usd": 1.0710,
                    "fee_usd": 0.1890
                }
            },
            "node_linux_ci_runner_01": {
                "machine_id": "node_linux_ci_runner_01",
                "hostname": "runner-eks-spot-04.corp",
                "os_name": "Linux",
                "os_version": "Debian 12 (bookworm)",
                "user_id": "agent_runner",
                "org_id": "org_enterprise",
                "project_id": "proj_fairyfly",
                "health_status": "HEALTHY",
                "last_seen_utc": now,
                "workspace_path": "/workspace",
                "active_worktree": "wt_branch_runner_01",
                "git_branch": "main",
                "git_commit": "ce77d0d3c21c",
                "uncommitted_changes": False,
                "active_task": {
                    "task_id": "task_fuzzer_02",
                    "task_name": "Adversarial Fuzzing Gate",
                    "progress_pct": 50.0,
                    "step_status": "Running Fuzzer",
                    "eta_seconds": 45,
                    "is_stuck": False
                },
                "finops": {
                    "tokens_saved": 980000,
                    "gross_savings_usd": 2.9400,
                    "net_savings_usd": 2.4990,
                    "fee_usd": 0.4410
                }
            },
            "node_dev_alice_win": {
                "machine_id": "node_dev_alice_win",
                "hostname": "alice-workstation.corp",
                "os_name": "Windows",
                "os_version": "10.0.22631",
                "user_id": "alice",
                "org_id": "org_enterprise",
                "project_id": "proj_billing",
                "health_status": "HEALTHY",
                "last_seen_utc": now,
                "workspace_path": "C:\\dev\\nb_fairyfly",
                "active_worktree": "wt_branch_alice",
                "git_branch": "feat/stripe",
                "git_commit": "8f3b2110c9a4",
                "uncommitted_changes": True,
                "active_task": {
                    "task_id": "task_review_03",
                    "task_name": "Contract Validation",
                    "progress_pct": 100.0,
                    "step_status": "Awaiting Review",
                    "eta_seconds": 0,
                    "is_stuck": False
                },
                "finops": {
                    "tokens_saved": 210000,
                    "gross_savings_usd": 0.6300,
                    "net_savings_usd": 0.5355,
                    "fee_usd": 0.0945
                }
            }
        }

    def ingest_heartbeat(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Ingests a lightweight heartbeat pulse from a workstation daemon."""
        machine_id = payload.get("machine_id")
        if not machine_id:
            raise ValueError("Heartbeat missing machine_id")

        now = datetime.now(timezone.utc).isoformat()
        if machine_id not in self.machines:
            self.machines[machine_id] = {
                "machine_id": machine_id,
                "hostname": payload.get("hostname", "unknown_host"),
                "os_name": "Unknown",
                "os_version": "Unknown",
                "user_id": "daemon_agent",
                "org_id": payload.get("org_id", "org_enterprise"),
                "project_id": payload.get("project_id", "proj_core"),
                "health_status": payload.get("health_status", "HEALTHY"),
                "last_seen_utc": now,
                "workspace_path": "",
                "active_worktree": "primary",
                "git_branch": "main",
                "git_commit": "HEAD",
                "uncommitted_changes": False,
                "active_task": {
                    "task_id": f"task_{machine_id}",
                    "task_name": payload.get("active_task", "Idle"),
                    "progress_pct": payload.get("progress_pct", 100.0),
                    "step_status": "Monitoring",
                    "eta_seconds": 0,
                    "is_stuck": False
                },
                "finops": {
                    "tokens_saved": payload.get("tokens_saved", 0),
                    "gross_savings_usd": (payload.get("tokens_saved", 0) / 1000.0) * 0.003,
                    "net_savings_usd": (payload.get("tokens_saved", 0) / 1000.0) * 0.003 * 0.85,
                    "fee_usd": (payload.get("tokens_saved", 0) / 1000.0) * 0.003 * 0.15
                }
            }
        else:
            m = self.machines[machine_id]
            m["last_seen_utc"] = now
            m["health_status"] = payload.get("health_status", m.get("health_status", "HEALTHY"))
            m["active_task"]["task_name"] = payload.get("active_task", m["active_task"]["task_name"])
            m["active_task"]["progress_pct"] = payload.get("progress_pct", m["active_task"]["progress_pct"])
            if "tokens_saved" in payload:
                tokens = payload["tokens_saved"]
                gross = (tokens / 1000.0) * 0.003
                m["finops"]["tokens_saved"] = tokens
                m["finops"]["gross_savings_usd"] = round(gross, 4)
                m["finops"]["net_savings_usd"] = round(gross * 0.85, 4)
                m["finops"]["fee_usd"] = round(gross * 0.15, 4)

        self._save()
        return {"status": "SUCCESS", "machine_id": machine_id, "recorded_at": now}

    def ingest_telemetry(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Ingests a complete node telemetry package."""
        machine_info = payload.get("machine", {})
        machine_id = machine_info.get("machine_id")
        if not machine_id:
            raise ValueError("Telemetry missing machine.machine_id")

        now = datetime.now(timezone.utc).isoformat()
        workspace_info = payload.get("workspace", {})
        task_info = payload.get("task", {})
        finops_info = payload.get("finops", {})

        record = {
            "machine_id": machine_id,
            "hostname": machine_info.get("hostname", "unknown"),
            "os_name": machine_info.get("os_name", "unknown"),
            "os_version": machine_info.get("os_version", "unknown"),
            "user_id": machine_info.get("user_id", "unknown"),
            "org_id": payload.get("org_id", "org_enterprise"),
            "project_id": payload.get("project_id", "proj_core"),
            "health_status": payload.get("health_status", "HEALTHY"),
            "last_seen_utc": now,
            "workspace_path": workspace_info.get("workspace_path", ""),
            "active_worktree": workspace_info.get("active_worktree", "primary"),
            "git_branch": workspace_info.get("git_branch", "main"),
            "git_commit": workspace_info.get("git_commit", "HEAD"),
            "uncommitted_changes": workspace_info.get("uncommitted_changes", False),
            "active_task": task_info,
            "finops": finops_info
        }

        self.machines[machine_id] = record

        # Add to telemetry history (keep latest 10 per machine)
        if machine_id not in self.telemetry_history:
            self.telemetry_history[machine_id] = []
        self.telemetry_history[machine_id].append({
            "timestamp_utc": now,
            "task_name": task_info.get("task_name"),
            "progress_pct": task_info.get("progress_pct"),
            "tokens_saved": finops_info.get("tokens_saved", 0)
        })
        self.telemetry_history[machine_id] = self.telemetry_history[machine_id][-10:]

        self._save()
        return {"status": "SUCCESS", "machine_id": machine_id, "recorded_at": now}

    def evaluate_liveness(self) -> None:
        """Evaluates timestamps and marks machines OFFLINE if heartbeat is stale."""
        now = datetime.now(timezone.utc)
        for m in self.machines.values():
            if m.get("health_status") == "QUARANTINED":
                continue
            last_seen = m.get("last_seen_utc")
            if last_seen:
                try:
                    seen_dt = datetime.fromisoformat(last_seen)
                    if (now - seen_dt).total_seconds() > self.HEARTBEAT_TIMEOUT_SECONDS:
                        m["health_status"] = "OFFLINE"
                except Exception:
                    pass

    def list_machines(
        self,
        org_id: Optional[str] = None,
        project_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Returns filtered list of registered fleet machines."""
        self.evaluate_liveness()
        results = []
        for m in self.machines.values():
            if org_id and m.get("org_id") != org_id:
                continue
            if project_id and m.get("project_id") != project_id:
                continue
            if status and m.get("health_status") != status:
                continue
            results.append(m)
        return results

    def get_finops_rollup(self) -> Dict[str, Any]:
        """
        Calculates aggregated token and dollar accounting across all machines:
        - Enterprise Gross Cloud Savings ($)
        - 15% Percipience Rev-Share Fee ($)
        - 85% Net Customer Retained Savings ($)
        - Machine-level and project-level leaderboards
        """
        self.evaluate_liveness()
        total_tokens = 0
        total_gross = 0.0
        total_net = 0.0
        total_fee = 0.0

        machine_board: List[Dict[str, Any]] = []
        project_aggregates: Dict[str, Dict[str, Any]] = {}

        for m in self.machines.values():
            f = m.get("finops", {})
            tok = f.get("tokens_saved", 0)
            gross = f.get("gross_savings_usd", 0.0)
            net = f.get("net_savings_usd", 0.0)
            fee = f.get("fee_usd", 0.0)

            total_tokens += tok
            total_gross += gross
            total_net += net
            total_fee += fee

            machine_board.append({
                "machine_id": m["machine_id"],
                "hostname": m["hostname"],
                "user_id": m["user_id"],
                "project_id": m["project_id"],
                "tokens_saved": tok,
                "gross_savings_usd": gross,
                "net_savings_usd": net
            })

            pid = m["project_id"]
            if pid not in project_aggregates:
                project_aggregates[pid] = {
                    "project_id": pid,
                    "machines_count": 0,
                    "tokens_saved": 0,
                    "gross_savings_usd": 0.0,
                    "net_savings_usd": 0.0
                }
            project_aggregates[pid]["machines_count"] += 1
            project_aggregates[pid]["tokens_saved"] += tok
            project_aggregates[pid]["gross_savings_usd"] += gross
            project_aggregates[pid]["net_savings_usd"] += net

        machine_board.sort(key=lambda x: x["gross_savings_usd"], reverse=True)
        project_board = sorted(project_aggregates.values(), key=lambda x: x["gross_savings_usd"], reverse=True)

        return {
            "summary": {
                "active_machines_count": len([m for m in self.machines.values() if m["health_status"] == "HEALTHY"]),
                "total_machines_count": len(self.machines),
                "total_tokens_saved": total_tokens,
                "enterprise_gross_savings_usd": round(total_gross, 2),
                "percipience_rev_share_fee_usd": round(total_fee, 2),
                "customer_net_retained_usd": round(total_net, 2)
            },
            "machine_leaderboard": machine_board,
            "project_leaderboard": project_board
        }

    def get_active_tasks(self) -> List[Dict[str, Any]]:
        """Returns real-time tasks with progress bars, ETAs, and stuck alerts."""
        self.evaluate_liveness()
        tasks = []
        for m in self.machines.values():
            t = m.get("active_task", {})
            if t:
                task_entry = dict(t)
                task_entry["machine_id"] = m["machine_id"]
                task_entry["hostname"] = m["hostname"]
                task_entry["user_id"] = m["user_id"]
                task_entry["project_id"] = m["project_id"]
                task_entry["health_status"] = m["health_status"]
                tasks.append(task_entry)
        return tasks

    def simulate_pulse(
        self,
        machine_id: Optional[str] = None,
        delta_tokens: int = 50000,
        advance_task: bool = True
    ) -> Dict[str, Any]:
        """Simulates activity pulse for UI and integration testing."""
        now = datetime.now(timezone.utc).isoformat()
        if not self.machines:
            self._seed_default_fleet()

        target_id = machine_id
        if not target_id:
            for mid, m in self.machines.items():
                if m.get("health_status") == "HEALTHY":
                    target_id = mid
                    break
            if not target_id:
                target_id = next(iter(self.machines.keys()), "node_docker_runner_01")

        if target_id not in self.machines:
            self.machines[target_id] = {
                "machine_id": target_id,
                "hostname": "docker-runner-swarm.local",
                "os_name": "Linux",
                "os_version": "Debian 12 (container)",
                "user_id": "agent_runner",
                "org_id": "org_enterprise",
                "project_id": "proj_docker_swarm",
                "health_status": "HEALTHY",
                "last_seen_utc": now,
                "workspace_path": "/workspace",
                "active_worktree": "wt_container_01",
                "git_branch": "feature/swarm-test",
                "git_commit": "d0c4e1f7",
                "uncommitted_changes": False,
                "active_task": {
                    "task_id": "task_swarm_01",
                    "task_name": "Swarm Parallel AST Pruning",
                    "progress_pct": 10.0,
                    "step_status": "Analyzing Modules",
                    "eta_seconds": 60,
                    "is_stuck": False
                },
                "finops": {
                    "tokens_saved": 0,
                    "gross_savings_usd": 0.0,
                    "net_savings_usd": 0.0,
                    "fee_usd": 0.0
                }
            }

        m = self.machines[target_id]
        m["last_seen_utc"] = now
        m["health_status"] = "HEALTHY"

        tok = m["finops"].get("tokens_saved", 0) + delta_tokens
        gross = round((tok / 1000.0) * 0.003, 4)
        m["finops"]["tokens_saved"] = tok
        m["finops"]["gross_savings_usd"] = gross
        m["finops"]["net_savings_usd"] = round(gross * 0.85, 4)
        m["finops"]["fee_usd"] = round(gross * 0.15, 4)

        if advance_task and "active_task" in m:
            curr_pct = m["active_task"].get("progress_pct", 0.0)
            new_pct = curr_pct + 15.0
            if new_pct > 100.0:
                new_pct = 15.0
                phases = ["AST Slicing", "Contract Verification", "Parallel Fuzzing", "Merkle Sealing"]
                current_phase = m["active_task"].get("step_status", "")
                idx = (phases.index(current_phase) + 1) % len(phases) if current_phase in phases else 0
                m["active_task"]["step_status"] = phases[idx]
            m["active_task"]["progress_pct"] = round(new_pct, 1)

        self._save()
        return {
            "status": "SUCCESS",
            "action": "SIMULATION_PULSE",
            "machine_id": target_id,
            "machine": m,
            "finops_rollup": self.get_finops_rollup()
        }

    def reset_fleet(self) -> Dict[str, Any]:
        """Resets fleet to standard baseline seeded state."""
        self._seed_default_fleet()
        self._save()
        return {
            "status": "SUCCESS",
            "action": "RESET_BASELINE",
            "machines_count": len(self.machines),
            "finops_rollup": self.get_finops_rollup()
        }
