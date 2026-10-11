# Standard Template Suite for Percipience Canonical Domain Plans (v3.0)

> **Target Directory**: [`.nb/plan/templates/`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/templates/)  
> **Reference Schema**: [`.nb/plan/MANIFEST_SCHEMA.json`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/MANIFEST_SCHEMA.json)  
> **Parity Audit Checklist**: [`.nb/plan/PARITY_AUDIT_CHECKLIST.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/PARITY_AUDIT_CHECKLIST.md)  
> **Automated Validation Suite**: [`bash .nb/plan/scripts/validate.sh`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/scripts/validate.sh)  
> **Sync Utility**: [`python3 .nb/plan/scripts/sync_plan_versions.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/scripts/sync_plan_versions.py)

---

## 1. Overview & Architecture Standards

The **Percipience Context Engineering Framework** governs workspace orchestration, contract validation, and multi-agent execution across an active 3-tier hierarchy:
1. **Master Architecture Plans** (`.nb/plan/master/`): Generic governance—poly-module lifecycles, cryptographic Merkle ledgers, AST token compression, security mesh, enterprise UI design systems, and sequential pipeline orchestration.
2. **Layerable Domain Plans** (`.nb/plan/l1/`): Modular capabilities—SaaS portal, VSCode extension, IntelliJ/PyCharm plugin, npx installer, and tiered wheel packaging.
3. **Verification & Test Plans** (`.nb/plan/test/`): Automated end-to-end regression harnesses and contract verification.

This directory provides the **Canonical 4-File Template Suite** conforming to **Manifest Schema v3.0**, enabling rapid scaffolding of production-ready, acyclic, and cryptographically verified plans.

---

## 2. Standard 4-File Plan Pattern

Every domain plan directory must contain exactly four standardized, synchronized files:

```
.nb/plan/<layer_level>/<domain-slug>/
├── README.md        # Human-readable navigation, capability summary & quick reference (~30-50 lines)
├── MANIFEST.yaml    # Canonical v3.0 metadata, maturity, semantic parity, DAG dependencies & SHA-256 hashes
├── concise.md       # Compact domain specification for token-optimized agentic context (~90-150 lines)
└── detailed.md      # Comprehensive engineering blueprint, wire contracts, visual DAGs & test harness (~350-550 lines)
```

### Core Invariants & File Responsibilities

| File | Primary Consumer | Target Line Count | Invariant Rules & Responsibilities |
| :--- | :--- | :---: | :--- |
| **`MANIFEST.yaml`** | Plan Gatekeeper & CI/CD | 45–75 lines | Strictly adheres to [`MANIFEST_SCHEMA.json`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/MANIFEST_SCHEMA.json). Contains `maturity`, `semantic_parity` (6 vectors), acyclic `dependencies`, and SHA-256 content hashes. |
| **`README.md`** | Human Engineers & Audits | 30–50 lines | High-level architectural overview, capability bullet points, cross-links, and execution prerequisites. |
| **`concise.md`** | Agent Prompt Context | 90–150 lines | Compact domain specification saving 60–80% tokens: YAML frontmatter, executive grounding, Mermaid pipeline DAG, quad-space layout, dynamic tier matrix, and CLI commands. |
| **`detailed.md`** | Deep Planning & Verification | 350–550 lines | Complete implementation guide: Full wire contract schemas, visual pipeline DAG & stage contract inspection drawer specs, specialist subagents, security mesh, and 100% test harness. |

> [!IMPORTANT]
> **Line Count Invariant**: `N_lines(concise.md) < N_lines(detailed.md)` is strictly enforced across all plan validation gates.

---

## 3. Canonical Schema v3.0 & Parity Vectors

Plans generated from these templates must fulfill the two core v3.0 quality pillars:

### 3.1. Maturity Model
```yaml
maturity:
  stage: "IMPLEMENTATION_READY"       # PLANNED | ACTIVE_DRAFT | IMPLEMENTATION_READY | COMPLETED | DEPRECATED
  implementation_status: "production_runtime"
  test_coverage: 100                  # 0 to 100%
  production_ready: true
```

### 3.2. 6-Vector Semantic Parity Audit
```yaml
semantic_parity:
  composite_score: 0.985              # Must be >= 0.95 for production readiness
  gate_status: "PASSED"               # PASSED | WARNING | BLOCKED
  vectors:
    ast_parity: 0.99                  # Code structural congruence against specs
    contract_parity: 0.98             # JSON/YAML wire schema completeness
    behavior_parity: 0.99             # Runtime execution and assertion consistency
    handover_parity: 0.98             # Inter-module Ed25519 token attestation
    doc_parity: 0.98                  # Parity between concise.md, detailed.md & code
    supply_chain_parity: 0.99         # Integrity of dependencies, hashes, and lockfiles
```

---

## 4. Architectural Enhancements Included in Templates

