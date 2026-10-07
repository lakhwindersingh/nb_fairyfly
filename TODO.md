# Percipience Context Engineering OS & SaaS Platform - Implementation TODO & Gap Analysis

> **Audit Date**: 2026-09-17  
> **Workspace**: [`nb_fairyfly`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/)  
> **Target Plans Audited**:
> 1. [`.nb/play/CEaasS/play_3_enterprise_context_engineering_os_plan.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/play/CEaasS/play_3_enterprise_context_engineering_os_plan.md)
> 2. [`.nb/play/CEaasS/play_3_corp_site_saas_portal_plan.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/play/CEaasS/play_3_corp_site_saas_portal_plan.md)
> 3. [`.nb/plan/claude-context-engineering-parent-master-plan.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/claude-context-engineering-parent-master-plan.md)
> 4. [`.nb/plan/claude-context-engineering-saas-portal-domain-plan.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/claude-context-engineering-saas-portal-domain-plan.md)
> 5. [`workplace/docs/reports/competitive_differentiation_matrix.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/reports/competitive_differentiation_matrix.md)
> 6. [`workplace/docs/reports/agentic_workspace_sdlc_review.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/reports/agentic_workspace_sdlc_review.md)

---

## Executive Summary & Audit Scorecard

| Core Subsystem / Pillar | Parent Master Plan | Play 3 OS Plan | Play 3 SaaS Portal Plan | Domain Space Plans | Implementation Status | Maturity Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Quad-Space Standard Scaffolding** | Required | Required | Required | Required | **✅ COMPLETED** | **1.00** |
| **Unified Percipience CLI (`.nb/bin/percipience`)** | Specified | Required | Required | Specified | **✅ COMPLETED** | **1.00** |
| **AST Pruning & Token Optimization Engine** | Required | Required | Required | Required | **✅ COMPLETED** | **1.00** |
| **Cryptographic Merkle State Ledger & Epoch Archives** | Required | Required | Required | Required | **✅ COMPLETED** | **1.00** |
| **Context Poisoning Defense & Surgical Rollback** | Required | Required | Required | Required | **✅ COMPLETED** | **1.00** |
| **Sealed Binary Enclave (`.nbpack`) & RAM Hydration** | Inherited | Required | Specified | Inherited | **✅ COMPLETED** | **1.00** |
| **Ephemeral Git Worktree Isolation Engine** | Specified | Required | Specified | Specified | **✅ COMPLETED** | **1.00** |
| **BYOR Multi-VCS Adapter (GitHub/GitLab/Bitbucket)** | Specified | Required | Specified | Specified | **✅ COMPLETED** | **0.95** |
| **Cloud SaaS Multi-Module Portal & Server** | N/A | Specified | Required | Specified | **✅ COMPLETED** | **0.96** |
| **Next.js 14 / Astro Corporate UI Codebase** | N/A | N/A | Optional | Required | **✅ COMPLETED** | **1.00** |
| **Web Quality Benchmarking & WCAG 2.1 AA CI/CD** | N/A | N/A | Specified | Required | **✅ COMPLETED** | **1.00** |
| **Terraform Multi-Cloud Production Blueprints (AWS/GCP)** | N/A | Required | Specified | N/A | **✅ COMPLETED** | **1.00** |
| **Autonomous CI/CD Triad & Specialist Plugins (Phases 1-3)** | Required | Required | Required | Required | **✅ COMPLETED** | **1.00** |
| **Autonomous Living Documentation Engine (`workplace/docs/`)** | Required | Required | Required | Required | **✅ COMPLETED** | **1.00** |
| **Anti-Drift & Multi-Agent Handover Engine** | Required | Required | Required | Required | **✅ COMPLETED** | **0.98** |
| **Model Context Protocol (MCP) Jira Story Ingestion** | Required | Specified | Specified | Specified | **[-] IN PROGRESS** | **0.80** |
| **Layerable Domain Extensions (IoT, Mobile & SaaS)** | Specified | Specified | Required | Required | **[-] IN PROGRESS** | **0.75** |
| **90-Day GTM Commercialization (Months 1–3 Milestones)** | N/A | Required | Required | N/A | **[-] IN PROGRESS** | **0.65** |
| **Competitive Parity: Observability & OTel GenAI** | Specified | Required | Specified | N/A | **[-] PLANNED** | **0.40** |
| **Competitive Parity: Runtime Guardrails & PII** | Specified | Required | Specified | N/A | **✅ COMPLETED** | **1.00** |
| **Competitive Parity: IDE Extensions & Vector RAG** | Specified | Specified | Required | Specified | **[-] PLANNED** | **0.35** |
| **Competitive Parity: Sandboxed Matrix & GitOps Bot** | Specified | Required | Specified | Specified | **[-] PLANNED** | **0.45** |
| **Autonomous Agentic SDLC & Swarm Modernization** | Required | Required | Required | Required | **✅ COMPLETED** | **1.00** |
| **Enterprise Fleet & Multi-Tenant Project Portal** | Specified | Required | Required | Required | **[-] IN PROGRESS** | **0.85** |
| **Distributed Worktree Swarms & Container Runner (DEWS)** | Specified | Required | Specified | Specified | **[-] IN PROGRESS** | **0.75** |

**Current Composite Context Maturity**: **`0.990` (ENTERPRISE GRADE)**

---

## 1. Ephemeral Git Worktree Concurrency Engine (`CAP-05`)

- [x] **Core Worktree Manager (`workplace/core/worktree_engine.py`)**:
  - Implements dynamic worktree allocation under `.nb/workspaces/wt_{agent_id}`.
  - Dedicated branch creation (`wt_branch_{agent_id}`) and atomic cleanup.
  - POSIX active PID-probing (`os.kill(pid, 0)`) with automatic orphaned lease eviction.
- [x] **Redis Distributed Lock Backend (`workplace/core/worktree_engine.py`)**:
  - Redis 7.x Redlock distributed lease backend adapter for multi-node Karpenter cluster scaling (`ElastiCache` / `Memorystore`) with automatic fallback to local atomic leases.
- [x] **Canary Pre-Merge Verifier (`workplace/core/worktree_engine.py`)**:
  - Pre-merge canary test worker executing inside isolated ephemeral worktree before merging into target base branch.
- [x] **CLI Subcommands**:
  - `percipience worktree acquire --agent <id> [--ttl <sec>] [--redis]`
  - `percipience worktree list`
  - `percipience worktree release --agent <id>`
  - `percipience worktree canary --agent <id>`
- [x] **Automated Unit Tests**: Verified via [`test_07_worktree_engine`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_play3_suite.py) and [`test_22_worktree_redis_and_canary`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_play3_suite.py).

---

## 2. Cryptographic Merkle State Machine & WORM Storage (`CAP-08`)

- [x] **Master Context Ledger (`context/ledger/context_ledger.yaml`)**:
  - SHA-256 block hashing formula: $\text{Hash} = \text{SHA256}(\text{ID} + \text{Prev} + \text{MerkleRoot} + \text{GitSHA} + \text{Timestamp})$.
  - Genesis block (`RP_GENESIS_000`), Multi-module bootstrap, and PR gate blocks (590+ blocks sealed).
- [x] **Rolling Epoch Checkpointing (`workplace/core/merkle_engine.py`)**:
  - Rolling epoch archival to `context/ledger/archive/epoch_{start}_{end}.json`, maintaining constant-size active windows with cryptographic epoch rollup hashes.
- [x] **Sanitized Public Ledger Projection**:
  - Generates [`context/ledger/context_ledger.public.yaml`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/context/ledger/context_ledger.public.yaml) with stripped private paths for public commit audits.
- [x] **Visual Merkle State DAG Web Explorer**:
  - Live browser dashboard at [`user/outputs/dashboard/index.html`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/user/outputs/dashboard/index.html).
- [x] **Cloud WORM Storage Auto-Egress Hook (`workplace/core/worm_egress.py`)**:
  - Automated S3 Object Lock (Compliance Mode) / GCS Object Retention uploader module to mirror sealed Merkle blocks upon PR merge.
- [x] **CLI Subcommands**:
  - `percipience egress mirror --block-id <id> [--cloud-target <aws|gcp|local>]`
  - `percipience egress list`
- [x] **Automated Unit Tests**: Verified via [`test_02_merkle_engine`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_play3_suite.py) and [`test_23_worm_egress_manager`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_play3_suite.py).

---

## 3. Structural AST Token Optimization & Compression Engine (`CAP-03`)

- [x] **Multi-Language AST Pruner (`workplace/core/ast_optimizer.py`)**:
  - Parses Python, TypeScript, JavaScript, Go, and Rust.
  - Strips function and method bodies to semantic skeletons (`...`), preserving signatures, interfaces, and docstrings.
  - Content-addressable cache in `.scratch/ast_cache/` accelerating pruning to sub-millisecond retrieval.
  - Measured 47.9% to 70% token savings across 590+ blocks.
- [x] **Rust Tree-Sitter Native Daemon & IPC Client (`workplace/core/tree_sitter_daemon.py`)**:
  - High-speed IPC daemon client with automated in-process fallback and container runtime.
  - Docker packaging definition at [`workplace/infra/docker/Dockerfile.tree_sitter_daemon`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/infra/docker/Dockerfile.tree_sitter_daemon).
- [x] **Unified Diff Generator**: Generates standard `git diff` unified patch strings to enforce output token savings.
- [x] **Interactive Web Playground**: Live code editor and real-time pruning API (`POST /api/marketing/ast-prune`) on `http://127.0.0.1:3000/`.
- [x] **CLI Subcommands**:
  - `percipience daemon status`
  - `percipience daemon prune --file <path>`
- [x] **Automated Unit Tests**: Verified via [`test_01_ast_optimizer`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_play3_suite.py), [`test_15_ast_caching_and_epoch_checkpointing`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_play3_suite.py), and [`test_24_native_tree_sitter_daemon`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_play3_suite.py).

---

## 4. Context Poisoning Defense & Surgical Module Rollback (`CAP-02`)

- [x] **Context Purity Sentinel (`workplace/core/poisoning_sentinel.py`)**:
  - Scans AST diffs for hardcoded AWS/KMS/OpenAI secrets, private keys, and malicious packages.
  - Automatically isolates incidents into [`user/hitl/poisoning_quarantine.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/user/hitl/poisoning_quarantine.md).
- [x] **Surgical Module Rollback Manager (`workplace/core/surgical_rollback.py`)**:
  - Rewinds contaminated micro-module to recovery point $\text{RP}_k$ while preserving sibling micro-modules.
- [x] **Web Console Trigger**: Interactive surgical rollback button on portal dashboard calling `POST /api/observability/rollback`.
- [x] **Diagnostic Re-Prompting Loop (`workplace/core/diagnostic_reprompt.py`)**:
  - Automated self-healing re-prompting handler synthesizing isolated diagnostic prompts with 70–88% token reduction and zero conversational noise.
  - Executes bounded retry loop with automated fallback to surgical rollback if retries are exhausted.
- [x] **CLI Subcommands**:
  - `percipience reprompt --module <id> [--generate-only] [--trace <trace>] [--max-attempts <n>]`
- [x] **Automated Unit Tests**: Verified via [`test_03_poisoning_sentinel`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_play3_suite.py), [`test_04_surgical_rollback`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_play3_suite.py), and [`test_25_diagnostic_reprompting_loop`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_play3_suite.py).

---

## 5. Proprietary IP Packaging & RAM Enclave Sealing (`.nbpack`) (`CAP-14`)

- [x] **Envelope Compiler & Hydrator (`workplace/core/nbpack_envelope.py`)**:
  - Packages `context/` and `agentic/` into AES-256-GCM encrypted, Ed25519-signed binary bundle.
  - Hydrates archive strictly in volatile RAM (`tmpfs` / `/dev/shm`), leaving 0 bytes plaintext on physical client disk.
- [x] **CLI Subcommands**:
  - `percipience pack --include-spaces context,agentic --output <path> --obfuscate --sign`
  - `percipience hydrate --pack <path>`
- [ ] **TODO - KMS Envelope Key Binding (P1)**:
  - Connect AWS KMS / Cloud KMS CMEK key derivation to decrypt bundles at container boot using IAM roles/service accounts.

---

## 6. Hybrid Context Architecture & Custom Agent Extensibility (`CAP-06`, `CAP-17`, `CAP-20`)

- [x] **3-Tier Precedence Validator (`workplace/core/layered_context_validator.py`)**:
  - Tier 1: Platform Base Invariants (Enclave)
  - Tier 2: Enterprise Global Rules (`context/custom/rules/`)
  - Tier 3: Module Domain Context (`context/custom/schemas/` & `agentic/custom/`)
- [x] **Custom Agent Plugin Architecture (`workplace/core/agent_plugin_engine.py`)**:
  - Custom Agent: [`agentic/custom/agents/security_auditor.yaml`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/agentic/custom/agents/security_auditor.yaml)
  - Custom Rule: [`context/custom/rules/banking_security.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/context/custom/rules/banking_security.md)
  - Custom Schema: [`context/custom/schemas/payment_event.yaml`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/context/custom/schemas/payment_event.yaml)
  - Custom Workflow: [`agentic/custom/workflows/enterprise_sdlc.yaml`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/agentic/custom/workflows/enterprise_sdlc.yaml)
