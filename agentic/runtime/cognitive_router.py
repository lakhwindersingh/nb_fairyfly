"""
Percipience Model-Agnostic Cognitive Tiering Router (Declarative Facade)
Imports from workplace/core/cognitive_router.py to preserve Quad-Space boundaries.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT / "workplace") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "workplace"))

from core.cognitive_router import CognitiveRouter

__all__ = ["CognitiveRouter"]
