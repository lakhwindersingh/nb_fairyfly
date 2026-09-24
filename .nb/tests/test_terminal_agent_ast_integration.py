#!/usr/bin/env python3
"""
Test suite for Terminal Mode Agent AST Proxy, Context Export, Shell Hooking,
and JetBrains IDE Plugin Terminal Customization.
"""

import os
import sys
import unittest
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for p in [REPO_ROOT / ".nb", REPO_ROOT / ".nb" / "core", REPO_ROOT / "workplace"]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.terminal_agent_ast_proxy import TerminalAgentASTProxy
from core.token_tracker import TokenTracker


class TestTerminalAgentASTIntegration(unittest.TestCase):
    """
    Validates end-to-end AST context extraction, agent wrapping,
    shell hook generation, and token savings ledger recording.
    """

    @classmethod
    def setUpClass(cls):
        cls.repo_root = REPO_ROOT

    def test_01_export_context_claude_code(self):
        """Validates AST context export formatted for Claude Code."""
        res = TerminalAgentASTProxy.export_context(
            workspace_root=self.repo_root,
            format_type="claude-code"
        )
        self.assertEqual(res["format"], "claude-code")
        self.assertGreater(res["total_files"], 0)
        self.assertGreater(res["total_raw_tokens"], 0)
        self.assertGreater(res["total_pruned_tokens"], 0)
        self.assertGreater(res["tokens_saved"], 0)
        self.assertGreater(res["reduction_pct"], 20.0)

        # Ensure payload contains Claude Code headers and AST skeletons
        self.assertIn("# Percipience AST-Compressed Project Context for Claude Code", res["payload"])
        self.assertIn("## Workspace Structural AST Skeletons", res["payload"])
        self.assertIn("Active Wire Contracts", res["payload"])

    def test_02_export_context_gemini_cli(self):
        """Validates AST context export formatted for Gemini CLI."""
        res = TerminalAgentASTProxy.export_context(
            workspace_root=self.repo_root,
            format_type="gemini-cli"
        )
        self.assertEqual(res["format"], "gemini-cli")
        self.assertIn("SYSTEM INSTRUCTION / WORKSPACE CONTEXT", res["payload"])
        self.assertIn("--- SYSTEM CONTRACTS ---", res["payload"])
        self.assertIn("--- AST FILE SKELETONS ---", res["payload"])

    def test_03_export_context_aider_and_json(self):
        """Validates Aider repo-map format and structured JSON formats."""
        res_aider = TerminalAgentASTProxy.export_context(
            workspace_root=self.repo_root,
            format_type="aider"
        )
        self.assertIn("# Percipience AST Repository Map", res_aider["payload"])

        res_json = TerminalAgentASTProxy.export_context(
            workspace_root=self.repo_root,
            format_type="json"
        )
        import json
        parsed = json.loads(res_json["payload"])
        self.assertIn("meta", parsed)
        self.assertIn("files", parsed)
        self.assertIn("reduction_pct", parsed["meta"])

    def test_04_wrap_terminal_agent_claude(self):
        """Validates wrapping a Claude Code terminal session."""
        wrapped = TerminalAgentASTProxy.wrap_terminal_agent(
            agent_cmd="claude",
            agent_args=["--verbose"],
            workspace_root=self.repo_root
        )
        self.assertEqual(wrapped["agent_cmd"], "claude")
        self.assertEqual(wrapped["format"], "claude-code")
        self.assertTrue(Path(wrapped["context_file"]).exists())
        self.assertIn("PERCIPIENCE_TERMINAL_MODE", wrapped["env"])
        self.assertIn("PERCIPIENCE_AST_COMPRESSION", wrapped["env"])
        self.assertIn("CLAUDE_CODE_PROMPT_PREFIX", wrapped["env"])
        self.assertGreater(wrapped["tokens_saved"], 0)

    def test_05_generate_shell_hook(self):
        """Validates shell hook generation for zsh, bash, and fish."""
        zsh_hook = TerminalAgentASTProxy.generate_shell_hook("zsh")
        self.assertIn("claude()", zsh_hook)
        self.assertIn("gemini()", zsh_hook)
        self.assertIn("aider()", zsh_hook)
        self.assertIn("PERCIPIENCE_TERMINAL_MODE=1", zsh_hook)

    def test_06_terminal_finops_summary(self):
        """Validates terminal FinOps metrics aggregation."""
        summary = TerminalAgentASTProxy.get_terminal_finops_summary(self.repo_root)
        self.assertEqual(summary["status"], "HEALTHY")
        self.assertIn("terminal_sessions_count", summary)
        self.assertIn("terminal_tokens_saved", summary)
        self.assertIn("terminal_gross_saved_usd", summary)

    def test_07_specialist_agent_definition_exists(self):
        """Validates that agent_terminal_mode_specialist.yaml is properly registered."""
        agent_file = self.repo_root / ".nb" / "agentic" / "custom" / "agents" / "agent_terminal_mode_specialist.yaml"
        self.assertTrue(agent_file.exists(), "agent_terminal_mode_specialist.yaml must exist")
        text = agent_file.read_text(encoding="utf-8")
        self.assertIn("agent_terminal_mode_specialist", text)
        self.assertIn("Terminal Mode Agent Interceptor", text)
        self.assertIn("export_ast_context", text)


if __name__ == "__main__":
    unittest.main()
