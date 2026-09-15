#!/usr/bin/env python3
"""
Backward-compatibility forwarding shim.
Delegates execution to the standardized test suite at tests/test_play3_suite.py.
"""
import sys
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
test_file = REPO_ROOT / "tests" / "test_play3_suite.py"

if __name__ == "__main__":
    sys.exit(subprocess.call([sys.executable, str(test_file)] + sys.argv[1:]))
