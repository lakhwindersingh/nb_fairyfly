# Runtime Execution & Cross-Module Sequence Flows

> **Autonomously Synchronized**: 2026-09-17T02:01:16.569103+00:00  
> **Engine**: `agent_living_doc_architect` (CAP-21)  
> **Diagram Validation**: ✅ Valid Mermaid

## End-to-End Context Gateway & CI/CD Verification Flow
```mermaid
sequenceDiagram
  autonumber
  actor Dev as Untrusted Local Subagent (Host OS)
  participant Gateway as Context Gateway (Option 1)
  participant Router as Cognitive Router (Tier A / B)
  participant LLM as Provider LLM (Sonnet / Haiku / GPT)
  participant Gate as PR Verification Gatekeeper (6 Stages)
  participant LivingDoc as Living Doc Architect (CAP-21)
  participant Merkle as Merkle Ledger Engine

  Dev->>Gateway: POST /v1/chat/completions {plan_id, repo_state, messages}
  Note over Gateway: Hydrate .nbpack blueprint into volatile RAM (0% exposure)
  Gateway->>Router: Classify task complexity & allocate cognitive tier
  Router->>LLM: Dispatch in-flight system prompt + invariants
  LLM-->>Gateway: Raw generation (code diff & tests)
  Gateway->>Gateway: Sanitize output (strip proprietary plan markers)
  Gateway-->>Dev: Clean code diff & Merkle execution receipt

  Note over Dev,Gate: Subagent executes local bounded TDD in worktree
  Dev->>Gate: Trigger PR Gatekeeper verification (bin/percipience gate)
  Gate->>Gate: Stage 1: Content-addressable AST diff & token savings
  Gate->>Gate: Stage 2: Supply-chain CVE & license audit (agent_dependency_cve_sentinel)
  Gate->>Gate: Stage 3: Wire contract backward-compatibility check (agent_contract_compatibility_checker)
  Gate->>Gate: Stage 4: Multi-run flaky test isolation (agent_flaky_test_detector)
  Gate->>Gate: Stage 5: Bounded TDD verification & doc drift check (agent_doc_drift_synchronizer)
  
  Note over Gate,LivingDoc: Stage 6: Living Documentation & Mermaid Synthesis
  Gate->>LivingDoc: Trigger AST introspection & diagram compile
  LivingDoc->>LivingDoc: Check .scratch/doc_ast_hashes.json (skip unchanged)
  LivingDoc->>LivingDoc: Synthesize workplace/docs/*.md with verified Mermaid
  LivingDoc->>Merkle: Append Merkle block with doc revision hashes
  Merkle-->>Gate: Merkle Block Sealed (SHA-256)
  Gate-->>Dev: Gate Passed: Safe to Merge
```

### Flow Mechanics
1. **Option 1 Gateway**: In-flight prompt injection ensures local developer agent never touches KMS keys or encrypted .nbpack plan contents.
2. **Deterministic TDD**: Worktree develops in isolation, executing bounded retry loops.
3. **Multi-Stage Verification**: All 6 PR verification stages run deterministically.
4. **Living Documentation**: AST changes automatically trigger doc updates before Merkle sealing.
