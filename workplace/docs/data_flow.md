# Data Transformation Pipelines & Event Streams

> **Autonomously Synchronized**: 2026-09-17T14:43:42.017830+00:00  
> **Engine**: `agent_living_doc_architect` (CAP-21)  
> **Diagram Validation**: Pipeline: ✅ Valid | State: ✅ Valid

## End-to-End Ingestion & Execution Pipeline
```mermaid
flowchart TD
  MVS["MVS Input Specs<br/>(user/inputs/templates/)"] --> Derivation["ASG Derivation Engine<br/>(Normalize into Canonical Graph)"]
  Derivation --> ASTPruner["Tree-Sitter AST Pruner<br/>(50%-70% Target Token Reduction)"]
  ASTPruner --> TierRouter{"Cognitive Router<br/>(.nb/config/token_compression_rules.yaml)"}
  
  TierRouter -->|"High Reasoning (Architecture / Security)"| TierA["Tier A (Frontier)<br/>Claude-3-7-Sonnet / Gemini-2.0-Pro"]
  TierRouter -->|"Fast / High Throughput (Diffs / Scaffolding)"| TierB["Tier B (Compact)<br/>Claude-3-5-Haiku / Gemini-2.0-Flash"]

  TierA --> Worktree["Ephemeral Sandboxed Worktree<br/>(.nb/workspaces/subagent_uuid/)"]
  TierB --> Worktree

  Worktree --> Gatekeeper["PR Verification Gatekeeper<br/>(6-Stage Security, Contract, & Flaky Checks)"]
  Gatekeeper --> LivingDoc["Living Doc Engine<br/>(Mermaid Synthesis into workplace/docs/)"]
  LivingDoc --> MerkleSeal["Merkle Hash Chain & Atomic Replace<br/>(.nb/context/ledger/context_ledger.yaml)"]
  MerkleSeal --> EpochArchive["Rolling Epoch Checkpointer<br/>(.nb/context/ledger/archive/epoch_*.json)"]
```

## Artifact State Lifecycle
```mermaid
stateDiagram-v2
  [*] --> Scaffolded: MVS Specification Derived
  Scaffolded --> InDevelopment: Worktree Lease Acquired
  InDevelopment --> Testing: Bounded TDD Execution
  Testing --> InDevelopment: Test Failure (Retry < 3)
  Testing --> Quarantined: Non-deterministic Flakiness Detected
  Quarantined --> Testing: Mock Injected / Stabilized
  Testing --> Verified: All Unit & Integration Tests Pass
  Verified --> LivingDocSynced: Living Documentation & Mermaid Visuals Compiled
  LivingDocSynced --> MerkleSealed: Atomic Merkle Block Append
  MerkleSealed --> [*]: PR Merged to Main
```
