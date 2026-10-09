"""
Test suite for Enterprise CI/CD Sandboxing, OIDC Keyless Cloud Auth & Distributed Test Sharding (Section 16.4 in TODO.md).

Validates:
- TODO-COMP-12: Sub-Second MicroVM / gVisor & WASM Sandbox Isolation (MicroVMSandbox)
- TODO-COMP-13: OIDC Keyless Cloud Authentication & Workload Identity Federation (OIDCAuthenticator)
- TODO-COMP-14: Parallel Test Sharding & Multi-Architecture Matrix Dispatcher (DistributedTestRunner)
"""

import os
import sys
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from workplace.core.microvm_sandbox import (
    MicroVMSandbox,
    SandboxConfig,
    SandboxRuntime,
    SandboxExecutionResult
)
from workplace.core.oidc_authenticator import (
    OIDCAuthenticator,
    CloudCredentialResult
)
from workplace.core.distributed_test_runner import (
    DistributedTestRunner,
    MatrixNode,
    ShardExecutionReceipt,
    AggregatedTestReceipt
)


class TestMicroVMSandbox(unittest.TestCase):
    """Unit tests for MicroVM / gVisor / WASM Sandbox Isolation (TODO-COMP-12)."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.sandbox_mgr = MicroVMSandbox(workspace_root=Path(self.temp_dir))

    def tearDown(self):
        self.sandbox_mgr.terminate_all()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_01_sandbox_spawning_and_sub_second_boot(self):
        instance = self.sandbox_mgr.spawn(SandboxConfig(runtime="auto", memory_limit_mb=256))
        self.assertTrue(instance.is_active)
        self.assertLess(instance.boot_latency_ms, 500.0, "Boot latency must be sub-500ms")
        self.assertTrue(instance.scratch_dir.exists())

        boxes = self.sandbox_mgr.list_sandboxes()
        self.assertEqual(len(boxes), 1)
        self.assertEqual(boxes[0]["sandbox_id"], instance.sandbox_id)

    def test_02_sandbox_isolated_command_execution(self):
        instance = self.sandbox_mgr.spawn(SandboxConfig(runtime="process_jail"))
        res = instance.execute([sys.executable, "-c", "print('SANDBOX_TEST_PASS')"])
        self.assertEqual(res.exit_code, 0)
        self.assertIn("SANDBOX_TEST_PASS", res.stdout)
        self.assertTrue(res.sandboxed)
        self.assertGreater(res.duration_ms, 0.0)
        self.assertLessEqual(res.memory_peak_mb, 256.0)
        self.assertEqual(len(res.security_violations), 0)

    def test_03_sandbox_security_violation_detection(self):
        instance = self.sandbox_mgr.spawn()
        res = instance.execute("cat /etc/shadow 2>/dev/null || echo blocked")
        self.assertIn("PROHIBITED_SYSTEM_PATH_ACCESS_ATTEMPT", res.security_violations)

    def test_04_sandbox_timeout_handling(self):
        cfg = SandboxConfig(timeout_seconds=1)
        instance = self.sandbox_mgr.spawn(cfg)
        res = instance.execute([sys.executable, "-c", "import time; time.sleep(3)"])
        self.assertEqual(res.exit_code, 124)
        self.assertIn("EXECUTION_TIMEOUT_EXCEEDED", res.security_violations)

    def test_05_sandbox_lifecycle_and_scrubbing(self):
        instance = self.sandbox_mgr.spawn()
        scratch_path = instance.scratch_dir
        self.assertTrue(scratch_path.exists())

        instance.terminate()
        self.assertFalse(instance.is_active)
        self.assertFalse(scratch_path.exists())

        with self.assertRaises(RuntimeError):
            instance.execute("echo test")


class TestOIDCAuthenticator(unittest.TestCase):
    """Unit tests for OIDC Keyless Cloud Authentication (TODO-COMP-13)."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.auth = OIDCAuthenticator(workspace_root=Path(self.temp_dir))

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_01_keypair_and_jwks(self):
        jwks = self.auth.get_public_jwks()
        self.assertIn("keys", jwks)
        self.assertGreater(len(jwks["keys"]), 0)
        self.assertEqual(jwks["keys"][0]["kty"], "RSA")
        self.assertEqual(jwks["keys"][0]["alg"], "RS256")

    def test_02_mint_and_verify_token(self):
        token = self.auth.mint_workload_token(
            subject="agent_autonomous_coder",
            audience="sts.amazonaws.com",
            ttl_seconds=600
        )
        self.assertIsInstance(token, str)

        claims = self.auth.verify_token(token, expected_audience="sts.amazonaws.com")
        self.assertEqual(claims["iss"], "https://auth.percipience.internal")
        self.assertIn("agent_autonomous_coder", claims["sub"])
        self.assertEqual(claims["aud"], "sts.amazonaws.com")
        self.assertEqual(claims["actor"], "agent_autonomous_coder")

    def test_03_invalid_audience_rejection(self):
        token = self.auth.mint_workload_token(
            subject="agent_reviewer",
            audience="sts.amazonaws.com"
        )
        with self.assertRaises(Exception):
            self.auth.verify_token(token, expected_audience="https://iam.googleapis.com/target")

    def test_04_cloud_credential_federation_aws(self):
        token = self.auth.mint_workload_token(
            subject="agent_sec_tester",
            audience="sts.amazonaws.com"
        )
        cred = self.auth.exchange_cloud_credentials(
            token=token,
            provider="aws",
            role_arn_or_pool="arn:aws:iam::123456789012:role/PercipienceDeployer"
        )
        self.assertEqual(cred.provider, "AWS_IAM_STS")
        self.assertTrue(cred.access_token_id.startswith("ASIA"))
        self.assertIsNotNone(cred.session_token)
        self.assertEqual(cred.target_role, "arn:aws:iam::123456789012:role/PercipienceDeployer")

        # Verify audit record written
        audit = self.auth.get_exchange_audit_trail()
        self.assertGreater(len(audit), 0)
        self.assertEqual(audit[-1]["provider"], "AWS_IAM_STS")
        self.assertEqual(audit[-1]["status"], "FEDERATION_SUCCESS")

    def test_05_cloud_credential_federation_gcp_and_azure(self):
        token = self.auth.mint_workload_token(
            subject="agent_cloud_worker",
            audience="cloud_provider"
        )
        gcp_cred = self.auth.exchange_cloud_credentials(
            token=token,
            provider="gcp",
            role_arn_or_pool="//iam.googleapis.com/projects/123/locations/global/workloadIdentityPools/percipience-pool"
        )
        self.assertEqual(gcp_cred.provider, "GCP_WORKLOAD_IDENTITY")
        self.assertTrue(gcp_cred.access_token_id.startswith("ya29."))

        az_cred = self.auth.exchange_cloud_credentials(
            token=token,
            provider="azure",
            role_arn_or_pool="spn:00000000-0000-0000-0000-000000000000"
        )
        self.assertEqual(az_cred.provider, "AZURE_AD_FEDERATION")
        self.assertTrue(az_cred.access_token_id.startswith("eyJ"))


