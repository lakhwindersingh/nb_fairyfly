"""
Percipience Surgical Rollback Manager (Declarative Facade)
Imports from workplace/core/autonomous_cicd.py.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT / "workplace") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "workplace"))

from core.autonomous_cicd import AutonomousHealer

__all__ = ["AutonomousHealer"]
