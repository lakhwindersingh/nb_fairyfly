"""
Percipience Model-Agnostic Cognitive Tiering Router (Declarative Facade)
Imports from workplace/core/cognitive_router.py to preserve Quad-Space boundaries.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for p_dir in [REPO_ROOT / ".nb", REPO_ROOT / ".nb" / "core", REPO_ROOT / "workplace"]:
    if str(p_dir) not in sys.path:
        sys.path.insert(0, str(p_dir))

from core.cognitive_router import CognitiveRouter

__all__ = ["CognitiveRouter"]