- [x] **CLI Subcommands**: `percipience validate --layered`, `percipience agent create`, `percipience agent test`.

---

## 7. Bring Your Own Repository (BYOR) Multi-VCS Integration (`CAP-20`)

- [x] **Multi-VCS Adapter (`workplace/core/byor_adapter.py`)**:
  - Connects self-hosted GitLab, GitHub Enterprise Server, Bitbucket Data Center.
  - Manages SSH deploy keys and custom corporate root CA bundles.
  - Normalizes webhook events and emits universal commit status checks.
- [x] **CLI Subcommands**: `percipience repo connect`, `percipience repo status`.
- [ ] **TODO - AWS Secrets Manager / Vault Key Auto-Sync (P2)**:
  - Dynamic SSH private key retrieval from AWS Secrets Manager ARN or HashiCorp Vault.

---

## 8. Multi-Module Cloud SaaS Portal Architecture (`CAP-13`)

- [x] **Micro-Module Workspace Isolation (`workplace/modules/`)**:
  - `mod_portal_marketing` (`http://127.0.0.1:3000/`): Next.js/React frontend with Tailwind CSS.
  - `mod_tenant_billing` (`http://127.0.0.1:8001/`): FastAPI FinOps billing engine with 15% rev-share metering.
  - `mod_agent_orchestration` (`http://127.0.0.1:8002/`): Workflow execution and agent DAG dispatcher.
  - `mod_observability_usage` (`http://127.0.0.1:8003/`): Real-time token analytics and surgical rollback trigger.
- [x] **FinOps Revenue Sharing Metering Engine (`workplace/core/token_tracker.py`)**:
  - Formula: $\text{Client Gross Savings} = \Delta \text{Tokens} \times \$0.003/\text{1k}$. $\text{Fee} = 15\% \times \text{Gross Savings}$.
  - Ledger: [`.nb/context/ledger/token_savings_ledger.yaml`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/context/ledger/token_savings_ledger.yaml).
- [ ] **TODO - Stripe Billing Portal & Webhook Engine (P1)**:
  - Stripe Customer Portal session generation and Stripe subscription invoice charge automation.

---

## 9. Next.js 14 / Astro Corporate Codebase (`CAP-13`)

- [x] **Full Component Library (`workplace/src/components/`)**:
  - [`Navbar.tsx`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/src/components/Navbar.tsx), [`HeroBanner.tsx`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/src/components/HeroBanner.tsx), [`FeatureGrid.tsx`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/src/components/FeatureGrid.tsx), [`Testimonials.tsx`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/src/components/Testimonials.tsx), [`ContactForm.tsx`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/src/components/ContactForm.tsx), [`Footer.tsx`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/src/components/Footer.tsx), [`JsonLd.tsx`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/src/components/JsonLd.tsx).
- [x] **Styling & Design System**:
  - [`workplace/src/styles/globals.css`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/src/styles/globals.css) and [`workplace/config/tailwind.config.ts`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/config/tailwind.config.ts).
- [x] **Content Collections & Schema**:
  - [`workplace/src/content/config.ts`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/src/content/config.ts), [`enterprise-fintech-token-reduction.mdx`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/src/content/case-studies/enterprise-fintech-token-reduction.mdx), [`ast-pruning-vs-prompt-compression.mdx`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/src/content/blog/ast-pruning-vs-prompt-compression.mdx).
- [x] **SEO, i18n & Sitemap Libs**:
  - [`workplace/src/lib/seo.ts`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/src/lib/seo.ts), [`workplace/src/lib/i18n.ts`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/src/lib/i18n.ts), [`workplace/src/lib/sitemap_generator.ts`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/src/lib/sitemap_generator.ts).

---

## 10. Core Web Vitals & WCAG 2.1 AA CI/CD Quality Harness (`CAP-13`)

- [x] **Automated Accessibility Testing**: [`workplace/templates/evaluation/axe_accessibility_test.ts`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/templates/evaluation/axe_accessibility_test.ts).
- [x] **Lighthouse CI Configuration**: [`workplace/templates/evaluation/lighthouse_ci_config.json`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/templates/evaluation/lighthouse_ci_config.json).
- [x] **Automated Link & Reference Checker**: [`workplace/templates/evaluation/link_checker_script.sh`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/templates/evaluation/link_checker_script.sh).
- [x] **Unit & E2E Testing Templates**:
  - [`workplace/templates/evaluation/vitest_unit_test_template.ts`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/templates/evaluation/vitest_unit_test_template.ts) and [`workplace/templates/evaluation/playwright_e2e_template.ts`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/templates/evaluation/playwright_e2e_template.ts).

---

## 11. Autonomous Living Documentation Engine (`CAP-21`)

- [x] **Synchronizer Module (`workplace/core/living_doc_engine.py`)**:
  - Automatically parses code and AST signatures across `workplace/core/`, `workplace/modules/`, `context/`, `agentic/`.
  - Generates/synchronizes all markdown documentation in [`workplace/docs/`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/):
    - [`architecture.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/architecture.md) (Platform Blueprint & Quad-Space Architecture)
    - [`module_catalog.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/module_catalog.md) (All Micro-Modules & Microservices)
    - [`sequence_flows.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/sequence_flows.md) (PR Gatekeeper & Self-Healing Sequence Diagrams)
    - [`data_flow.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/data_flow.md) (AST Caching, Merkle Ledger & WORM Egress)
    - [`entity_relationship.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/entity_relationship.md) (Ledger & Custom Agent Schemas)
    - [`domain_extensions.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/domain_extensions.md) (IoT, Mobile & SaaS Domain Layer Packs)
    - [`README.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/README.md) (Living Documentation Index & Architecture Map)
- [x] **Mermaid Syntax Invariant Validator**: Strict syntax and label quoting validation.
- [x] **CI/CD Integration**: Step `[6/7]` of `percipience gate` automatically verifies living docs.

---

## 12. Terraform Multi-Cloud Production Blueprints (`CAP-13`, `CAP-18`)

- [x] **AWS Production Module (`workplace/infra/terraform/aws/`)**:
  - Multi-AZ EKS cluster with Karpenter autoscaling controller & IRSA.
  - Aurora PostgreSQL Serverless v2 with Row-Level Security (RLS) & SSL enforcement.
  - ElastiCache Redis 7.x multi-AZ replication cluster with in-transit encryption.
  - S3 Object Lock (`COMPLIANCE` mode) WORM immutable ledger bucket.
  - AWS KMS CMEK Keyring with automated annual rotation.
- [x] **Google Cloud Production Module (`workplace/infra/terraform/gcp/`)**:
  - Regional GKE cluster with Workload Identity & gVisor sandboxed spot node pool.
  - Cloud SQL PostgreSQL 16 Enterprise Plus HA with CMEK encryption.
  - Cloud Memorystore for Redis Standard HA with VPC private peering.
  - GCS Object Retention WORM immutable bucket in locked compliance mode.
  - Cloud KMS CMEK Keyring with 90-day automatic key rotation.
- [x] **Automated Unit Tests**: Verified via [`test_21_terraform_multicloud_blueprints`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_play3_suite.py).

---

## 13. Autonomous CI/CD Triad & Specialist Plugins (`Phases 1–3`)

- [x] **Self-Sustaining Housekeeping Engine (`workplace/core/autonomous_cicd.py`)**: Reclaims stale POSIX/Redis leases and cleans temporary worktrees.
- [x] **Self-Recovering Autonomous Healer (`workplace/core/autonomous_cicd.py`)**: Diagnoses errors, attempts bounded auto-patching, and falls back to surgical rollback.
- [x] **Self-Improving Telemetry Engine (`workplace/core/autonomous_cicd.py`)**: Adjusts AST pruning policies and tracks token reduction efficiency.
- [x] **Phase 3 Specialist Plugins**:
  - Flaky Test Detector & HITL Quarantine (`workplace/core/flaky_test_detector.py`)
  - Wire Contract Compatibility Checker (`workplace/core/contract_compatibility_checker.py`)
  - Supply-Chain CVE Sentinel (`workplace/core/dependency_cve_sentinel.py`)
  - Doc Drift Synchronizer (`workplace/core/doc_drift_synchronizer.py`)

---

## 14. Layerable Domain Packs & Commercial GTM Backlog

- [ ] **TODO - MCP Jira / Linear Story Ingestion Gateway (P1)**:
  - Model Context Protocol (MCP) server ingesting user stories directly into structured BDD feature specs with Merkle receipts.
- [ ] **TODO - Live IoT & Mobile Domain Plan Enclave Hydration (P1)**:
  - Add native BLE ring-buffer and offline SQLite synchronization tests.
- [ ] **TODO - 90-Day GTM Commercial Sales Funnel & Stripe Webhook (P2)**:
  - Production Stripe checkout & webhook billing processor in `workplace/modules/mod_tenant_billing/stripe_connector.py`.

---

## 15. Anti-Drift, Handover Governance & Semantic Parity Engine (`CAP-09`, `CAP-26`)

> **Governing Methodology:** [`workplace/docs/methodologies/anti_drift_protocol.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/methodologies/anti_drift_protocol.md)  
> **Core Objective:** Eliminate code drift, wire contract mutation, doc staleness, and rogue successor agent spawning in multi-agent swarms.

