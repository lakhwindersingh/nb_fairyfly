#!/usr/bin/env python3
"""
Unit Test Suite for Declarative Tool Contracts & JSON Schema Validation (TODO-AGT-04 / GAP-AGT-04)
Validates Draft-07 parameter and return validation, idempotency caching,
and execution deadline timeout enforcement.
"""

import os
import sys
import time
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for p in [REPO_ROOT / ".nb", REPO_ROOT / ".nb" / "core", REPO_ROOT / "workplace", REPO_ROOT / "workplace" / "core"]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.tool_contract_validator import (
    ToolContractValidator,
    ToolContract,
    ToolContractValidationError,
    ToolTimeoutError
)


class TestToolContractValidator(unittest.TestCase):

    def setUp(self):
        self.validator = ToolContractValidator()

    def test_01_registry_loads_platform_tools(self):
        """Validates that YAML contracts for core tools are discovered and loaded."""
        self.assertIn("ast_pruner", self.validator.registry)
        self.assertIn("cve_sentinel", self.validator.registry)
        self.assertIn("contract_checker", self.validator.registry)
        self.assertIn("merkle_auditor", self.validator.registry)

        ast_tool = self.validator.registry["ast_pruner"]
        self.assertTrue(ast_tool.is_idempotent)
        self.assertFalse(ast_tool.mutates_filesystem)
        self.assertEqual(ast_tool.timeout_seconds, 15)

    def test_02_argument_validation_rejects_malformed_inputs(self):
        """Validates pre-call validation catches missing required parameters and invalid types."""
        # Missing required 'language' in ast_pruner
        valid, err = self.validator.validate_arguments("ast_pruner", {"source_code": "def foo(): pass"})
        self.assertFalse(valid)
        self.assertIn("Missing required property: 'language'", err)

        # Invalid enum for language
        valid, err = self.validator.validate_arguments("ast_pruner", {"source_code": "code", "language": "fortran"})
        self.assertFalse(valid)
        self.assertIn("not in allowed enum", err)

        # Valid arguments
        valid, err = self.validator.validate_arguments("ast_pruner", {"source_code": "def foo(): pass", "language": "python"})
        self.assertTrue(valid)
        self.assertIsNone(err)

    def test_03_output_validation_rejects_malformed_returns(self):
        """Validates post-call validation catches non-conforming return payloads."""
        # Missing tokens_saved in return payload
        bad_output = {"pruned_code": "def foo(): ...", "reduction_pct": 50.0}
        valid, err = self.validator.validate_output("ast_pruner", bad_output)
        self.assertFalse(valid)
        self.assertIn("Missing required property: 'tokens_saved'", err)

        # Correct output
        good_output = {"pruned_code": "def foo(): ...", "tokens_saved": 100, "reduction_pct": 50.0}
        valid, err = self.validator.validate_output("ast_pruner", good_output)
        self.assertTrue(valid)
        self.assertIsNone(err)

    def test_04_idempotency_caching_avoids_redundant_compute(self):
        """Validates that tools marked is_idempotent=True cache results and skip repeated execution."""
        call_counter = [0]

        def handler(source_code, language):
            call_counter[0] += 1
            return {"pruned_code": "def foo(): ...", "tokens_saved": 20, "reduction_pct": 40.0}

        args = {"source_code": "def foo(): return 1", "language": "python"}

        # First call executes handler
        res1 = self.validator.execute_tool("ast_pruner", args, handler)
        self.assertEqual(res1["status"], "SUCCESS")
        self.assertFalse(res1["cache_hit"])
        self.assertEqual(call_counter[0], 1)

        # Second call hits cache
        res2 = self.validator.execute_tool("ast_pruner", args, handler)
        self.assertEqual(res2["status"], "CACHED")
        self.assertTrue(res2["cache_hit"])
        self.assertEqual(call_counter[0], 1, "Handler must not be invoked on cache hit")

    def test_05_execution_timeout_enforcement(self):
        """Validates that tools exceeding timeout deadline raise ToolTimeoutError."""
        def slow_handler(manifest_path):
            time.sleep(0.5)
            return {"status": "PASS", "vulnerabilities_found": [], "compliant": True}

        # Override timeout to 0.1 seconds
        with self.assertRaises(ToolTimeoutError):
            self.validator.execute_tool(
                "cve_sentinel",
                {"manifest_path": "package.json"},
                slow_handler,
                timeout_override=0.1
            )

    def test_06_execute_tool_catches_invalid_arguments_exception(self):
        """Validates ToolContractValidationError on malformed arguments during execute_tool."""
        with self.assertRaises(ToolContractValidationError):
            self.validator.execute_tool("cve_sentinel", {}, lambda **kw: {})


if __name__ == "__main__":
    unittest.main()
