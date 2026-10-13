"""
Unit Tests for the Agent Registry, Rules & Contract Synchronizer
Verifies canonical source discovery, drift detection, idempotent reconciliation
of agent/rules/contracts registries, key-preservation semantics, and that the
live repository settings are fully in sync.
"""

import json
import tempfile
import unittest
from pathlib import Path

from core.agent_registry_synchronizer import AgentRegistrySynchronizer


class TestAgentRegistrySynchronizer(unittest.TestCase):

    def setUp(self):
        self.workspace_root = Path(__file__).resolve().parents[2]

    def _make_temp_workspace(self, agent_ids, registry_root, registry_claude, rules=None, contracts=None):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)

        agents = root / ".nb" / "agentic" / "custom" / "agents"
        agents.mkdir(parents=True, exist_ok=True)
        for aid in agent_ids:
            (agents / f"{aid}.yaml").write_text(f'agent_id: "{aid}"\n', encoding="utf-8")

        for rel_dir, files in ((".nb/context/rules", rules or {}), (".nb/context/contracts", contracts or {})):
            target = root / rel_dir
            target.mkdir(parents=True, exist_ok=True)
            for name, content in files.items():
                (target / name).write_text(content, encoding="utf-8")

        (root / "settings.json").write_text(
            json.dumps(registry_root, indent=2) + "\n", encoding="utf-8"
        )
        claude = root / ".claude"
        claude.mkdir(parents=True, exist_ok=True)
        (claude / "settings.json").write_text(
            json.dumps(registry_claude, indent=2) + "\n", encoding="utf-8"
        )
        self.addCleanup(tmp.cleanup)
        return root

    def _blank_settings(self):
        return {"agent_registry": [], "context_rules": {}, "context_contracts": {}}

    def test_01_scan_agent_ids_from_directory(self):
        """Scans canonical agent_ids from YAML manifests, sorted and de-duplicated."""
        root = self._make_temp_workspace(["agent_zeta", "agent_alpha", "agent_alpha"], self._blank_settings(), self._blank_settings())
        syncer = AgentRegistrySynchronizer(root)
        self.assertEqual(syncer.scan_agent_ids(), ["agent_alpha", "agent_zeta"])

    def test_02_scan_falls_back_to_stem(self):
        """Manifests without an explicit agent_id fall back to the agent_ prefixed stem."""
        root = self._make_temp_workspace([], self._blank_settings(), self._blank_settings())
        agents = root / ".nb" / "agentic" / "custom" / "agents"
        (agents / "quality_guard.yaml").write_text("name: Quality Guard\n", encoding="utf-8")
        syncer = AgentRegistrySynchronizer(root)
        self.assertEqual(syncer.scan_agent_ids(), ["agent_quality_guard"])

    def test_03_check_detects_agent_drift(self):
        """check() reports missing and extra agent entries without mutating files."""
        root_settings = self._blank_settings()
        root_settings["agent_registry"] = ["agent_alpha", "agent_stale"]
        claude_settings = self._blank_settings()
        claude_settings["agent_registry"] = ["agent_alpha", "agent_beta"]
        root = self._make_temp_workspace(["agent_alpha", "agent_beta"], root_settings, claude_settings)

        report = AgentRegistrySynchronizer(root).check()
        self.assertTrue(report["drift"])
        root_file = report["files"]["settings.json"]["agent_registry"]
        self.assertEqual(root_file["missing"], ["agent_beta"])
        self.assertEqual(root_file["extra"], ["agent_stale"])
        self.assertTrue(report["files"][".claude/settings.json"]["agent_registry"]["in_sync"])

    def test_04_preserves_existing_keys_and_adds_new(self):
        """Existing symbolic keys are preserved; new files receive derived keys."""
        rules = {
            "jetbrains_platform_threading_rules.md": "rule",
            "zero_trust_rules.md": "rule",
        }
        current = self._blank_settings()
        current["context_rules"] = {
            "merkle_ledger": ".nb/context/ledger/context_ledger.yaml",
            "jetbrains_threading": ".nb/context/rules/jetbrains_platform_threading_rules.md",
        }
        root = self._make_temp_workspace([], current, self._blank_settings(), rules=rules)
        desired = AgentRegistrySynchronizer(root)._project(current)["context_rules"]

        self.assertEqual(desired["jetbrains_threading"], ".nb/context/rules/jetbrains_platform_threading_rules.md")
        self.assertEqual(desired["zero_trust_rules"], ".nb/context/rules/zero_trust_rules.md")
        self.assertEqual(desired["merkle_ledger"], ".nb/context/ledger/context_ledger.yaml")

    def test_05_sync_is_idempotent_across_all_sections(self):
        """sync() projects all sections then becomes a no-op on re-run."""
        current = self._blank_settings()
        current["context_contracts"] = {"stale": ".nb/context/contracts/daemon_rpc_contract.json"}
        contracts = {"daemon_rpc_contract.json": "{}", "new_contract.json": "{}"}
        root = self._make_temp_workspace(
            ["agent_alpha", "agent_beta"], current, self._blank_settings(), contracts=contracts
        )
        syncer = AgentRegistrySynchronizer(root)

        first = syncer.sync()
        self.assertEqual(first["status"], "SYNCHRONIZED")
        self.assertIn("settings.json", first["updated"])
        self.assertIn(".claude/settings.json", first["updated"])

        second = syncer.sync()
        self.assertEqual(second["status"], "IN_SYNC")
        self.assertEqual(second["updated"], [])
        self.assertFalse(syncer.check()["drift"])

        # Pre-existing key retained, new file added with derived key.
        desired = syncer._project(syncer._read_settings(root / "settings.json"))["context_contracts"]
        self.assertEqual(desired["stale"], ".nb/context/contracts/daemon_rpc_contract.json")
        self.assertEqual(desired["new_contract"], ".nb/context/contracts/new_contract.json")

    def test_06_live_repository_registries_in_sync(self):
        """Committed settings files fully match the canonical agents/rules/contracts sources."""
        syncer = AgentRegistrySynchronizer(self.workspace_root)
        self.assertGreaterEqual(len(syncer.scan_agent_ids()), 30)
        self.assertGreaterEqual(len(syncer.scan_files(syncer.RULES_DIR)), 10)
        self.assertGreaterEqual(len(syncer.scan_files(syncer.CONTRACTS_DIR)), 20)
        self.assertFalse(syncer.check()["drift"], "Registry drift detected in live settings files")


if __name__ == "__main__":
    unittest.main()
