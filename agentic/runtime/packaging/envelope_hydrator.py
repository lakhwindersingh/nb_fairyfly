"""
Percipience Envelope Hydrator (Declarative Facade)
Imports from workplace/core/nbpack_envelope.py.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT / "workplace") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "workplace"))

from core.nbpack_envelope import NBPackEnvelope

__all__ = ["NBPackEnvelope"]
