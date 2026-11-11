# Sequential Plan Implementation & Zero-Drift Orchestration Framework

**Plan ID**: `master_sequential_plan_orchestrator`  
**Version**: `2.0.0`  
**Status**: Planned (Design Complete)  
**Layer**: Master Orchestration  

## Quick Links
- [Concise Specification](concise.md) - Agentic context-optimized operational specification with token budgeting & resumption
- [Detailed Specification](detailed.md) - Comprehensive implementation blueprint, wire contracts, and execution engine
- [Sync Status](MANIFEST.yaml) - Version and dependency tracking

## Summary
The **Sequential Plan Implementation & Zero-Drift Orchestration Framework** describes an end-to-end engine for synthesizing, verifying, testing, documenting, and sealing L1–L5 plans up to a requested target, using the master framework, plan manifests, and supporting reference documents.

Its design includes token-budget management and deterministic multi-session resumption; current Python runtime support is described below.

## Current Python Runtime

`WorkflowRunner.run_plan_by_id(target_plan_id, plan_executors=..., dry_run=...)` resolves the target's manifest dependency closure in prerequisite-first order. `dry_run=True` returns a `DRY_RUN` preview without invoking executors or writing state. Live execution requires `dry_run=False` and a callable registered for each canonical plan ID; no plan implementation executors are bundled, and missing executors fail closed.

Each callable receives `step` and `context`. `step` contains `plan_id`, `manifest_path`, `spec_files`, and canonical `dependency_ids`; `context["plan_handover_records"]` contains already verified direct prerequisites. After producing and testing real output files, the callable must seal a recovery point with `MerkleEngine.seal_block`, build a handover with `PlanHandoverVerifier.build_handover(step, workspace_root, artifact_paths, prerequisite_handovers, recovery_point_id)`, and return `{"status": "SUCCESS", "handover": handover}`. Artifact paths must be workspace-relative. Missing or altered artifacts, specifications, prerequisite hashes, or recovery points block execution and resumption.

Resumption is scoped to the same target and revalidates every completed dependency before skipping it. Recovery points created before versioned block hashes and block bindings are not eligible. The existing archived ledger contains legacy blocks without verifiable hash inputs; live sealing remains blocked until an operator establishes a trusted, auditable ledger migration or re-anchoring without discarding the historical records.

Live runs require a private, independently generated signing key of at least 32 bytes supplied as `BEEHIVE_ORCHESTRATOR_STATE_KEY` (or explicitly to the state manager); never commit the key. State is atomically replaced in a target-specific `orchestrator_state_<target-digest>.json` file, and live plan runs serialize on `plan_execution.lock`. The shared `plan_handovers.json` is a derived report; parity accepts it only when it exactly matches authenticated target state and revalidated handovers. A caller using a custom state path must not expect the default parity evaluator to find it. Previously public-key-signed legacy state is untrusted and must be re-executed or migrated through a separately trusted, audited process. HMAC alone does not prevent rollback of an entire valid old snapshot; anti-rollback requires a trusted monotonic external anchor.

Parity evidence must be supplied separately. `.nb/context/ledger/test_results.json` identifies a workspace-relative JUnit report using `junit_path` and `junit_sha256`; failed, skipped, inconsistent, missing, or altered reports score zero. `.nb/context/ledger/contract_compatibility_results.json` contains a nonempty `checks` array, each with workspace-relative `baseline_path` and `candidate_path` plus their `baseline_sha256` and `candidate_sha256`. Compatibility is conservative: unchanged schemas and optional top-level additions to closed schemas without pattern properties are accepted; unproven changes score zero. The design goals below, including autonomous agent implementation and token-budget orchestration, are not all implemented by this Python runtime.

## Core Pillars (Design Goals)

1. **Topological Dependency Resolution**: Uses plan `MANIFEST.yaml` dependencies to establish a prerequisite-first execution pipeline up to the requested target plan.
2. **Token Budget Engine & Phased Execution**: Real-time sliding window token accounting across turns, plans, and phases. Gracefully triggers suspension (`suspend_hook`) when remaining tokens drop below safety headroom ($\le 20,000$ tokens or $< 15\%$).
3. **Deterministic Re-Entrant Resumption**: Proposed CLI, token-budget, and worktree restoration are design goals, not current runtime capabilities. Current resumption uses authenticated target-specific state and revalidates each dependency before skipping it.
4. **Specialist Agent Architecture (`agent_sequential_plan_orchestrator`)**: 4-tier swarm authority tree with Tier A/B/C cognitive model cascading, hermetic Git worktree sandboxing, and bounded supervisor loops ($N_{\max} = 3$).
5. **Standardized Re-Entrant Hook Lifecycle**:
   - `pre_step_hook`: Differential SHA-256 state fingerprinting & skippability caching (`step_cache.json`).
   - `spawn_hook`: Pre-flight contract assertion, isolated ephemeral worktree leasing, and Redis Redlock synchronization.
   - `step_execution`: Bounded TDD self-repair, AST log slicing, attention budget enforcement, and prefix pinning.
   - `handoff_hook`: Cryptographic `HandoffToken` (HMAC-SHA256) passing state safely across agent boundaries.
   - `post_step_hook` / `verification_gate_hook`: 6-vector Semantic Parity scoring ($S_{SP} \ge 0.95$) and invariant assertion.
   - `sealing_hook`: Immutable Merkle DAG block appending to `context_ledger.yaml`, recovery point snapshotting ($RP_k$), and cloud WORM egress mirroring.
   - `suspend_hook` & `resume_hook`: Safe worktree serialization and zero-waste re-entry.
6. **Anti-Drift & Zero-Hallucination Governance**:
   - Composite 6-vector Semantic Parity scoring ($S_{SP} = 0.20 S_{\text{AST}} + 0.25 S_{\text{Contract}} + 0.20 S_{\text{Behavior}} + 0.15 S_{\text{Handover}} + 0.10 S_{\text{Doc}} + 0.10 S_{\text{SupplyChain}}$).
   - 4-pillar error classification (`TRANSIENT`, `STRUCTURAL`, `INVARIANT`, `HALLUCINATORY`) with automated surgical rollbacks to clean recovery points.
7. **Autonomous Living Documentation**: Continuous synthesis of Mermaid C4 diagrams, sequence flows, data pipelines, and contract catalogs in `workplace/docs/` after every plan increment.

## Dependencies
- **Requires**:
  - `master/parent-master-plan`
  - `master/plan-assessment`
- **Reference documents**:
  - `PLAN_GUIDE.md`
  - `PLAN_INDEX.md`
- **Enables**:
  - Systematic, hands-off sequential implementation of all L1→L5 plans
  - Multi-session phased delivery respecting token limits
  - Deterministic CI/CD pipeline execution
