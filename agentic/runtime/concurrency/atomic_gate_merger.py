"""
Percipience Atomic Gate Merger (Declarative Facade)
Imports from workplace/core/autonomous_cicd.py and worktree_engine.py.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT / "workplace") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "workplace"))

from core.worktree_engine import WorktreeEngine
from core.autonomous_cicd import AutonomousCICDOrchestrator

__all__ = ["WorktreeEngine", "AutonomousCICDOrchestrator"]
