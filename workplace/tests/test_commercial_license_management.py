import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
from workplace.core.commercial_packager_provisioner import CommercialPackagerProvisioner


class TestCommercialLicenseManagement(unittest.TestCase):
    """
    Test suite for Commercial License Minting, Signing, Installation,
    and Post-Payment Self-Generation Engine (PROP-LIC-001).
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.workspace_root = Path(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_01_mint_free_tier_license(self):
        """Validates minting a Free Community Tier license."""
        lic = CommercialPackagerProvisioner.generate_license(
            workspace_root=self.workspace_root,
            tier="plan_free",
            tenant_id="tenant_solo_dev"
        )
        self.assertEqual(lic["tier"], "plan_free")
        self.assertEqual(lic["included_seats"], 1)
        self.assertEqual(lic["included_concurrent_worktrees"], 1)
        self.assertEqual(lic["included_pr_audits_monthly"], 500)
        self.assertIsNotNone(lic["signature_sha256"])
        self.assertTrue(lic["license_id"].startswith("lic_plan_free_"))

    def test_02_mint_team_tier_license(self):
        """Validates minting a Team Tier license."""
        lic = CommercialPackagerProvisioner.generate_license(
            workspace_root=self.workspace_root,
            tier="plan_team",
            tenant_id="tenant_startup_inc"
        )
        self.assertEqual(lic["tier"], "plan_team")
        self.assertEqual(lic["included_seats"], 15)
        self.assertEqual(lic["included_concurrent_worktrees"], 5)
        self.assertEqual(lic["included_pr_audits_monthly"], 5000)
        self.assertIsNotNone(lic["signature_sha256"])

    def test_03_mint_business_tier_license_with_overrides(self):
        """Validates minting a Business Tier license with custom quota overrides."""
        lic = CommercialPackagerProvisioner.generate_license(
            workspace_root=self.workspace_root,
            tier="plan_business",
            tenant_id="tenant_growth_co",
            seats=80,
            worktrees=25,
            audits=35000
        )
        self.assertEqual(lic["tier"], "plan_business")
        self.assertEqual(lic["included_seats"], 80)
        self.assertEqual(lic["included_concurrent_worktrees"], 25)
        self.assertEqual(lic["included_pr_audits_monthly"], 35000)
        self.assertTrue(lic["entitled_features"]["nbpack_obfuscation"])

    def test_04_mint_enterprise_dedicated_license(self):
        """Validates minting an Enterprise Dedicated license with unlimited quotas."""
        lic = CommercialPackagerProvisioner.generate_license(
            workspace_root=self.workspace_root,
            tier="plan_enterprise",
            tenant_id="tenant_acme_bank",
            tenant_name="Acme International Bank"
        )
        self.assertEqual(lic["tier"], "plan_enterprise")
        self.assertEqual(lic["included_seats"], -1)
        self.assertEqual(lic["included_concurrent_worktrees"], -1)
        self.assertEqual(lic["included_pr_audits_monthly"], -1)
        self.assertTrue(lic["entitled_features"]["private_vpc_deploy"])
        self.assertTrue(lic["entitled_features"]["dedicated_slack_sla"])

    def test_05_install_license_into_workspace(self):
        """Validates installation of a license into .nb/context/tenant_license.json."""
        lic = CommercialPackagerProvisioner.generate_license(
            workspace_root=self.workspace_root,
            tier="plan_enterprise",
            tenant_id="tenant_acme_bank"
        )
        inst_res = CommercialPackagerProvisioner.install_license(self.workspace_root, lic)
        self.assertEqual(inst_res["status"], "INSTALLED")
        target_path = Path(inst_res["installed_path"])
        self.assertTrue(target_path.exists())

        active = CommercialPackagerProvisioner.get_active_license(self.workspace_root)
        self.assertEqual(active["tier"], "plan_enterprise")
        self.assertTrue(active["is_installed"])
        self.assertEqual(active["license_id"], lic["license_id"])

    def test_06_post_payment_self_generation_hook(self):
        """Validates autonomous self-generation of license after payment confirmation."""
        payment_payload = {
            "payment_id": "ch_stripe_autotest_9981",
            "tenant_id": "tenant_stripe_buyer",
            "tenant_name": "Stripe Buyer Org",
            "tier": "plan_business"
        }
        res = CommercialPackagerProvisioner.self_generate_license_after_payment(
            self.workspace_root,
            payment_payload
        )
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["license"]["payment_reference"], "ch_stripe_autotest_9981")
        self.assertEqual(res["license"]["tier"], "plan_business")

        # Verify audit file was written
        audit_file = self.workspace_root / ".nb" / "context" / "ledger" / "payment_license_audit.jsonl"
        self.assertTrue(audit_file.exists())
        audit_content = audit_file.read_text(encoding="utf-8")
        self.assertIn("POST_PAYMENT_LICENSE_SELF_GENERATED", audit_content)
        self.assertIn("ch_stripe_autotest_9981", audit_content)

        # Verify active license
        active = CommercialPackagerProvisioner.get_active_license(self.workspace_root)
        self.assertEqual(active["tier"], "plan_business")
        self.assertEqual(active["payment_reference"], "ch_stripe_autotest_9981")


    def test_07_tier_gated_workflow_and_hook_bundling(self):
        """Validates per-tier workflow gating (mirrors CORE_TIER_RULES) and git hook bundling."""
        expected_workflows = {
            "plan_free": {"basic_autonomous_cicd.yaml", "intellij_pycharm_plugin_delivery_flow.yaml"},
            "plan_team": {"basic_autonomous_cicd.yaml", "intellij_pycharm_plugin_delivery_flow.yaml",
                          "vscode_plugin_delivery_flow.yaml"},
        }
        for tier, wf_set in expected_workflows.items():
            res = CommercialPackagerProvisioner.package_tier(
                workspace_root=REPO_ROOT,
                tier=tier,
                output_dir=self.workspace_root / f"bundle_{tier}",
                tenant_id=f"tenant_{tier}_wf"
            )
            pkg = Path(res["package_dir"])
            bundled_wf = {p.name for p in (pkg / "workflows").glob("*.yaml")}
            self.assertEqual(bundled_wf, wf_set, f"{tier} workflow set mismatch")
            self.assertTrue((pkg / "hooks" / "pre-commit.sh").exists(), "git hook must be bundled")
            self.assertTrue((pkg / "scripts" / "install_git_hook.sh").exists(), "hook installer must be bundled")
            self.assertIn("hooks/pre-commit.sh", res["bundled_files"])

        biz = Path(CommercialPackagerProvisioner.package_tier(
            workspace_root=REPO_ROOT, tier="plan_business",
            output_dir=self.workspace_root / "bundle_business", tenant_id="t_biz")["package_dir"])
        biz_wf = {p.name for p in (biz / "workflows").glob("*.yaml")}
        self.assertTrue({"commercial_packaging_provisioning_flow.yaml", "saas_portal_delivery_flow.yaml",
                         "iot_mobile_delivery_flow.yaml"} <= biz_wf)

        ent = Path(CommercialPackagerProvisioner.package_tier(
            workspace_root=REPO_ROOT, tier="plan_enterprise",
            output_dir=self.workspace_root / "bundle_enterprise", tenant_id="t_ent")["package_dir"])
        ent_wf = {p.name for p in (ent / "workflows").glob("*.yaml")}
        self.assertIn("enterprise_sdlc.yaml", ent_wf)

        # Entitlement spec exposes the tier-gated workflow allowlist
        ent_spec = CommercialPackagerProvisioner.get_tier_spec("plan_enterprise", REPO_ROOT)
        self.assertEqual(ent_spec["rules"]["allowed_workflows"], "ALL")
        free_spec = CommercialPackagerProvisioner.get_tier_spec("plan_free", REPO_ROOT)
        self.assertNotIn("enterprise_sdlc.yaml", free_spec["rules"]["allowed_workflows"])


if __name__ == "__main__":
    unittest.main()
