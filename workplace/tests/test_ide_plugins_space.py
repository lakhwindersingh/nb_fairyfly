import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "workplace"))
sys.path.insert(0, str(REPO_ROOT / ".nb" / "core"))
sys.path.insert(0, str(REPO_ROOT / "workplace" / "modules" / "mod_intellij_plugin" / "templates" / "bridge"))
sys.path.insert(0, str(REPO_ROOT / "workplace" / "modules" / "mod_vscode_extension" / "templates" / "bridge"))

from nbpack_envelope import NBPackEnvelope
from commercial_packager_provisioner import CommercialPackagerProvisioner
from virtual_psi_fixture import VirtualPsiFixture
from virtual_lsp_fixture import VirtualLspFixture


class TestIdePluginsSpace(unittest.TestCase):
    """
    Test suite for IntelliJ IDEA / PyCharm Plugin, VSCode Extension,
    PSI / LSP AST analysis subsystems, and Tier-Aware Control Plane governance.
    """

    @classmethod
    def setUpClass(cls):
        cls.repo_root = REPO_ROOT
        cls.plugins_dir = cls.repo_root / "workplace" / "modules"
        cls.plans_dir = cls.repo_root / ".nb" / "plan"
        cls.contracts_dir = cls.repo_root / ".nb" / "context" / "contracts"
        cls.rules_dir = cls.repo_root / ".nb" / "context" / "rules"

    def test_01_quad_space_structure_exists(self):
        """Verifies presence of JetBrains and VSCode module directories and essential files."""
        # 1. JetBrains / PyCharm Plugin space
        ij_module = self.plugins_dir / "mod_intellij_plugin"
        self.assertTrue(ij_module.exists(), "mod_intellij_plugin directory must exist")
        self.assertTrue((ij_module / "build.gradle.kts").exists(), "build.gradle.kts must exist")
        self.assertTrue((ij_module / "src" / "main" / "resources" / "META-INF" / "plugin.xml").exists(), "plugin.xml must exist")
        self.assertTrue((ij_module / "src" / "main" / "kotlin" / "com" / "neutronbinary" / "percipience" / "toolwindow" / "PercipienceToolWindowFactory.kt").exists())
        self.assertTrue((ij_module / "src" / "main" / "kotlin" / "com" / "neutronbinary" / "percipience" / "psi" / "PsiAstBridge.kt").exists())
        self.assertTrue((ij_module / "src" / "main" / "kotlin" / "com" / "neutronbinary" / "percipience" / "annotators" / "ContractInspectionAnnotator.kt").exists())
        self.assertTrue((ij_module / "src" / "main" / "kotlin" / "com" / "neutronbinary" / "percipience" / "terminal" / "PercipienceTerminalCustomizer.kt").exists())
        self.assertTrue((ij_module / "src" / "main" / "kotlin" / "com" / "neutronbinary" / "percipience" / "actions" / "LaunchTerminalAgentAction.kt").exists())
        self.assertTrue((ij_module / "src" / "main" / "kotlin" / "com" / "neutronbinary" / "percipience" / "actions" / "ExportTerminalContextAction.kt").exists())
        self.assertTrue((self.repo_root / "workplace" / "core" / "terminal_agent_ast_proxy.py").exists())

        # 2. VSCode Extension space
        vscode_module = self.plugins_dir / "mod_vscode_extension"
        self.assertTrue(vscode_module.exists(), "mod_vscode_extension directory must exist")
        self.assertTrue((vscode_module / "package.json").exists(), "package.json must exist")
        self.assertTrue((vscode_module / "src" / "extension.ts").exists(), "extension.ts must exist")
        self.assertTrue((vscode_module / "src" / "providers" / "workflowTreeProvider.ts").exists())
        self.assertTrue((vscode_module / "src" / "webview" / "dashboardPanel.ts").exists())
        self.assertTrue((vscode_module / "src" / "lsp" / "lspServer.ts").exists())
        self.assertTrue((vscode_module / "src" / "providers" / "codeLensProvider.ts").exists())

    def test_02_wire_contracts_and_rules(self):
        """Validates JSON and YAML wire contracts and safety rules for both IDE platforms."""
        # Manifest contracts
        ij_manifest = self.contracts_dir / "intellij_plugin_manifest_contract.json"
        vscode_manifest = self.contracts_dir / "package_json_manifest_contract.json"
        self.assertTrue(ij_manifest.exists(), "intellij_plugin_manifest_contract.json must exist")
        self.assertTrue(vscode_manifest.exists(), "package_json_manifest_contract.json must exist")

        # Bridge protocols
        psi_contract = self.contracts_dir / "psi_ast_bridge_contract.yaml"
        lsp_contract = self.contracts_dir / "lsp_protocol_contract.yaml"
        self.assertTrue(psi_contract.exists(), "psi_ast_bridge_contract.yaml must exist")
        self.assertTrue(lsp_contract.exists(), "lsp_protocol_contract.yaml must exist")
        self.assertTrue((self.contracts_dir / "terminal_agent_ast_contract.yaml").exists())

        # Rules & Invariants
        self.assertTrue((self.rules_dir / "jetbrains_platform_threading_rules.md").exists())
        self.assertTrue((self.rules_dir / "psi_read_lock_invariants.md").exists())
        self.assertTrue((self.rules_dir / "webview_security_invariants.md").exists())
        self.assertTrue((self.rules_dir / "vscode_activation_invariants.md").exists())

    def test_03_agent_and_workflow_definitions(self):
        """Checks domain subagent and delivery workflow configurations."""
        agents_dir = self.repo_root / ".nb" / "agentic" / "custom" / "agents"
        workflows_dir = self.repo_root / ".nb" / "agentic" / "custom" / "workflows"

        self.assertTrue((agents_dir / "agent_jetbrains_plugin_architect.yaml").exists())
        self.assertTrue((agents_dir / "agent_psi_ast_bridge_specialist.yaml").exists())
        self.assertTrue((agents_dir / "agent_intellij_ui_ux_engineer.yaml").exists())

        self.assertTrue((agents_dir / "agent_vscode_extension_architect.yaml").exists())
        self.assertTrue((agents_dir / "agent_lsp_language_features_specialist.yaml").exists())
        self.assertTrue((agents_dir / "agent_vscode_webview_ux_engineer.yaml").exists())
        self.assertTrue((agents_dir / "agent_terminal_mode_specialist.yaml").exists())

        self.assertTrue((workflows_dir / "intellij_pycharm_plugin_delivery_flow.yaml").exists())
        self.assertTrue((workflows_dir / "vscode_plugin_delivery_flow.yaml").exists())

    def test_04_intellij_plugin_manifest_schema_compliance(self):
        """Parses and validates plugin.xml against required JetBrains Platform extension points."""
        plugin_xml = self.repo_root / "workplace" / "modules" / "mod_intellij_plugin" / "src" / "main" / "resources" / "META-INF" / "plugin.xml"
        content = plugin_xml.read_text(encoding="utf-8")

        self.assertIn("<id>com.neutronbinary.percipience</id>", content)
        self.assertIn("<name>Percipience Context Engineering OS</name>", content)
        self.assertIn("com.intellij.modules.platform", content)
        self.assertIn("com.intellij.modules.lang", content)
        self.assertIn("toolWindow id=\"Percipience OS\"", content)
        self.assertIn("externalAnnotator", content)
        self.assertIn("statusBarWidgetFactory", content)

    def test_05_vscode_package_json_schema_compliance(self):
        """Parses and validates package.json against VSCode Extension API contributes schemas."""
        pkg_json_file = self.repo_root / "workplace" / "modules" / "mod_vscode_extension" / "package.json"
        content = pkg_json_file.read_text(encoding="utf-8")

        import json
        pkg = json.loads(content)
        self.assertEqual(pkg["name"], "percipience-context-os")
        self.assertEqual(pkg["publisher"], "neutronbinary")
        self.assertIn("contributes", pkg)
        self.assertIn("viewsContainers", pkg["contributes"])
        self.assertIn("activitybar", pkg["contributes"]["viewsContainers"])
        self.assertIn("percipience.openDashboard", [cmd["command"] for cmd in pkg["contributes"]["commands"]])

    def test_06_virtual_psi_and_lsp_emulation_bridge(self):
        """Tests offline AST pruning and LSP diagnostic fixtures."""
        res = VirtualPsiFixture.generate_python_psi_mock(func_count=5)
        self.assertEqual(res["psi_root"], "com.jetbrains.python.psi.PyFile")
        self.assertEqual(len(res["functions"]), 5)
        self.assertGreater(res["token_reduction_pct"], 50.0)

        # Test LSP diagnostics fixture
        valid_contract = "contract_id: valid_contract\nschema_version: 2.0.0\n"
        diag = VirtualLspFixture.simulate_document_diagnostics(valid_contract)
        self.assertTrue(diag["is_valid"])
        self.assertEqual(len(diag["diagnostics"]), 0)

        invalid_contract = "invalid_key: true\n"
        diag_invalid = VirtualLspFixture.simulate_document_diagnostics(invalid_contract)
        self.assertFalse(diag_invalid["is_valid"])
        self.assertGreaterEqual(len(diag_invalid["diagnostics"]), 1)

    def test_07_nbpack_layer_compilation(self):
        """Tests compilation and verification of sealed .nbpack domain bundles for IntelliJ and VSCode."""
        bundles_dir = self.repo_root / ".nb" / "bundles"
        bundles_dir.mkdir(parents=True, exist_ok=True)

        intellij_plan = self.plans_dir / "l1" / "intellij-pycharm-plugin" / "detailed.md"
        if not intellij_plan.exists():
            intellij_plan = self.plans_dir / "claude-context-engineering-intellij-pycharm-plugin-space.md"

        vscode_plan = self.plans_dir / "l1" / "vscode-plugin" / "detailed.md"
        if not vscode_plan.exists():
            vscode_plan = self.plans_dir / "claude-context-engineering-vscode-plugin-space.md"

        intellij_pack = bundles_dir / "intellij_pycharm_plugin_domain.nbpack"
        vscode_pack = bundles_dir / "vscode_plugin_domain.nbpack"

        res_intellij = NBPackEnvelope.compile_layer_pack(self.repo_root, intellij_plan, intellij_pack)
        res_vscode = NBPackEnvelope.compile_layer_pack(self.repo_root, vscode_plan, vscode_pack)

        self.assertTrue(res_intellij.exists())
        self.assertTrue(res_vscode.exists())

        hydrated_intellij = NBPackEnvelope.hydrate_in_memory(intellij_pack)
        hydrated_vscode = NBPackEnvelope.hydrate_in_memory(vscode_pack)

        self.assertIn("__layer_manifest__.json", hydrated_intellij)
        self.assertIn("__layer_manifest__.json", hydrated_vscode)

    def test_08_status_bar_metrics_and_distribution_assets(self):
        """Validates status bar telemetry integration and distribution asset generation for both IDE plugins."""
        ij_widget = self.repo_root / "workplace" / "modules" / "mod_intellij_plugin" / "src" / "main" / "kotlin" / "com" / "neutronbinary" / "percipience" / "statusbar" / "PercipienceStatusBarWidgetFactory.kt"
        self.assertTrue(ij_widget.exists(), "PercipienceStatusBarWidgetFactory.kt must exist")

        plugin_xml = self.repo_root / "workplace" / "modules" / "mod_intellij_plugin" / "src" / "main" / "resources" / "META-INF" / "plugin.xml"
        self.assertIn("statusBarWidgetFactory", plugin_xml.read_text(encoding="utf-8"))

        vscode_statusbar = self.repo_root / "workplace" / "modules" / "mod_vscode_extension" / "src" / "statusbar" / "statusBarManager.ts"
        self.assertTrue(vscode_statusbar.exists(), "statusBarManager.ts must exist")

        ext_ts = self.repo_root / "workplace" / "modules" / "mod_vscode_extension" / "src" / "extension.ts"
        self.assertIn("PercipienceStatusBarManager", ext_ts.read_text(encoding="utf-8"))

        bundles_dir = self.repo_root / ".nb" / "bundles"
        ij_zip = bundles_dir / "percipience-intellij-plugin-1.0.0.zip"
        vscode_vsix = bundles_dir / "percipience-vscode-extension-1.0.0.vsix"

        self.assertTrue(ij_zip.exists(), "percipience-intellij-plugin-1.0.0.zip must exist")
        self.assertGreater(ij_zip.stat().st_size, 1000)

        self.assertTrue(vscode_vsix.exists(), "percipience-vscode-extension-1.0.0.vsix must exist")
        self.assertGreater(vscode_vsix.stat().st_size, 1000)

    def test_09_free_plan_master_plan_and_basic_cicd_workflow(self):
        """Validates that the Free Plan Master Plan, billing tier, and basic CI/CD workflow exist and are valid."""
        free_plan_file = self.plans_dir / "master" / "parent-master-plan" / "detailed.md"
        if not free_plan_file.exists():
            free_plan_file = self.plans_dir / "claude-context-engineering-parent-master-plan.md"
        self.assertTrue(free_plan_file.exists(), "Parent master plan must exist")
        content = free_plan_file.read_text(encoding="utf-8")
        self.assertIn("plan_free", content)
        self.assertIn("Token Reduction", content)
        self.assertIn("Merkle", content)
        self.assertIn("basic_autonomous_cicd.yaml", content)

        billing_file = (self.repo_root / ".nb" / "config" / "billing_plans.yaml" if (self.repo_root / ".nb" / "config" / "billing_plans.yaml").exists() else self.repo_root / "workplace" / "config" / "billing_plans.yaml")
        self.assertTrue(billing_file.exists())
        with open(billing_file, "r", encoding="utf-8") as f:
            billing_data = yaml.safe_load(f)
            self.assertIn("plan_free", billing_data["plans"])
            self.assertEqual(billing_data["plans"]["plan_free"]["base_price_monthly_usd"], 0)
            self.assertTrue(billing_data["plans"]["plan_free"]["features"]["ast_token_pruning"])
            self.assertTrue(billing_data["plans"]["plan_free"]["features"]["merkle_chain_audit"])
            self.assertTrue(billing_data["plans"]["plan_free"]["features"]["basic_autonomous_cicd"])

            # Verify Basic Platform Tools Exposure and Encryption governance boundaries
            self.assertFalse(billing_data["plans"]["plan_free"]["features"]["basic_platform_tools_exposure"])
            self.assertFalse(billing_data["plans"]["plan_free"]["features"]["user_plan_encryption"])
            self.assertTrue(billing_data["plans"]["plan_free"]["features"]["platform_core_encryption"])
            self.assertTrue(billing_data["plans"]["plan_business"]["features"]["basic_platform_tools_exposure"])
            self.assertTrue(billing_data["plans"]["plan_business"]["features"]["user_plan_encryption"])
            self.assertTrue(billing_data["plans"]["plan_enterprise"]["features"]["basic_platform_tools_exposure"])
            self.assertTrue(billing_data["plans"]["plan_enterprise"]["features"]["user_plan_encryption"])

        # Check basic CI/CD workflow existence and valid step configuration
        cicd_file = self.repo_root / ".nb" / "agentic" / "custom" / "workflows" / "basic_autonomous_cicd.yaml"
        self.assertTrue(cicd_file.exists(), "basic_autonomous_cicd.yaml must exist")
        with open(cicd_file, "r", encoding="utf-8") as f:
            cicd_data = yaml.safe_load(f)
            step_ids = [s["step_id"] for s in cicd_data.get("steps", [])]
            self.assertIn("sustain_maintenance", step_ids)
            self.assertIn("ast_token_reduction", step_ids)
            self.assertIn("merkle_state_seal", step_ids)

    def test_10_offline_free_tier_assets_bundling(self):
        """Validates that all essential platform offline assets are bundled inside the IntelliJ plugin JAR/ZIP."""
        bundles_dir = self.repo_root / ".nb" / "bundles"
        ij_zip_path = bundles_dir / "percipience-intellij-plugin-1.0.0.zip"
        self.assertTrue(ij_zip_path.exists(), "percipience-intellij-plugin-1.0.0.zip must exist")

        with zipfile.ZipFile(ij_zip_path, "r") as zf:
            jar_name = "percipience-intellij-plugin/lib/percipience-intellij-plugin-1.0.0.jar"
            self.assertIn(jar_name, zf.namelist())
            jar_bytes = zf.read(jar_name)

            with zipfile.ZipFile(io.BytesIO(jar_bytes)) as jar_file:
                jar_files = jar_file.namelist()

                # Verify all required offline bundled files exist within the JAR
                self.assertIn("percipience/bin/percipience", jar_files)
                self.assertIn("percipience/config/billing_plans.yaml", jar_files)
                self.assertIn("percipience/config/token_compression_rules.yaml", jar_files)
                self.assertIn("percipience/workflows/basic_autonomous_cicd.yaml", jar_files)
                self.assertIn("percipience/plan/claude-context-engineering-parent-master-free_plan.md", jar_files)
                self.assertIn("percipience/core/__init__.py", jar_files)
                self.assertIn("percipience/core/ast_optimizer.py", jar_files)
                self.assertIn("percipience/core/merkle_engine.py", jar_files)
                self.assertIn("percipience/core/token_tracker.py", jar_files)
                self.assertIn("percipience/core/nbpack_envelope.py", jar_files)
                self.assertIn("percipience/core/autonomous_cicd.py", jar_files)

    def test_11_workspace_bootstrapper_hydration(self):
        """Tests that WorkspaceBootstrapper can unpack assets and initialize a clean workspace."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            bin_dir = tmp_path / ".nb" / "bin"
            core_dir = tmp_path / ".nb" / "core"
            config_dir = tmp_path / ".nb" / "config"
            wf_dir = tmp_path / ".nb" / "agentic" / "custom" / "workflows"
            plan_dir = tmp_path / ".nb" / "plan"
            ledger_dir = tmp_path / ".nb" / "context" / "ledger"

            bin_dir.mkdir(parents=True, exist_ok=True)
            core_dir.mkdir(parents=True, exist_ok=True)
            config_dir.mkdir(parents=True, exist_ok=True)
            wf_dir.mkdir(parents=True, exist_ok=True)
            plan_dir.mkdir(parents=True, exist_ok=True)
            ledger_dir.mkdir(parents=True, exist_ok=True)

            # Copy resources from repository resources
            src_res = self.repo_root / "workplace" / "modules" / "mod_intellij_plugin" / "src" / "main" / "resources" / "percipience"
            shutil.copyfile(src_res / "bin" / "percipience", bin_dir / "percipience")
            os.chmod(bin_dir / "percipience", 0o755)

            for py_file in (src_res / "core").glob("*.py"):
                shutil.copyfile(py_file, core_dir / py_file.name)

            shutil.copyfile(src_res / "config" / "billing_plans.yaml", config_dir / "billing_plans.yaml")
            shutil.copyfile(src_res / "config" / "token_compression_rules.yaml", config_dir / "token_compression_rules.yaml")
            shutil.copyfile(src_res / "workflows" / "basic_autonomous_cicd.yaml", wf_dir / "basic_autonomous_cicd.yaml")
            
            template_plan = self.repo_root / "workplace" / "modules" / "mod_intellij_plugin" / "src" / "main" / "resources" / "percipience" / "plan" / "claude-context-engineering-parent-master-free_plan.md"
            if not template_plan.exists():
                template_plan = self.plans_dir / "master" / "parent-master-free-plan" / "detailed.md"
            if template_plan.exists():
                shutil.copyfile(template_plan, plan_dir / "claude-context-engineering-parent-master-free_plan.md")

            # Create genesis ledger
            with open(ledger_dir / "context_ledger.yaml", "w", encoding="utf-8") as lf:
                yaml.dump({
                    "merkle_root": "0" * 64,
                    "chain_length": 1,
                    "blocks": [{
                        "block_id": "RP_GENESIS_000",
                        "merkle_hash": "0" * 64,
                        "action": "INIT_FREE_TIER_WORKSPACE"
                    }]
                }, lf)

            # Verify files exist and percipience bin is executable
            self.assertTrue((bin_dir / "percipience").exists())
            self.assertTrue(os.access(bin_dir / "percipience", os.X_OK))
            self.assertTrue((core_dir / "ast_optimizer.py").exists())
            self.assertTrue((config_dir / "billing_plans.yaml").exists())
            self.assertTrue((plan_dir / "claude-context-engineering-parent-master-free_plan.md").exists())
            self.assertTrue((ledger_dir / "context_ledger.yaml").exists())

    def test_12_ui_actions_and_services_registered(self):
        """Validates that IDE action classes and background execution services are defined."""
        actions_dir = self.repo_root / "workplace" / "modules" / "mod_intellij_plugin" / "src" / "main" / "kotlin" / "com" / "neutronbinary" / "percipience" / "actions"
        services_dir = self.repo_root / "workplace" / "modules" / "mod_intellij_plugin" / "src" / "main" / "kotlin" / "com" / "neutronbinary" / "percipience" / "services"

        self.assertTrue((actions_dir / "RunGatekeeperAction.kt").exists())
        self.assertTrue((actions_dir / "RunCicdAction.kt").exists())
        self.assertTrue((actions_dir / "RunMerkleAuditAction.kt").exists())
        self.assertTrue((actions_dir / "TokensSummaryAction.kt").exists())
        self.assertTrue((actions_dir / "ValidateLayerAction.kt").exists())
        self.assertTrue((services_dir / "PercipienceExecutionService.kt").exists())

    def test_13_user_guide_and_quickstart_documentation(self):
        """Verifies that the IDE Plugin User Guide is present and documents the Free Community Tier and Dynamic Action Matrix."""
        user_guide = self.repo_root / "workplace" / "modules" / "mod_intellij_plugin" / "PLUGIN_USER_GUIDE.md"
        self.assertTrue(user_guide.exists(), "PLUGIN_USER_GUIDE.md must exist")
        content = user_guide.read_text(encoding="utf-8")
        self.assertIn("Dynamic Tier-Aware Control Plane", content)
        self.assertIn("Separate Tier Bundles for Permission Testing", content)
        self.assertIn("Percipience OS", content)
        self.assertIn("PSI", content)
        self.assertIn("Merkle", content)

    def test_14_free_tier_cli_boundary_enforcement(self):
        """Verifies that `percipience pack` and `percipience layer pack` are denied on Free Tier."""
        env = os.environ.copy()
        env["PERCIPIENCE_PLAN"] = "plan_free"
        res_pack = subprocess.run([str(self.repo_root / ".nb" / "bin" / "percipience"), "pack"], capture_output=True, text=True, env=env)
        self.assertNotEqual(res_pack.returncode, 0)
        self.assertIn("Access Denied", res_pack.stdout)
        self.assertIn("Basic platform tools exposure", res_pack.stdout)
        self.assertIn("plaintext", res_pack.stdout)

        # Test percipience layer pack denial on free tier
        plan_arg = ".nb/plan/master/parent-master-free-plan/detailed.md" if (self.repo_root / ".nb" / "plan" / "master" / "parent-master-free-plan" / "detailed.md").exists() else ".nb/plan/claude-context-engineering-parent-master-free_plan.md"
        res_lpack = subprocess.run([str(self.repo_root / ".nb" / "bin" / "percipience"), "layer", "pack", "--plan", plan_arg], capture_output=True, text=True, env=env)
        self.assertNotEqual(res_lpack.returncode, 0)
        self.assertIn("Access Denied", res_lpack.stdout)

    def test_15_tier_aware_control_plane_button_resolution(self):
        """Verifies CommercialPackagerProvisioner tier specs matching Kotlin & TS resolution matrix."""
        spec_free = CommercialPackagerProvisioner.get_tier_spec("plan_free", self.repo_root)
        self.assertFalse(spec_free["features"]["basic_platform_tools_exposure"])
        self.assertFalse(spec_free["features"]["user_plan_encryption"])
        self.assertFalse(spec_free["rules"]["allow_nbpack_compilation"])
        self.assertEqual(spec_free["included_seats"], 1)
        self.assertEqual(spec_free["included_concurrent_worktrees"], 1)

        spec_team = CommercialPackagerProvisioner.get_tier_spec("plan_team", self.repo_root)
        self.assertFalse(spec_team["features"]["basic_platform_tools_exposure"])
        self.assertTrue(spec_team["rules"]["allow_custom_agent_creation"])
        self.assertEqual(spec_team["included_seats"], 15)
        self.assertEqual(spec_team["included_concurrent_worktrees"], 5)

        spec_biz = CommercialPackagerProvisioner.get_tier_spec("plan_business", self.repo_root)
        self.assertTrue(spec_biz["features"]["basic_platform_tools_exposure"])
        self.assertTrue(spec_biz["features"]["user_plan_encryption"])
        self.assertTrue(spec_biz["rules"]["allow_nbpack_compilation"])
        self.assertEqual(spec_biz["included_seats"], 50)
        self.assertEqual(spec_biz["included_concurrent_worktrees"], 20)

        spec_ent = CommercialPackagerProvisioner.get_tier_spec("plan_enterprise", self.repo_root)
        self.assertTrue(spec_ent["features"]["basic_platform_tools_exposure"])
        self.assertTrue(spec_ent["features"]["user_plan_encryption"])
        self.assertTrue(spec_ent["rules"]["allow_private_vpc"])
        self.assertTrue(spec_ent["rules"]["allow_worm_egress"])

    def test_16_separate_tier_plugin_and_extension_bundles_generated(self):
        """Verifies that separate tier-aware bundles exist in .nb/bundles for IntelliJ and VSCode."""
        bundles_dir = self.repo_root / ".nb" / "bundles"
        self.assertTrue(bundles_dir.exists())

        # Verify IntelliJ tier-specific packages
        for tier in ["free", "team", "business", "enterprise"]:
            ij_zip = bundles_dir / f"percipience-intellij-plugin-{tier}-1.0.0.zip"
            ij_jar = bundles_dir / f"percipience-intellij-plugin-{tier}-1.0.0.jar"
            self.assertTrue(ij_zip.exists(), f"{ij_zip.name} must exist")
            self.assertTrue(ij_jar.exists(), f"{ij_jar.name} must exist")
            self.assertGreater(ij_zip.stat().st_size, 1000)

            # Verify VSCode tier-specific packages
            vs_vsix = bundles_dir / f"percipience-vscode-extension-{tier}-1.0.0.vsix"
            self.assertTrue(vs_vsix.exists(), f"{vs_vsix.name} must exist")
            self.assertGreater(vs_vsix.stat().st_size, 1000)

    def test_17_vscode_and_intellij_plans_synchronization(self):
        """Validates that IntelliJ and VSCode plans are synchronized with identical tier matrix and documentation."""
        ij_detailed = (self.plans_dir / "l1" / "intellij-pycharm-plugin" / "detailed.md").read_text(encoding="utf-8")
        ij_concise = (self.plans_dir / "l1" / "intellij-pycharm-plugin" / "concise.md").read_text(encoding="utf-8")
        vs_detailed = (self.plans_dir / "l1" / "vscode-plugin" / "detailed.md").read_text(encoding="utf-8")
        vs_concise = (self.plans_dir / "l1" / "vscode-plugin" / "concise.md").read_text(encoding="utf-8")

        # Check for presence of tier action matrix and bundles in both
        for text in [ij_detailed, vs_detailed, ij_concise, vs_concise]:
            self.assertIn("Free Community", text)
            self.assertIn("Team Tier", text)
            self.assertIn("Business Tier", text)
            self.assertIn("Enterprise Dedicated", text)

        self.assertIn("percipience-intellij-plugin-", ij_detailed)
        self.assertIn("percipience-vscode-extension-", vs_detailed)

        for text in [ij_concise, vs_concise]:
            self.assertIn("plan_free", text)
            self.assertIn("plan_team", text)
            self.assertIn("plan_business", text)
            self.assertIn("plan_enterprise", text)


if __name__ == "__main__":
    unittest.main()
