"""
Unit Tests for the Agent Registry Synchronizer
Verifies canonical agent-id discovery, drift detection, idempotent reconciliation
of settings registries, and that the live repository settings are in sync.
"""

import json
import tempfile
import unittest
from pathlib import Path

from core.agent_registry_synchronizer import AgentRegistrySynchronizer


class TestAgentRegistrySynchronizer(unittest.TestCase):

    def setUp(self):
        self.workspace_root = Path(__file__).resolve().parents[2]

    def _make_temp_workspace(self, agent_ids, registry_root, registry_claude):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        agents = root / ".nb" / "agentic" / "custom" / "agents"
        agents.mkdir(parents=True, exist_ok=True)
        for aid in agent_ids:
            (agents / f"{aid}.yaml").write_text(f'agent_id: "{aid}"\n', encoding="utf-8")

        (root / "settings.json").write_text(
            json.dumps({"agent_registry": registry_root}, indent=2) + "\n", encoding="utf-8"
        )
        claude = root / ".claude"
        claude.mkdir(parents=True, exist_ok=True)
        (claude / "settings.json").write_text(
            json.dumps({"agent_registry": registry_claude}, indent=2) + "\n", encoding="utf-8"
        )
        self.addCleanup(tmp.cleanup)
        return root

    def test_01_scan_agent_ids_from_directory(self):
        """Scans canonical agent_ids from YAML manifests, sorted and de-duplicated."""
        root = self._make_temp_workspace(
            ["agent_zeta", "agent_alpha", "agent_alpha"], [], []
        )
        syncer = AgentRegistrySynchronizer(root)
        self.assertEqual(syncer.scan_agent_ids(), ["agent_alpha", "agent_zeta"])

    def test_02_scan_falls_back_to_stem(self):
        """Manifests without an explicit agent_id fall back to the agent_ prefixed stem."""
        root = self._make_temp_workspace([], [], [])
        agents = root / ".nb" / "agentic" / "custom" / "agents"
        (agents / "quality_guard.yaml").write_text("name: Quality Guard\n", encoding="utf-8")
        syncer = AgentRegistrySynchronizer(root)
        self.assertEqual(syncer.scan_agent_ids(), ["agent_quality_guard"])

    def test_03_check_detects_drift(self):
        """check() reports missing and extra entries without mutating files."""
        root = self._make_temp_workspace(
            ["agent_alpha", "agent_beta"],
            registry_root=["agent_alpha", "agent_stale"],
            registry_claude=["agent_alpha", "agent_beta"],
        )
        syncer = AgentRegistrySynchronizer(root)
        report = syncer.check()
        self.assertTrue(report["drift"])
        root_file = report["files"]["settings.json"]
        self.assertEqual(root_file["missing"], ["agent_beta"])
        self.assertEqual(root_file["extra"], ["agent_stale"])
        self.assertTrue(report["files"][".claude/settings.json"]["in_sync"])

    def test_04_sync_is_idempotent(self):
        """sync() projects the canonical set then becomes a no-op on re-run."""
        root = self._make_temp_workspace(
            ["agent_alpha", "agent_beta"],
            registry_root=["agent_stale"],
            registry_claude=[],
        )
        syncer = AgentRegistrySynchronizer(root)

        first = syncer.sync()
        self.assertEqual(first["status"], "SYNCHRONIZED")
        self.assertIn("settings.json", first["updated"])
        self.assertIn(".claude/settings.json", first["updated"])

        second = syncer.sync()
        self.assertEqual(second["status"], "IN_SYNC")
        self.assertEqual(second["updated"], [])
        self.assertEqual(sorted(second["unchanged"]), [".claude/settings.json", "settings.json"])
        self.assertFalse(syncer.check()["drift"])

    def test_05_live_repository_registries_in_sync(self):
        """The committed settings.json and .claude/settings.json registries match the agents dir."""
        syncer = AgentRegistrySynchronizer(self.workspace_root)
        self.assertGreaterEqual(len(syncer.scan_agent_ids()), 30)
        self.assertFalse(syncer.check()["drift"], "Agent registry drift detected in live settings files")


if __name__ == "__main__":
    unittest.main()
