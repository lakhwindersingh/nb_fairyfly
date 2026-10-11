---
plan_type: "layerable_domain_plan"
plan_id: "domain_npx_installer"
name: "NPX Instant Execution & Bootstrapping Architecture Plan"
parent_master_plan: "master/parent-master-plan/concise.md"
tier_mapping:
  tier_2: "Enterprise Domain Rules & Wire Contracts (.nb/context/contracts/, .nb/context/rules/)"
  tier_3: "Specialist Subagents & Delivery Workflows (.nb/agentic/custom/agents/, .nb/agentic/custom/workflows/)"
model_tiering_policy:
  provider_agnostic: true
  tier_a_model: "claude-3-7-sonnet / pro"
  tier_b_model: "claude-3-5-haiku / flash"
---

# Layerable Context Engineering Plan: NPX Instant Execution & Bootstrapping Space (Concise Plan)

### Executive Overview & Domain Grounding

This plan defines the **NPX Instant Execution and Bootstrapping Subsystem** for Percipience. It establishes zero-installation, single-command onboarding, repository initialization, and PR gatekeeping via `npx @neutronbinary/percipience` or `npx percipience`.

```mermaid
graph TD
  Developer["Developer / CI Runner"] -->|npx @neutronbinary/percipience init| NpxRunner["npx / Node.js Engine (>=18.0.0)"]
  NpxRunner --> Detect["Environment & Platform Detection"]
  Detect --> BinaryResolve{"Native Binary Available?"}
  BinaryResolve -->|Yes (darwin/linux/win)| ExecNative["Execute Prebuilt Binary (.nb/bin/percipience)"]
  BinaryResolve -->|No (Fallback)| ExecPython["Execute Python Bridge (.nb/core/ percipience)"]
  ExecNative --> Scaffold["Scaffold Quad-Space (.nb/, workplace/, user/)"]
  ExecPython --> Scaffold
  Scaffold --> ProvisionMcp["Provision .claude/mcp.json & settings.json"]
  Scaffold --> SealGenesis["Seal Genesis Merkle Block (#0)"]
  Scaffold --> FastPath["Install Fast-Path Script to package.json"]
```

---

## 1. Package Specification (`@neutronbinary/percipience`)

### 1.1. Package Manifest Layout (`package.json`)
```json
{
  "name": "@neutronbinary/percipience",
  "version": "1.0.0",
  "description": "Enterprise Context Engineering OS & Autonomous CI/CD Gatekeeper",
  "bin": {
    "percipience": "./bin/percipience-cli.js",
    "nb": "./bin/percipience-cli.js"
  },
  "engines": {
    "node": ">=18.0.0"
  },
  "files": [
    "bin/",
    "scripts/",
    "templates/",
    "vendor/",
    "README.md",
    "LICENSE"
  ],
  "optionalDependencies": {
    "@neutronbinary/percipience-darwin-arm64": "1.0.0",
    "@neutronbinary/percipience-darwin-x64": "1.0.0",
    "@neutronbinary/percipience-linux-x64": "1.0.0",
    "@neutronbinary/percipience-linux-arm64": "1.0.0",
    "@neutronbinary/percipience-win32-x64": "1.0.0"
  }
}
```

### 1.2. CLI Entry Point (`bin/percipience-cli.js`)
- **Node.js Wrapper**: Inspects host architecture (`process.arch`) and platform (`process.platform`).
- **Binary Resolution Order**:
  1. Local repository binary: `.nb/bin/percipience` (if initialized).
  2. Platform optional dependency binary in `node_modules/@neutronbinary/percipience-<os>-<arch>/bin/percipience`.
  3. Python fallback bridge invoking system Python (`python3 .nb/core/...`).
- **Execution Pipeline**: Forwards command line arguments, handles POSIX exit codes (`0` success, `1` general error, `2` security/gate failure), and pipes `stdio`.

---

## 2. Core Command Surface

| Subcommand | Purpose | Execution Mode | Target Invariants |
| :--- | :--- | :--- | :--- |
| `npx percipience init` | Scaffolds Quad-Space, provisions `.claude/mcp.json`, installs fast-path `.nb/bin/percipience`. | Ingested | $<3$s duration; Genesis block sealed. |
| `npx percipience bootstrap` | Idempotent workspace verification, environment checks, and binary integrity validation. | Ingested / Ephemeral | Zero mutation if already bootstrapped. |
| `npx percipience gate` | Autonomous PR Gatekeeper validation for CI/CD pipelines (GitHub Actions, GitLab CI). | Ephemeral | Strict exit code; evaluates AST compression & contracts. |
| `npx percipience audit` | Verifies SHA-256 Merkle chain continuity and context maturity score. | Ephemeral | Enforces Merkle height $\ge 1$ and maturity $\ge 0.85$. |
| `npx percipience tokens summary`| Outputs AST token compression metrics, FinOps ROI, and net savings. | Ephemeral | Reads `token_savings_ledger.yaml`. |
| `npx percipience status` | Reports active license tier, concurrent worktrees, and ledger height. | Ephemeral | Non-mutating read of context ledger. |

---

## 3. Dual Execution Modes

### 3.1. Mode A: Ephemeral Zero-Install (CI/CD Optimized)
- Runs completely inside the npm temporary cache (`~/.npm/_npx/`).
- Invoked in CI/CD without polluting project dependencies:
  ```yaml
  - name: Run Percipience PR Gatekeeper
    run: npx @neutronbinary/percipience gate --enforce-merkle-chain --min-maturity 0.85
  ```
- Guaranteed zero residual dependencies in `package.json` or `node_modules/`.

### 3.2. Mode B: Ingested Fast-Path (Developer Workstation)
- Invoked via `npx @neutronbinary/percipience init`.
- Writes `.nb/bin/percipience` native executable directly into the workspace.
- Injects npm convenience scripts into host `package.json`:
  ```json
  "scripts": {
    "percipience": "percipience",
    "gate": "percipience gate",
    "audit": "percipience audit --enforce-merkle-chain"
  }
  ```
- Provisions `.claude/mcp.json` pointing directly to local CLI.

---

## 4. Security Mesh & Enterprise Air-Gapped Operation

1. **Cryptographic Checksum Verification**:
   - Every downloaded prebuilt binary is verified against SHA-256 digests in `vendor/manifest.json`.
2. **Private Registry & Proxy Support**:
   - Reads standard npm configuration (`.npmrc`):
     ```ini
     @neutronbinary:registry=https://artifactory.corp.internal/artifactory/api/npm/npm-virtual/
     always-auth=true
     ```
3. **Offline / Air-Gapped Tarball Distribution**:
   - Supports local tarball installation:
     ```bash
     npx /shared/dist/neutronbinary-percipience-1.0.0.tgz init
     ```
