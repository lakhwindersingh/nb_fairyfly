#!/usr/bin/env python3
"""
Unit Test Suite for Structured Multi-Pass Self-Reflection & Critic Verification Loops (TODO-AGT-02 / GAP-AGT-02)
Validates 3-phase Reflexion cycle, 5 invariant pillars, convergence scoring,
bounded iterations, and zero-disk-write invariants.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for p in [REPO_ROOT / ".nb", REPO_ROOT / ".nb" / "core", REPO_ROOT / "workplace", REPO_ROOT / "workplace" / "core"]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.self_reflection_engine import (
    SelfReflectionEngine,
    CritiqueEnvelope,
    ReflexionVerificationError
)


class TestSelfReflectionEngine(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.out_file = Path(self.tmp_dir.name) / "generated_module.py"

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_01_evaluate_invariants_clean_code(self):
        """Validates that well-typed, defensive, clean code achieves >= 0.90 convergence."""
        clean_code = '''
from typing import Optional

def calculate_fee(amount: float, rate: float = 0.05) -> Optional[float]:
    """Calculates processing fee with null guards."""
    if amount is None or amount < 0:
        return None
    try:
        return round(amount * rate, 2)
    except Exception:
        return None
'''
        envelope = SelfReflectionEngine.evaluate_invariants(clean_code)
        self.assertTrue(envelope.passes_invariants)
        self.assertGreaterEqual(envelope.convergence_score, 0.90)
        self.assertEqual(len(envelope.defects_found), 0)
        self.assertEqual(envelope.severity, "LOW")

    def test_02_evaluate_invariants_detects_defects(self):
        """Validates detection of missing return types, lack of defensive checks, and unsafe calls."""
        flawed_code = '''
import os

def run_cmd(cmd):
    os.system(cmd)
    return cmd
'''
        envelope = SelfReflectionEngine.evaluate_invariants(flawed_code)
        self.assertFalse(envelope.passes_invariants)
        self.assertLess(envelope.convergence_score, 0.90)
        defects_text = " ".join(envelope.defects_found)
        self.assertIn("return type annotations", defects_text)
        self.assertIn("os.system", defects_text)
        self.assertIn("error handling", defects_text)
        self.assertIn(envelope.severity, ["MEDIUM", "HIGH"])

    def test_03_reflexion_cycle_early_exit(self):
        """Validates that a generator producing clean code exits on turn 1 without unnecessary refinement."""
        def generator(spec):
            return '''
from typing import Dict, Any

def get_tenant_config(tenant_id: str) -> Dict[str, Any]:
    if not tenant_id:
        return {}
    try:
        return {"tenant_id": tenant_id, "active": True}
    except Exception:
        return {}
'''
        result = SelfReflectionEngine.run_reflexion_cycle(
            task_spec={"target_module": "auth"},
            generator_fn=generator
        )
        self.assertEqual(result["status"], "APPROVED")
        self.assertTrue(result["passes_invariants"])
        self.assertEqual(result["iterations"], 1)

    def test_04_reflexion_cycle_multi_pass_refinement(self):
        """Validates GENERATE -> CRITIQUE -> REFINE convergence over multiple turns."""
        turns = [0]

        def generator(spec):
            turns[0] += 1
            # Turn 1: Flawed without return type or try/except
            return "def process_data(data):\n    return data"

        def refiner(current, envelope, spec):
            turns[0] += 1
            # Turn 2: Fixed code with type annotation and try/except
            return '''
from typing import Any

def process_data(data: Any) -> Any:
    if data is None:
        return None
    try:
        return data
    except Exception:
        return None
'''

        result = SelfReflectionEngine.run_reflexion_cycle(
            task_spec={},
            generator_fn=generator,
            refiner_fn=refiner,
            max_turns=2
        )
        self.assertEqual(result["status"], "APPROVED")
        self.assertTrue(result["passes_invariants"])
        self.assertEqual(result["iterations"], 2)
        self.assertEqual(len(result["history"]), 2)

    def test_05_bounded_max_turns_escalation(self):
        """Validates that unresolved defects after max turns escalate to HITL."""
        def stubborn_generator(spec):
            return "def bad_func(): eval('1+1')"

        result = SelfReflectionEngine.run_reflexion_cycle(
            task_spec={},
            generator_fn=stubborn_generator,
            refiner_fn=lambda curr, env, spec: curr,  # Does not fix anything
            max_turns=2
        )
        self.assertEqual(result["status"], "ESCALATED_TO_HITL")
        self.assertFalse(result["passes_invariants"])
        self.assertEqual(result["iterations"], 2)

    def test_06_zero_disk_write_enforcement(self):
        """Ensures filesystem write is strictly blocked if passes_invariants=False."""
        flawed_result = {
            "passes_invariants": False,
            "final_envelope": {
                "convergence_score": 0.65,
                "defects_found": ["Prohibited eval() invocation detected"]
            }
        }
        with self.assertRaises(ReflexionVerificationError):
            SelfReflectionEngine.safe_apply_filesystem_write(
                target_path=self.out_file,
                content="eval('danger')",
                reflexion_result=flawed_result
            )
        self.assertFalse(self.out_file.exists(), "Flawed artifact must never be written to disk")

        # When passes_invariants=True, write succeeds
        approved_result = {
            "passes_invariants": True,
            "final_envelope": {"convergence_score": 0.95, "defects_found": []}
        }
        written = SelfReflectionEngine.safe_apply_filesystem_write(
            target_path=self.out_file,
            content="print('safe')",
            reflexion_result=approved_result
        )
        self.assertTrue(written)
        self.assertTrue(self.out_file.exists())
        self.assertEqual(self.out_file.read_text(), "print('safe')")


if __name__ == "__main__":
    unittest.main()
