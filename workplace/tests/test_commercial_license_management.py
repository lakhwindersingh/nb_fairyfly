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


if __name__ == "__main__":
    unittest.main()
