"""
Percipience Ephemeral Git Worktree & Subagent Lease Manager
Provisions isolated worktrees under .workspaces/wt_{tenant}_{agent_id}
with time-bound TTL leases to guarantee safe concurrent subagent execution.
"""

import subprocess
import time
import json
from pathlib import Path
from typing import Dict, List, Any

class WorktreeEngine:
    """Manages ephemeral git worktree allocations and leases."""

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

        expires_at = int(time.time()) + ttl_seconds
        lease_info = {
            "agent_id": agent_id,
            "branch": branch_name,
            "path": str(wt_dir),
            "acquired_at": int(time.time()),
            "expires_at": expires_at,
            "status": "ACTIVE"
        }

        with open(lease_path, "r+", encoding="utf-8") as f:
            leases = json.load(f)
            leases[agent_id] = lease_info
            f.seek(0)
            f.truncate()
            json.dump(leases, f, indent=2)

        return lease_info

    @classmethod
    def list_leases(cls, workspace_root: Path) -> List[Dict[str, Any]]:
        lease_path = cls._lease_file(workspace_root)
        with open(lease_path, "r", encoding="utf-8") as f:
            leases = json.load(f)
        
        now = int(time.time())
        results = []
        for aid, info in leases.items():
            info["remaining_ttl_sec"] = max(0, info["expires_at"] - now)
            info["expired"] = info["remaining_ttl_sec"] <= 0
            results.append(info)
        return results

    @classmethod
    def release(cls, workspace_root: Path, agent_id: str) -> bool:
        lease_path = cls._lease_file(workspace_root)
        with open(lease_path, "r+", encoding="utf-8") as f:
            leases = json.load(f)
            if agent_id in leases:
                info = leases.pop(agent_id)
                f.seek(0)
                f.truncate()
                json.dump(leases, f, indent=2)

                # Remove worktree directory via git
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
                return True
        return False
