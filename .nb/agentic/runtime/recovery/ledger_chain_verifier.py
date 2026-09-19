"""
Percipience Ledger Chain Verifier (Declarative Facade)
Imports from workplace/core/merkle_engine.py.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT / "workplace") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "workplace"))

from core.merkle_engine import MerkleEngine

__all__ = ["MerkleEngine"]