class TestDistributedTestRunner(unittest.TestCase):
    """Unit tests for Parallel Test Sharding & Matrix Dispatcher (TODO-COMP-14)."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.runner = DistributedTestRunner(workspace_root=Path(self.temp_dir))

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_01_sharding_strategies(self):
        tests = [f"test_module_{i}.py" for i in range(10)]

        # Round robin across 3 shards
        s0 = self.runner.shard_test_suite(tests, total_shards=3, shard_index=0, strategy="round_robin")
        s1 = self.runner.shard_test_suite(tests, total_shards=3, shard_index=1, strategy="round_robin")
        s2 = self.runner.shard_test_suite(tests, total_shards=3, shard_index=2, strategy="round_robin")

        # Disjoint verification
        self.assertEqual(len(set(s0) & set(s1)), 0)
        self.assertEqual(len(set(s1) & set(s2)), 0)
        self.assertEqual(len(set(s0) | set(s1) | set(s2)), 10)

        # Chunk strategy
        c0 = self.runner.shard_test_suite(tests, total_shards=2, shard_index=0, strategy="chunk")
        c1 = self.runner.shard_test_suite(tests, total_shards=2, shard_index=1, strategy="chunk")
        self.assertEqual(len(set(c0) | set(c1)), 10)

    def test_02_matrix_generation(self):
        spec = {
            "os": ["ubuntu-latest", "macos-latest"],
            "arch": ["amd64", "arm64"],
            "python": ["3.11"]
        }
        nodes = self.runner.generate_matrix(spec)
        self.assertEqual(len(nodes), 4)
        for node in nodes:
            self.assertIn("os", node.dimensions)
            self.assertIn("arch", node.dimensions)
            self.assertIn("python", node.dimensions)

    def test_03_run_and_aggregate_shards(self):
        tests = [f"workplace/tests/test_case_{i}.py" for i in range(6)]
        shard0 = self.runner.run_shard(shard_index=0, total_shards=2, tests=tests, dry_run=True)
        shard1 = self.runner.run_shard(shard_index=1, total_shards=2, tests=tests, dry_run=True)

        self.assertEqual(shard0.passed_count, 3)
        self.assertEqual(shard1.passed_count, 3)
        self.assertEqual(shard0.status, "PASSED")

        receipt = self.runner.aggregate_shard_reports([shard0, shard1])
        self.assertEqual(receipt.total_tests, 6)
        self.assertEqual(receipt.total_passed, 6)
        self.assertEqual(receipt.total_failed, 0)
        self.assertGreaterEqual(receipt.parallel_speedup_factor, 1.0)
        self.assertIsInstance(receipt.merkle_integrity_hash, str)
        self.assertTrue(receipt.receipt_id.startswith("RP_TEST_MATRIX_"))

        receipts = self.runner.get_matrix_receipts()
        self.assertEqual(len(receipts), 1)
        self.assertEqual(receipts[0]["receipt_id"], receipt.receipt_id)


if __name__ == "__main__":
    unittest.main()
