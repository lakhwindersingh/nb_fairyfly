"""
Unit and Integration Test Suite for Percipience Multi-Tenant Project Provisioning,
IAM Hierarchy, PostgreSQL RLS, KMS Key Broker & One-Click Scaffolding Wizard (CAP-40 / Section 18.1)
"""

import base64
import datetime
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "workplace") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "workplace"))

from core.tenant_manager import (
    TenantManager,
    TenantRole,
    Tenant,
    Project,
    Repository,
    WorkspaceNode,
    TenantUser,
    ROLE_PERMISSIONS
)
from core.kms_broker import KMSBroker, KeyRecord, SealedEnclaveBundle
from core.project_scaffolder import ProjectScaffolder, ScaffoldResult


class TestTenantProvisioningSection18_1(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_path = Path(self.temp_dir.name)
        self.tenant_db_file = self.base_path / "tenants.json"
        self.kms_db_file = self.base_path / "kms.json"

        self.tenant_mgr = TenantManager(persistence_file=self.tenant_db_file)
        self.kms_broker = KMSBroker(persistence_file=self.kms_db_file)
        self.scaffolder = ProjectScaffolder(self.tenant_mgr, self.kms_broker)

    def tearDown(self):
        self.temp_dir.cleanup()

    # -------------------------------------------------------------------------
    # 1. Multi-Tenant Organization & Project Hierarchy CRUD (TODO-PRT-01)
    # -------------------------------------------------------------------------

    def test_01_tenant_and_project_hierarchy_crud(self):
        """Tests Org -> Projects -> Repositories -> Workspaces/Nodes hierarchy CRUD."""
        # 1. Create Tenant
        t1 = self.tenant_mgr.create_tenant(
            tenant_id="tenant_fintech_corp",
            name="FinTech Corp",
            tier="plan_enterprise",
            settings={"max_concurrent_nodes": 50}
        )
        self.assertEqual(t1.tenant_id, "tenant_fintech_corp")
        self.assertEqual(t1.slug, "fintech-corp")

        # Duplicate tenant rejection
        with self.assertRaises(ValueError):
            self.tenant_mgr.create_tenant(tenant_id="tenant_fintech_corp", name="Duplicate Corp")

        # 2. Create Projects under Tenant
        p1 = self.tenant_mgr.create_project(
            tenant_id="tenant_fintech_corp",
            project_id="proj_algo_trading",
            name="Algorithmic Trading Core",
            mode="multi_module",
            billing_tier="plan_enterprise"
        )
        self.assertEqual(p1.project_id, "proj_algo_trading")
        self.assertEqual(p1.tenant_id, "tenant_fintech_corp")

        # Project under non-existent tenant rejection
        with self.assertRaises(ValueError):
            self.tenant_mgr.create_project(
                tenant_id="non_existent_tenant",
                project_id="proj_invalid",
                name="Invalid"
            )

        # 3. Register Repositories
        repo1 = self.tenant_mgr.register_repository(
            tenant_id="tenant_fintech_corp",
            project_id="proj_algo_trading",
            repo_id="repo_algo_engine",
            name="algo-engine",
            url="git@github.com:fintech-corp/algo-engine.git"
        )
        self.assertEqual(repo1.repo_id, "repo_algo_engine")
        self.assertIn("repo_algo_engine", p1.repositories)

        # 4. Register Workspace Nodes
        node1 = self.tenant_mgr.register_workspace_node(
            tenant_id="tenant_fintech_corp",
            project_id="proj_algo_trading",
            node_id="node_mac_m3_01",
            hostname="macbook-dev-01.local",
            worktree_path="/workspaces/algo_wt1"
        )
        self.assertEqual(node1.node_id, "node_mac_m3_01")
        self.assertEqual(node1.status, "HEALTHY")
        self.assertIn("node_mac_m3_01", p1.workspace_nodes)

        # Update node heartbeat
        updated_node = self.tenant_mgr.update_node_heartbeat("node_mac_m3_01", status="HEALING", metadata_patch={"task": "AST Pruning"})
        self.assertIsNotNone(updated_node)
        self.assertEqual(updated_node.status, "HEALING")
        self.assertEqual(updated_node.metadata["task"], "AST Pruning")

        # 5. Register Users
        self.tenant_mgr.register_user(
            tenant_id="tenant_fintech_corp",
            user_id="user_admin_01",
            email="admin@fintechcorp.com",
            display_name="Alice Admin",
            role=TenantRole.ENTERPRISE_SUPER_ADMIN
        )
        self.tenant_mgr.register_user(
            tenant_id="tenant_fintech_corp",
            user_id="user_lead_01",
            email="lead@fintechcorp.com",
            display_name="Bob Lead",
            role=TenantRole.PROJECT_LEAD,
            project_assignments=["proj_algo_trading"]
        )

        # 6. Verify Hierarchy Tree
        hierarchy = self.tenant_mgr.get_tenant_hierarchy("tenant_fintech_corp")
        self.assertEqual(hierarchy["tenant"]["name"], "FinTech Corp")
        self.assertEqual(len(hierarchy["projects"]), 1)
        self.assertEqual(hierarchy["projects"][0]["project"]["name"], "Algorithmic Trading Core")
        self.assertEqual(len(hierarchy["projects"][0]["repositories"]), 1)
        self.assertEqual(len(hierarchy["projects"][0]["workspace_nodes"]), 1)
        self.assertEqual(hierarchy["summary"]["total_projects"], 1)
        self.assertEqual(hierarchy["summary"]["total_users"], 2)

    # -------------------------------------------------------------------------
    # 2. RBAC Authorization Matrix (TODO-PRT-01)
    # -------------------------------------------------------------------------

    def test_02_rbac_authorization_matrix(self):
        """Tests enterprise RBAC permissions across all 4 roles."""
        t_id = "tenant_cyber_defense"
        self.tenant_mgr.create_tenant(tenant_id=t_id, name="Cyber Defense Ltd")
        self.tenant_mgr.create_project(tenant_id=t_id, project_id="proj_sentinel", name="Sentinel Shield")

        # 1. Super Admin
        self.tenant_mgr.register_user(t_id, "u_super", "super@cyber.com", "Super Admin", TenantRole.ENTERPRISE_SUPER_ADMIN)
        ok, _ = self.tenant_mgr.authorize("u_super", "tenant:manage", t_id)
        self.assertTrue(ok)
        ok, _ = self.tenant_mgr.authorize("u_super", "project:scaffold", t_id, "proj_sentinel")
        self.assertTrue(ok)
        ok, _ = self.tenant_mgr.authorize("u_super", "kms:rotate", t_id)
        self.assertTrue(ok)

        # 2. Project Lead
        self.tenant_mgr.register_user(t_id, "u_lead", "lead@cyber.com", "Project Lead", TenantRole.PROJECT_LEAD, ["proj_sentinel"])
        ok, _ = self.tenant_mgr.authorize("u_lead", "project:scaffold", t_id, "proj_sentinel")
        self.assertTrue(ok)
        ok, _ = self.tenant_mgr.authorize("u_lead", "cicd:run", t_id, "proj_sentinel")
        self.assertTrue(ok)
        # Cannot delete tenant or manage other projects
        ok, _ = self.tenant_mgr.authorize("u_lead", "tenant:delete", t_id)
        self.assertFalse(ok)
        ok, _ = self.tenant_mgr.authorize("u_lead", "project:read", t_id, "proj_unassigned")
        self.assertFalse(ok)

        # 3. Security Auditor
        self.tenant_mgr.register_user(t_id, "u_auditor", "auditor@cyber.com", "Auditor", TenantRole.SECURITY_AUDITOR)
        ok, _ = self.tenant_mgr.authorize("u_auditor", "audit:read", t_id)
        self.assertTrue(ok)
        ok, _ = self.tenant_mgr.authorize("u_auditor", "merkle:verify", t_id)
        self.assertTrue(ok)
        # Auditor cannot scaffold or run cicd
        ok, _ = self.tenant_mgr.authorize("u_auditor", "project:scaffold", t_id)
        self.assertFalse(ok)
        ok, _ = self.tenant_mgr.authorize("u_auditor", "cicd:run", t_id)
        self.assertFalse(ok)

        # 4. Agent Worker
        self.tenant_mgr.register_user(t_id, "u_worker", "worker@cyber.com", "Worker Node", TenantRole.AGENT_WORKER)
        ok, _ = self.tenant_mgr.authorize("u_worker", "node:telemetry", t_id)
        self.assertTrue(ok)
        ok, _ = self.tenant_mgr.authorize("u_worker", "ast:prune", t_id)
        self.assertTrue(ok)
        # Worker cannot manage users or delete projects
        ok, _ = self.tenant_mgr.authorize("u_worker", "user:assign", t_id)
        self.assertFalse(ok)

        # 5. Cross-Tenant Rejection
        t2_id = "tenant_other_corp"
        self.tenant_mgr.create_tenant(tenant_id=t2_id, name="Other Corp")
        ok, msg = self.tenant_mgr.authorize("u_lead", "project:read", t2_id)
        self.assertFalse(ok)
        self.assertIn("does not match target tenant", msg)

    # -------------------------------------------------------------------------
    # 3. PostgreSQL RLS Schemas & Isolation Simulator (TODO-PRT-01)
    # -------------------------------------------------------------------------

    def test_03_postgresql_rls_schema_and_simulation(self):
        """Validates generated PostgreSQL RLS DDL and tests zero cross-tenant data leakage simulation."""
        ddl = TenantManager.generate_rls_sql_schema()
        self.assertIn("ENABLE ROW LEVEL SECURITY", ddl)
        self.assertIn("FORCE ROW LEVEL SECURITY", ddl)
        self.assertIn("CREATE POLICY tenant_isolation_policy", ddl)
        self.assertIn("current_setting('app.current_tenant_id'", ddl)
        self.assertIn("FUNCTION set_tenant_context", ddl)

        # Simulate RLS filter on multi-tenant rows
        dataset = [
            {"id": "proj_1", "tenant_id": "tenant_alpha", "name": "Alpha Project"},
            {"id": "proj_2", "tenant_id": "tenant_alpha", "name": "Alpha Project 2"},
            {"id": "proj_3", "tenant_id": "tenant_beta", "name": "Beta Project"},
            {"id": "proj_4", "tenant_id": "tenant_gamma", "name": "Gamma Project"},
        ]

        # Session in tenant_alpha should ONLY see alpha projects
        alpha_view = TenantManager.simulate_rls_filter(dataset, session_tenant_id="tenant_alpha")
        self.assertEqual(len(alpha_view), 2)
        for r in alpha_view:
            self.assertEqual(r["tenant_id"], "tenant_alpha")

        # Session in tenant_beta should ONLY see beta projects
        beta_view = TenantManager.simulate_rls_filter(dataset, session_tenant_id="tenant_beta")
        self.assertEqual(len(beta_view), 1)
        self.assertEqual(beta_view[0]["tenant_id"], "tenant_beta")

    # -------------------------------------------------------------------------
    # 4. Automated KMS Key Broker & Cryptography (TODO-PRT-03)
    # -------------------------------------------------------------------------

    def test_04_kms_broker_provisioning_and_cryptography(self):
        """Tests Ed25519 signing/verification, AES-256-GCM authenticated encryption, and key rotation."""
        t_id = "tenant_health_ai"
        p_id = "proj_diagnostics"

        # 1. Provision project keys
        k1 = self.kms_broker.provision_project_keys(t_id, p_id)
        self.assertEqual(k1.key_version, 1)
        self.assertEqual(k1.status, "ACTIVE")
        self.assertIsNotNone(k1.ed25519_public_b64)

        # 2. Ed25519 Digital Signing
        payload = b"Sample context engineering wire contract payload"
        sig = self.kms_broker.sign_data(p_id, payload)
        self.assertTrue(self.kms_broker.verify_signature(p_id, payload, sig))
        # Tampered payload fails verification
        self.assertFalse(self.kms_broker.verify_signature(p_id, b"Tampered context payload", sig))

        # 3. AES-256-GCM Encryption & Decryption
        secret_data = b"Proprietary prompt template: You are an autonomous health AI."
        aad = b"tenant_health_ai:proj_diagnostics:v1"
        ciphertext, nonce, version = self.kms_broker.encrypt_bytes(p_id, secret_data, associated_data=aad)
        self.assertEqual(version, 1)

        decrypted = self.kms_broker.decrypt_bytes(p_id, ciphertext, nonce, version, associated_data=aad)
        self.assertEqual(decrypted, secret_data)

        # Ciphertext tampering causes decryption failure
        tampered_cipher = bytearray(ciphertext)
        tampered_cipher[0] ^= 0xFF
        with self.assertRaises(Exception):
            self.kms_broker.decrypt_bytes(p_id, bytes(tampered_cipher), nonce, version, associated_data=aad)

        # 4. Key Rotation
        k2 = self.kms_broker.rotate_project_keys(t_id, p_id)
        self.assertEqual(k2.key_version, 2)
        self.assertEqual(k2.status, "ACTIVE")
        # Check that k1 is now ROTATED
        old_k1 = self.kms_broker.get_key_version(p_id, 1)
        self.assertEqual(old_k1.status, "ROTATED")

        # Historical decryption: k1 ciphertext can still be decrypted using version=1
        decrypted_old = self.kms_broker.decrypt_bytes(p_id, ciphertext, nonce, 1, associated_data=aad)
        self.assertEqual(decrypted_old, secret_data)

    # -------------------------------------------------------------------------
    # 5. Sealed Enclave (.nbpack) Packaging & In-Memory Hydration (TODO-PRT-03)
    # -------------------------------------------------------------------------

    def test_05_sealed_enclave_nbpack_and_zero_disk_hydration(self):
        """Tests self-serve .nbpack sealing and in-memory enclave mounting with zero disk leakage."""
        t_id = "tenant_finance"
        p_id = "proj_settlement"

        secret_blueprint = {
            "domain": "settlement_engine",
            "internal_rules": ["Strict ledger balance", "Double-entry accounting"],
            "proprietary_prompts": {
                "agent_settler": "Verify all clearing records against FedWire invariants."
            }
        }

        # 1. Seal .nbpack envelope
        bundle = self.kms_broker.seal_nbpack_envelope(t_id, p_id, secret_blueprint, metadata={"author": "lead_architect"})
        self.assertEqual(bundle.envelope_format, "NBPACK_AES256_ED25519")
        self.assertEqual(bundle.version, "2.0.0")
        self.assertEqual(bundle.tenant_id, t_id)
        self.assertEqual(bundle.project_id, p_id)
        self.assertIsNotNone(bundle.merkle_seal)

        # 2. In-Memory Enclave Mount (Zero disk exposure)
        mounted_payload = self.kms_broker.mount_in_memory_enclave(p_id, bundle.to_dict())
        self.assertEqual(mounted_payload["domain"], "settlement_engine")
        self.assertEqual(mounted_payload["proprietary_prompts"]["agent_settler"], "Verify all clearing records against FedWire invariants.")

        # 3. Tampered signature rejection
        tampered_bundle = bundle.to_dict()
        tampered_bundle["signature_b64"] = base64.b64encode(b"invalid_signature_bytes_32b_pad__").decode("utf-8")
        with self.assertRaises(PermissionError):
            self.kms_broker.mount_in_memory_enclave(p_id, tampered_bundle)

    # -------------------------------------------------------------------------
    # 6. One-Click Project Scaffolding Wizard (TODO-PRT-02)
    # -------------------------------------------------------------------------

    def test_06_one_click_project_scaffolding_wizard(self):
        """Tests automated scaffolding of standard Quad-Space topology, genesis ledger minting, and KMS keys."""
        target_proj_dir = self.base_path / "scaffolded_demo_project"

        result = self.scaffolder.scaffold_project(
            tenant_id="tenant_quantum_cloud",
            project_id="proj_qsim",
            project_name="Quantum Simulator Platform",
            target_dir=target_proj_dir,
            mode="multi_module",
            billing_tier="plan_enterprise"
        )

        self.assertEqual(result.status, "SUCCESS")
        self.assertEqual(result.tenant_id, "tenant_quantum_cloud")
        self.assertEqual(result.project_id, "proj_qsim")
        self.assertEqual(result.genesis_recovery_point, "RP_GENESIS_000")
        self.assertIsNotNone(result.genesis_merkle_hash)
        self.assertEqual(len(result.genesis_merkle_hash), 64)

        # 1. Verify Quad-Space layout created on disk
        self.assertTrue((target_proj_dir / ".nb" / "context" / "contracts").exists())
        self.assertTrue((target_proj_dir / ".nb" / "context" / "ledger").exists())
        self.assertTrue((target_proj_dir / ".nb" / "context" / "rules").exists())
        self.assertTrue((target_proj_dir / ".nb" / "config").exists())
        self.assertTrue((target_proj_dir / ".nb" / "agentic" / "workflows").exists())
        self.assertTrue((target_proj_dir / "workplace" / "modules" / "mod_core_service").exists())
        self.assertTrue((target_proj_dir / "workplace" / "config").exists())
        self.assertTrue((target_proj_dir / "user" / "inputs" / "specs").exists())
        self.assertTrue((target_proj_dir / "user" / "hitl").exists())
        self.assertTrue((target_proj_dir / "user" / "outputs" / "dashboard").exists())

        # 2. Verify Genesis Merkle Ledger
        ledger_path = target_proj_dir / ".nb" / "context" / "ledger" / "context_ledger.yaml"
        self.assertTrue(ledger_path.exists())
        with open(ledger_path, "r", encoding="utf-8") as f:
            ledger_data = yaml.safe_load(f)
            self.assertEqual(ledger_data["tenant_id"], "tenant_quantum_cloud")
            self.assertEqual(ledger_data["project_id"], "proj_qsim")
            self.assertEqual(ledger_data["merkle_chain"][0]["recovery_point_id"], "RP_GENESIS_000")
            self.assertEqual(ledger_data["merkle_chain"][0]["block_height"], 0)
            self.assertEqual(ledger_data["recovery_points"][0]["id"], "RP_GENESIS_000")

        # 3. Verify Public sanitized ledger
        public_ledger_path = target_proj_dir / ".nb" / "context" / "ledger" / "context_ledger.public.yaml"
        self.assertTrue(public_ledger_path.exists())
        with open(public_ledger_path, "r", encoding="utf-8") as f:
            pub_data = yaml.safe_load(f)
            self.assertEqual(pub_data["latest_merkle_root"], result.genesis_merkle_hash)
            self.assertEqual(pub_data["active_recovery_point"], "RP_GENESIS_000")

        # 4. Verify Wire Contract Skeleton & Autonomous CI/CD Workflow
        contract_path = target_proj_dir / ".nb" / "context" / "contracts" / "service_contract.json"
        self.assertTrue(contract_path.exists())
        with open(contract_path, "r", encoding="utf-8") as f:
            cdata = json.load(f)
            self.assertIn("contract_id", cdata)

        cicd_path = target_proj_dir / ".nb" / "agentic" / "workflows" / "basic_autonomous_cicd.yaml"
        self.assertTrue(cicd_path.exists())

        # 5. Verify Project & Node registration in TenantManager
        proj_record = self.tenant_mgr.get_project("proj_qsim")
        self.assertIsNotNone(proj_record)
        nodes = self.tenant_mgr.list_nodes(project_id="proj_qsim")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].status, "HEALTHY")

        # 6. Verify Automated KMS Key Provisioning
        kms_key = self.kms_broker.get_active_key("proj_qsim")
        self.assertIsNotNone(kms_key)
        self.assertEqual(kms_key.key_id, result.kms_key_id)


if __name__ == "__main__":
    unittest.main()
