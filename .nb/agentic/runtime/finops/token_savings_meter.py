"""
Percipience Token Savings Meter (Declarative Facade)
Imports from workplace/core/token_optimizer_suite.py and token_tracker.py.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT / "workplace") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "workplace"))

from core.token_tracker import TokenTracker
from core.token_optimizer_suite import UnifiedTokenOptimizer, TokenOptimizationConfig

__all__ = ["TokenTracker", "UnifiedTokenOptimizer", "TokenOptimizationConfig"]
