# Standard Template Kit for Percipience Layerable Domain Plans

> **Target Directory**: [`.nb/plan/templates/`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/templates/)  
> **Parent Framework**: [`.nb/plan/master/parent-master-plan/`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/master/parent-master-plan/)  
> **Sync Utility**: [`python3 .nb/plan/scripts/sync_plan_versions.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/scripts/sync_plan_versions.py)

---

## 1. Overview & Purpose

The **Percipience Context Engineering OS** employs a modular, two-tier plan architecture:
1. **Parent Master Framework Plans** ([`master/parent-master-plan/`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/master/parent-master-plan/) and [`master/parent-master-free-plan/`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/master/parent-master-free-plan/)): Provide generic, non-domain-specific governance—poly-module lifecycles, cryptographic Merkle ledgers, AST token compression, and autonomous CI/CD gates.
2. **Layerable Domain Plans** (`l1/`, `l2/`, `l3/`): Overlay onto the Parent Master Framework to inject domain-specific wire contracts, specialized subagents, runtime simulator bridges, and dynamic tier-permission matrices.

This directory provides the **Standardized 4-File Template Suite** for authoring, versioning, and distributing domain layers.

---

## 2. Standard 4-File Plan Architecture

Every layerable domain plan directory must contain exactly four standardized files:

```
.nb/plan/<layer_level>/<domain-slug>/
├── README.md        # Quick reference, overview, and navigation index (~30-50 lines)
├── MANIFEST.yaml    # Cryptographic ledger, line counts, dependencies & SHA-256 hashes
├── concise.md       # Compact domain specification for token-optimized context (~80-120 lines)
└── detailed.md      # Comprehensive engineering blueprint, wire contracts & test harnesses (~300-500 lines)
```

### File Responsibilities

| File | Primary Consumer | Target Size | Core Contents |
| :--- | :--- | :---: | :--- |
| **`README.md`** | Human Engineers & Quick Scanners | 30–50 lines | Domain summary, quick links, capability overview, and success criteria. |
| **`MANIFEST.yaml`** | Percipience CLI & Gatekeeper | 40–70 lines | Plan metadata, capability rating, dependencies, and cryptographic SHA-256 hashes. Synchronized via `sync_plan_versions.py`. |
| **`concise.md`** | LLM Agents (Prompt Context) | 80–120 lines | Fast-injection plan saving 60–80% tokens: frontmatter, executive overview, Mermaid diagram, quad-space mapping, and tier matrix. |
| **`detailed.md`** | Deep Planning, Refactoring & CI/CD | 300–500 lines | Full architectural blueprint: API wire contracts, invariant rules, subagent definitions, testing harnesses, and implementation phases. |

---

## 3. Template Catalog in this Directory

| Template File | Purpose |
| :--- | :--- |
| [**`README.md`**](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/templates/README.md) | Standard documentation and usage instructions for the template suite. |
| [**`MANIFEST.yaml`**](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/templates/MANIFEST.yaml) | Parameterized version manifest with cryptographic hash fields and dependency bindings. |
| [**`concise.md`**](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/templates/concise.md) | Compact domain plan template featuring frontmatter, Mermaid graph, quad-space layout, and CLI commands. |
| [**`detailed.md`**](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/templates/detailed.md) | Exhaustive implementation blueprint template covering architecture, contracts, agents, and testing. |
| [**`custom_domain_layer_template.md`**](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/templates/custom_domain_layer_template.md) | Standalone reference guide unifying concise and detailed specifications. |

---

## 4. Standard Placeholder Variables

When scaffolding a new plan from these templates, replace the following variables:

| Variable | Description | Example |
| :--- | :--- | :--- |
| `{{DOMAIN_SLUG}}` | Lowercase snake_case identifier | `iot_mobile_ecosystem` |
| `{{DOMAIN_NAME}}` | Human-readable title | `IoT & Mobile BLE Ecosystem` |
| `{{CAPABILITY_RATING}}` | Plan maturity tier | `L1` (Foundation), `L2` (Ecosystem), `L3` (Specialized) |
| `{{PARENT_PLAN}}` | Relative path to parent plan | `master/parent-master-plan/concise.md` |
| `{{CURRENT_DATE}}` | Date in ISO format | `2026-10-06` |
| `{{DOMAIN_CAPABILITY_1..4}}` | Core domain pillars | `GATT Characteristic Wire Contract Validation` |
| `{{DOMAIN_WIRE_CONTRACT_1..2}}` | Wire contract filenames | `ble_telemetry_packet_contract.yaml` |
| `{{DOMAIN_INVARIANT_RULE_1..2}}` | Rule filenames | `ble_packet_mtu_invariants.md` |
| `{{SPECIALIST_AGENT_1..2}}` | Subagent manifest IDs | `agent_embedded_firmware_specialist` |
| `{{DELIVERY_WORKFLOW}}` | Workflow manifest ID | `iot_mobile_delivery_flow.yaml` |
| `{{MODULE_PROVIDER}}` | Implementation module | `mod_embedded_firmware` |
| `{{MODULE_CONSUMER}}` | Implementation consumer | `mod_mobile_companion_app` |

---

## 5. Workflow: Scaffolding a New Layerable Plan

### Step 1: Create Plan Directory
```bash
# Example: Creating an L1 domain plan
mkdir -p .nb/plan/l1/my-new-domain
```

### Step 2: Copy Template Files
```bash
cp .nb/plan/templates/MANIFEST.yaml .nb/plan/l1/my-new-domain/
cp .nb/plan/templates/concise.md .nb/plan/l1/my-new-domain/
cp .nb/plan/templates/detailed.md .nb/plan/l1/my-new-domain/
cp .nb/plan/templates/README.md .nb/plan/l1/my-new-domain/README.md
```

### Step 3: Populate Placeholders
Replace all `{{...}}` tags across `MANIFEST.yaml`, `concise.md`, `detailed.md`, and `README.md` with your domain specifications.

### Step 4: Synchronize Cryptographic Hashes
```bash
python3 .nb/plan/scripts/sync_plan_versions.py
```
This updates line counts and SHA-256 content hashes in `MANIFEST.yaml` atomically.

### Step 5: Verify Plan Sync
```bash
python3 .nb/plan/scripts/sync_plan_versions.py --check-only
```

### Step 6: Package into Sealed `.nbpack` Envelope
```bash
./.nb/bin/percipience layer pack \
  --plan .nb/plan/l1/my-new-domain/concise.md \
  --output .nb/bundles/my_new_domain.nbpack
```
