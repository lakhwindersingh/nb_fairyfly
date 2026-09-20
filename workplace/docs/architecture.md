# System Architecture & C4 Topologies

> **Autonomously Synchronized**: 2026-09-19T16:00:00+00:00  
> **Engine**: `agent_living_doc_architect` (CAP-21)  
> **Diagram Validation**: ✅ Valid Mermaid

## Overview
This document visualizes the complete high-level system topology, container boundaries, IDE plugin extensions, and communication pathways of the Percipience Context Engineering platform across Free Community, Team, Business, and Enterprise tiers.

```mermaid
graph TD
  subgraph Client_Layer["Client & Developer Interface Layer"]
    CLI["CLI Control Plane<br/>(.nb/bin/percipience)"]
    IntelliJ["IntelliJ IDEA / PyCharm Plugin<br/>(mod_intellij_plugin: ToolWindow + StatusBar)"]
    VSCode["VSCode Extension<br/>(mod_vscode_extension: LSP IPC + Webview)"]
    WebPortal["Percipience SaaS Cloud Portal<br/>(Portal Server: Plan Matrix, Gateway, Client Space)"]
    TimeTravelDash["Visual DAG & Time-Travel Console<br/>(user/outputs/dashboard/index.html)"]
  end

  subgraph Gateway_Enclave["Secure Context Gateway (Option 1)"]
    GW["Context Gateway Enclave<br/>(.nb/core/context_gateway.py)"]
    KMS["CMEK Secret Key Broker<br/>(arn:aws:kms:percipience-gateway)"]
    RAMEnclave["In-Memory RAM Vault<br/>(0.0% Client Plan Exposure)"]
  end

  subgraph Sandbox_Security["Sandbox Source Permission Broker"]
    Broker["SandboxPermissionBroker<br/>(READ_PRUNED_AST, READ_RAW, DENY_IMMUTABLE)"]
    ThirdPartyLLM["Third-Party AI Assistants<br/>(Copilot, Cody, JetBrains AI, Continue)"]
    Broker --> ThirdPartyLLM
  end

  subgraph Orchestration_Layer["Autonomous CI/CD & Agent Fleet"]
    Orchestrator["Autonomous CI/CD Orchestrator<br/>(basic_autonomous_cicd.yaml & pr_gatekeeper.yaml)"]
    CognitiveRouter["Model-Agnostic Cognitive Router<br/>(Tier A: Sonnet/Pro vs Tier B: Haiku/Flash)"]
    WorktreeEngine["Worktree Lease Engine<br/>(Active POSIX PID-Probing)"]
    Gatekeeper["PR Verification Gatekeeper<br/>(AST Skeletonizer & Contract Gate)"]
  end

  subgraph Specialist_Fleet["Specialist Agent Plugins (.nb/agentic/custom/agents/)"]
    FlakyAgent["Flaky Test Detector<br/>(agent_flaky_test_detector)"]
    ContractAgent["Contract Compatibility Guard<br/>(agent_contract_compatibility_checker)"]
    CVEAgent["Supply-Chain Sentinel<br/>(agent_dependency_cve_sentinel)"]
    DriftAgent["Doc Drift Synchronizer<br/>(agent_doc_drift_synchronizer)"]
    LivingDocAgent["Living Documentation Architect<br/>(agent_living_doc_architect)"]
  end

  subgraph Domain_Modules["Workplace Domain Modules (workplace/modules/)"]
    PluginMod["IntelliJ & VSCode Plugins<br/>(mod_intellij_plugin, mod_vscode_extension)"]
    TenantMod["Tenant Onboarding & BYOR<br/>(mod_tenant_onboarding)"]
    BillingMod["FinOps & 15% Metering<br/>(mod_billing_metering)"]
    ObsMod["Observability & Quarantines<br/>(mod_observability_usage)"]
    BridgeMod["Virtual Simulator Bridge<br/>(mod_shared_infra_bridge)"]
  end

  subgraph Enclave_Ledger["Cryptographic Merkle Enclave & Sealed State"]
    MerkleChain["Linear Merkle Hash Chain<br/>(SHA-256 Block Continuity)"]
    EpochArchive["Rolling Epoch Checkpoints<br/>(.nb/context/ledger/archive/)"]
    TokenLedger["Token FinOps Ledger<br/>(token_savings_ledger.yaml)"]
    HITLStores["Append-Only HITL Stores<br/>(user/hitl/poisoning/, user/hitl/flaky/)"]
  end

  CLI --> GW
  IntelliJ --> Broker
  VSCode --> Broker
  Broker --> Orchestrator
  WebPortal --> GW
  GW --> Orchestrator
  GW -.-> KMS
  GW -.-> RAMEnclave
  Orchestrator --> CognitiveRouter
  Orchestrator --> WorktreeEngine
  WorktreeEngine --> Domain_Modules
  Domain_Modules --> Gatekeeper
  Gatekeeper --> Specialist_Fleet
  Specialist_Fleet --> MerkleChain
  MerkleChain --> EpochArchive
  Gatekeeper --> TokenLedger
  Gatekeeper --> HITLStores
  TimeTravelDash -.-> MerkleChain
```

### Component Topologies
- **Client & Developer Interface Layer**: Host environment containing CLI (`.nb/bin/percipience`), IntelliJ/PyCharm Kotlin Plugin (`mod_intellij_plugin`), VSCode Extension (`mod_vscode_extension`), and Web Portal (`workplace/portal/server.py`).
- **Sandbox Source Permission Broker**: Brokers file read and write access for third-party IDE AI plugins (GitHub Copilot, Continue, Cody, JetBrains AI), enforcing AST token reduction by default (`READ_SOURCE_PRUNED`) and protecting immutable ledger zones (`DENY_IMMUTABLE`).
- **Context Gateway (Option 1)**: Architectural enclave ensuring 0% client-side plan exposure with in-flight prompt injection and `.nbpack` encrypted archives.
- **Orchestration Layer**: Quad-Space engine with cognitive tiering, POSIX PID-probed worktrees, and Autonomous CI/CD workflows (`basic_autonomous_cicd.yaml`).
- **Specialist Agent Fleet**: Pre-configured CI/CD subagents enforcing security, SemVer contracts, test stability, and living documentation.
- **Plan Tier Matrix & Boundary Ceilings**: 4 architectural tiers (`plan_free`, `plan_team`, `plan_business`, `plan_enterprise`) with strict isolation and concurrency ceilings.
