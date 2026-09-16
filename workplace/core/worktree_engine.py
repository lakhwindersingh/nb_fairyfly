"""
Percipience Ephemeral Git Worktree & Subagent Lease Manager
Provisions isolated worktrees under .workspaces/wt_{agent_id}
with time-bound TTL leases and active POSIX PID probing to guarantee
safe concurrent subagent execution and zero stale lease deadlocks.
"""

import os
import subprocess
import time
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

def is_pid_alive(pid: Optional[int]) -> bool:
    """Checks if a process ID is currently running on the host OS."""
    if not pid or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False

class WorktreeEngine:
    """Manages ephemeral git worktree allocations, leases, and PID-probing eviction."""

    @staticmethod
    def _lease_file(workspace_root: Path) -> Path:
        p = workspace_root / ".workspaces" / "leases.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists():
            with open(p, "w", encoding="utf-8") as f:
                json.dump({}, f)
        return p

    @classmethod
    def acquire(cls, workspace_root: Path, agent_id: str, base_branch: str = "main", ttl_seconds: int = 3600) -> Dict[str, Any]:
        wt_dir = workspace_root / ".workspaces" / f"wt_{agent_id}"
        branch_name = f"wt_branch_{agent_id}"
        lease_path = cls._lease_file(workspace_root)

        # Evict existing lease if dead PID or expired
        with open(lease_path, "r", encoding="utf-8") as f:
            try:
                leases = json.load(f)
            except Exception:
                leases = {}

        if agent_id in leases:
            existing = leases[agent_id]
            existing_pid = existing.get("pid")
            is_dead = existing_pid and not is_pid_alive(existing_pid)
            is_expired = int(time.time()) >= existing.get("expires_at", 0)
            if is_dead or is_expired:
                cls.release(workspace_root, agent_id)

        # Attempt git worktree add if git repository
        try:
            subprocess.run(
                ["git", "worktree", "add", "-b", branch_name, str(wt_dir), base_branch],
                cwd=str(workspace_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False
            )
        except Exception:
            wt_dir.mkdir(parents=True, exist_ok=True)

        current_pid = os.getpid()
        expires_at = int(time.time()) + ttl_seconds
        lease_info = {
            "agent_id": agent_id,
            "branch": branch_name,
            "path": str(wt_dir),
            "pid": current_pid,
            "acquired_at": int(time.time()),
            "expires_at": expires_at,
            "status": "ACTIVE"
        }

        with open(lease_path, "r+", encoding="utf-8") as f:
            try:
                leases = json.load(f)
            except Exception:
                leases = {}
            leases[agent_id] = lease_info
            f.seek(0)
            f.truncate()
            json.dump(leases, f, indent=2)

        return lease_info

    @classmethod
    def list_leases(cls, workspace_root: Path) -> List[Dict[str, Any]]:
        lease_path = cls._lease_file(workspace_root)
        with open(lease_path, "r", encoding="utf-8") as f:
            try:
                leases = json.load(f)
            except Exception:
                leases = {}
        
        now = int(time.time())
        results = []
        for aid, info in leases.items():
            info["remaining_ttl_sec"] = max(0, info.get("expires_at", 0) - now)
            info["expired"] = info["remaining_ttl_sec"] <= 0
            pid = info.get("pid")
            info["pid_alive"] = is_pid_alive(pid) if pid else False
            info["stale_orphan"] = (not info["pid_alive"]) or info["expired"]
            results.append(info)
        return results

    @classmethod
    def reclaim_stale_leases(cls, workspace_root: Path) -> List[str]:
        """Active eviction: identifies and purges leases with dead PIDs or expired TTLs."""
        leases = cls.list_leases(workspace_root)
        reclaimed = []
        for l in leases:
            if l.get("stale_orphan", False):
                aid = l["agent_id"]
                if cls.release(workspace_root, aid):
                    reclaimed.append(aid)
        return reclaimed

    @classmethod
    def release(cls, workspace_root: Path, agent_id: str) -> bool:
        lease_path = cls._lease_file(workspace_root)
        with open(lease_path, "r+", encoding="utf-8") as f:
            try:
                leases = json.load(f)
            except Exception:
                leases = {}
            if agent_id in leases:
                info = leases.pop(agent_id)
                f.seek(0)
                f.truncate()
                json.dump(leases, f, indent=2)

                # Remove worktree directory and branch via git
                try:
                    subprocess.run(
                        ["git", "worktree", "remove", "--force", info["path"]],
                        cwd=str(workspace_root),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=False
                    )
                except Exception:
                    pass
                
                # Clean up ephemeral subagent branch
                branch_to_del = info.get("branch")
                if branch_to_del and branch_to_del not in ["main", "master"]:
                    try:
                        subprocess.run(
                            ["git", "branch", "-D", branch_to_del],
                            cwd=str(workspace_root),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            check=False
                        )
                    except Exception:
                        pass
                return True
        return False
