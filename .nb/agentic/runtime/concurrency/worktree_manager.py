"""
Percipience Ephemeral Git Worktree Manager (Declarative Facade)
Imports from workplace/core/worktree_engine.py to preserve Quad-Space boundaries.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for p_dir in [REPO_ROOT / ".nb", REPO_ROOT / ".nb" / "core", REPO_ROOT / "workplace"]:
    if str(p_dir) not in sys.path:
        sys.path.insert(0, str(p_dir))

from core.worktree_engine import WorktreeEngine, is_pid_alive

__all__ = ["WorktreeEngine", "is_pid_alive"]
