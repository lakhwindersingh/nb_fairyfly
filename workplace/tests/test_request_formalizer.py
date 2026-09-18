"""
Unit and Integration Tests for RequestFormalizerEngine & agent_request_formalizer
Validates parsing and translation of unstructured requests into all 4 Quad-Space MVS specification formats:
- Jira Story Interchange (JSON)
- OpenAPI 3.1.0 API Contract (YAML with front-matter)
- UI Design Tokens & Accessibility Tokens (JSON)
- AsyncAPI 3.0.0 Event Stream Specification (YAML with front-matter)

Also validates persistence into user/inputs/formal_requests/, ledger logging, Merkle sealing,
and CLI execution via 'percipience formalize'.
"""

import unittest
import json
import subprocess
import shutil
import tempfile
from pathlib import Path
import sys
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2] if Path(__file__).resolve().parents[1].name == "workplace" else Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "workplace"))

from core.request_formalizer import RequestFormalizerEngine
from core.merkle_engine import MerkleEngine


class TestRequestFormalizerEngine(unittest.TestCase):

    def setUp(self):
        self.repo_root = REPO_ROOT
        self.sample_input_path = self.repo_root / "user" / "inputs" / "improv1.md"
        self.formal_requests_dir = self.repo_root / "user" / "inputs" / "formal_requests"
        self.formal_requests_dir.mkdir(parents=True, exist_ok=True)

    def test_01_detect_format(self):
        """Validates heuristic format detection across domain keywords."""
        # Tokens
        text_tokens = "Please update our design token system, color palette, and ensure WCAG contrast ratio >= 4.5."
        self.assertEqual(RequestFormalizerEngine.detect_format(text_tokens), "ui_design_tokens")

        # Event stream
        text_events = "Configure an AsyncAPI Kafka event stream for real-time telemetry stream and publish message payloads."
        self.assertEqual(RequestFormalizerEngine.detect_format(text_events), "event_stream_asyncapi")

        # OpenAPI / REST
        text_api = "Add OpenAPI swagger endpoints for REST API http post requestBody and status 200 response."
        self.assertEqual(RequestFormalizerEngine.detect_format(text_api), "api_contract_openapi")

        # Default Jira Story
        text_jira = "As a developer, I want to optimize the database query latency so users load pages faster."
        self.assertEqual(RequestFormalizerEngine.detect_format(text_jira), "jira_issue_interchange")

    def test_02_parse_unstructured_text(self):
        """Validates parsing of unstructured markdown proposals."""
        self.assertTrue(self.sample_input_path.exists())
        text = self.sample_input_path.read_text(encoding="utf-8")
        parsed = RequestFormalizerEngine.parse_unstructured_text(text)

        self.assertIn("title", parsed)
        self.assertIn("acceptance_criteria", parsed)
        self.assertIn("target_module", parsed)
        self.assertIn("priority", parsed)
        self.assertIn("components", parsed)
        self.assertGreater(len(parsed["acceptance_criteria"]), 0)

    def test_03_to_jira_story(self):
        """Validates generation of Jira Story Interchange specification."""
        text = self.sample_input_path.read_text(encoding="utf-8")
        payload = RequestFormalizerEngine.to_jira_story(text, metadata={"issue_key": "PERC-701"})

        self.assertEqual(payload["mvs_version"], "1.0.0")
        self.assertEqual(payload["format_type"], "jira_issue_interchange")
        self.assertEqual(payload["issue"]["key"], "PERC-701")
        self.assertIn("Ready for Dev", payload["issue"]["status"])
        self.assertIsInstance(payload["issue"]["acceptance_criteria"], list)
        self.assertGreater(len(payload["issue"]["acceptance_criteria"]), 0)
        self.assertIn("target_module", payload["issue"])
        self.assertIn("custom_fields", payload["issue"])

    def test_04_to_api_contract(self):
        """Validates generation of OpenAPI 3.1.0 contract with YAML front-matter."""
        text = self.sample_input_path.read_text(encoding="utf-8")
        fm, doc, formatted = RequestFormalizerEngine.to_api_contract(text, metadata={"id": "MVS-API-701"})

        self.assertEqual(fm["mvs_version"], "1.0.0")
        self.assertEqual(fm["format_type"], "api_contract_openapi")
        self.assertEqual(fm["id"], "MVS-API-701")

        self.assertEqual(doc["openapi"], "3.1.0")
        self.assertIn("paths", doc)
        self.assertIn("components", doc)
        self.assertIn("schemas", doc["components"])

        # Check front-matter delimiter
        self.assertTrue(formatted.startswith("---\n"))
        self.assertIn("\n---\n", formatted)

    def test_05_to_design_tokens(self):
        """Validates generation of UI Design & Accessibility tokens."""
        text = self.sample_input_path.read_text(encoding="utf-8")
        tokens = RequestFormalizerEngine.to_design_tokens(text, metadata={"id": "MVS-UI-701"})

        self.assertEqual(tokens["mvs_version"], "1.0.0")
        self.assertEqual(tokens["format_type"], "ui_design_tokens")
        self.assertEqual(tokens["id"], "MVS-UI-701")
        self.assertEqual(tokens["accessibility"]["wcag_target"], "WCAG_2_1_AA")
        self.assertIn("tokens", tokens)
        self.assertIn("color", tokens["tokens"])
        self.assertIn("typography", tokens["tokens"])
        self.assertIn("spacing", tokens["tokens"])

    def test_06_to_event_stream(self):
        """Validates generation of AsyncAPI 3.0.0 event stream specification."""
        text = self.sample_input_path.read_text(encoding="utf-8")
        fm, doc, formatted = RequestFormalizerEngine.to_event_stream(text, metadata={"id": "MVS-EVENT-701"})

        self.assertEqual(fm["mvs_version"], "1.0.0")
        self.assertEqual(fm["format_type"], "event_stream_asyncapi")
        self.assertEqual(fm["id"], "MVS-EVENT-701")

        self.assertEqual(doc["asyncapi"], "3.0.0")
        self.assertIn("channels", doc)
        self.assertIn("components", doc)
        self.assertIn("messages", doc["components"])
        self.assertTrue(formatted.startswith("---\n"))

    def test_07_formalize_and_persistence(self):
        """Validates end-to-end formalization and output capture in user/inputs/formal_requests/."""
        # Test converting improv1.md to all 4 formats
        formats = ["jira_story", "api_contract", "design_tokens", "event_stream"]
        for fmt in formats:
            res = RequestFormalizerEngine.formalize(
                input_data=self.sample_input_path,
                target_format=fmt,
                workspace_root=self.repo_root
            )
            self.assertEqual(res["status"], "FORMALIZED")
            self.assertTrue(Path(res["formal_file_path"]).exists())
            self.assertTrue(str(res["formal_file_path"]).startswith(str(self.formal_requests_dir)))
            self.assertGreater(Path(res["formal_file_path"]).stat().st_size, 50)
            self.assertIn("content_sha256", res)

    def test_08_run_through_workflow_and_merkle_seal(self):
        """Validates derivation workflow execution, context_ledger.yaml updating, and Merkle block sealing."""
        res = RequestFormalizerEngine.formalize(
            input_data=self.sample_input_path,
            target_format="jira_story",
            workspace_root=self.repo_root
        )
        formal_path = res["formal_file_path"]

        wf_res = RequestFormalizerEngine.run_through_workflow(
            formal_file_path=formal_path,
            workflow_name="derivation_pipeline",
            workspace_root=self.repo_root
        )

        self.assertEqual(wf_res["status"], "SUCCESS")
        self.assertIn("merkle_block_id", wf_res)
        self.assertIn("merkle_block_hash", wf_res)

        # Check ledger update
        ledger_path = self.repo_root / "context" / "ledger" / "context_ledger.yaml"
        self.assertTrue(ledger_path.exists())
        with open(ledger_path, "r", encoding="utf-8") as f:
            ledger_data = yaml.safe_load(f)

        self.assertIn("formal_requests", ledger_data)
        matches = [r for r in ledger_data["formal_requests"] if r["request_id"] == wf_res["request_id"]]
        self.assertGreater(len(matches), 0)

    def test_09_cli_formalize_execution(self):
        """Validates CLI command 'percipience formalize'."""
        cli_bin = self.repo_root / "workplace" / "bin" / "percipience"
        cmd = [
            str(cli_bin),
            "formalize",
            "--input", str(self.sample_input_path),
            "--format", "jira_story",
            "--run-workflow"
        ]
        proc = subprocess.run(cmd, cwd=str(self.repo_root), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"CLI execution failed:\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}")
        self.assertIn("Request formalized successfully!", proc.stdout)
        self.assertIn("Captured At: user/inputs/formal_requests/", proc.stdout)
        self.assertIn("Derivation workflow execution completed!", proc.stdout)
        self.assertIn("Merkle Block Sealed:", proc.stdout)


if __name__ == "__main__":
    unittest.main()
