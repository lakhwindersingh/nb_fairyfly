"""
Percipience Ephemeral Git Worktree Manager (Declarative Facade)
Imports from workplace/core/worktree_engine.py to preserve Quad-Space boundaries.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT / "workplace") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "workplace"))

from core.worktree_engine import WorktreeEngine, is_pid_alive

__all__ = ["WorktreeEngine", "is_pid_alive"]
