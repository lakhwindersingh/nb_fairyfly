"""
Synthetic Virtual PSI Fixture Generator for Offline CI Validation
"""

import time
from typing import Dict, Any

class VirtualPsiFixture:
    """Generates synthetic multi-language AST / PSI representations for offline testing."""

    @staticmethod
    def generate_python_psi_mock(func_count: int = 5) -> Dict[str, Any]:
        start = time.time()
        functions = []
        for i in range(func_count):
            functions.append({
                "name": f"calculate_tax_{i}",
                "args": ["amount: float", "rate: float"],
                "return_type": "float",
                "docstring": f"Calculates tax tier {i}.",
                "body_loc": 25
            })
        duration_ms = (time.time() - start) * 1000

        raw_tokens = func_count * 150
        pruned_tokens = func_count * 35
        reduction = ((raw_tokens - pruned_tokens) / raw_tokens) * 100.0

        return {
            "psi_root": "com.jetbrains.python.psi.PyFile",
            "file_name": "tax_service.py",
            "functions": functions,
            "raw_tokens": raw_tokens,
            "pruned_tokens": pruned_tokens,
            "token_reduction_pct": round(reduction, 2),
            "traversal_ms": round(duration_ms, 2)
        }
