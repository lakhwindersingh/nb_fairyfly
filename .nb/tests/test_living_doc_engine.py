"""
Unit and Integration Tests for LivingDocEngine (CAP-21 & Step 15)
Validates autonomous living documentation generation, syntax-checking of Mermaid diagrams,
AST-driven incremental caching, and Merkle ledger registration.
"""

import unittest
import shutil
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "workplace"))

from core.living_doc_engine import LivingDocEngine


class TestLivingDocEngine(unittest.TestCase):

    def setUp(self):
        self.repo_root = REPO_ROOT
        self.docs_dir = self.repo_root / "workplace" / "docs"

    def test_01_sync_all_docs_generates_all_files(self):
        """Validates that sync_all_docs creates all 7 expected documentation files."""
        res = LivingDocEngine.sync_all_docs(self.repo_root, force=True)
        self.assertEqual(res["status"], "SYNCHRONIZED")
        self.assertGreaterEqual(res["generated_count"], 7)
        self.assertTrue(res["all_mermaid_valid"])

        expected_files = [
            "architecture.md",
            "module_catalog.md",
            "sequence_flows.md",
            "data_flow.md",
            "entity_relationship.md",
            "domain_extensions.md",
            "README.md"
        ]
        for f in expected_files:
            p = self.docs_dir / f
            self.assertTrue(p.exists(), f"File {f} was not generated!")
            self.assertGreater(p.stat().st_size, 50, f"File {f} is unexpectedly empty!")

    def test_02_mermaid_syntax_validation(self):
        """Validates that Mermaid diagram syntax validation catches unquoted labels with brackets/parens."""
        valid_block = """graph TD
  NodeA["FastAPI Gateway (Port 8000)"] --> NodeB["PostgreSQL Persistence (v16)"]
"""
        res_valid = LivingDocEngine.validate_mermaid_syntax(valid_block)
        self.assertTrue(res_valid["is_valid"])

        invalid_block = """graph TD
  NodeA[FastAPI Gateway (Port 8000)] --> NodeB[PostgreSQL]
"""
        res_invalid = LivingDocEngine.validate_mermaid_syntax(invalid_block)
        self.assertFalse(res_invalid["is_valid"])
        self.assertTrue(any("Unquoted" in err for err in res_invalid["errors"]))

    def test_03_diagram_content_completeness(self):
        """Validates that generated markdown files contain valid Mermaid code blocks."""
        arch_text = (self.docs_dir / "architecture.md").read_text(encoding="utf-8")
        self.assertIn("```mermaid", arch_text)
        self.assertIn("graph TD", arch_text)
        self.assertIn("Context Gateway Enclave", arch_text)

        seq_text = (self.docs_dir / "sequence_flows.md").read_text(encoding="utf-8")
        self.assertIn("```mermaid", seq_text)
        self.assertIn("sequenceDiagram", seq_text)
        self.assertIn("autonumber", seq_text)

        erd_text = (self.docs_dir / "entity_relationship.md").read_text(encoding="utf-8")
        self.assertIn("```mermaid", erd_text)
        self.assertIn("erDiagram", erd_text)
        self.assertIn("TENANT", erd_text)

    def test_04_ledger_registration(self):
        """Validates that context_ledger.yaml records the living_docs tracking block."""
        import yaml
        ledger_path = (self.repo_root / ".nb" / "context" / "ledger" / "context_ledger.yaml" if (self.repo_root / ".nb" / "context").exists() else self.repo_root / "context" / "ledger" / "context_ledger.yaml")
        self.assertTrue(ledger_path.exists())
        with open(ledger_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        self.assertIn("living_docs", data)
        self.assertTrue(data["living_docs"]["engine_enabled"])
        self.assertEqual(data["living_docs"]["preferred_diagram_engine"], "mermaid")
        self.assertGreaterEqual(len(data["living_docs"]["documents"]), 7)


if __name__ == "__main__":
    unittest.main()
