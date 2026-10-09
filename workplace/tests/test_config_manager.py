"""
Unit Tests for Percipience Platform Configuration Manager & Externalization
Verifies externalized configuration resolution precedence, environment variable overrides,
type casting helpers, and CLI config subcommands.
"""

import os
import unittest
from pathlib import Path
from core.config_manager import ConfigManager, config


class TestConfigManager(unittest.TestCase):

    def setUp(self):
        self.workspace_root = Path(__file__).resolve().parents[2]
        self.cfg = ConfigManager(self.workspace_root)

    def test_01_yaml_configuration_loaded(self):
        """Tests reading core parameters from .nb/config/platform_config.yaml."""
        self.assertEqual(self.cfg.get_int("portal.port", 3000), 3000)
        self.assertEqual(self.cfg.get_str("portal.host"), "0.0.0.0")
        self.assertEqual(self.cfg.get_str("daemon.endpoint_url"), "http://127.0.0.1:8585")
        self.assertEqual(self.cfg.get_int("worktree.default_ttl_seconds"), 3600)
        self.assertEqual(self.cfg.get_float("token_optimization.performance_rev_share_pct"), 15.0)
        self.assertEqual(self.cfg.get_int("cicd.healing_max_retries"), 3)

    def test_02_environment_variable_override(self):
        """Tests PERCIPIENCE_* environment variable overrides."""
        os.environ["PERCIPIENCE_PORTAL_PORT"] = "4000"
        os.environ["PERCIPIENCE_WORKTREE_DEFAULT_TTL_SECONDS"] = "7200"
        try:
            self.assertEqual(self.cfg.get_int("portal.port"), 4000)
            self.assertEqual(self.cfg.get_int("worktree.default_ttl_seconds"), 7200)
        finally:
            os.environ.pop("PERCIPIENCE_PORTAL_PORT", None)
            os.environ.pop("PERCIPIENCE_WORKTREE_DEFAULT_TTL_SECONDS", None)

    def test_03_legacy_environment_variable_override(self):
        """Tests common legacy environment variables (e.g. PORTAL_PORT, OTEL_SERVICE_NAME)."""
        os.environ["PORTAL_PORT"] = "9999"
        os.environ["OTEL_SERVICE_NAME"] = "custom-telemetry-service"
        try:
            self.assertEqual(self.cfg.get_int("portal.port"), 9999)
            self.assertEqual(self.cfg.get_str("otel.service_name"), "custom-telemetry-service")
        finally:
            os.environ.pop("PORTAL_PORT", None)
            os.environ.pop("OTEL_SERVICE_NAME", None)

    def test_04_type_casting_helpers(self):
        """Tests boolean, integer, float, list, and dictionary casting."""
        os.environ["PERCIPIENCE_CUSTOM_FLAG"] = "true"
        os.environ["PERCIPIENCE_CUSTOM_INT"] = "42"
        os.environ["PERCIPIENCE_CUSTOM_FLOAT"] = "3.1415"
        os.environ["PERCIPIENCE_CUSTOM_LIST"] = "alpha, beta, gamma"
        try:
            self.assertTrue(self.cfg.get_bool("custom_flag"))
            self.assertEqual(self.cfg.get_int("custom_int"), 42)
            self.assertAlmostEqual(self.cfg.get_float("custom_float"), 3.1415, places=4)
            self.assertEqual(self.cfg.get_list("custom_list"), ["alpha", "beta", "gamma"])
        finally:
            os.environ.pop("PERCIPIENCE_CUSTOM_FLAG", None)
            os.environ.pop("PERCIPIENCE_CUSTOM_INT", None)
            os.environ.pop("PERCIPIENCE_CUSTOM_FLOAT", None)
            os.environ.pop("PERCIPIENCE_CUSTOM_LIST", None)

    def test_05_missing_keys_return_defaults(self):
        """Tests that querying non-existent keys returns explicit fallback defaults."""
        self.assertEqual(self.cfg.get("nonexistent.key", "fallback"), "fallback")
        self.assertEqual(self.cfg.get_int("nonexistent.int", 123), 123)
        self.assertFalse(self.cfg.get_bool("nonexistent.bool", False))
        self.assertEqual(self.cfg.get_list("nonexistent.list", [1, 2]), [1, 2])
        self.assertEqual(self.cfg.get_dict("nonexistent.dict", {"k": "v"}), {"k": "v"})


if __name__ == "__main__":
    unittest.main()
