"""
Percipience Plan Pack Compiler (Declarative Facade)
Imports from workplace/core/nbpack_envelope.py.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for p_dir in [REPO_ROOT / ".nb", REPO_ROOT / ".nb" / "core", REPO_ROOT / "workplace"]:
    if str(p_dir) not in sys.path:
        sys.path.insert(0, str(p_dir))

from core.nbpack_envelope import NBPackEnvelope

__all__ = ["NBPackEnvelope"]