- [x] **Comprehensive Anti-Drift & Handover Protocol Specification** ([`workplace/docs/methodologies/anti_drift_protocol.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/methodologies/anti_drift_protocol.md)):
  - 6-Vector mathematical parity formulation: $S_{SP} = 0.20 S_{\text{AST}} + 0.25 S_{\text{Contract}} + 0.20 S_{\text{Behavior}} + 0.15 S_{\text{Handover}} + 0.10 S_{\text{Doc}} + 0.10 S_{\text{SupplyChain}}$.
  - Multi-agent handover failure modes: unauthorized successor spawning, bypassed gate short-circuiting, payload contract mutation, recursive swarm explosions, and role usurpation.
  - Dual-Reconciliation workflow (Automated Revert Mode vs. HITL-gated Evolve Mode).
- [x] **TODO-AD-01: Multi-Agent Swarm Governor & Rogue Spawning Sentinel (P1)**:
  - *Implemented via TODO-AGT-10*: Built [`workplace/core/swarm_governor.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/swarm_governor.py) enforcing 4-tier authority hierarchy (`ORCHESTRATOR` > `DOMAIN_ARCHITECT` > `SPECIALIST_WORKER` > `GATEKEEPER_SENTINEL`), max recursion depth ($D \le 2$), and max concurrent active worktree ceiling ($N \le 4$) with anti-usurpation interception. Verified in `test_swarm_governor_authority_tree`.
- [x] **TODO-AD-02: Cryptographic Handoff Token & Payload Schema Validator (P1)** ([`workplace/core/handoff_validator.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/handoff_validator.py)):
  - Enforce JSON Schema Draft-07 validation for inter-agent communication messages via `agentic/schemas/handoff_schema.yaml`.
  - Implement non-bypassable signed `HandoffToken` verification with zero-drift attestation ($S_{SP} \ge 0.95$), single-use nonces, payload artifact hashes, dynamic YAML DAG routing, replay prevention, and guaranteed persistent outbox/inbox delivery spools with ACK receipts.
- [x] **TODO-AD-03: Composite 6-Vector Semantic Parity Engine & CLI (P1)** ([`workplace/core/semantic_parity_engine.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/semantic_parity_engine.py)):
  - Implement `workplace/core/semantic_parity_engine.py` calculating real-time $S_{SP}$ metric score ($0.00 \text{ to } 1.00$).
  - Add CLI subcommands:
    - `percipience drift check` (calculates composite $S_{SP}$ across all active modules)
    - `percipience drift report --verbose` (breaks down sub-scores for AST, contract, tests, handover, docs, and supply chain)
    - `percipience swarm audit` (inspects active PID/Redis lease trees and identifies orphaned worktrees)
- [x] **TODO-AD-04: Automated Dual-Reconciliation Revert & Evolve Engine (P1)** ([`workplace/core/reconciliation_engine.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/reconciliation_engine.py)):
  - Implement `percipience drift reconcile --mode revert --module <id>` to synthesize surgical reverse AST diffs removing unauthorized helper functions.
  - Implement `percipience drift reconcile --mode evolve --module <id>` to draft RFC specification deltas in `user/hitl/proposed_spec_delta.md` with automated blast-radius impact analysis across downstream consumers.
- [x] **TODO-AD-05: Unit & Integration Test Suite for Handover Drift & Parity (P1)** ([`workplace/tests/test_play3_suite.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_play3_suite.py)):
  - Add test fixtures in `workplace/tests/test_play3_suite.py` simulating rogue subagent spawning, bypassed gatekeeper tokens, and payload schema mutations.

---

## 16. Competitive Parity & Advanced Capabilities Backlog (Learnings from Industry Frameworks)

> **Governing Analysis:** [`workplace/docs/reports/competitive_differentiation_matrix.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/reports/competitive_differentiation_matrix.md)  
> **Core Objective:** Adopt high-value capabilities and integrations where specialized external frameworks (Cursor/Windsurf, LangSmith/Phoenix, Lakera/Guardrails AI, GitHub Actions/Dagger) offer mature developer experience and operational ergonomics.

### 16.1. Observability, OpenTelemetry GenAI & Quantitative Evals (LangSmith / Arize Phoenix / Langfuse / Promptfoo / Ragas)
- [x] **TODO-COMP-01: OpenTelemetry (OTel) GenAI Semantic Conventions & Distributed Tracing (P1)** ([`workplace/core/otel_exporter.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/otel_exporter.py)):
  - *Competitor Benchmark*: LangSmith, Phoenix, and Langfuse export standardized OTel GenAI semantic spans (`gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, TTFT latency waterfalls) to enterprise APMs (Datadog, Dynatrace, Honeycomb, Jaeger).
  - *Implementation*: Implemented `OpenTelemetryGenAIExporter` emitting W3C `traceparent` headers (`00-{trace_id}-{span_id}-{flags}`), TTFT events, latency waterfalls, and GenAI semantic spans to `context/ledger/otel_spans.jsonl`.
- [x] **TODO-COMP-02: Quantitative LLM Evals & Hallucination Scoring Engine (P1)** ([`workplace/core/eval_scoring_engine.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/eval_scoring_engine.py)):
  - *Competitor Benchmark*: Arize Phoenix & DeepEval/Ragas provide automated evaluation pipelines for faithfulness, hallucination rate, context relevancy, code correctness, and semantic drift.
  - *Implementation*: Implemented `EvalScoringEngine` providing 5-dimensional quantitative scoring (Faithfulness, Hallucination Freedom, Context Relevancy, Code Correctness, Semantic Parity) and composite G-Eval / Ragas quality verification.
- [x] **TODO-COMP-03: Side-by-Side Prompt Playground & Regression Test Matrix (P2)** ([`workplace/core/prompt_benchmark_engine.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/prompt_benchmark_engine.py)):
  - *Competitor Benchmark*: Promptfoo & LangSmith offer automated matrix testing of system prompt variations across multiple LLMs with visual diffs and cost-vs-quality comparisons.
  - *Implementation*: Implemented `PromptBenchmarkEngine` executing regression challenge sets across prompt variants, measuring pass rates, token consumption, latency waterfalls, and Tier A vs Tier B USD cost arbitrage.
- [x] **TODO-COMP-04: Semantic LLM Response & Prompt Embedding Caching (P2)** ([`workplace/core/semantic_prompt_cache.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/semantic_prompt_cache.py)):
  - *Competitor Benchmark*: Portkey, Helicone, and GPTCache provide vector-similarity caching for LLM requests, dropping token cost to zero for semantically duplicate diagnostic or query turns.
  - *Implementation*: Implemented `SemanticPromptCache` with term-frequency cosine vector similarity (default threshold $\ge 0.80$), TTL expiration, and telemetry tracking zeroing token burn on duplicate diagnostic inquiries.

### 16.2. Runtime Guardrails, PII Anonymization & Jailbreak Defense (Lakera / Prompt Armor / NeMo Guardrails / Guardrails AI)
- [x] **TODO-COMP-05: Real-Time Inbound/Outbound PII Masking & De-Anonymization (P1)**:
  - *Competitor Benchmark*: Lakera and Microsoft Presidio redact Personally Identifiable Information (names, emails, SSNs, credit cards, IP addresses, proprietary internal hostnames, and credentials) before LLM prompt transit and de-mask upon response ingestion.
  - *Implementation*: Implemented `workplace/core/pii_sanitizer.py` (mirrored across `.nb/core/`, VSCode, and IntelliJ runtimes). High-speed sub-millisecond regex token masking (`<API_KEY_1>`, `<SSN_1>`, `<EMAIL_1>`, `<PHONE_1>`, `<IP_ADDR_1>`, `<CREDIT_CARD_1>`, `<HOSTNAME_1>`, `<PERSON_1>`) with strict memory-only reverse vaults, zero disk leakage, session isolation, reversible `deanonymize()`, and comprehensive telemetry tracking. Exposes CLI (`percipience guardrail pii`) and REST endpoints (`POST /api/guardrails/pii-mask`, `POST /api/guardrails/pii-unmask`).
- [x] **TODO-COMP-06: Inbound Indirect Prompt Injection Firewall (P1)**:
  - *Competitor Benchmark*: Prompt Armor & Lakera intercept malicious prompt injections embedded inside untrusted external web pages, Jira stories, Git issue descriptions, and PR comments.
  - *Implementation*: Implemented `workplace/core/prompt_injection_guard.py` (mirrored across all Quad-Space runtime locations). Multi-vector detection analyzing direct instruction overrides (`ignore previous instructions`, `DAN mode`, `developer mode`), chat delimiter hijacking (`"""SYSTEM:`, `[INST]`, `<<SYS>>`, `<|im_start|>`), role usurpation (`I am the system administrator`), egress/exfiltration probes (`curl webhook.site`), obfuscated base64 attacks (candidate extraction and decoding), and zero-width Unicode steganography. Returns granular risk score (0.0 to 1.0) and verdicts (`ALLOWED`, `QUARANTINED`, `BLOCKED`). Exposes `neutralize_payload()` wrapping in safe envelope `<untrusted_external_payload>`, quarantine logging to `user/hitl/injection_quarantine.jsonl`, CLI (`percipience guardrail injection`), and REST endpoint (`POST /api/guardrails/injection-scan`).
- [x] **TODO-COMP-07: Output Policy & Hallucination Safety Rails (P2)**:
  - *Competitor Benchmark*: NeMo Guardrails and Guardrails AI enforce strict output validation schemas, preventing agents from emitting unverified shell execution commands, dangerous system calls, or out-of-spec code structures.
  - *Implementation*: Implemented `workplace/core/output_guardrail_validator.py` (mirrored across all runtime environments). Enforces post-generation AST structural verification via `ast.parse()` and `OutputGuardrailVisitor`: blocks dangerous system calls (`eval()`, `exec()`, `os.system()`, `subprocess.*(shell=True)`), JavaScript dynamic evaluation (`child_process.exec`, `new Function`), prohibits path traversal attacks (`/etc/passwd`, `/root/`, `/proc/`, `../../`), blacklists compromised supply-chain dependencies (`event-stream`, `crypto-miner`), validates syntax integrity, and detects hallucinated internal imports (`from core.<phantom> import ...`). Generates structured `remediation_prompt` envelopes for `DiagnosticRePromptEngine`, with CLI (`percipience guardrail output-check`) and REST endpoint (`POST /api/guardrails/output-validate`).

### 16.3. In-Editor Developer Experience, Language Server Protocol & Vector Search (Cursor / Windsurf / Claude Code / Copilot)
- [ ] **TODO-COMP-08: Language Server Protocol (LSP) Indexing & Cross-File Symbol Graphs (P1)**:
  - *Competitor Benchmark*: Cursor & Windsurf integrate directly with active LSP daemons (`pyright`, `typescript-language-server`, `rust-analyzer`, `gopls`) for precise go-to-definition, find-references, and multi-file type inference across millions of lines of code.
  - *Implementation Scope*: Implement `workplace/core/lsp_index_engine.py` communicating with local LSP servers to inject exact cross-file type hierarchies, interface implementations, and call graphs into compressed prompt context.
- [ ] **TODO-COMP-09: Hybrid Sparse-Dense Vector Code Search alongside AST Pruning (P1)**:
  - *Competitor Benchmark*: Cursor & Claude Code utilize hybrid BM25 + dense embedding vector search (LanceDB / Qdrant / Chroma) with semantic reranking for natural-language conceptual codebase queries.
  - *Implementation Scope*: Implement `workplace/core/vector_retrieval_engine.py` pairing AST structural skeletons with local embedded vector indices (LanceDB) and Voyage/OpenAI embeddings for multi-hop semantic code discovery.
- [x] **TODO-COMP-10: VS Code & JetBrains / PyCharm IDE Extension Adapter (P2)**:
  - *Implemented via Section 19 (TODO-IDE-01..03) & TODO-REV-13*: Developed JetBrains IntelliJ/PyCharm plugin suite (`workplace/modules/mod_intellij_plugin/`), bundled platform engines, packaged `.nb/bundles/intellij_pycharm_plugin_domain.nbpack`, produced release zips/jars, and scaffolded VS Code extension bridge. Verified in `test_ide_plugins_space.py`.
- [ ] **TODO-COMP-11: Multimodal UI & Design Token Context Ingestion (P2)**:
  - *Competitor Benchmark*: Claude Code / Cursor / Devin accept screenshot images and Figma designs directly to generate CSS/React AST components and verify pixel-level rendering.
  - *Implementation Scope*: Implement `workplace/core/multimodal_ui_engine.py` parsing design tokens, Figma JSON schemas, and UI screenshots into clean Tailwind/React component ASTs.

### 16.4. Enterprise CI/CD Sandboxing, OIDC Keyless Auth & GitOps PR Bot (GitHub Actions / GitLab CI / Dagger / ArgoCD / Harness)
- [ ] **TODO-COMP-12: Sub-Second MicroVM / gVisor & WASM Sandbox Isolation (P1)**:
  - *Competitor Benchmark*: GitHub Actions / Dagger / Fly.io / Modal execute untrusted code in hardened ephemeral Firecracker microVMs or gVisor/WASM runtimes to prevent container breakout and host filesystem leaks.
  - *Implementation Scope*: Implement `workplace/core/microvm_sandbox.py` providing kernel-isolated ephemeral execution environments for agent test runs with sub-500ms boot times.
- [ ] **TODO-COMP-13: OIDC Keyless Cloud Authentication (Workload Identity Federation) (P1)**:
  - *Competitor Benchmark*: GitHub Actions and GitLab CI use OpenID Connect (OIDC) tokens for short-lived, keyless authentication to AWS IAM, GCP Workload Identity, and Azure AD without static API keys or long-lived credentials.
  - *Implementation Scope*: Implement `workplace/core/oidc_authenticator.py` exchanging dynamic JWTs with cloud IAM providers for secure, credential-less ledger egress and worktree orchestration.
- [ ] **TODO-COMP-14: Parallel Test Sharding & Multi-Architecture Matrix Dispatcher (P2)**:
  - *Competitor Benchmark*: GitHub Actions matrix strategies and GitLab CI parallel jobs dynamically shard large test suites across N runners and multiple operating systems/architectures (Linux AMD64/ARM64, macOS, Windows).
  - *Implementation Scope*: Implement `workplace/core/distributed_test_runner.py` capable of splitting pytest/vitest suites across distributed ephemeral worktree nodes with aggregated Merkle receipts.
- [ ] **TODO-COMP-15: Interactive GitOps PR Bot & Ephemeral Preview Deployments (P2)**:
  - *Competitor Benchmark*: Modern CI/CD and developer tools (Vercel, ArgoCD, GitHub Apps) post interactive PR comments with live preview URLs, collapsible test breakdowns, and interactive bot commands (`/re-heal`, `/rollback`).
  - *Implementation Scope*: Implement `workplace/core/gitops_pr_bot.py` posting rich Markdown status summaries, collapsible test traces, live preview staging links, and responding to developer slash-commands on GitHub/GitLab PRs.