1. **Visual Pipeline DAG & Stage Contract Inspection Drawer**:
   - Visual workflow DAG representations compatible with IntelliJ/PyCharm, VSCode, and SaaS Portal surfaces.
   - Interactive pipeline stages with explicit `handled_contracts` per stage (input schema, output schema, preconditions, postconditions, and mock payloads).
   - Expandable contract drawer specifications for real-time inspection during CI/CD execution.
2. **Clean Quad-Space Architecture**:
   - `.nb/`: Platform governance, schemas, rules, subagents, and delivery workflows.
   - `workplace/`: Production modules (`workplace/modules/`), test suites (`workplace/tests/`), portals, and plugins.
   - `user/`: Sparse specifications (`user/inputs/`), execution outputs (`user/outputs/`), and poisoning quarantine (`user/hitl/`).
   - Ephemeral: Isolated Git worktrees for safe, hermetic agent operations.
3. **Security Mesh & Tenant Context Isolation**:
   - Ed25519 signed handoff tokens preventing unauthorized pipeline jumps.
   - Per-module surgical rollback isolating faults without polluting sibling modules.
   - Terminology-agnostic, responsive glassmorphism UI design tokens.
4. **FinOps Token Analytics & Model Tiering**:
   - Explicit token budgeting in frontmatter.
   - Tier A (pro reasoning) vs Tier B (flash speed) allocation.
   - Content-addressable AST token pruning targeting $\ge 60\%$ context reduction.

---

## 5. Template Placeholder Catalog

When scaffolding a new plan from this directory, substitute the following variables:

| Placeholder Variable | Description | Canonical Example |
| :--- | :--- | :--- |
| `{{DOMAIN_SLUG}}` | Lowercase snake_case identifier | `cloud_provisioner` |
| `{{DOMAIN_NAME}}` | Human-readable domain title | `Cloud Infrastructure Provisioner` |
| `{{LAYER}}` | Target hierarchy layer | `master` or `l1` |
| `{{CAPABILITY_RATING}}` | Maturity rating badge | `TIER_L1` or `MASTER` |
| `{{PARENT_PLAN}}` | Relative path to parent plan | `master/parent-master-plan/concise.md` |
| `{{CURRENT_DATE}}` | ISO date string | `2026-10-11` |
| `{{SHA256_HASH}}` | Placeholder computed by sync tool | Auto-populated by `sync_plan_versions.py` |
| `{{DOMAIN_CAPABILITY_1..4}}` | Core domain pillars | `Hermetic Multi-Region Resource Orchestration` |
| `{{DOMAIN_WIRE_CONTRACT_1..2}}` | Wire contract filenames | `resource_provisioning_contract.yaml` |
| `{{DOMAIN_INVARIANT_RULE_1..2}}` | Safety rule filenames | `cross_region_isolation_invariants.md` |
| `{{SPECIALIST_AGENT_1..2}}` | Subagent manifest identifiers | `agent_infra_provisioning_specialist` |
| `{{DELIVERY_WORKFLOW}}` | Pipeline workflow manifest ID | `infra_delivery_flow.yaml` |
| `{{MODULE_PROVIDER}}` | Provider implementation module | `mod_infra_engine` |
| `{{MODULE_CONSUMER}}` | Consumer implementation module | `mod_infra_client` |

---

## 6. Scaffolding & Verification Workflow

Follow this step-by-step procedure to create, populate, and certify a new plan:

### Step 1: Create Plan Directory
```bash
# Example: Creating an L1 domain plan
mkdir -p .nb/plan/l1/my-new-domain
```

### Step 2: Copy Canonical Template Files
```bash
cp .nb/plan/templates/MANIFEST.yaml .nb/plan/l1/my-new-domain/
cp .nb/plan/templates/README.md .nb/plan/l1/my-new-domain/
cp .nb/plan/templates/concise.md .nb/plan/l1/my-new-domain/
cp .nb/plan/templates/detailed.md .nb/plan/l1/my-new-domain/
```

### Step 3: Populate Domain Placeholders
Replace all `{{...}}` tags across all four files with your domain-specific architectural specifications.

### Step 4: Synchronize Line Counts & Cryptographic Hashes
```bash
python3 .nb/plan/scripts/sync_plan_versions.py
```
This computes and records exact SHA-256 hashes and line counts into `MANIFEST.yaml`.

### Step 5: Execute Automated Plan Integrity Gates
```bash
bash .nb/plan/scripts/validate.sh
```
This validates:
- Schema v3.0 compliance via [`MANIFEST_SCHEMA.json`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/MANIFEST_SCHEMA.json).
- Dependency DAG cycle freedom and topological ordering.
- 100% cryptographic SHA-256 hash matching.
- Automatic regeneration of [`CAPABILITY_MATRIX.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/CAPABILITY_MATRIX.md).

### Step 6: Verify Regression Test Suite
```bash
pytest workplace/tests/
```
Ensure 100% test pass rate across all workplace unit, integration, and security tests.
