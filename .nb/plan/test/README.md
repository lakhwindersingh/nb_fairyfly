# 🧪 Percipience Master Test Plan Space (`.nb/plan/test/`)

> **Master Test Governance & Automated Verification Framework**  
> **Target Release**: Percipience Enterprise 2026 / 2027  
> **Status**: **ACTIVE & CODIFIED**  
> **Framework Stack**: **Pytest 8.4+ Enterprise Engine + Allure Report 2.x + DeepEval / Ragas AI Evaluation + Playwright 1.48+ E2E + OpenTelemetry GenAI**  

---

## 📌 Space Overview

The `.nb/plan/test/` space defines the authoritative, end-to-end testing blueprint for the **Neutron Binary Percipience Context Engineering OS & SaaS Platform**. It establishes an AI-assisted, fully automatable testing harness covering all 16 core subsystems across the 7 architecture plans and the unified codebase.

```text
📦 .nb/plan/test/
├── 📖 README.md              ← YOU ARE HERE (Quick Reference & Navigation)
├── 📋 MANIFEST.yaml          ← Cryptographic Hash & Line Count Version Manifest
├── 📄 concise.md             ← High-Density Test Specification for AI Context Ingestion
├── 📑 detailed.md            ← Exhaustive 360-Degree Implementation Test Plan
└── ⚙️ test_runner.py         ← Automatable AI-Assisted Test Orchestrator & Report Generator
```

---

## 🎯 Test Framework Rationale (2026 Modern Standard)

To satisfy the dual requirements of **human developer ergonomics** and **autonomous AI coding agent orchestration**, the testing stack is standardized on:

1. **Pytest 8.4+ / 9.x Enterprise Engine**:
   - Universal execution engine for backend services, AST compiler, cryptographic Merkle state, and CLI commands.
   - Strict async support (`pytest-asyncio`), parallel execution (`pytest-xdist`), and isolated mock workspaces.
2. **Allure Report 2.x & `pytest-json-report`**:
   - Machine-readable structured JSON outputs (`test_results.json`) consumed instantly by AI agents.
   - Interactive HTML visual reports with step-by-step logs, attachment diffs, and execution timelines.
3. **DeepEval / Ragas / G-Eval AI Evaluation Engine**:
   - Quantitative evaluation of LLM prompt outputs: **Faithfulness ($\ge 0.90$)**, **Hallucination Freedom ($\ge 0.95$)**, **Context Relevancy ($\ge 0.85$)**, and **Spec-to-Code Semantic Parity ($S_{SP} \ge 0.95$)**.
4. **OpenTelemetry GenAI (OTel) Distributed Tracing**:
   - Validates W3C `traceparent` headers and GenAI semantic spans (`gen_ai.system`, `gen_ai.usage.*`) in `context/ledger/otel_spans.jsonl`.
5. **Playwright 1.48+ & Vitest 2.x / Axe-Core**:
   - Headless browser testing of the SaaS Portal, interactive AST pruner playground, and WCAG 2.1 AA accessibility benchmarks.
6. **Percipience Autonomous Self-Healing Triad**:
   - Direct integration with `workplace/core/diagnostic_reprompt.py` to trigger bounded 3-step AI repair loops upon test failures.

---

## 🗺️ Subsystem Coverage Matrix (16 Pillars)

| Subsystem # | Architecture Subsystem & Pillar | Governing Plan Reference | Test Suite File(s) | Target Verification |
| :---: | :--- | :--- | :--- | :--- |
| **01** | **Quad-Space Standard Scaffolding & CLI** | `master/parent-master-plan` | `test_play3_suite.py` | CLI subcommands, space layout |
| **02** | **Structural AST Token Optimization** | `CAP-03`, `CAP-15` | `test_play3_suite.py` | Rust daemon, $<120\text{ms}$, 48–70% savings |
| **03** | **Cryptographic Merkle State Ledger** | `CAP-08` | `test_play3_suite.py` | SHA-256 DAG, epoch rolling, public view |
| **04** | **Immutable Cloud WORM Storage** | `CAP-08`, `CAP-18` | `test_play3_suite.py` | AWS S3 & GCP GCS Object Lock egress |
| **05** | **Context Poisoning & Surgical Rollback** | `CAP-02`, `CAP-29` | `test_play3_suite.py` | Secret scanning, rollback to $RP_k$ |
| **06** | **Sealed Binary Enclave (`.nbpack`)** | `CAP-14` | `test_play3_suite.py` | AES-256-GCM, RAM hydration, 0B disk |
| **07** | **Hybrid Context & Agent Plugin Engine** | `CAP-06`, `CAP-17` | `test_play3_suite.py` | 3-tier precedence, custom agent YAML |
| **08** | **Bring Your Own Repository (BYOR)** | `CAP-20` | `test_play3_suite.py` | GitLab/Bitbucket/GHES SSH & webhooks |
| **09** | **Cloud SaaS Portal & Microservices** | `l1/saas-portal-domain`, `CAP-13` | `test_portal_*.py` | 4 micro-modules, server endpoints |
| **10** | **FinOps Token Savings Metering** | `CAP-13`, `CAP-34` | `test_fleet_telemetry_finops.py` | 15% rev-share calculation & ledger |
| **11** | **Corporate UI & Web Quality (WCAG 2.1)** | `l2/corp-site-saas-portal` | `test_play3_suite.py` | Axe-core a11y, Lighthouse, link integrity |
| **12** | **Terraform Multi-Cloud Blueprints** | `CAP-18`, `CAP-30` | `test_play3_suite.py` | AWS EKS/RDS & GCP GKE/Cloud SQL IaC |
| **13** | **Autonomous CI/CD Triad & Plugins** | `CAP-27`, `CAP-28` | `test_play3_suite.py` | Flaky quarantine, contract compatibility |
| **14** | **Anti-Drift & 6-Vector Semantic Parity** | `CAP-09`, `CAP-26` | `test_play3_suite.py` | $S_{SP} \ge 0.95$, signed `HandoffToken` |
| **15** | **IDE Plugin Spaces (VS Code & JetBrains)**| `l1/vscode-plugin`, `l1/intellij`| `test_ide_plugins_space.py` | LSP 3.17, PSI AST analysis, packaging |
| **16** | **Distributed Swarms (DEWS) & Docker** | `CAP-AGT-01` to `CAP-AGT-10` | `test_dynamic_dag_orchestrator.py`| Container runners, Redlock leases |

---

## 🚀 Quick Execution Guide

### 1. Run Complete Automated Test Suite
```bash
python3 -m pytest workplace/tests/ -v
```

### 2. Run via AI-Assisted Test Orchestrator
```bash
# Execute specific tier with structured JSON output and AI evaluation
python3 .nb/plan/test/test_runner.py --tier all --report json,html

# Execute with automated AI failure diagnosis and surgical repair suggestions
python3 .nb/plan/test/test_runner.py --tier unit --ai-triage
```

### 3. Verify Links and MDX Documentation Integrity
```bash
bash workplace/templates/evaluation/link_checker_script.sh
```

---

## 🔗 Key Plan Documents

- **[Detailed Test Specification (`detailed.md`)](./detailed.md)**: Full 360-degree testing methodology, test suites, edge cases, and compliance verification.
- **[Concise Test Specification (`concise.md`)](./concise.md)**: Compact reference for fast AI agent context injection.
- **[Version Manifest (`MANIFEST.yaml`)](./MANIFEST.yaml)**: Cryptographic SHA-256 integrity hashes for all files in this space.