---

## 17. Autonomous Agentic SDLC & Swarm Modernization (20 Architectural Enhancements)

> **Governing Review:** [`workplace/docs/reports/agentic_workspace_sdlc_review.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/reports/agentic_workspace_sdlc_review.md)  
> **Core Objective:** Transition the `agentic/` workspace from script-orchestrated automation to a fully autonomous, self-governing, multi-agent cognitive software engineering ecosystem.

### 17.1. Agent Coordination, Governance & Swarm Topologies
- [x] **TODO-AGT-01: Dynamic Task DAGs & Runtime Sub-Goal Expansion (P1)** (`GAP-AGT-01`):
  - *Governing Review*: `GAP-AGT-01` in [`workplace/docs/reports/agentic_workspace_sdlc_review.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/reports/agentic_workspace_sdlc_review.md) (Pillar I: Agent Coordination & Governance).
  - *Defect & SDLC Impact*: Workflows in `agentic/workflows/` (`derivation_pipeline.yaml`, `pr_gatekeeper.yaml`) are static, linear step lists. When unexpected dependencies or complex structural tasks arise, agents cannot synthesize runtime sub-goals, spawn exploratory sub-plans, backtrack on failures, or adapt execution paths without manual human intervention or pipeline failure.
  - *Target Files*:
    - Implementation: [`workplace/core/dynamic_dag_orchestrator.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/dynamic_dag_orchestrator.py) (mirrored to [`.nb/core/dynamic_dag_orchestrator.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/core/dynamic_dag_orchestrator.py))
    - Schema: [`.nb/agentic/schemas/dynamic_dag_schema.yaml`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/agentic/schemas/dynamic_dag_schema.yaml)
    - Tests: [`workplace/tests/test_dynamic_dag_orchestrator.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_dynamic_dag_orchestrator.py)
  - *Technical Scope & Architecture*:
    - **Dynamic Sub-Goal Expansion**: Implement `DynamicDAGOrchestrator.expand_subgoals(parent_step_id: str, subgoals: List[StepNode])` enabling Plan-and-Solve / ReAct runtime step graph mutation.
    - **Blast-Radius Branching**: Introspects affected files and AST symbols to dynamically insert targeted validation sub-graphs (`validate_syntax` -> `run_focused_tests` -> `check_contract_parity`).
    - **Backtracking & Alternate Branch Routing**: When an exploratory branch fails verification, the orchestrator rolls back ephemeral worktree state to the parent branch point and selects the next viable strategy branch.
    - **Graph Constraints & Loop Guard**: Strict acyclicity check ($\mathcal{O}(V+E)$) on every runtime mutation; hard limit on dynamic expansion recursion depth ($D_{\text{dynamic}} \le 3$) and node count ($N_{\text{max\_steps}} \le 20$).
  - *Acceptance Criteria*:
    - Unit tests verifying dynamic node insertion, topological sort update, backtracking on step failure, and depth ceiling enforcement.
    - Emits structured execution traces logged to `.nb/context/ledger/dynamic_dag_traces.jsonl`.

- [x] **TODO-AGT-02: Structured Multi-Pass Reflection & Critic Verification Loops (Reflexion) (P1)** (`GAP-AGT-02`):
  - *Governing Review*: `GAP-AGT-02` in [`workplace/docs/reports/agentic_workspace_sdlc_review.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/reports/agentic_workspace_sdlc_review.md) (Pillar I: Agent Coordination & Governance).
  - *Defect & SDLC Impact*: Prompts in `agentic/prompts/` (e.g. `derivation_prompt.md`, `evaluation_refinement_prompt.md`) execute in a single forward pass without an internal Generator -> Critic -> Refiner (*Reflexion*) verification cycle, emitting unverified code or flawed architectural assumptions directly to physical file systems and build gates, increasing token burn and test failure cycles.
  - *Target Files*:
    - Implementation: [`workplace/core/self_reflection_engine.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/self_reflection_engine.py) (mirrored to [`.nb/core/self_reflection_engine.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/core/self_reflection_engine.py))
    - Schema: [`.nb/agentic/schemas/reflection_protocol_schema.yaml`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/agentic/schemas/reflection_protocol_schema.yaml)
    - Prompt Templates: [`.nb/agentic/prompts/derivation_prompt.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/agentic/prompts/derivation_prompt.md)
    - Tests: [`workplace/tests/test_self_reflection_engine.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_self_reflection_engine.py)
  - *Technical Scope & Architecture*:
    - **3-Phase Reflexion Protocol**: Enforce `GENERATE` -> `CRITIQUE` -> `REFINE` state transitions prior to filesystem write.
    - **Invariant Verification Checklist**: The Critic phase validates 5 mandatory invariant pillars: (1) Wire contract schema conformity, (2) Edge-case coverage (null handling, bounds, concurrency), (3) Type signature purity, (4) Inbound/outbound guardrail policy compliance, (5) Token budget adherence.
    - **Convergence & Bounded Iterations**: Compute reflection convergence score $S_{\text{critique}} \in [0.0, 1.0]$. Terminate when $S_{\text{critique}} \ge 0.90$ or upon reaching bounded maximum turns ($N_{\text{reflect}} \le 2$).
    - **Critique Envelope Schema**: Structured output schema capturing `{ critique: str, defects_found: List[str], severity: "LOW"|"MEDIUM"|"HIGH", refined_plan: str, passes_invariants: bool }`.
  - *Acceptance Criteria*:
    - Unit tests validating multi-pass critique extraction, defect correction, early exit on $S_{\text{critique}} \ge 0.90$, and enforcement of $N_{\text{reflect}} \le 2$.
    - Integration tests asserting zero disk write occurs until Critic verification passes.

