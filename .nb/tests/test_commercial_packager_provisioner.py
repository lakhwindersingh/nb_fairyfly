#!/usr/bin/env python3
"""
Unit and Integration Tests for Percipience Commercial Packager, Provisioner & Permissioning Engine.
Verifies tier packaging, asset filtering, license cryptographic sealing,
multi-IDE and SaaS portal provisioning, and feature gating.
"""

import sys
import json
import yaml
import shutil
import unittest
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / ".nb"))
sys.path.insert(0, str(REPO_ROOT / ".nb" / "core"))
sys.path.insert(0, str(REPO_ROOT / "workplace"))

from core.commercial_packager_provisioner import CommercialPackagerProvisioner


class TestCommercialPackagerProvisioner(unittest.TestCase):
    """Test suite for CommercialPackagerProvisioner and CLI commands."""

    def setUp(self):
        self.repo_root = REPO_ROOT
        self.test_bundle_dir = self.repo_root / ".nb" / "bundles" / "test_pkg_out"
        if self.test_bundle_dir.exists():
            shutil.rmtree(self.test_bundle_dir)

    def tearDown(self):
        if self.test_bundle_dir.exists():
            shutil.rmtree(self.test_bundle_dir)

    def test_01_tier_spec_retrieval(self):
        """Verifies pricing models, seat allocations, and rules for all tiers."""
        free_spec = CommercialPackagerProvisioner.get_tier_spec("free", self.repo_root)
        self.assertEqual(free_spec["tier_id"], "plan_free")
        self.assertEqual(free_spec["base_price_monthly_usd"], 0)
        self.assertEqual(free_spec["included_seats"], 1)
        self.assertFalse(free_spec["rules"]["expose_basic_platform_tools"])

        ent_spec = CommercialPackagerProvisioner.get_tier_spec("enterprise", self.repo_root)
        self.assertEqual(ent_spec["tier_id"], "plan_enterprise")
        self.assertEqual(ent_spec["base_price_monthly_usd"], 9999)
        self.assertEqual(ent_spec["included_seats"], -1) # Unlimited
        self.assertTrue(ent_spec["rules"]["allow_private_vpc"])

    def test_02_free_tier_packaging_and_filtering(self):
        """Tests asset filtering and bundling for Free Community tier."""
        pkg_res = CommercialPackagerProvisioner.package_tier(
            workspace_root=self.repo_root,
            tier="free",
            output_dir=self.test_bundle_dir,
            tenant_id="tenant_free_test"
        )
        self.assertEqual(pkg_res["status"], "PACKAGED")
        self.assertEqual(pkg_res["tier"], "plan_free")
        self.assertTrue(Path(pkg_res["package_dir"]).exists())

        # License file check
        lic_file = Path(pkg_res["package_dir"]) / "PERCIPIENCE_LICENSE.json"
        self.assertTrue(lic_file.exists())
        lic_data = json.loads(lic_file.read_text(encoding="utf-8"))
        self.assertEqual(lic_data["tier"], "plan_free")
        self.assertIsNotNone(lic_data.get("signature_sha256"))

        # Check that core contains essential engines but respects Free rules
        bundled_files = pkg_res["bundled_files"]
        self.assertTrue(any("core/merkle_engine.py" in f for f in bundled_files))
        self.assertTrue(any("bin/percipience" in f for f in bundled_files))

    def test_03_enterprise_tier_packaging(self):
        """Tests bundling for Enterprise Dedicated tier."""
        pkg_res = CommercialPackagerProvisioner.package_tier(
            workspace_root=self.repo_root,
            tier="enterprise",
            output_dir=self.test_bundle_dir,
            tenant_id="tenant_enterprise_test"
        )
        self.assertEqual(pkg_res["status"], "PACKAGED")
        self.assertEqual(pkg_res["tier"], "plan_enterprise")
        self.assertGreater(pkg_res["total_files"], 80)

    def test_04_cross_platform_provisioning(self):
        """Tests provisioning across IntelliJ, VSCode, and SaaS portal."""
        prov_res = CommercialPackagerProvisioner.provision_target(
            workspace_root=self.repo_root,
            tenant_id="tenant_provision_test",
            tier="team",
            target="all"
        )
        self.assertEqual(prov_res["status"], "PROVISIONED")
        self.assertEqual(prov_res["tenant_id"], "tenant_provision_test")
        self.assertEqual(prov_res["tier"], "plan_team")
        self.assertIn("mod_intellij_plugin", prov_res["provisioned_targets"])
        self.assertIn("mod_vscode_extension", prov_res["provisioned_targets"])
        self.assertIn("saas_portal_gateway", prov_res["provisioned_targets"])

        # Check IntelliJ license file
        ij_lic = self.repo_root / "workplace" / "modules" / "mod_intellij_plugin" / "src" / "main" / "resources" / "percipience" / "tenant_license.json"
        self.assertTrue(ij_lic.exists())

        # Check tenant hierarchy
        tenant_file = self.repo_root / ".nb" / "context" / "tenant_hierarchy.json"
        data = json.loads(tenant_file.read_text(encoding="utf-8"))
        self.assertIn("tenant_provision_test", data.get("tenants", {}))

    def test_05_permission_verification(self):
        """Tests permission checking and feature gating logic."""
        # Free Tier Checks
        res_free_tools = CommercialPackagerProvisioner.verify_permissions(
            self.repo_root, "plan_free", "basic_platform_tools_exposure"
        )
        self.assertFalse(res_free_tools["allowed"])

        res_free_ast = CommercialPackagerProvisioner.verify_permissions(
            self.repo_root, "plan_free", "ast_token_pruning"
        )
        self.assertTrue(res_free_ast["allowed"])

        # Enterprise Tier Checks
        res_ent_vpc = CommercialPackagerProvisioner.verify_permissions(
            self.repo_root, "plan_enterprise", "private_vpc_deploy"
        )
        self.assertTrue(res_ent_vpc["allowed"])

    def test_06_cli_subcommands(self):
        """Tests CLI execution of package, provision, and permission commands."""
        # 1. Package CLI
        cmd_pkg = [str(self.repo_root / ".nb" / "bin" / "percipience"), "package", "--tier", "free"]
        p1 = subprocess.run(cmd_pkg, capture_output=True, text=True, cwd=self.repo_root)
        self.assertEqual(p1.returncode, 0, f"STDOUT: {p1.stdout} STDERR: {p1.stderr}")
        self.assertIn("Packaging complete: PACKAGED", p1.stdout)

        # 2. Provision CLI
        cmd_prov = [str(self.repo_root / ".nb" / "bin" / "percipience"), "provision", "--tenant", "tenant_cli_test", "--tier", "business", "--target", "intellij"]
        p2 = subprocess.run(cmd_prov, capture_output=True, text=True, cwd=self.repo_root)
        self.assertEqual(p2.returncode, 0, f"STDOUT: {p2.stdout} STDERR: {p2.stderr}")
        self.assertIn("Provisioning complete: PROVISIONED", p2.stdout)

        # 3. Permission CLI
        cmd_perm = [str(self.repo_root / ".nb" / "bin" / "percipience"), "permission", "check", "--tier", "free", "--feature", "private_vpc_deploy"]
        p3 = subprocess.run(cmd_perm, capture_output=True, text=True, cwd=self.repo_root)
        self.assertEqual(p3.returncode, 0, f"STDOUT: {p3.stdout} STDERR: {p3.stderr}")
        self.assertIn("Allowed: False", p3.stdout)

    def test_07_agent_and_workflow_manifests(self):
        """Verifies that the specialist agent and delivery workflow manifests exist and are valid YAML."""
        agent_file = self.repo_root / ".nb" / "agentic" / "custom" / "agents" / "agent_commercial_packager_provisioner.yaml"
        self.assertTrue(agent_file.exists())
        agent_data = yaml.safe_load(agent_file.read_text(encoding="utf-8"))
        self.assertEqual(agent_data["agent_id"], "agent_commercial_packager_provisioner")

        wf_file = self.repo_root / ".nb" / "agentic" / "custom" / "workflows" / "commercial_packaging_provisioning_flow.yaml"
        self.assertTrue(wf_file.exists())
        wf_data = yaml.safe_load(wf_file.read_text(encoding="utf-8"))
        self.assertEqual(wf_data["name"], "commercial_packaging_provisioning_flow")
        self.assertGreaterEqual(len(wf_data.get("steps", [])), 5)


if __name__ == "__main__":
    unittest.main()
