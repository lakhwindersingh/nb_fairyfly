"""
Percipience Atomic Gate Merger (Declarative Facade)
Imports from workplace/core/autonomous_cicd.py and worktree_engine.py.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for p_dir in [REPO_ROOT / ".nb", REPO_ROOT / ".nb" / "core", REPO_ROOT / "workplace"]:
    if str(p_dir) not in sys.path:
        sys.path.insert(0, str(p_dir))

from core.worktree_engine import WorktreeEngine
from core.autonomous_cicd import AutonomousCICDOrchestrator

__all__ = ["WorktreeEngine", "AutonomousCICDOrchestrator"]
