"""
Percipience Core Workplace Modules:
Multi-Tenant Project Provisioning, Fleet Workspaces, IAM & KMS Enclaves.
Extends the core namespace to seamlessly merge workplace/core and .nb/core.
"""

import pkgutil
__path__ = pkgutil.extend_path(__path__, __name__)

from .tenant_manager import (
    TenantManager,
    TenantRole,
    Tenant,
    Project,
    Repository,
    WorkspaceNode,
    TenantUser,
)
from .project_scaffolder import ProjectScaffolder, ScaffoldResult
from .kms_broker import KMSBroker, KeyRecord, SealedEnclaveBundle
from .project_policy_engine import (
    ProjectPolicyManager,
    ProjectPolicy,
    AttentionSlicingPolicy,
    CognitiveRoutingPolicy,
    ASTPruningPolicy,
    SelfHealingSLAPolicy,
    WireContractRule
)

__all__ = [
    "TenantManager",
    "TenantRole",
    "Tenant",
    "Project",
    "Repository",
    "WorkspaceNode",
    "TenantUser",
    "ProjectScaffolder",
    "ScaffoldResult",
    "KMSBroker",
    "KeyRecord",
    "SealedEnclaveBundle",
    "ProjectPolicyManager",
    "ProjectPolicy",
    "AttentionSlicingPolicy",
    "CognitiveRoutingPolicy",
    "ASTPruningPolicy",
    "SelfHealingSLAPolicy",
    "WireContractRule"
]
