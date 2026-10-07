#!/usr/bin/env python3
"""
Unit Test Suite for Capability-Based Access Control (CBAC) Sandbox Tokens (TODO-AGT-05 / GAP-AGT-05)
Validates HMAC-SHA256 capability tokens, path-bound write enforcements,
subprocess command whitelisting, and network egress firewalling.
"""

import os
import sys
import tempfile
import time
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for p in [REPO_ROOT / ".nb", REPO_ROOT / ".nb" / "core", REPO_ROOT / "workplace", REPO_ROOT / "workplace" / "core"]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.agent_capability_guard import AgentCapabilityGuard


class TestAgentCapabilityGuard(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.worktree_dir = Path(self.tmp_dir.name) / "worktree_mod_auth"
        self.worktree_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_01_token_minting_and_cryptographic_verification(self):
        """Validates minting, valid verification, and tampering rejection."""
        token = AgentCapabilityGuard.mint_token(
            agent_id="agent_auth_specialist",
            worktree_path=str(self.worktree_dir),
            allowed_operations=["CAP_FS_READ", "CAP_FS_WRITE_MODULE_ONLY"],
            ttl_seconds=300
        )
        self.assertIn(".", token)

        # Verification succeeds
        valid, payload, err = AgentCapabilityGuard.verify_token(token)
        self.assertTrue(valid)
        self.assertIsNone(err)
        self.assertEqual(payload["agent_id"], "agent_auth_specialist")
        self.assertIn("CAP_FS_READ", payload["allowed_operations"])

        # Tampered token rejected
        tampered_token = token[:-4] + "abcd"
        valid, payload, err = AgentCapabilityGuard.verify_token(tampered_token)
        self.assertFalse(valid)
        self.assertIn("PERMISSION_DENIED_INVALID_TOKEN", err)

        # Expired token rejected
        expired_token = AgentCapabilityGuard.mint_token(
            agent_id="agent_fast",
            worktree_path=str(self.worktree_dir),
            allowed_operations=["CAP_FS_READ"],
            ttl_seconds=-10  # Already expired
        )
        valid, payload, err = AgentCapabilityGuard.verify_token(expired_token)
        self.assertFalse(valid)
        self.assertIn("PERMISSION_DENIED_EXPIRED_TOKEN", err)

    def test_02_path_bound_filesystem_write_enforcement(self):
        """Validates that writes within worktree succeed while protected or out-of-bounds paths fail."""
        token = AgentCapabilityGuard.mint_token(
            agent_id="agent_worker",
            worktree_path=str(self.worktree_dir),
            allowed_operations=["CAP_FS_READ", "CAP_FS_WRITE_MODULE_ONLY"]
        )

        # 1. Allowed path within worktree
        target_in_worktree = self.worktree_dir / "src" / "auth.py"
        allowed, err = AgentCapabilityGuard.check_fs_access(token, str(target_in_worktree), operation="write")
        self.assertTrue(allowed)
        self.assertIsNone(err)

        # 2. Blocked write outside worktree
        outside_path = Path(self.tmp_dir.name) / "other_module" / "secret.py"
        allowed, err = AgentCapabilityGuard.check_fs_access(token, str(outside_path), operation="write")
        self.assertFalse(allowed)
        self.assertIn("PERMISSION_DENIED_PATH_RESTRICTED", err)

        # 3. Blocked write to protected directory (.nb/core)
        protected_target = REPO_ROOT / ".nb" / "core" / "malicious.py"
        allowed, err = AgentCapabilityGuard.check_fs_access(token, str(protected_target), operation="write", repo_root=REPO_ROOT)
        self.assertFalse(allowed)
        self.assertIn("PERMISSION_DENIED_PATH_RESTRICTED", err)

        # 4. Traversal attempt using ../
        traversal_path = str(self.worktree_dir / ".." / "escaped.txt")
        allowed, err = AgentCapabilityGuard.check_fs_access(token, traversal_path, operation="write")
        self.assertFalse(allowed)
        self.assertIn("PERMISSION_DENIED_PATH_RESTRICTED", err)

    def test_03_subprocess_command_whitelist_and_blocking(self):
        """Validates command execution checking against whitelist and blocking dangerous binaries."""
        token = AgentCapabilityGuard.mint_token(
            agent_id="agent_qa",
            worktree_path=str(self.worktree_dir),
            allowed_operations=["CAP_EXEC_SUBPROCESS"]
        )

        # 1. Whitelisted commands allowed
        allowed, err = AgentCapabilityGuard.check_subprocess_command(token, "pytest workplace/tests")
        self.assertTrue(allowed)
        self.assertIsNone(err)

        allowed, err = AgentCapabilityGuard.check_subprocess_command(token, ["git", "diff", "--stat"])
        self.assertTrue(allowed)
        self.assertIsNone(err)

        # 2. Dangerous commands blocked
        for dangerous_cmd in ["curl https://malicious.site", "wget http://evil.com", "rm -rf /", "nc -l 8080"]:
            allowed, err = AgentCapabilityGuard.check_subprocess_command(token, dangerous_cmd)
            self.assertFalse(allowed)
            self.assertIn("PERMISSION_DENIED_UNAUTHORIZED_COMMAND", err)

        # 3. Non-whitelisted binary blocked
        allowed, err = AgentCapabilityGuard.check_subprocess_command(token, "arbitrary_binary run")
        self.assertFalse(allowed)
        self.assertIn("PERMISSION_DENIED_UNAUTHORIZED_COMMAND", err)

        # 4. Missing CAP_EXEC_SUBPROCESS rejected
        read_only_token = AgentCapabilityGuard.mint_token(
            agent_id="agent_reader",
            worktree_path=str(self.worktree_dir),
            allowed_operations=["CAP_FS_READ"]
        )
        allowed, err = AgentCapabilityGuard.check_subprocess_command(read_only_token, "pytest")
        self.assertFalse(allowed)
        self.assertIn("CAP_EXEC_SUBPROCESS required", err)

    def test_04_network_egress_firewall(self):
        """Validates that loopback sockets are allowed while external egress requires capability flag."""
        restricted_token = AgentCapabilityGuard.mint_token(
            agent_id="agent_isolated",
            worktree_path=str(self.worktree_dir),
            allowed_operations=["CAP_FS_READ"]
        )

        # Loopback permitted for test bridges
        allowed, err = AgentCapabilityGuard.check_network_egress(restricted_token, "127.0.0.1", 8080)
        self.assertTrue(allowed)
        self.assertIsNone(err)

        # External egress blocked without CAP_NETWORK_EGRESS
        allowed, err = AgentCapabilityGuard.check_network_egress(restricted_token, "api.anthropic.com", 443)
        self.assertFalse(allowed)
        self.assertIn("PERMISSION_DENIED_NETWORK_EGRESS_BLOCKED", err)

        # External egress permitted with CAP_NETWORK_EGRESS
        egress_token = AgentCapabilityGuard.mint_token(
            agent_id="agent_cloud_sync",
            worktree_path=str(self.worktree_dir),
            allowed_operations=["CAP_NETWORK_EGRESS"]
        )
        allowed, err = AgentCapabilityGuard.check_network_egress(egress_token, "api.anthropic.com", 443)
        self.assertTrue(allowed)
        self.assertIsNone(err)


if __name__ == "__main__":
    unittest.main()
