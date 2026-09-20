"""
Percipience Token Savings Meter (Declarative Facade)
Imports from workplace/core/token_optimizer_suite.py and token_tracker.py.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for p_dir in [REPO_ROOT / ".nb", REPO_ROOT / ".nb" / "core", REPO_ROOT / "workplace"]:
    if str(p_dir) not in sys.path:
        sys.path.insert(0, str(p_dir))

from core.token_tracker import TokenTracker
from core.token_optimizer_suite import UnifiedTokenOptimizer, TokenOptimizationConfig

__all__ = ["TokenTracker", "UnifiedTokenOptimizer", "TokenOptimizationConfig"]