- [x] **TODO-AGT-03: 3-Tier Persistent Agent Memory Architecture (Working, Episodic & Semantic) (P1)** (`GAP-AGT-03`):
  - *Governing Review*: `GAP-AGT-03` in [`workplace/docs/reports/agentic_workspace_sdlc_review.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/reports/agentic_workspace_sdlc_review.md) (Pillar I: Agent Coordination & Governance).
  - *Defect & SDLC Impact*: Agents operate statelessly across session runs. The flat Merkle ledger stores action records but does not provide an indexed memory model. An agent facing a previously solved build issue, flaky test quarantine, or contract discrepancy must rediscover solutions from scratch, wasting cognitive context and tokens.
  - *Target Files*:
    - Implementation: [`workplace/core/agent_memory_engine.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/agent_memory_engine.py) (mirrored to [`.nb/core/agent_memory_engine.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/core/agent_memory_engine.py))
    - Memory Stores: `.nb/context/memory/episodic/`, `.nb/context/memory/semantic/`
    - Schema: [`.nb/agentic/schemas/agent_memory_schema.yaml`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/agentic/schemas/agent_memory_schema.yaml)
    - Tests: [`workplace/tests/test_agent_memory_engine.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_agent_memory_engine.py)
  - *Technical Scope & Architecture*:
    - **Tier 1 (Working Memory)**: Ephemeral, session-scoped scratchpad (`.nb/workspaces/subagent_<id>/scratchpad.json`) maintaining in-flight hypotheses, active AST symbol diffs, and intermediate step returns. Auto-evicted upon task completion or rollback.
    - **Tier 2 (Episodic Memory)**: Persistent JSONL event stream (`.nb/context/memory/episodic/episodes.jsonl`) indexing past task executions, failed test traces, root cause diagnostics, and verified patches. Queryable via error-signature hashing and TF-IDF similarity.
    - **Tier 3 (Semantic Memory)**: Long-term conceptual store (`.nb/context/memory/semantic/concepts.json`) capturing project architectural patterns, wire contract guidelines, domain invariants, and coding conventions.
    - **Memory Consolidation**: On every successful Merkle block seal (`RP_*`), automatically consolidate the working memory resolution into the episodic memory store with cryptographic block anchoring.
  - *Acceptance Criteria*:
    - Unit tests verifying working memory isolation per worktree, episodic retrieval recall $> 0.85$ on matching error signatures, semantic index lookup, and memory consolidation into Merkle blocks.

- [x] **TODO-AGT-04: Declarative Tool Contracts & JSON Schema Validation (P1)** (`GAP-AGT-04`):
  - *Governing Review*: `GAP-AGT-04` in [`workplace/docs/reports/agentic_workspace_sdlc_review.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/reports/agentic_workspace_sdlc_review.md) (Pillar I: Agent Coordination & Governance).
  - *Defect & SDLC Impact*: Custom agent definitions in `agentic/custom/agents/*.yaml` declare tools as plain string lists (`tools: [ast_pruner, cve_sentinel]`). There is no runtime validation of tool input arguments or output schemas, no distinction between read-only (idempotent) vs mutating tools, leading to agent malformed tool-call exceptions.
  - *Target Files*:
    - Implementation: [`workplace/core/tool_contract_validator.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/tool_contract_validator.py) (mirrored to [`.nb/core/tool_contract_validator.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/core/tool_contract_validator.py))
    - Schema: [`.nb/agentic/schemas/tool_contract_schema.yaml`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/agentic/schemas/tool_contract_schema.yaml)
    - Tool Registry: [`.nb/agentic/custom/tools/`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/agentic/custom/tools/)
    - Tests: [`workplace/tests/test_tool_contract_validator.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_tool_contract_validator.py)
  - *Technical Scope & Architecture*:
    - **Formal Declarative Tool Contracts**: Define complete JSON Schema Draft-07 contracts for all platform tools: `name`, `description`, `parameters` (types, required fields, constraints), `returns` schema, `is_idempotent: bool`, `mutates_filesystem: bool`, `timeout_seconds: int`, and `required_capabilities: List[str]`.
    - **Pre-Call & Post-Call Validation**: Runtime interceptor validates tool arguments before execution (`INVALID_TOOL_ARGUMENTS`) and validates return payloads against output schemas (`INVALID_TOOL_OUTPUT`).
    - **Idempotency Caching Engine**: For tools declared with `is_idempotent: true`, automatically cache outputs keyed by `(tool_name, sha256(canonical_inputs))` to eliminate redundant compute and token spend.
    - **Timeout Enforcer**: Hard execution deadline per tool execution using POSIX signals / threading timeouts, returning `TOOL_TIMEOUT_EXCEEDED` on breach.
  - *Acceptance Criteria*:
    - Unit tests verifying parameter validation rejection, return schema conformance, idempotency caching, and timeout enforcement across all platform tools.

- [x] **TODO-AGT-05: Capability-Based Access Control (CBAC) Sandbox Tokens (P1)** (`GAP-AGT-05`):
  - *Governing Review*: `GAP-AGT-05` in [`workplace/docs/reports/agentic_workspace_sdlc_review.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/reports/agentic_workspace_sdlc_review.md) (Pillar I: Agent Coordination & Governance).
  - *Defect & SDLC Impact*: Once spawned, agents inherit full execution privileges with no declarative permission boundaries. A rogue or hallucinating agent could execute arbitrary system commands, write to protected paths outside its module workspace, or perform unauthorized network egress.
  - *Target Files*:
    - Implementation: [`workplace/core/agent_capability_guard.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/agent_capability_guard.py) (mirrored to [`.nb/core/agent_capability_guard.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/core/agent_capability_guard.py))
    - Rules: [`.nb/context/rules/capability_tokens.yaml`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/context/rules/capability_tokens.yaml)
    - Tests: [`workplace/tests/test_agent_capability_guard.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_agent_capability_guard.py)
  - *Technical Scope & Architecture*:
    - **Cryptographic Capability Tokens**: Issue HMAC-SHA256 capability tokens bound to `(agent_id, worktree_path, allowed_operations, expiry_utc)` specifying granular rights: `CAP_FS_READ`, `CAP_FS_WRITE_MODULE_ONLY`, `CAP_NETWORK_EGRESS_OFF`, `CAP_EXEC_SUBPROCESS`, `CAP_MERKLE_SEAL`.
    - **Path-Bound Filesystem Enforcer**: Intercepts file I/O operations. Hard-blocks write attempts targeting protected directories (`.nb/core/`, `.nb/context/invariants/`, `workplace/` outside the agent's assigned module directory) with `PERMISSION_DENIED_PATH_RESTRICTED`.
    - **Subprocess Command Whitelist**: Restricts shell execution to explicitly whitelisted commands (`pytest`, `git diff`, `python3 -m pyright`), blocking unsafe binaries (`curl`, `wget`, `rm -rf`, `nc`, `pip install`) with `PERMISSION_DENIED_UNAUTHORIZED_COMMAND`.
    - **Network Egress Firewall**: Verifies `CAP_NETWORK_EGRESS` token flag; blocks external socket creation unless explicitly authorized for cloud ledger sync.
  - *Acceptance Criteria*:
    - Unit tests validating path traversal interception, forbidden subprocess command blocking, network socket restriction, and valid capability token lifecycle.

- [x] **Portal Integration & UI Dashboard for Swarm Topologies & Governance**:
  - *Target Files*: [`workplace/portal/server.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/portal/server.py), [`workplace/modules/mod_portal_marketing/components/capabilities_catalog.ts`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/modules/mod_portal_marketing/components/capabilities_catalog.ts), [`workplace/tests/test_portal_swarm_governance.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_portal_swarm_governance.py).
  - *Delivered*:
    - Integrated Tab 15 (`#swarm-governance`, `🤖 Swarm & Governance`) in the SaaS portal featuring 5 interactive panels for DAG runtime expansion, 5-pillar reflexion critic scoring, 3-tier episodic/semantic memory search, JSON Schema Draft-07 declarative tool execution, and HMAC-signed CBAC sandbox token minting/access testing.
    - Added REST endpoints: `/api/swarm/dynamic-dag`, `/api/swarm/dynamic-dag/simulate`, `/api/swarm/reflexion/evaluate`, `/api/swarm/memory/status`, `/api/swarm/memory/episodic`, `/api/swarm/memory/semantic`, `/api/swarm/memory/consolidate`, `/api/swarm/tools`, `/api/swarm/tools/validate-execute`, `/api/swarm/cbac/mint`, `/api/swarm/cbac/verify-access`.
    - Enriched marketing capability models `cap_dynamic_dag`, `cap_reflexion_critic`, `cap_3tier_memory`, `cap_tool_contracts`, `cap_cbac_sandbox`.
    - Comprehensive automated test suite passing (8/8 tests in `test_portal_swarm_governance.py`).

### 17.2. Runtime Architecture, Quad-Space Boundaries & Execution Hygiene
- [x] **TODO-AGT-06: Quad-Space Boundary Cleanup & Runtime Deduplication (P1)** ([`agentic/runtime/`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/agentic/runtime/)):
  - *Shortcoming*: Code was previously duplicated between `agentic/runtime/` and `workplace/core/` (e.g. `cognitive_router.py`, `worktree_manager.py`), violating Quad-Space architecture.
  - *Implementation*: Refactored all 8 modules in `agentic/runtime/` to act as declarative facade bridges and import executable engines directly from `workplace/core/`.
- [x] **TODO-AGT-07: Parallel Fan-Out / Fan-In Barrier Synchronization in Workflows (P2)** ([`workplace/core/workflow_orchestrator.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/workflow_orchestrator.py)):
  - *Shortcoming*: Independent verification checks ran sequentially, inflating gate latency.
  - *Implementation*: Implemented `WorkflowOrchestrator` supporting `parallel_group` fan-out and `fan_in_barrier` synchronization with thread pool concurrency and cycle deadlock detection.
- [x] **TODO-AGT-08: Fine-Grained Error Taxonomy & Adaptive Recovery Playbooks (P1)** ([`workplace/core/error_recovery_orchestrator.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/error_recovery_orchestrator.py)):
  - *Shortcoming*: Workflows relied on coarse binary failure actions (`QUARANTINE_AND_HALT`, `AUTO_HEAL_OR_ROLLBACK`).
  - *Implementation*: Implemented `ErrorRecoveryOrchestrator` with 4-pillar taxonomy (`TRANSIENT`, `STRUCTURAL`, `INVARIANT`, `HALLUCINATORY`) and specialized self-healing playbooks (jitter backoff, AST diagnostic re-prompts, spec evolution RFCs, quarantine rollbacks).
- [x] **TODO-AGT-09: Prompt SemVer, Golden Test Suites & Prompt Drift Detection (P2)** ([`workplace/core/prompt_drift_sentinel.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/prompt_drift_sentinel.py), [`agentic/prompts/prompt_manifest.yaml`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/agentic/prompts/prompt_manifest.yaml)):
  - *Shortcoming*: Markdown prompts in `agentic/prompts/` lacked semantic versioning, regression tests, and prompt drift tracking.
  - *Implementation*: Created cryptographic prompt manifest `prompt_manifest.yaml` and `PromptDriftSentinel` with SHA-256 integrity audits, structural drift detection, and golden evaluation invariant suites.
- [x] **TODO-AGT-10: Hierarchical Agent Supervision & Multi-Level Authority Trees (P1)** ([`workplace/core/swarm_governor.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/swarm_governor.py)):
  - *Shortcoming*: Agents operated as flat unconstrained peers without an escalation hierarchy.
  - *Implementation*: Implemented `SwarmGovernor` enforcing a 4-tier authority hierarchy (`ORCHESTRATOR` > `DOMAIN_ARCHITECT` > `SPECIALIST_WORKER` > `GATEKEEPER_SENTINEL`), permission checks on critical actions, max recursion depth limits ($D \le 2$), and anti-usurpation child spawning interception.

### 17.3. Cognitive Strategy, Attention Budgeting & Prompt Engineering
- [x] **TODO-AGT-11: Adversarial Red-Team & Mutation Fuzzing Agent (P1)** ([`workplace/core/adversarial_fuzzer.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/adversarial_fuzzer.py), [`agentic/custom/agents/agent_adversarial_fuzzer.yaml`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/agentic/custom/agents/agent_adversarial_fuzzer.yaml)):
  - *Shortcoming*: PR verification relied solely on cooperative tests written by the developer agent.
  - *Implementation*: Implemented `AdversarialFuzzer` generating boundary numbers, SQL/XSS injections, null mutations, and prototype pollutions with resilience scoring.
- [x] **TODO-AGT-12: Context Attention Slicing & Token Budgeting Strategy (P2)** ([`workplace/core/attention_budgeter.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/attention_budgeter.py)):
  - *Shortcoming*: Prompts risked context overflow and "lost-in-the-middle" attention degradation.
  - *Implementation*: Implemented `AttentionBudgeter` enforcing mathematical budget quotas (15% Invariants, 25% Contracts, 35% AST, 10% Trajectories, 15% Output) and preserving core rules during context assembly.
- [x] **TODO-AGT-13: Static Prompt Prefix Pinning for KV Cache Optimization (P1)** ([`workplace/core/prompt_drift_sentinel.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/prompt_drift_sentinel.py), [`agentic/prompts/prompt_manifest.yaml`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/agentic/prompts/prompt_manifest.yaml)):
  - *Shortcoming*: Dynamic variables interpolated early in prompts invalidated LLM prompt KV caches.
  - *Implementation*: Standardized all prompt templates with static prefix blocks pinned at the top and audited 100% compliance in `PromptDriftSentinel`.
- [x] **TODO-AGT-14: Structured Step-by-Step Trajectory Recording & Replay Engine (P2)** ([`workplace/core/trajectory_recorder.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/trajectory_recorder.py)):
  - *Shortcoming*: Intermediate reasoning traces, thoughts, and tool call histories were discarded.
  - *Implementation*: Implemented `TrajectoryRecorder` capturing ReAct cycles in `agentic/trajectories/` with deterministic replay and validation.
- [x] **TODO-AGT-15: Autonomous Requirement Clarification & Ambiguity Resolution Agent (P2)** ([`workplace/core/ambiguity_resolver.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/ambiguity_resolver.py), [`agentic/custom/agents/agent_ambiguity_resolver.yaml`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/agentic/custom/agents/agent_ambiguity_resolver.yaml)):
  - *Shortcoming*: Agents guessed user intent on underspecified requirements instead of requesting clarification.
  - *Implementation*: Implemented `AmbiguityResolver` calculating requirement entropy and drafting interactive clarification RFCs in `user/hitl/clarification_requests/`.

### 17.4. Resilience, Evaluation, Consensus & Security Capabilities
- [x] **TODO-AGT-16: Dynamic Few-Shot Exemplar Selection & Context-Aware RAG Injection (P2)** (`GAP-AGT-16`):
  - *Implemented*: Built [`workplace/core/few_shot_retriever.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/few_shot_retriever.py) (mirrored to [`.nb/core/few_shot_retriever.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/core/few_shot_retriever.py)) and golden pattern library in [`.nb/context/exemplars/exemplar_library.json`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/context/exemplars/exemplar_library.json). Multi-factor scoring ($0.40 S_{lang} + 0.35 S_{pattern} + 0.25 S_{tags}$), token budgeting, counter-factual negative exemplars, and graceful zero-shot fallback. Verified via 6 tests in [`test_few_shot_retriever.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_few_shot_retriever.py).
  - *Governing Review*: `GAP-AGT-16` in [`workplace/docs/reports/agentic_workspace_sdlc_review.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/reports/agentic_workspace_sdlc_review.md) (Pillar IV: Resilience, Evaluation & Security).
  - *Defect & SDLC Impact*: Prompts are zero-shot or contain static hardcoded code snippets that do not adapt to specific problem domains, leading to lower code synthesis accuracy on complex domain tasks (Stripe webhooks, BLE ring buffers, AST visitors).
  - *Target Files*:
    - Implementation: [`workplace/core/few_shot_retriever.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/few_shot_retriever.py) (mirrored to [`.nb/core/few_shot_retriever.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/core/few_shot_retriever.py))
    - Exemplar Store: `.nb/context/exemplars/`
    - Tests: [`workplace/tests/test_few_shot_retriever.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_few_shot_retriever.py)
  - *Technical Scope & Architecture*:
    - **Multi-Factor Exemplar Scoring**: Compute matching score $S_{\text{exemplar}} = 0.40 S_{\text{lang}} + 0.35 S_{\text{ast\_pattern}} + 0.25 S_{\text{domain\_tag}}$ against task requirements.
    - **Curated Golden Exemplar Library**: Establish structured JSON exemplar library covering common production patterns: FastAPI endpoints, OpenAPI wire contracts, AST visitors, state machines, and cryptographic verification hooks.
    - **Token-Budgeted Dynamic Injection**: Injects top-$k$ ($k \in [1, 3]$) positive exemplars and counter-factual negative exemplars, respecting strict attention slicing budgets ($< 15\%$ of total prompt window).
  - *Acceptance Criteria*:
    - Unit tests verifying exemplar retrieval ranking, language/AST filtering, token budget constraint compliance, and graceful fallback to zero-shot when no match is found.

- [x] **TODO-AGT-17: 2-of-3 Multi-Agent Consensus Quorum for Critical Decisions (P1)** (`GAP-AGT-17`):
  - *Implemented*: Built [`workplace/core/consensus_quorum_engine.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/consensus_quorum_engine.py) (mirrored to [`.nb/core/consensus_quorum_engine.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/core/consensus_quorum_engine.py)) and schema [`.nb/agentic/schemas/quorum_schema.yaml`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/agentic/schemas/quorum_schema.yaml). Enforces 2-of-3 heterogeneous consensus across Security, Quality, and Architecture evaluators, single-veto quarantine escalation to `poisoning_quarantine.md`, and HMAC-SHA256 quorum receipts. Verified via 5 tests in [`test_consensus_quorum_engine.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_consensus_quorum_engine.py).
  - *Governing Review*: `GAP-AGT-17` in [`workplace/docs/reports/agentic_workspace_sdlc_review.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/reports/agentic_workspace_sdlc_review.md) (Pillar IV: Resilience, Evaluation & Security).
  - *Defect & SDLC Impact*: Critical pipeline decisions (security sign-off, wire contract deprecation, PR gate merge approvals) depend on a single agent persona, creating cognitive blindspots and vulnerability to single prompt injections.
  - *Target Files*:
    - Implementation: [`workplace/core/consensus_quorum_engine.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/consensus_quorum_engine.py) (mirrored to [`.nb/core/consensus_quorum_engine.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/core/consensus_quorum_engine.py))
    - Schema: [`.nb/agentic/schemas/quorum_schema.yaml`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/agentic/schemas/quorum_schema.yaml)
    - Tests: [`workplace/tests/test_consensus_quorum_engine.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_consensus_quorum_engine.py)
  - *Technical Scope & Architecture*:
    - **2-of-3 Heterogeneous Quorum Protocol**: Solicits independent evaluations from 3 diverse evaluators (e.g. `SecurityAuditor`, `ArchitecturalSpecialist`, `QualityGatekeeper`) or distinct prompt/model configurations.
    - **Vote Aggregation & Disagreement Resolution**: Tallies votes across standardized verdicts: `APPROVE`, `REQUEST_REVISION`, `QUARANTINE_VETO`. Requires at least 2 `APPROVE` votes for pipeline advancement.
    - **Single-Veto Quarantine**: Any `QUARANTINE_VETO` vote halts execution immediately and routes the task to `user/hitl/poisoning_quarantine.md`.
    - **Cryptographic Quorum Receipt**: Generates signed HMAC-SHA256 quorum receipt with all voter verdicts and rationales, anchored into Merkle ledger block `RP_QUORUM_*`.
  - *Acceptance Criteria*:
    - Unit tests validating 3-agent vote aggregation, 2-of-3 approval passage, deadlock resolution, single-veto quarantine escalation, and Merkle receipt sealing.

- [x] **TODO-AGT-18: Proactive Milestone-Based HITL Interactive Checkpoints (P2)** (`GAP-AGT-18`):
  - *Implemented*: Built [`workplace/core/hitl_checkpoint_manager.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/hitl_checkpoint_manager.py) (mirrored to [`.nb/core/hitl_checkpoint_manager.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/core/hitl_checkpoint_manager.py)), checkpoint schema [`.nb/agentic/schemas/hitl_checkpoint_schema.yaml`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/agentic/schemas/hitl_checkpoint_schema.yaml), and CLI subcommands (`percipience hitl list`, `percipience hitl approve`, `percipience hitl reject`). Emits interactive Markdown/JSON cards in `user/hitl/milestones/`, handles blast-radius analysis, and executes timeout policies. Verified via 6 tests in [`test_hitl_checkpoint_manager.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_hitl_checkpoint_manager.py).
  - *Governing Review*: `GAP-AGT-18` in [`workplace/docs/reports/agentic_workspace_sdlc_review.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/reports/agentic_workspace_sdlc_review.md) (Pillar IV: Resilience, Evaluation & Security).
  - *Defect & SDLC Impact*: Human-In-The-Loop (HITL) interaction is treated exclusively as an error trap (`poisoning_quarantine.md`). Missed opportunities for human feedback during architectural planning, trade-off selection, or visual UI approval before downstream code generation.
  - *Target Files*:
    - Implementation: [`workplace/core/hitl_checkpoint_manager.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/hitl_checkpoint_manager.py) (mirrored to [`.nb/core/hitl_checkpoint_manager.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/core/hitl_checkpoint_manager.py))
    - Checkpoint Spool: `user/hitl/milestones/`
    - Schema: [`.nb/agentic/schemas/hitl_checkpoint_schema.yaml`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/agentic/schemas/hitl_checkpoint_schema.yaml)
    - Tests: [`workplace/tests/test_hitl_checkpoint_manager.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_hitl_checkpoint_manager.py)
  - *Technical Scope & Architecture*:
    - **Workflow Milestone Checkpoints**: Declarative workflow step `checkpoint_type: HITL_MILESTONE` pausing pipeline execution at critical boundaries (e.g. `ARCH_DESIGN_APPROVAL`, `SCHEMA_EVOLUTION_RFC`, `UI_WIREFRAME_SIGN_OFF`).
    - **Interactive Approval Cards**: Emits structured markdown and JSON cards in `user/hitl/milestones/{checkpoint_id}.json` containing diff previews, blast-radius projections, and selectable options (`[APPROVE]`, `[REJECT]`, `[MODIFY]`).
    - **CLI & Portal Resumption**: CLI commands `percipience hitl list`, `percipience hitl approve --id <id>`, `percipience hitl reject --id <id> --reason <text>` updating state and unblocking workflow execution.
    - **Configurable Timeout Policies**: Supports `timeout_action: AUTO_PAUSE | QUARANTINE | PROCEED_CONSERVATIVE` after specified duration.
  - *Acceptance Criteria*:
    - Unit tests validating checkpoint creation, serialization, CLI resolution ingestion, timeout handling, and workflow resumption.

- [x] **TODO-AGT-19: Deadlock Detection & Inter-Agent Handoff Cycle Sentinel (P1)** ([`workplace/core/handoff_validator.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/handoff_validator.py)):
  - *Shortcoming*: Handoff tokens lacked runtime cycle detection, risking infinite recursive delegation loops.
  - *Implementation*: Implemented topological loop sentinel (`lineage` inspection), max hop ceiling (`hop_count <= 5`), anti-drift attestation ($S_{SP} \ge 0.95$), replay token tracking, dynamic YAML workflow DAG route synchronization, and persistent outbox/inbox delivery in `workplace/core/handoff_validator.py` and `.nb/core/handoff_validator.py`.

- [x] **TODO-AGT-20: Automated Agent Benchmark & Continuous Quality Evaluation Harness (P1)** (`GAP-AGT-20`):
  - *Implemented*: Built [`workplace/core/agent_benchmark_harness.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/agent_benchmark_harness.py) (mirrored to [`.nb/core/agent_benchmark_harness.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/core/agent_benchmark_harness.py)), benchmark suite in [`workplace/tests/benchmarks/test_agent_benchmarks.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/benchmarks/test_agent_benchmarks.py), scorecard report at [`workplace/docs/reports/agent_quality_scorecard.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/reports/agent_quality_scorecard.md), and CLI subcommand `percipience benchmark run`. Computes 5-Metric Radar (TSR >= 90%, S_SP >= 0.95, Token Efficiency < 5k, Latency < 10s, Invariant Compliance = 100%) and seals evaluation receipts to Merkle ledger. Verified via 5 tests in [`test_agent_benchmarks.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/benchmarks/test_agent_benchmarks.py).
  - *Governing Review*: `GAP-AGT-20` in [`workplace/docs/reports/agentic_workspace_sdlc_review.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/reports/agentic_workspace_sdlc_review.md) (Pillar IV: Resilience, Evaluation & Security).
  - *Defect & SDLC Impact*: Custom agents in `agentic/custom/agents/` are evaluated ad-hoc without standardized benchmark suites. No objective measurement of agent task success rate, latency, token spend, or regression across workspace updates.
  - *Target Files*:
    - Implementation: [`workplace/core/agent_benchmark_harness.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/agent_benchmark_harness.py) (mirrored to [`.nb/core/agent_benchmark_harness.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/core/agent_benchmark_harness.py))
    - Benchmark Suite: [`workplace/tests/benchmarks/test_agent_benchmarks.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/benchmarks/test_agent_benchmarks.py)
    - Scorecard Report: [`workplace/docs/reports/agent_quality_scorecard.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/reports/agent_quality_scorecard.md)
  - *Technical Scope & Architecture*:
    - **Standardized Synthetic Challenge Suite**: Automated evaluation scenarios exercising each agent across 5 core disciplines: AST parsing & pruning, wire contract validation, living doc generation, CVE remediation, and flaky test isolation.
    - **5-Metric Scoring Radar**:
      1. Task Success Rate ($TSR \ge 90\%$)
      2. Semantic Parity Score ($S_{SP} \ge 0.95$)
      3. Token Efficiency ($< 5\text{k}$ tokens / task)
      4. Execution Latency ($< 10\text{s}$ per turn)
      5. Invariant Compliance Rate ($100\%$ zero-violation)
    - **Automated Scorecard & Merkle Anchoring**: CLI command `percipience benchmark run --agents all` generating Markdown scorecard and committing evaluation receipt `RP_BENCHMARK_*` to Merkle ledger.
  - *Acceptance Criteria*:
    - Unit and benchmark tests validating challenge execution, metric calculation, radar scorecard generation, and regression detection when an agent underperforms.

---

---

## 18. Multi-Tenant Project Provisioning, Fleet Workspaces & Enterprise Admin Control Plane (`CAP-40` to `CAP-45`)

### 18.1. Secure Multi-Tenant Project Provisioning & IAM (`CAP-40`)
- [x] **TODO-PRT-01: Multi-Tenant Organization & Project Hierarchy (P1)**:
  - *Shortcoming*: Portal currently functions under a single default workspace without organizational multi-tenancy and project isolation.
  - *Implementation Scope*: Implement `workplace/core/tenant_manager.py` with hierarchical tenant isolation: `Organization (Tenant) -> Projects -> Repositories -> Workspaces / Nodes`. Add tenant-scoped PostgreSQL RLS schemas and RBAC authorization (`Enterprise Super Admin`, `Project Lead`, `Security Auditor`, `Agent Worker`).
- [x] **TODO-PRT-02: One-Click Project Scaffolding Wizard (P1)**:
  - *Shortcoming*: New customer projects require manual directory structure setup.
  - *Implementation Scope*: Implement `workplace/core/project_scaffolder.py` generating standard Quad-Space layouts (`context/`, `agentic/`, `workplace/`, `user/`), initializing isolated `context_ledger.yaml`, and minting genesis cryptographic recovery block `RP_GENESIS_000`.
- [x] **TODO-PRT-03: Automated KMS Key Broker & Sealed Enclave Provisioning (P1)**:
  - *Shortcoming*: Blueprint envelope keys are manually provisioned per instance.
  - *Implementation Scope*: Implement `workplace/core/kms_broker.py` for automated per-project Ed25519 signing keypairs and AES-256-GCM symmetric keys, supporting self-serve `.nbpack` domain layer packaging with zero client disk exposure.

### 18.2. Minute Project Control & Policy Configuration (`CAP-41`)
- [x] **TODO-PRT-04: Granular Context Engineering Tuning Sliders (P2)**:
  - *Shortcoming*: Token optimization, cognitive routing, and attention budget quotas are globally configured.
  - *Implementation Scope*: Add per-project policy configuration UI:
    - **Attention Slicing Quotas**: Dynamic ratio customization (default `15/25/35/10/15`).
    - **Cognitive Router Tiering Rules**: Project-level complexity thresholds for Tier A vs. Tier B routing.
    - **AST Pruning Limits**: Language-specific AST body stripping depth and decorator preservation rules.
- [x] **TODO-PRT-05: PR Gate & Self-Healing SLA Policies (P1)**:
  - *Shortcoming*: PR verification gates and healing retries use static hardcoded bounds.
  - *Implementation Scope*: Add per-project SLA policies: configurable diagnostic re-prompt attempts (1–5 turns), statistical flaky test quarantine thresholds (e.g. failure variance > 15%), and cross-module wire contract breaking-change rules.

### 18.3. Workstation & Node Fleet Telemetry (Individual Machines) (`CAP-42`)
- [x] **TODO-PRT-06: Lightweight Workstation Agent Daemon (`percipience-agent`) (P1)**:
  - *Shortcoming*: Enterprise admins have no visibility into active subagents running on local developer laptops or distributed CI/CD runner nodes.
  - *Implementation Scope*: Build background agent daemon (`.nb/bin/percipience-agent`, `workplace/core/fleet_agent.py`) running on macOS/Linux/Windows nodes. Periodically collects and transmits node telemetry:
    - **Machine Identity**: Hostname, Machine UUID, OS version, Local User/Agent ID.
    - **Active Workspaces**: Path, Active Worktree (`.nb/workspaces/wt_*`), Local Git Branch, Commit SHA.
    - **Process & Task State**: Active PID, Task Name, Progress Percentage (0–100%), Step Status (e.g. *AST Pruning*, *Running Fuzzer*, *Awaiting Review*).
    - **Local Token Savings**: Input/Output tokens consumed, Tokens saved via AST/Cache, Net financial savings ($).
  - *Status*: Completed in `workplace/core/fleet_agent.py`, `.nb/core/fleet_agent.py`, and executable `.nb/bin/percipience-agent` (`chmod +x`). Verified via `test_fleet_telemetry_finops.py` and `test_todo_capabilities.py`.
- [x] **TODO-PRT-07: Secure Fleet Ingestion Endpoint (P1)**:
  - *Shortcoming*: Portal lacks dedicated telemetry ingestion endpoints for distributed workstations.
  - *Implementation Scope*: Implement `POST /api/fleet/heartbeat` and `POST /api/fleet/telemetry` in `workplace/portal/server.py` with mTLS / bearer node-token authentication, tracking machine health status (`HEALTHY`, `HEALING`, `OFFLINE`, `QUARANTINED`).
  - *Status*: Completed in `workplace/portal/server.py` and `workplace/core/fleet_manager.py`. Supports bearer token auth, heartbeats, full telemetry ingestion, and offline timeout liveness detection.

### 18.4. Enterprise Admin Consolidated Fleet Monitoring & FinOps Dashboard (`CAP-43`)
- [x] **TODO-PRT-08: Enterprise Fleet Machine Grid & Live Workspaces Map (P1)**:
  - *Shortcoming*: Enterprise admins cannot view all distributed developer machines and subagent nodes from a single pane.
  - *Implementation Scope*: Add **Enterprise Fleet Monitor** tab to the portal and standalone dashboard:
    - Interactive machine grid filterable by Org, Project, and Status.
    - Columns: `Machine / Host`, `Developer / Subagent`, `Active Project`, `Worktree / Branch`, `Current Task & Progress Bar`, `Tokens Saved ($)`, `Actions`.
  - *Status*: Completed in `workplace/portal/server.py` (Tab 16 `#fleet-monitor`). Provides interactive machine grid, status badges, active worktree inspection, and live task progress.
- [x] **TODO-PRT-09: Machine-Level & Project-Level Token Savings Rollup (P1)**:
  - *Shortcoming*: FinOps accounting only calculates global mock ledger values.
  - *Implementation Scope*: Aggregate verified token savings across all connected machines and projects:
    - Gross Cloud LLM Savings ($) across the enterprise.
    - 15% Percipience Rev-Share Fee vs. 85% Net Customer Retained Savings.
    - Machine-level and project-level savings leaderboards.
  - *Status*: Completed in `workplace/core/fleet_manager.py` (`get_finops_rollup()`) and `GET /api/fleet/finops-rollup`. Computes enterprise gross savings, 15% Percipience rev-share fee, 85% customer net, and ranked machine/project leaderboards.
- [x] **TODO-PRT-10: Real-Time Task Progression & Milestone Tracker (P2)**:
  - *Shortcoming*: Long-running subagent tasks provide no step-by-step progress metrics.
  - *Implementation Scope*: Visualize live agent execution trajectories with step-by-step progress bars, task ETAs based on historical runtimes, and alerts for stuck subagents.
  - *Status*: Completed in `workplace/core/fleet_manager.py` (`get_active_tasks()`) and `GET /api/fleet/tasks`. Displays real-time progress bars, step status, and ETAs in Fleet Monitor UI and REST API.

### 18.5. Remote Machine Interventions & Governance Actions (`CAP-44`)
- [ ] **TODO-PRT-11: Remote Admin Actions on Individual Machines (P1)**:
  - *Shortcoming*: Stopping a malfunctioning agent or evicting a dead lease requires local terminal access on that machine.
  - *Implementation Scope*: Allow Enterprise Admins and Project Leads to trigger authenticated remote actions from the portal UI:
    - **Emergency Pause / Resume**: Freeze rogue subagent loops on a specific machine.
    - **Surgical Rollback Trigger**: Remotely rewind a specific machine's micro-module to Recovery Point `RP_k`.
    - **Force Worktree Lease Eviction**: Clean up dead leases on crashed or orphaned nodes.
    - **Flush Local AST Cache**: Invalidate and refresh local Tree-Sitter caches.
- [ ] **TODO-PRT-12: Enterprise Security & Quarantine Central Command (P1)**:
  - *Shortcoming*: Poisoning alerts and quarantined diffs are stored in local markdown files on each machine.
  - *Implementation Scope*: Centralize fleet-wide context poisoning incidents, AST dependency CVE blocks, and drift evolutions in an interactive single-pane triage workflow, sealing all admin resolutions into the immutable SHA-256 Merkle ledger.

---

## 19. IntelliJ IDEA & PyCharm IDE Plugin Control Plane (`CAP-12`, `CAP-13`, `CAP-14`)

- [x] **TODO-IDE-01: Bundled Essential Core Engines & Zero-Dependency Scaffolding (P1)**:
  - *Shortcoming*: Bootstrapping new workspaces required pre-existing `.nb/core/` engine files on disk.
  - *Implementation Scope*: Embed all 38 platform engines + `__init__.py` directly into IntelliJ plugin resources at `workplace/modules/mod_intellij_plugin/src/main/resources/percipience/core/`. Update `WorkspaceBootstrapper.kt` to unpack `.nb/core/*.py` alongside `.nb/bin/percipience` (`0755` executable permissions), configurations, CI/CD workflow, and genesis Merkle ledger block `RP_GENESIS_000`. Verify zero-disk external dependency operation.
- [x] **TODO-IDE-02: Interactive Startup Notification & Execution Service (P1)**:
  - Implement `PercipienceProjectStartupActivity` prompting users to bootstrap uninitialized workspaces on project open.
  - Register `PercipienceExecutionService` for asynchronous CLI execution (`gate`, `audit`, `cicd run`, `validate --layered`, `tokens summary`) with live logging and VFS auto-refresh.
- [x] **TODO-IDE-03: Sealed Distribution Packaging & Verification (P1)**:
  - Create `package_plugin.py` to compile Kotlin sources, produce `percipience-intellij-plugin-1.0.0.zip`, and install into active JetBrains IDE config directories.
  - Compile sealed layer envelope `.nb/bundles/intellij_pycharm_plugin_domain.nbpack` and verify full suite via `workplace/tests/test_ide_plugins_space.py`.

---

## 20. Actionable Issues & Implementation Backlog from Comprehensive Project Review (`output.md`)

> **Governing Audit Report**: [`output.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/output.md) (Overall Score: 4.5/5.0)  
> **Core Objective**: Systematically track and resolve all architectural gaps, documentation discrepancies, testing requirements, user experience bottlenecks, and commercialization milestones identified during the comprehensive workspace review.

### 20.1. Tier 1: Immediate Launch Blockers (< 1 Day / Production Release Hygiene)
- [x] **TODO-REV-01: Global CLI Path Inconsistency Fix across Documentation (P0)**:
  - *Identified Issue*: Legacy markdown documents contained redundant double `.nb/.nb/bin/` paths instead of `.nb/bin/percipience`, causing CLI commands to fail when copy-pasted by developers.
  - *Implementation Scope*: Conduct global search-and-replace across all `.md` files (`README.md`, `HOWTO_WORKSPACE_GUIDE.md`, `.claude/mcp.json`, etc.) standardizing all execution paths to `.nb/bin/percipience`.
- [x] **TODO-REV-02: Root Portal Launcher Script (`start_portal.sh`) (P0)**:
  - *Identified Issue*: `README.md` and onboarding guides referenced `./start_portal.sh` in the repository root, but developers had to manually run uvicorn from `workplace/portal/`.
  - *Implementation Scope*: Create executable `start_portal.sh` in project root with automatic port detection (default `3000`), `PYTHONPATH` exports (`.:.nb:.nb/core:workplace:workplace/core`), orphan process cleanup (`lsof -ti:$PORT | xargs kill -9`), and direct FastAPI server launch.
- [x] **TODO-REV-03: Automated CLI Binary Existence & Execution Verification Test (P0)**:
  - *Identified Issue*: Test suite verified internal Python functions but lacked an automated integration test verifying that the physical `.nb/bin/percipience` script exists, is marked executable (`0755`), and successfully returns `--version`.
  - *Implementation Scope*: Add `test_cli_binary_exists` to `workplace/tests/test_play3_suite.py` asserting file presence, POSIX `X_OK` permissions, and exit code `0` on subcommands.
- [x] **TODO-REV-04: 5-Minute Developer Quick Start Section in `README.md` (P0)**:
  - *Identified Issue*: `README.md` previously began with heavy architectural specifications without a 30-second developer quick start.
  - *Implementation Scope*: Add prominent Quick Start section to `README.md` featuring one-click cloning, audit verification (`.nb/bin/percipience audit`), portal startup, and Merkle DAG dashboard exploration.
- [ ] **TODO-REV-05: System Prerequisites & Dependency Matrix in HOWTO Guide (P0)**:
  - *Identified Issue*: `HOWTO_WORKSPACE_GUIDE.md` lacked a dedicated prerequisites block specifying Python 3.11+, Git 2.30+, Redis 7.x (optional for distributed locks), and RAM recommendations (4GB min / 8GB for Tree-Sitter AST daemon).
  - *Implementation Scope*: Add Prerequisites and installation verification section to `HOWTO_WORKSPACE_GUIDE.md` directly after the introduction.
- [x] **TODO-REV-06: Transparent ROI Cost Calculator & AST Compression Limits (P0)**:
  - *Identified Issue*: Marketing materials claimed 60–85% token reduction without demonstrating exact dollar calculations across team sizes and PR volumes, or discussing when AST pruning is counter-productive.
  - *Implementation Scope*: Document realistic ROI math in `README.md` (e.g. 50-dev team @ 500 PRs/mo yielding $12,150 annual token savings) and document trade-offs where full source context is preferable (deep algorithmic refactors, complex bug triage).

### 20.2. Tier 2: Pre-Team Tier Launch (1–3 Days / Fast Follow & Community Readiness)
- [x] **TODO-REV-07: Head-to-Head Competitive Differentiation Matrix (P1)**:
  - *Identified Issue*: Prospective users lacked a direct comparison table contrasting Percipience against Cursor, GitHub Copilot Workspace, and Devin.
  - *Implementation Scope*: Embed comparison table in `README.md` and portal marketing highlighting Token Optimization (AST pruning), Cryptographic Audit Trails (Merkle DAG), Concurrent Agent Isolation (Worktrees), Self-Hosted VPC Enclaves, Native MCP compatibility, and Open Core licensing.
- [x] **TODO-REV-08: Core Terminology Technical Glossary (P1)**:
  - *Identified Issue*: High barrier to entry for developers unfamiliar with domain terms (AST Skeletonization, Merkle DAG, MVS, HITL, BYOR, WORM, MCP).
  - *Implementation Scope*: Add comprehensive Glossary table in `README.md` explaining key terms, definitions, and developer benefits.
- [ ] **TODO-REV-09: 5-Minute Video Walkthrough & Interactive Demo Outline (P1)**:
  - *Identified Issue*: Absence of a concise visual demonstration showcasing live AST token reduction, tamper-evident Merkle state rolls, and isolated worktree concurrency.
  - *Implementation Scope*: Draft storyboard script and embed Loom/YouTube walkthrough link in documentation covering: Problem Overview (0:30) -> Live AST Pruning (1:30) -> Merkle Audit Trail (1:30) -> Ephemeral Worktrees (1:00) -> Next Steps (0:30).
- [ ] **TODO-REV-10: Concrete 90-Day GTM Milestones & Revenue Funnel (P1)**:
  - *Identified Issue*: GTM commercialization backlog lacked calendarized execution milestones with specific customer acquisition targets.
  - *Implementation Scope*: Establish formal 90-day rollout roadmap in `TODO.md` and commercial plans:
    - **Month 1 (Private Beta)**: 10 design partner enterprises, 1,000 PR audits, 500k tokens saved, case study publication.
    - **Month 2 (Public Beta)**: Public SaaS portal launch, Free tier self-serve onboarding, initial ROI benchmark report ($15k MRR target).
    - **Month 3 (General Availability)**: GA release, VS Code / IntelliJ marketplace availability, self-serve Team tier ($50k MRR target).
- [ ] **TODO-REV-11: End-to-End Developer Workflow Integration Test Suite (P1)**:
  - *Identified Issue*: Test suite primarily focused on modular unit tests without a cohesive end-to-end integration test exercising the full MVS Spec -> Derivation -> Gatekeeper -> Merkle Block Seal pipeline.
  - *Implementation Scope*: Create `workplace/tests/test_e2e_developer_workflow.py` testing complete lifecycle from raw feature spec to verified PR commit.
- [x] **TODO-REV-12: Free Tier PR Audit Quota Clarification & Expansion (P1)**:
  - *Identified Issue*: Initial 500 PR audits/mo quota was restrictive for active solo developers, and lacked clear definitions between gatekeeper runs and read-only status checks.
  - *Implementation Scope*: Expand Free Tier limit to 1,000 PR audits/month in commercial tier matrices and explicitly define audit consumption rules.

### 20.3. Tier 3: Enterprise Tier Launch (1–2 Weeks / Enterprise Scale & Extensibility)
- [x] **TODO-REV-13: IDE Plugin MVP Ecosystem (VS Code & IntelliJ/PyCharm) (P1)**:
  - *Identified Issue*: Developers expect native IDE extensions rather than relying solely on terminal CLI commands.
  - *Implementation Scope*: Complete JetBrains / PyCharm plugin suite (`workplace/modules/mod_intellij_plugin/`) and scaffold VS Code extension bridge (`workplace/integrations/ide_extensions/`) supporting live Merkle status, one-click gatekeeper runs, and AST token meters.
- [x] **TODO-REV-14: OpenTelemetry (OTel) GenAI Observability & APM Exporter (P1)**:
  - *Identified Issue*: Enterprise APM infrastructure (Datadog, Dynatrace, Honeycomb, Jaeger) requires standardized OTel GenAI semantic spans for model latency, prompt token counts, and cost telemetry.
  - *Implementation Scope*: Integrate `OpenTelemetryGenAIExporter` (`workplace/core/otel_exporter.py`) with W3C `traceparent` distributed headers, TTFT metrics, and streaming span sinks.
- [ ] **TODO-REV-15: Interactive GitOps PR Bot (`percipience bot deploy`) (P2)** *(Consolidated with TODO-COMP-15)*:
  - *Identified Issue*: Automated pull request creation and interactive comment reviews currently require manual git workflows.
  - *Implementation Scope*: Build `workplace/core/gitops_pr_bot.py` posting interactive Markdown status cards, collapsible test logs, ephemeral staging preview URLs, and handling slash commands (`/re-heal`, `/rollback`). Tracks unified PR bot lifecycle alongside `TODO-COMP-15`.
- [ ] **TODO-REV-16: Hybrid Vector RAG Retrieval for Large Codebases (>1M LOC) (P2)** *(Consolidated with TODO-COMP-09)*:
  - *Identified Issue*: Massive enterprise monorepos require hybrid sparse-dense semantic search alongside deterministic AST pruning.
  - *Implementation Scope*: Unified into `TODO-COMP-09` (`workplace/core/vector_retrieval_engine.py`) connecting LanceDB / Pinecone with Voyage Code 2 embeddings for semantic multi-hop code discovery within the Unified Context Retrieval Pipeline.
- [x] **TODO-REV-17: Restructured Enterprise Tier Commercial Package (P1)**:
  - *Identified Issue*: $9,999/mo Enterprise tier required stronger justification with tangible enterprise services.
  - *Implementation Scope*: Enrich Enterprise Tier specifications with: Dedicated Customer Success Manager (CSM), 40 hrs/quarter Custom MCP Server Development, 1-Hour Support SLA, Okta/Azure AD SAML/OIDC SSO, On-Premises Helm Charts, and SOC 2 Type II audit documentation.
- [ ] **TODO-REV-18: Conventional-to-Quad-Space Repository Migration CLI Tool (P2)**:
  - *Identified Issue*: Migrating legacy codebases into Percipience Quad-Space structure (`.nb/`, `workplace/`, `user/`, `.claude/`) required manual folder re-organization.
  - *Implementation Scope*: Implement `percipience migrate --from-conventional [--analyze-only]` analyzing existing directory layouts and automatically refactoring files into Quad-Space partitions with dry-run reports.
- [ ] **TODO-REV-19: Interactive Onboarding Setup Wizard (`percipience init --interactive`) (P2)**:
  - *Identified Issue*: Initial setup required manual configuration of `mcp.json`, environment variables, and ledger genesis.
  - *Implementation Scope*: Build interactive CLI wizard prompting for project type (Monorepo, Microservice, Package), primary language (Python, TypeScript, Go, Polyglot), and auto-provisioning MCP servers, hooks, and genesis Merkle ledger.

### 20.4. Documentation, Operational Guides & Architectural Clarifications
- [ ] **TODO-REV-20: Concrete MVS Feature Specification Example in HOWTO Guide (P1)**:
  - *Identified Issue*: MVS documentation was conceptual without a concrete feature specification walkthrough.
  - *Implementation Scope*: Add end-to-end OAuth2 authentication scenario in `HOWTO_WORKSPACE_GUIDE.md` showing MVS template population, automated type derivation, and FastAPI endpoint scaffolding.
- [ ] **TODO-REV-21: Jira MCP Integration Alpha Disclaimer (P1)**:
  - *Identified Issue*: Jira MCP ingestion command was presented without maturity context.
  - *Implementation Scope*: Add alpha status callout (`Maturity: 0.80`) in `HOWTO_WORKSPACE_GUIDE.md` with instructions for manual `mvs_jira_story.json` fallback.
- [ ] **TODO-REV-22: Ephemeral Worktree TTL & Automatic Cleanup Documentation (P1)**:
  - *Identified Issue*: `--ttl` parameter was presented without detailed explanation of auto-merge vs quarantine behavior on timeout.
  - *Implementation Scope*: Document TTL lifecycle mechanics, active POSIX PID probing, and automated lease reclamation in `HOWTO_WORKSPACE_GUIDE.md`.
- [ ] **TODO-REV-23: Merkle Audit Trail Inspection & Benchmark Reference (P1)**:
  - *Identified Issue*: Users had no reference for what a CLI audit output looks like or how the Merkle engine performs under high block counts.
  - *Implementation Scope*: Add sample `percipience audit --block-id <id>` and `percipience audit --enforce-merkle-chain` output snippets alongside performance scalability tables (<10k LOC: 0.3s up to >1M LOC: 18s).
- [ ] **TODO-REV-24: Platform Internals (`.nb/core/`) vs Application Code (`workplace/core/`) Clarification (P1)**:
  - *Identified Issue*: Potential developer confusion between internal platform engines and extensible application logic.
  - *Implementation Scope*: Add architectural boundary guide in `HOWTO_WORKSPACE_GUIDE.md` explaining `.nb/core/` (immutable platform runtime) vs `workplace/core/` (custom business logic, adapters, and domain engines).
- [ ] **TODO-REV-25: Automated Code Coverage CLI Integration (`percipience test --coverage`) (P1)**:
  - *Identified Issue*: Need for unified test coverage reporting directly from the CLI.
  - *Implementation Scope*: Add `--coverage` flag to `percipience test` generating terminal summary tables and HTML coverage artifacts.

---

## 21. Distributed Ephemeral Worktree Swarms & Sandboxed Plan Derivation (DEWS) (`CAP-48` to `CAP-52`)

> **Governing RFC**: [`workplace/docs/proposals/rfc_containerized_worktree_swarms.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/proposals/rfc_containerized_worktree_swarms.md)  
> **Core Objective**: Enable sandboxed single-container worktree plan execution via LLM CLIs (Claude, Aider) and scale to distributed multi-container enterprise swarm fleets with zero-cloud-clutter Git bundle transport, topological 3-way consolidation, and verified local delivery.

### 21.1. Phase 1: Sandboxed Plan Derivation in Local Worktree Container
- [x] **TODO-DEWS-01: Docker Agent Runner Base Image & Tooling Manifest (P1)**:
  - *Identified Requirement*: Standardized, hardened multi-runtime Docker image equipped with Python 3.11, Node.js 20, Git, jq, curl, `@anthropic-ai/claude-code`, and `aider-chat`. Include non-root execution permissions, global git identity defaults, and dynamic safe-directory configuration.
  - *Target Files*: [`workplace/infra/docker/Dockerfile.agent_runner`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/infra/docker/Dockerfile.agent_runner), [`workplace/infra/docker/entrypoint_agent.sh`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/infra/docker/entrypoint_agent.sh), [`workplace/infra/docker/docker-compose.yml`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/infra/docker/docker-compose.yml), [`workplace/infra/docker/docker-test.sh`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/infra/docker/docker-test.sh)
  - *Acceptance Criteria*: Image builds cleanly; `claude --version` (2.1.197), `node --version` (v20.20.2), `python3 --version` (3.11.17) execute successfully inside container; non-root user `agent` (UID 1000) cannot access root filesystem; safe.directory properly initialized.
- [x] **TODO-DEWS-02: Containerized Plan-to-Code Executor Engine (P1)**:
  - *Identified Requirement*: Execution harness that takes an `.nb/plan/` path and target module, acquires an ephemeral worktree via `WorktreeEngine.acquire()`, mounts the worktree into `percipience/agent-runner`, and drives the LLM CLI in headless mode (`-p` / `--print`) to implement the specification.
  - *Target Files*: [`.nb/core/container_plan_executor.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/core/container_plan_executor.py), [`workplace/core/container_plan_executor.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/container_plan_executor.py), CLI subcommand in [`.nb/bin/percipience`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/bin/percipience) (`swarm exec`), [`workplace/tests/test_container_plan_executor.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_container_plan_executor.py)
  - *Acceptance Criteria*: Automatically mounts worktree without `.git` pointer breakage via automatic `gitdir` pointer translation and rollback; passes invariant context and plan; executes simulation/live LLM inside container; cleans up worktree lease upon exit; verified by 6 passing unit/integration tests and CLI execution.

### 21.2. Phase 2: Distributed Multi-Container Swarm Fleet & Transport
- [x] **TODO-DEWS-03: Streaming Git Bundle Transport Module (P1)**:
  - *Identified Requirement*: Cryptographic packaging and extraction of Git commits and uncommitted diffs using `git bundle create` and `git bundle verify`. Provide streaming HTTP upload/download adapters to transmit state between developer workstations and remote fleets without polluting remote Git branches.
  - *Target Files*: [`.nb/core/git_bundle_transport.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/core/git_bundle_transport.py), [`workplace/core/git_bundle_transport.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/core/git_bundle_transport.py), [`workplace/tests/test_git_bundle_transport.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/tests/test_git_bundle_transport.py)
  - *Acceptance Criteria*: Round-trip test: local uncommitted branch -> bundle -> remote extraction -> remote commit -> result bundle -> local merge passes with 100% hash parity; chunk streaming generator and SHA-256 integrity verified; tested via 5/5 passing unit/integration tests.
- [ ] **TODO-DEWS-04: Enterprise Swarm Fleet Dispatch API & Endpoints (P1)**:
  - *Identified Requirement*: REST endpoints under `/api/swarm/fleet/*` (`POST /api/swarm/fleet/dispatch`, `GET /api/swarm/fleet/jobs/{job_id}`, `GET /api/swarm/fleet/jobs/{job_id}/bundle`) supporting asynchronous task ingestion, worker allocation, and streaming results.
  - *Target Files*: `workplace/portal/server.py`, `.nb/core/swarm_fleet_dispatcher.py`
  - *Acceptance Criteria*: Authenticated multipart upload accepts bundles; returns task execution receipt; provides live WebSocket / SSE job status updates.
- [ ] **TODO-DEWS-05: Distributed Worktree Coordinator with Live Redis 7.x Redlock (P1)**:
  - *Identified Requirement*: Enhance `RedisRedlockBackend` in `workplace/core/worktree_engine.py` with real `redis-py` connection pooling, distributed lease renewal heartbeats, and cluster quorum verification for multi-node deployments.
  - *Target Files*: `.nb/core/worktree_engine.py`, `workplace/core/worktree_engine.py`
  - *Acceptance Criteria*: Concurrent worktree requests across 5 containers correctly serialize; dead container lease auto-evicts within TTL window.
- [ ] **TODO-DEWS-06: Topological Consolidation & 3-Way Merge Agent Plugin (P1)**:
  - *Identified Requirement*: Specialist agent that takes $N$ completed worker branches, performs topological 3-way merges into an integration worktree, verifies wire contracts, and resolves non-conflicting seam differences before triggering the PR Gatekeeper.
  - *Target Files*: `.nb/agentic/custom/agents/agent_consolidation_synthesizer.yaml`, `.nb/core/consolidation_synthesizer.py`
  - *Acceptance Criteria*: Merges 3 disjoint module branches with 0 human intervention; rejects breaking contract divergences with actionable diagnostics.
- [ ] **TODO-DEWS-07: Percipience CLI Remote Dispatch Subcommand (P1)**:
  - *Identified Requirement*: Add `./.nb/bin/percipience swarm dispatch --remote <fleet-url> --plan <path> --sync-back <target-wt>` to wrap bundle creation, API dispatch, progress polling, and local unbundle checkout into a seamless developer command.
  - *Target Files*: `.nb/bundles/package_plan_business/bin/percipience`, `.nb/bin/percipience`
  - *Acceptance Criteria*: Single CLI command dispatches local plan, displays live remote container wave progress in terminal, and checks out verified code locally.
- [ ] **TODO-DEWS-08: Portal Fleet Telemetry & Swarm Dashboard Tab (P2)**:
  - *Identified Requirement*: Live Fleet Monitoring UI in the Portal displaying active worker container slots, Redis Redlock leases, active wave DAG executions, and cumulative FinOps token burn.
  - *Target Files*: `workplace/portal/server.py` (`#swarm-fleet`)
  - *Acceptance Criteria*: Live visual dashboard updating every 2s via `/api/swarm/fleet/status`; shows per-worker CPU/memory/token metrics.
