# Neutron Binary Percipience (`nb_fairyfly`)
**Enterprise Context Engineering OS, Autonomous CI/CD Gatekeeper & Model Context Protocol (MCP) Hub**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Architecture](https://img.shields.io/badge/Architecture-Quad--Space%20Partitioning-emerald.svg)](HOWTO_WORKSPACE_GUIDE.md)
[![Operating Mode](https://img.shields.io/badge/Operating%20Mode-Multi--Module%20(Play%203)-blueviolet.svg)](HOWTO_WORKSPACE_GUIDE.md)
[![Context Maturity](https://img.shields.io/badge/Context%20Maturity-0.990%20(Enterprise)-green.svg)](workplace/docs/reports/context_maturity_report.md)
[![MCP Protocol](https://img.shields.io/badge/MCP-Compliant-orange.svg)](.claude/mcp.json)

---

## 📖 Operational Documentation & Key References

- 📘 **[HOWTO_WORKSPACE_GUIDE.md](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/HOWTO_WORKSPACE_GUIDE.md)**: Complete Step-by-Step Operator & Developer Guide for running autonomous derivation, managing isolated Git worktrees, handling context poisoning, executing surgical rollbacks, and verifying Merkle block chains.
- 🏛️ **[Parent Master Context Engineering Plan](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/master/parent-master-plan/detailed.md)**: Foundational specification defining the core capabilities, Quad-Space clean partitioning, Merkle DAG ledger engine, and multi-tier commercial models.
- 🔌 **[IntelliJ IDEA & PyCharm Plugin Plan](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/l1/intellij-pycharm-plugin/detailed.md)**: Layerable L1 domain plan detailing JetBrains Platform SDK integration, PSI AST token reduction, ToolWindow Control Plane, and out-of-the-box Claude MCP auto-provisioning.
- 🚀 **[Play 3: Enterprise Context Engineering OS Plan](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/play/CEaasS/play_3_enterprise_context_engineering_os_plan.md)**: Commercial enterprise master plan for Percipience as a B2B SaaS platform and CI/CD gatekeeper.
- 💻 **[Play 3 SaaS Portal & Corporate Site Plan](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/play/CEaasS/play_3_corp_site_saas_portal_plan.md)**: Engineering plan for the commercial web portal, self-serve tenant onboarding, Stripe billing, usage metering, and observability dashboard.
- 📚 **[Workplace Documentation Hub](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/README.md)**: Single canonical repository for all living documentation, architecture diagrams, sequence flows, methodologies, benchmark analyses, guides, and reports.

---

## 🏛️ System Architecture: Quad-Space Partitioning

Percipience organizes repositories into four strictly bounded spaces to prevent prompt pollution, enable deterministic agent execution, and guarantee cryptographic auditability:

```text
nb_fairyfly/
├── .claude/         # 🤖 Model Context Protocol (MCP) & AI Agent Workspace Bindings
│   ├── mcp.json     # MCP server endpoints (percipience, ast_optimizer, gatekeeper, merkle_auditor)
│   └── settings.json# Claude model routing, rules, and 20+ agent specialist registry
├── .nb/             # ⚙️ Platform Agentic CI/CD System (Context Engineering OS)
│   ├── bin/         # Unified Percipience CLI executable (.nb/bin/percipience)
│   ├── config/      # Platform configurations (billing_plans, token_compression_rules, byor)
│   ├── core/        # 38 Platform core engines (Merkle, AST Optimizer, Poisoning Sentinel, CI/CD, etc.)
│   ├── context/     # Governance, schemas, wire contracts, Merkle ledger & recovery points
│   │   ├── contracts/   # Machine-readable wire contracts (.json / .yaml)
│   │   ├── rules/       # Domain safety invariants and threading rules
│   │   └── ledger/      # Immutable SHA-256 Merkle chain and FinOps savings ledger
│   ├── agentic/     # Prompt suites, workflows, custom agents & declarative runtime
│   ├── bundles/     # Packaged multi-tier IDE plugin bundles and sealed .nbpack layers
│   ├── scripts/     # Operational hooks & developer automation
│   ├── tests/       # Platform CI/CD verification suites
│   └── plan/        # Governing parent plans and modular domain layer plans
├── workplace/       # 🔨 Project-Specific Source Code & Layered Domain Implementations
│   ├── modules/     # Layered domain modules (mod_intellij_plugin, mod_vscode_extension, etc.)
│   ├── portal/      # Cloud SaaS Portal web server & FastAPI backend
│   ├── src/         # Web application frontend
│   ├── shared/      # DTOs, cross-module protocols & protobuf definitions
│   ├── config/      # Project configurations
│   ├── tests/       # Project-specific domain test suites
│   └── docs/        # 📂 CANONICAL DOCUMENTATION (Living C4 diagrams, flows & reports)
└── user/            # 👤 Customer-Owned Inputs & Ephemeral Outputs
    ├── inputs/      # Minimum Viable Set (MVS) data tokens, schemas & event streams
    ├── hitl/        # Active quarantine manifests & human-in-the-loop incident records
    └── outputs/     # Observability dashboards & context maturity scorecards
```

---

## 🤖 Model Context Protocol (MCP) & Agent Interoperability

Percipience exposes a rich suite of local MCP tools allowing Anthropic Claude (Claude Code, Claude Desktop), Google Gemini (Gemini CLI), Cursor, Windsurf, and terminal autonomous agents to seamlessly invoke platform operations:

### Exposed MCP Servers ([`.claude/mcp.json`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.claude/mcp.json))
| Server Name | Command | Description |
| :--- | :--- | :--- |
| **`percipience`** | `python3 .nb/bin/percipience` | Unified CLI execution interface for workflows, worktrees, and ledger audits. |
| **`ast_optimizer`** | `python3 .nb/bin/percipience optimize` | Polyglot Tree-Sitter 6D AST skeletonization & prompt token pruner (60-85% savings). |
| **`gatekeeper`** | `python3 .nb/bin/percipience gate` | Automated 7-stage CI/CD gatekeeper validating wire contracts, security, and tests. |
| **`merkle_auditor`**| `python3 .nb/bin/percipience audit` | SHA-256 Merkle DAG state auditor, recovery point validator, and maturity scorecard. |
| **`worktree_manager`**| `python3 .nb/bin/percipience worktree` | Ephemeral isolated Git worktree allocator preventing concurrent agent clobbering. |
| **`living_doc_engine`**| `python3 .nb/bin/percipience doc` | Continuous AST-to-Mermaid architecture synchronizer and contract doc generator. |

> [!NOTE]
> When the IntelliJ/PyCharm plugin bootstraps any project in **any** tier (`free`, `team`, `business`, `enterprise`, or universal), it automatically provisions and verifies `.claude/mcp.json` and `.claude/settings.json` in the project root.

---

## 🧩 JetBrains IntelliJ & PyCharm IDE Plugin

The Kotlin-based JetBrains IDE plugin (`mod_intellij_plugin`) brings the full power of Percipience into IntelliJ IDEA, PyCharm, and JetBrains IDEs:

- **Dockable ToolWindow Control Plane**: Dynamic 6-tab control plane providing real-time Merkle DAG visualization, workflow execution status, AST token FinOps meters, and JCEF living architecture documentation.
- **Dynamic Tier-Permission-Aware Action Matrix**: Real-time evaluation of active license (`tenant_license.json` / `PERCIPIENCE_PLAN`), dynamically rendering Free (Gatekeeper/Audit/CI/CD), Team (+Worktrees/Agents/Drift), Business (+NBPack Layer Packaging/Gateway Provisioner), and Enterprise (+Swarm Triad/VPC/WORM Egress) action buttons.
- **Program Structure Interface (PSI) AST Pruner**: Deep in-editor AST analysis extracting class and function signatures while stripping bodies to reduce LLM prompt token consumption by 60–85%.
- **In-Editor Annotators & Quick-Fix Intentions**: Real-time wire contract validation with gutter markers and `Alt+Enter` / `Option+Return` quick-fixes.
- **Terminal Agent Interception**: Automatic injection of `PERCIPIENCE_TERMINAL_MODE=1` and `PERCIPIENCE_AST_COMPRESSION=1` into embedded terminal sessions.

---

## 💳 Commercial Tier Matrix & Packaging

| Capability | Free Community (`plan_free`) | Team (`plan_team`) | Business (`plan_business`) | Enterprise Dedicated (`plan_enterprise`) |
| :--- | :---: | :---: | :---: | :---: |
| **Base Monthly Price** | **$0** | **$1,499** | **$4,499** | **$9,999** |
| **Included Seats** | 1 | 15 | 50 | Unlimited |
| **Concurrent Worktrees** | 1 | 5 | 20 | Unlimited |
| **Monthly PR Audits** | 500 | 5,000 | 25,000 | Unlimited |
| **AST Token Pruning (60-85%)** | ✅ | ✅ | ✅ | ✅ |
| **Merkle Chain State Auditing** | ✅ | ✅ | ✅ | ✅ |
| **Basic Autonomous CI/CD** | ✅ | ✅ | ✅ | ✅ |
| **Claude & MCP Agent Interop** | ✅ | ✅ | ✅ | ✅ |
| **Specialist Agents Registry** | ❌ | ✅ | ✅ | ✅ |
| **Dynamic Worktree Manager** | ❌ | ✅ | ✅ | ✅ |
| **Encrypted .nbpack Packaging**| ❌ | ❌ | ✅ | ✅ |
| **Multi-Tenant Gateway Provisioner**| ❌ | ❌ | ✅ | ✅ |
| **Private Air-Gapped VPC Enclave** | ❌ | ❌ | ❌ | ✅ |
| **Immutable WORM Cloud Egress** | ❌ | ❌ | ❌ | ✅ |

---

## ⚡ Unified CLI Commands

The unified Percipience CLI (`.nb/bin/percipience`) serves as the central command-line interface:

```bash
# 1. Run 7-stage CI/CD gatekeeper check
./.nb/bin/percipience gate

# 2. Audit Merkle DAG ledger continuity and context maturity score
./.nb/bin/percipience audit --enforce-merkle-chain

# 3. Optimize AST token footprint and display FinOps savings
./.nb/bin/percipience tokens summary
./.nb/bin/percipience optimize --target workplace/

# 4. Run autonomous CI/CD hygiene and bounded self-healing
./.nb/bin/percipience cicd run

# 5. Manage isolated Git worktrees for concurrent subagents
./.nb/bin/percipience worktree list
./.nb/bin/percipience worktree create wt_feature_01

# 6. Package and provision commercial tiers
./.nb/bin/percipience package --tier plan_free
./.nb/bin/percipience provision --target all --tier plan_enterprise

# 7. Compile and seal Ed25519-signed .nbpack layer envelope
./.nb/bin/percipience layer pack --plan .nb/plan/l1/intellij-pycharm-plugin/concise.md --output .nb/bundles/intellij_pycharm_plugin_domain.nbpack
```

---

## 🚀 SaaS Portal Quickstart

```bash
# Start the commercial SaaS Portal & FastAPI backend
kill -9 $(lsof -t -i :3000) 2>/dev/null || true
./start_portal.sh
```

For complete step-by-step developer workflows, see **[HOWTO_WORKSPACE_GUIDE.md](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/HOWTO_WORKSPACE_GUIDE.md)**.
