"""
Global runtime state and singletons for Percipience Portal.
Houses active tenant managers, KMS brokers, swarm memory engines,
fleet managers, and authenticated client session caches.
"""

from pathlib import Path
from typing import Dict, Any, Optional

REPO_ROOT = Path(__file__).resolve().parents[3]

from core.tenant_manager import TenantManager, TenantRole
from core.kms_broker import KMSBroker
from core.project_scaffolder import ProjectScaffolder
from core.project_policy_engine import ProjectPolicyManager
from core.dynamic_dag_orchestrator import DynamicDAGOrchestrator, StepNode
from core.agent_memory_engine import AgentMemoryEngine
from core.tool_contract_validator import ToolContractValidator
from core.agent_capability_guard import AgentCapabilityGuard
from core.fleet_manager import FleetManager


CLIENT_SESSIONS: Dict[str, Dict[str, Any]] = {}

DEMO_CLIENT = {
    "client_id": "acme_corp_fintech",
    "client_name": "Acme Global Financial Technologies",
    "tier": "Enterprise Tier A",
    "project_id": "proj_fairyfly_core_9921",
    "project_name": "NB Fairyfly Enterprise Trading Engine",
    "workspace_mode": "multi_module",
    "active_modules": ["mod_auth", "mod_billing", "mod_portal_marketing", "mod_trading"],
    "worm_vault_status": "LOCKED (S3 WORM)",
    "active_worktrees": 2,
    "gross_savings_usd": 15.6974,
    "rev_share_due_usd": 2.3546,
    "mcp_jira_connected": True
}

GLOBAL_TENANT_MGR = TenantManager(persistence_file=REPO_ROOT / ".nb" / "context" / "tenant_hierarchy.json")
GLOBAL_KMS_BROKER = KMSBroker(persistence_file=REPO_ROOT / ".nb" / "context" / "kms_keyring.json")
GLOBAL_SCAFFOLDER = ProjectScaffolder(GLOBAL_TENANT_MGR, GLOBAL_KMS_BROKER)
GLOBAL_POLICY_MGR = ProjectPolicyManager(policy_dir=REPO_ROOT / ".nb" / "config" / "policies")

# Seed demo enterprise tenant & project if not exists
if not GLOBAL_TENANT_MGR.get_tenant("tenant_acme_fintech"):
    GLOBAL_TENANT_MGR.create_tenant(
        tenant_id="tenant_acme_fintech",
        name="Acme Global Financial Technologies",
        tier="plan_enterprise",
        settings={"max_concurrent_nodes": 50}
    )
    GLOBAL_TENANT_MGR.create_project(
        tenant_id="tenant_acme_fintech",
        project_id="proj_fairyfly_core_9921",
        name="NB Fairyfly Enterprise Trading Engine",
        mode="multi_module",
        billing_tier="plan_enterprise"
    )
    GLOBAL_TENANT_MGR.register_repository(
        tenant_id="tenant_acme_fintech",
        project_id="proj_fairyfly_core_9921",
        repo_id="repo_fairyfly_core",
        name="nb_fairyfly",
        url="git@github.com:neutronbinary/nb_fairyfly.git"
    )
    GLOBAL_TENANT_MGR.register_workspace_node(
        tenant_id="tenant_acme_fintech",
        project_id="proj_fairyfly_core_9921",
        node_id="node_macbook_primary",
        hostname="macbook-pro.local",
        worktree_path=str(REPO_ROOT)
    )
    GLOBAL_TENANT_MGR.register_user(
        tenant_id="tenant_acme_fintech",
        user_id="user_super_alice",
        email="alice@acmeglobal.com",
        display_name="Alice (Enterprise Super Admin)",
        role=TenantRole.ENTERPRISE_SUPER_ADMIN
    )

# Section 17.1 Swarm coordination singletons
GLOBAL_SWARM_DAG = DynamicDAGOrchestrator(dag_id="percipience_swarm_pipeline")
if not GLOBAL_SWARM_DAG.nodes:
    GLOBAL_SWARM_DAG.add_node(StepNode(id="step_ingest_spec", action="ingest_spec", name="Ingest Specification", metadata={"agent": "agent_planner"}))
    GLOBAL_SWARM_DAG.add_node(StepNode(id="step_plan_architecture", action="plan_architecture", name="Synthesize Architecture", dependencies=["step_ingest_spec"], metadata={"agent": "agent_architect"}))
    GLOBAL_SWARM_DAG.add_node(StepNode(id="step_code_derivation", action="code_derivation", name="Derive Implementation", dependencies=["step_plan_architecture"], blast_radius=["workplace/core/engine.py"], metadata={"agent": "agent_coder"}))
    GLOBAL_SWARM_DAG.add_node(StepNode(id="step_verify_gate", action="verify_gate", name="Attest Verification Gate", dependencies=["step_code_derivation"], metadata={"agent": "agent_verifier"}))

GLOBAL_SWARM_MEMORY = AgentMemoryEngine(base_dir=REPO_ROOT / ".nb" / "context" / "swarm_memory")
if not GLOBAL_SWARM_MEMORY.get_concept("CONCEPT_DAG_EXPANSION"):
    GLOBAL_SWARM_MEMORY.store_concept(
        concept_id="CONCEPT_DAG_EXPANSION",
        title="Dynamic Runtime DAG Expansion",
        description="Enables autonomous agents to dynamically spawn sub-goals without cycle formation.",
        rules=["Verify acyclicity via Kahn algorithm", "Limit recursion depth <= 3", "Rewire terminal dependents"],
        tags=["dag", "orchestration", "subgoals"]
    )
if not GLOBAL_SWARM_MEMORY.get_concept("CONCEPT_CBAC_TOKENS"):
    GLOBAL_SWARM_MEMORY.store_concept(
        concept_id="CONCEPT_CBAC_TOKENS",
        title="Capability-Based Access Control",
        description="Cryptographic HMAC-signed capability tokens scoping agent filesystem and network access.",
        rules=["Enforce directory path sandboxing", "Reject loopback or shell breakout", "Require unexpired token"],
        tags=["security", "cbac", "sandbox"]
    )
GLOBAL_SWARM_MEMORY.record_episode(
    task_id="task_swarm_bootstrap",
    error_signature="NONE_SUCCESS",
    root_cause="Bootstrap initialization",
    patch_summary="Initialized 3-tier persistent memory, dynamic DAG orchestrator, and CBAC sandboxing.",
    resolution_status="RESOLVED",
    merkle_block_hash="0000abc123"
)

GLOBAL_SWARM_TOOLS = ToolContractValidator()
GLOBAL_SWARM_GUARD = AgentCapabilityGuard()
GLOBAL_FLEET_MGR = FleetManager(storage_path=REPO_ROOT / ".nb" / "context" / "fleet" / "fleet_registry.json")
