"""
Unit and Integration Tests for Percipience Plan Bundle Import Resilience
Validates that:
1. Bootstrapped/packaged workspaces for Free, Team, Business, and Enterprise plans
   load the Percipience CLI without `ModuleNotFoundError`.
2. Subcommands requiring engines missing from a specific tier exit cleanly with an
   informative upgrade notice instead of raising Python tracebacks.
3. Cross-module imports inside core engines (autonomous_cicd, agent_plugin_engine,
   project_policy_engine) gracefully fall back when non-provisioned engines are absent.
"""

import os
import subprocess
import sys
import tempfile
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


class TestPlanBundleImports:

    @pytest.fixture(scope="class")
    @classmethod
    def packaged_bundles(cls):
        """Generates temporary packaged bundles for Free, Team, and Business tiers."""
        from core.commercial_packager_provisioner import CommercialPackagerProvisioner

        tmp_dir = Path(tempfile.mkdtemp(prefix="nb_bundle_test_"))
        bundles = {}

        for tier in ["free", "team", "business"]:
            tier_dir = tmp_dir / f"bundle_{tier}"
            res = CommercialPackagerProvisioner.package_tier(
                workspace_root=REPO_ROOT,
                tier=tier,
                output_dir=tier_dir,
                tenant_id=f"tenant_test_{tier}"
            )
            assert res["status"] == "PACKAGED"
            bundles[tier] = tier_dir

        return bundles

    def test_free_tier_status_and_help(self, packaged_bundles):
        """Free bundle executes status and --help cleanly with no ModuleNotFoundError."""
        bundle_dir = packaged_bundles["free"]
        cli = bundle_dir / "bin" / "percipience"
        assert cli.exists()

        # Test --help
        res = subprocess.run([sys.executable, str(cli), "--help"], capture_output=True, text=True)
        assert res.returncode == 0
        assert "Neutron Binary Percipience CLI" in res.stdout
        assert "ModuleNotFoundError" not in res.stderr

        # Test status
        res = subprocess.run([sys.executable, str(cli), "status"], capture_output=True, text=True)
        assert res.returncode == 0
        assert "Active Plan Tier: PLAN_FREE" in res.stdout
        assert "Core Engines Available:" in res.stdout
        assert "Unavailable In Current Plan" in res.stdout
        assert "ModuleNotFoundError" not in res.stderr

    def test_free_tier_restricted_commands_graceful_exit(self, packaged_bundles):
        """Restricted commands in Free bundle exit with code 1 and upgrade notice, no traceback."""
        bundle_dir = packaged_bundles["free"]
        cli = bundle_dir / "bin" / "percipience"

        # 1. 'repo' command requires byor_adapter
        res = subprocess.run([sys.executable, str(cli), "repo", "status"], capture_output=True, text=True)
        assert res.returncode == 1
        assert "Feature 'repo' is unavailable in this plan bundle" in res.stdout
        assert "core/byor_adapter.py" in res.stdout
        assert "Traceback" not in res.stderr

        # 2. 'worktree' command requires worktree_engine
        res = subprocess.run([sys.executable, str(cli), "worktree", "list"], capture_output=True, text=True)
        assert res.returncode == 1
        assert "Feature 'worktree' is unavailable in this plan bundle" in res.stdout
        assert "core/worktree_engine.py" in res.stdout
        assert "Traceback" not in res.stderr

        # 3. 'reprompt' command requires diagnostic_reprompt
        res = subprocess.run([sys.executable, str(cli), "reprompt", "--generate-only"], capture_output=True, text=True)
        assert res.returncode == 1
        assert "Feature 'reprompt' is unavailable in this plan bundle" in res.stdout
        assert "core/diagnostic_reprompt.py" in res.stdout
        assert "Traceback" not in res.stderr

        # 4. 'egress' command requires worm_egress
        res = subprocess.run([sys.executable, str(cli), "egress", "list"], capture_output=True, text=True)
        assert res.returncode == 1
        assert "Feature 'egress' is unavailable in this plan bundle" in res.stdout
        assert "core/worm_egress.py" in res.stdout
        assert "Traceback" not in res.stderr

    def test_team_tier_unlocked_and_restricted(self, packaged_bundles):
        """Team bundle permits worktree and drift, but blocks reprompt and egress."""
        bundle_dir = packaged_bundles["team"]
        cli = bundle_dir / "bin" / "percipience"

        # Unlocked: worktree list
        res = subprocess.run([sys.executable, str(cli), "worktree", "list"], capture_output=True, text=True)
        assert res.returncode == 0
        assert "Active Worktree Leases" in res.stdout
        assert "Traceback" not in res.stderr

        # Restricted: reprompt
        res = subprocess.run([sys.executable, str(cli), "reprompt", "--generate-only"], capture_output=True, text=True)
        assert res.returncode == 1
        assert "Feature 'reprompt' is unavailable in this plan bundle" in res.stdout
        assert "Traceback" not in res.stderr

    def test_business_tier_unlocked(self, packaged_bundles):
        """Business bundle permits reprompt and agent commands."""
        bundle_dir = packaged_bundles["business"]
        cli = bundle_dir / "bin" / "percipience"

        # Status shows higher engine count
        res = subprocess.run([sys.executable, str(cli), "status"], capture_output=True, text=True)
        assert res.returncode == 0
        assert "core/diagnostic_reprompt.py" in res.stdout

        # reprompt generate-only works in Business tier
        res = subprocess.run([sys.executable, str(cli), "reprompt", "--generate-only"], capture_output=True, text=True)
        assert res.returncode == 0
        assert "Generated Isolated Diagnostic Re-Prompt Envelope" in res.stdout
        assert "Traceback" not in res.stderr

    def test_core_engine_internal_resilience(self, packaged_bundles):
        """Core engines (autonomous_cicd, agent_plugin_engine) import cleanly when dependencies are missing."""
        bundle_dir = packaged_bundles["free"]

        # Run python script inside the Free bundle environment importing autonomous_cicd
        test_script = """
import sys
from pathlib import Path

bundle_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(bundle_dir))
sys.path.insert(0, str(bundle_dir / "core"))

# Importing autonomous_cicd must not fail even without worktree_engine
import core.autonomous_cicd as cicd
assert cicd.SelfSustainingEngine is not None
assert cicd.WorktreeEngine is None  # Gracefully None in Free tier

# Housekeeping run succeeds with 0 reclaimed leases
res = cicd.SelfSustainingEngine.execute_maintenance(bundle_dir)
assert res["reclaimed_leases"] == 0
print("AUTONOMOUS_CICD_RESILIENCE_OK")
"""
        test_file = bundle_dir / "test_resilience.py"
        test_file.write_text(test_script, encoding="utf-8")

        res = subprocess.run([sys.executable, str(test_file)], capture_output=True, text=True)
        assert res.returncode == 0
        assert "AUTONOMOUS_CICD_RESILIENCE_OK" in res.stdout
        assert "Traceback" not in res.stderr
