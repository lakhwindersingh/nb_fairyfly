# Neutron Binary Percipience (`nb_fairyfly`)
**Enterprise Context Engineering OS & Cloud SaaS Platform (Play 3 CEaaS)**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Architecture](https://img.shields.io/badge/Architecture-Quad--Space%20Partitioning-emerald.svg)](HOWTO_WORKSPACE_GUIDE.md)
[![Operating Mode](https://img.shields.io/badge/Operating%20Mode-Multi--Module%20(Play%203)-blueviolet.svg)](HOWTO_WORKSPACE_GUIDE.md)
[![Context Maturity](https://img.shields.io/badge/Context%20Maturity-0.957%20(Enterprise)-green.svg)](workplace/docs/reports/context_maturity_report.md)

---

## 📖 Operational Documentation & Developer Guides

- 📘 **[HOWTO_WORKSPACE_GUIDE.md](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/HOWTO_WORKSPACE_GUIDE.md)**: Complete Step-by-Step Operator & Developer Guide for running autonomous derivation, managing isolated Git worktrees, handling context poisoning, executing surgical rollbacks, and verifying Merkle block chains.
- 🏛️ **[Parent Master Context Engineering Plan](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/claude-context-engineering-parent-master-plan.md)**: Foundational specification defining the 21 core capabilities, Quad-Space clean partitioning, Merkle DAG ledger engine, and dual-mode architecture.
- 🚀 **[Play 3: Enterprise Context Engineering OS Plan](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/play/CEaasS/play_3_enterprise_context_engineering_os_plan.md)**: Commercial enterprise master plan for Percipience as a B2B SaaS platform and CI/CD gatekeeper.
- 💻 **[Play 3 SaaS Portal & Corporate Site Plan](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/play/CEaasS/play_3_corp_site_saas_portal_plan.md)**: Multi-module engineering plan for the commercial web portal, self-serve tenant onboarding, Stripe billing, usage metering, and observability dashboard.
- 📚 **[Centralized Workplace Documentation Hub](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/README.md)**: Single canonical repository for all living documentation, architecture diagrams, sequence flows, methodologies, benchmark analyses, guides, and reports.

---

## 🏛️ Standard Quad-Space Architecture

```text
nb_fairyfly/
├── .nb/           # Governing parent plans (.nb/plan/) and execution plays (.nb/play/)
├── context/       # Governance, schemas, contracts, Merkle ledger & recovery points
├── agentic/       # 6-phase prompt suites, workflows, custom agents & cognitive router
├── workplace/     # Application source code, configs, shared DTOs, tools & canonical documentation
│   ├── bin/       # Unified Percipience CLI executable (workplace/bin/percipience)
│   ├── scripts/   # Operational hooks & developer automation (install_git_hook.sh)
│   ├── tests/     # Automated unit & integration test suites (pytest)
│   ├── node_modules/ # Local dependencies & packaged enclave distributions
│   ├── core/      # Platform engines (Merkle, AST, Poisoning Sentinel, Living Docs)
│   ├── modules/   # mod_portal_marketing, mod_tenant_onboarding, mod_billing_metering, etc.
│   ├── shared/    # DTOs, Merkle crypto verification & headless UI primitives
│   ├── config/    # Runtime configuration, billing plans, token compression rules
│   └── docs/      # 📂 CANONICAL DOCUMENTATION LOCATION
│       ├── architecture.md       # Living system architecture & C4 topologies
│       ├── module_catalog.md     # Poly-module interface catalog & contracts
│       ├── sequence_flows.md     # Execution flows & verification gate sequences
│       ├── data_flow.md          # Ingestion pipelines & artifact state transitions
│       ├── entity_relationship.md# Relational entities & ledger schemas
│       ├── domain_extensions.md  # Active layered domain deep-dives
│       ├── methodologies/        # Token optimization & anti-drift protocols
│       ├── guides/               # Developer guides, quickstarts, plugin manuals
│       ├── reports/              # Context maturity scorecards & whitepapers
│       ├── benchmarks/           # Durability benchmarks, test harnesses & results
│       ├── hitl/                 # HITL governance runbooks & quarantine documentation
│       └── templates/            # Domain layer & MVS specification templates
└── user/          # Customer-owned inputs & ephemeral outputs
    ├── inputs/    # Minimum Viable Set (MVS) data tokens, schemas & event streams
    ├── hitl/      # Active quarantine manifests (flaky_quarantine.yaml) & incident records
    └── outputs/   # Browser observability dashboard (user/outputs/dashboard/index.html)
```

For quickstart commands and execution workflows, see [HOWTO_WORKSPACE_GUIDE.md](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/HOWTO_WORKSPACE_GUIDE.md).
