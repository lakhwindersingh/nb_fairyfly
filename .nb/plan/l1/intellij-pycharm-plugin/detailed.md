---
plan_type: "layerable_domain_plan"
plan_id: "domain_intellij_pycharm_plugin"
name: "IntelliJ IDEA & PyCharm IDE Plugin, PSI AST Analysis & Percipience Control Plane Space"
parent_master_plan: "master/parent-master-plan/concise.md"
tier_mapping:
  tier_2: "Enterprise Domain Rules & Wire Contracts (.nb/context/contracts/, .nb/context/rules/)"
  tier_3: "Specialist Subagents & Delivery Workflows (.nb/agentic/custom/agents/, .nb/agentic/custom/workflows/)"
model_tiering_policy:
  provider_agnostic: true
  tier_a_model: "claude-3-7-sonnet / pro"
  tier_b_model: "claude-3-5-haiku / flash"
  tier_a_reference_models: ["claude-3-7-sonnet", "gemini-2.0-pro", "gpt-4o", "deepseek-r1"]
  tier_b_reference_models: ["claude-3-5-haiku", "gemini-2.0-flash", "gpt-4o-mini"]
---

# Layerable Context Engineering Plan: IntelliJ IDEA & PyCharm Plugin Space — Detailed Implementation Guide

### Executive Overview & Domain Grounding

<!-- Plan Co-Location Notice -->
> **Co-Located Agent Specifications**: Agent definitions for this plan are stored along-with the plan in [`.nb/agentic/custom/agents/`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/agentic/custom/agents/) and embedded directly in Section 3. In newly created projects where the `agentic/` directory does not yet exist, `./bin/percipience layer apply` automatically extracts and hydra-instantiates these files into `.nb/agentic/custom/agents/`.

This document is a **Layerable Domain-Specific Context Engineering Plan** designed to overlay onto the generic **Parent Master Context Engineering Framework** (`master/parent-master-plan/concise.md`). While the parent framework governs universal poly-module lifecycle orchestration, cryptographic Merkle state verification, AST token compression, and autonomous CI/CD, this domain layer injects concrete IDE integration patterns, JetBrains Platform SDK APIs, Program Structure Interface (PSI) tree analysis, ToolWindow orchestration, and tier-permission-aware Control Plane button governance required for:

1. **JetBrains Platform SDK & IntelliJ / PyCharm ToolWindow Control Plane**:
   - Modern Kotlin-based plugin built with Gradle IntelliJ Plugin (`org.jetbrains.intellij.platform`).
   - Integrated dockable `ToolWindow` ("Percipience OS") offering dynamic, tier-governed Control Plane action buttons, live Merkle DAG chain visualization, workflow execution status, AST token FinOps meters, and living documentation viewer (JCEF / Java Chromium Embedded Framework).
   - Project-level background services (`ProjectService`) maintaining synchronized state with the local Percipience daemon via non-blocking Kotlin Coroutines (`Dispatchers.Default` and `Dispatchers.EDT`).

2. **Dynamic Tier-Permission-Aware Control Plane UI & Tooling Isolation**:
   - Dynamic tier resolution evaluating workspace licenses (`tenant_license.json`, `.percipience_license.json`), context ledger, and environment (`PERCIPIENCE_PLAN`).
   - Granular Control Plane button rendering mapping strictly to active entitlements across **Free Community**, **Team**, **Business**, and **Enterprise Dedicated** tiers.
   - Enforcing strict platform tools exposure boundaries: Free Tier exposes exclusively safe gatekeeper actions while paid tiers expose raw tool suites and encrypted `.nbpack` compilers.

3. **Program Structure Interface (PSI) Tree Analysis & Real-Time AST Token Optimization**:
   - Deep PSI inspection for multi-language workspaces (Python via `PyFile`/`PyClass`/`PyFunction`, Kotlin/Java via `PsiClass`/`PsiMethod`, TypeScript/JavaScript).
   - Real-time token calculation engine diffing raw source vs. AST-pruned interfaces ($60-85\%$ token reduction).
   - Pre-prompt AST pruning inspection popup allowing developers to visually inspect and verify stripped function bodies before dispatching prompts to LLM agents.

4. **In-Editor Annotators, Gutter Icons & Quick-Fix Intentions**:
   - `ExternalAnnotator` and `LocalInspectionTool` verifying active wire contracts (`.nb/context/contracts/`) against calling code in real time.
   - Editor gutter icons highlighting active workflow steps, live Merkle recovery points, and verified test assertions.
   - Quick-fix intention actions (`Alt+Enter` / `Option+Return`) triggering automatic wire contract re-synchronization, AST living doc synthesis, and PR gate checks.

5. **Hermetic Threading & Read/Write Action Safety**:
   - Strict adherence to JetBrains Platform threading models (`ReadAction`, `WriteAction`, `ProgressIndicator`, `runBackgroundableTask`).
   - Non-blocking daemon communication over local UNIX domain sockets or IPC loopback bridges, avoiding UI freezes (EDT latency $< 16\text{ms}$).

6. **Terminal-Mode Autonomous Agent Integration & AST Token Compression**:
   - Deep integration with terminal-based autonomous AI agents (Claude Code, Gemini CLI, Aider) executing inside the embedded IDE terminal tool window.
   - Transparent interception & environment variable injection (`PERCIPIENCE_TERMINAL_MODE=1`, `PERCIPIENCE_AST_COMPRESSION=1`) via `PercipienceTerminalCustomizer`.
   - Real-time token metering and gross USD spend tracking recorded directly into the cryptographic `token_savings_ledger.yaml`.

---

## 1. Domain-Specific Quad-Space Mapping

```
.
├── .nb/context/
│   ├── contracts/
│   │   ├── intellij_plugin_manifest_contract.json  # plugin.xml contributes schema, actions, toolWindows
│   │   ├── psi_ast_bridge_contract.yaml            # PSI traversal nodes & language AST mapping rules
│   │   └── daemon_rpc_contract.json                # JSON-RPC IPC contract between IDE and daemon
│   └── rules/
│       ├── jetbrains_platform_threading_rules.md   # EDT vs. Background coroutine dispatch rules
│       ├── psi_read_lock_invariants.md             # ReadAction requirements for PSI tree traversal
│       └── jcef_security_invariants.md             # Content-Security-Policy & origin sandboxing
├── .nb/agentic/
│   └── custom/
│       ├── agents/
│       │   ├── agent_jetbrains_plugin_architect.yaml      # Domain Expert: Kotlin, Gradle, Plugin SDK
│       │   ├── agent_psi_ast_bridge_specialist.yaml       # Subagent: PSI visitor, AST pruning
│       │   └── agent_intellij_ui_ux_engineer.yaml         # Subagent: Swing/JCEF ToolWindow UI
│       └── workflows/
│           └── intellij_pycharm_plugin_delivery_flow.yaml # Build -> PSI Test -> ToolWindow -> Package
├── workplace/
│   ├── docs/
│   │   ├── intellij_pycharm_plugin_architecture.md        # System C4 component topologies & module interfaces (Mermaid)
│   │   ├── intellij_pycharm_plugin_sequence.md            # End-to-end execution sequence flows (Mermaid)
│   │   ├── intellij_pycharm_plugin_data_flow.md           # Topological data flow & contract exchange DAGs (Mermaid)
│   │   ├── intellij_pycharm_plugin_entity_relation.md     # Entity-relationship & state transition models (Mermaid)
│   │   └── intellij_pycharm_plugin_contracts_registry.md  # Machine-readable contract registry & artifact handoff matrix
│   ├── modules/
│   │   └── mod_intellij_plugin/
│   │       ├── build.gradle.kts                           # Gradle IntelliJ Platform plugin configuration
│   │       ├── package_plugin.py                          # Multi-tier JAR, ZIP & .nbpack packaging script
│   │       ├── PLUGIN_USER_GUIDE.md                       # Comprehensive guide and tier matrix
│   │       ├── src/main/
│   │       │   ├── kotlin/com/neutronbinary/percipience/
│   │       │   │   ├── PercipienceIcons.kt                # Custom SVG icons and UI assets
│   │       │   │   ├── bootstrap/
│   │       │   │   │   ├── PercipienceProjectStartupActivity.kt # Startup prompt for unconfigured workspaces
│   │       │   │   │   └── WorkspaceBootstrapper.kt       # Offline Quad-Space scaffolding & extraction
│   │       │   │   ├── actions/
│   │       │   │   │   ├── BootstrapWorkspaceAction.kt    # Manual Tools menu trigger for bootstrap
│   │       │   │   │   ├── InspectAstPruningAction.kt     # In-editor Shift+Alt+P AST inspection
│   │       │   │   │   └── InspectSandboxPermissionsAction.kt # Tools menu trigger for permissions
│   │       │   │   ├── annotators/
│   │       │   │   │   └── ContractInspectionAnnotator.kt # Editor line markers for wire contracts
│   │       │   │   ├── intentions/
│   │       │   │   │   └── SyncWireContractIntention.kt   # Alt+Enter quick-fix for schema drift
│   │       │   │   ├── ledger/
│   │       │   │   │   └── WorkspaceLedgerReader.kt       # Real-time reader for FinOps, Merkle & TierInfo
│   │       │   │   ├── psi/
│   │       │   │   │   └── PsiAstBridge.kt                # Multi-language PSI AST pruning engine
│   │       │   │   ├── security/
│   │       │   │   │   └── SandboxPermissionBroker.kt     # Cross-plugin LLM access control & token enforcement
│   │       │   │   ├── services/
│   │       │   │   │   ├── PercipienceExecutionService.kt # Non-blocking CLI process execution
│   │       │   │   │   └── PercipienceProjectService.kt   # State synchronization background service
│   │       │   │   ├── statusbar/
│   │       │   │   │   └── PercipienceStatusBarWidgetFactory.kt # Dynamic tier-aware status bar widget
│   │       │   │   ├── terminal/
│   │       │   │   │   └── PercipienceTerminalCustomizer.kt # Terminal agent AST compression & shell hooks
│   │       │   │   └── toolwindow/
│   │       │   │       └── PercipienceToolWindowFactory.kt # Dynamic tier-aware 6-tab Control Plane UI
│   │       │   └── resources/
│   │       │       ├── META-INF/
│   │       │       │   └── plugin.xml                         # Plugin descriptor & extension points
│   │       │       └── percipience/                           # Embedded offline platform runtime
│   │       └── src/test/kotlin/                               # LightPlatformTestCase & fixtures
│   └── templates/bridge/
│       ├── mock_jetbrains_daemon.py                           # Loopback JSON-RPC server simulating IntelliJ actions
│       └── virtual_psi_fixture.py                             # Synthetic PSI tree generator for offline CI validation
└── user/
    ├── inputs/
    │   ├── intellij_plugin_config.yaml                        # Target IDE versions & feature flags
    │   └── ui_theme_tokens.json                               # Dark/Light theme colors and typography
    ├── hitl/
    │   └── poisoning_quarantine.md                            # Quarantined plugin bytecode or invalid PSI transforms
    └── outputs/
        ├── dashboard/index.html                               # JCEF rendered living dashboard & Merkle state viewer
        ├── intellij_plugin_metrics.json                       # PSI parse throughput, EDT frame time, token savings
        └── context_maturity_report.md                         # 6-dimensional context scorecard with IDE plugin audit
```

---\n
## 2. Wire Contracts & Safety Invariants (`.nb/context/contracts/`, `.nb/context/rules/`)

### 2.1. IntelliJ Plugin Manifest Contract (`.nb/context/contracts/intellij_plugin_manifest_contract.json`)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "IntelliJPluginManifestContract",
  "type": "object",
  "required": ["plugin_id", "plugin_name", "version", "since_build", "dependencies", "extension_points"],
  "properties": {
    "plugin_id": { "type": "string", "pattern": "^[a-z0-9.]+$", "example": "com.neutronbinary.percipience" },
    "plugin_name": { "type": "string", "example": "Percipience Context Engineering OS" },
    "version": { "type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$" },
    "since_build": { "type": "string", "example": "241.0" },
    "until_build": { "type": "string", "example": "262.*" },
    "dependencies": {
      "type": "array",
      "items": { "type": "string" },
      "uniqueItems": true
    },
    "extension_points": {
      "type": "object",
      "required": ["toolWindow", "externalAnnotator", "inspectionTool"],
      "properties": {
        "toolWindow": { "type": "string" },
        "externalAnnotator": { "type": "string" },
        "inspectionTool": { "type": "string" }
      }
    }
  }
}
```

### 2.2. PSI AST Bridge Contract (`.nb/context/contracts/psi_ast_bridge_contract.yaml`)
```yaml
schema_version: "2.0.0"
contract_id: "psi_ast_bridge_contract"
supported_languages:
  - id: "python"
    psi_root: "com.jetbrains.python.psi.PyFile"
    prunable_elements: ["PyFunction", "PyClass", "PyDocStringExpression"]
  - id: "kotlin"
    psi_root: "org.jetbrains.kotlin.psi.KtFile"
    prunable_elements: ["KtNamedFunction", "KtClass", "KtProperty"]
  - id: "java"
    psi_root: "com.intellij.psi.PsiJavaFile"
    prunable_elements: ["PsiMethod", "PsiClass"]
performance_targets:
  max_psi_traversal_ms: 35
  max_memory_per_file_kb: 512
  min_token_reduction_ratio: 0.60
```

### 2.3. JetBrains Platform Threading & PSI Invariants (`.nb/context/rules/jetbrains_platform_threading_rules.md`)
```markdown
# JetBrains Platform Threading & PSI Invariants

1. **Absolute Event Dispatch Thread (EDT) Freedom**:
   - Network requests, JSON-RPC IPC calls, and heavy AST token calculations MUST NEVER run on the EDT.
   - All external execution must use Kotlin Coroutines (`withContext(Dispatchers.Default)`) or `ProgressManager.getInstance().run(Task.Backgroundable)`.
   - UI updates to ToolWindows and editor popups MUST be dispatched via `Dispatchers.EDT` or `ApplicationManager.getApplication().invokeLater()`.

2. **Read/Write Lock Synchronization**:
   - All PSI tree reads must occur inside a read action (`runReadAction`).
   - All modifications to documents or workspace files must execute inside a write action (`runWriteAction`) within a Command (`CommandProcessor.getInstance().executeCommand()`).
   - If the IDE is in "Dumb Mode" (indexing), PSI resolution features must either defer execution via `DumbService.getInstance(project).runWhenSmart()` or display informative placeholder badges.

3. **JCEF Webview Security Constraints**:
   - Java Chromium Embedded Framework (JCEF) browser instances hosting the Percipience Dashboard must enforce strict Content-Security-Policy (CSP) with `script-src 'self'`.
   - Communication between JCEF JavaScript and the Kotlin plugin layer must use asynchronous query handlers (`CefMessageRouterHandlerAdapter`) with verified request nonce validation.
```

---\n
## 3. Specialized Domain Subagents & Workflows (`.nb/agentic/custom/`)

### 3.1. `.nb/agentic/custom/agents/agent_jetbrains_plugin_architect.yaml`
- **Role**: JetBrains Platform SDK, Gradle IntelliJ Plugin, PSI Navigation & ToolWindow Architecture Auditor
- **Model Tier**: `Tier_A` (`claude-3-7-sonnet / pro`, `gemini-2.0-pro`, `gpt-4o`)
- **Sandboxed Worktree**: `.nb/workspaces/wt_jetbrains_arch_01`
- **Module Scope**: `workplace/modules/mod_intellij_plugin/`

### 3.2. `.nb/agentic/custom/agents/agent_psi_ast_bridge_specialist.yaml`
- **Role**: PSI Visitor, AST Token Compression & Wire Contract Inspection Annotator
- **Model Tier**: `Tier_B` (`claude-3-5-haiku / flash`, `gemini-2.0-flash`, `gpt-4o-mini`)
- **Sandboxed Worktree**: `.nb/workspaces/wt_psi_bridge_01`
- **Module Scope**: `workplace/modules/mod_intellij_plugin/src/main/kotlin/com/neutronbinary/percipience/psi/`

### 3.3. `.nb/agentic/custom/agents/agent_intellij_ui_ux_engineer.yaml`
- **Role**: Swing/JCEF ToolWindow, Gutter LineMarkers, Context Actions & Quick-Fixes
- **Model Tier**: `Tier_A` (`claude-3-7-sonnet / pro`, `gemini-2.0-pro`, `gpt-4o`)
- **Sandboxed Worktree**: `.nb/workspaces/wt_intellij_ui_01`
- **Module Scope**: `workplace/modules/mod_intellij_plugin/src/main/kotlin/com/neutronbinary/percipience/toolwindow/`

---\n
## 4. Virtual End-to-End Emulation Bridge & UI Action Architecture

```mermaid
sequenceDiagram
  autonumber
  participant Dev as Developer in PyCharm
  participant Editor as IntelliJ Editor (PSI Engine)
  participant Bridge as PSI AST Bridge (com.neutronbinary.percipience.psi)
  participant Daemon as Percipience Daemon (bin/percipience)
  participant ToolWin as Percipience ToolWindow (JCEF / Swing)
  participant Ledger as Merkle Chain (.nb/context/ledger)

  Note over Dev,Editor: 1. Code Edit & Real-Time PSI Contract Inspection
  Dev->>Editor: Open and edit workplace/modules/mod_service/src/service.py
  Editor->>Bridge: Trigger LocalInspectionTool on PSI Tree (PyFunction)
  Bridge->>Bridge: Verify against .nb/context/contracts/service_contract.yaml
  Bridge-->>Editor: Display Gutter Marker & Inline Diagnostic: [✔ CONTRACT VALID]

  Note over Dev,Daemon: 2. AST Token Compression Preview & Pre-Prompt Pruning
  Dev->>Editor: Click Context Action: "Inspect Percipience AST Token Pruning"
  Editor->>Bridge: Extract PSI Class & Function Signatures (Strip bodies)
  Bridge->>Bridge: Compute Token Metrics (Raw: 1,840 tokens -> Pruned: 412 tokens, 77.6% savings)
  Bridge-->>ToolWin: Update Token FinOps Widget & AST Difference Viewer

  Note over Dev,ToolWin: 3. Autonomous Workflow Execution & ToolWindow Feedback
  Dev->>ToolWin: Trigger Action: "Run Layered Verification Workflow"
  ToolWin->>Daemon: Dispatch JSON-RPC: execute_workflow("wf_intellij_pycharm_plugin_delivery")
  Daemon->>Daemon: Execute DAG steps via background Kotlin Coroutine
  Daemon->>Ledger: Append Merkle Block RP_INTELLIJ_PLUGIN_001
  Daemon-->>ToolWin: Stream execution events (100% Complete, [✔ HEALTHY])
  ToolWin-->>Dev: Refresh live Mermaid DAG and display green status notification
```

### 4.7. Tier-Permission-Aware Control Plane & Dynamic Action Matrix

The Percipience IntelliJ / PyCharm plugin dynamically resolves the user's active billing tier and selectively displays, enables, and manages Control Plane buttons:

```mermaid
graph TD
  Resolver["WorkspaceLedgerReader.resolveTier()"]
  
  subgraph Tier_Entitlements["Dynamic Tier Permissions"]
    FreeTier["plan_free (Community)"]
    TeamTier["plan_team"]
    BizTier["plan_business"]
    EntTier["plan_enterprise"]
  end

  Resolver --> FreeTier
  Resolver --> TeamTier
  Resolver --> BizTier
  Resolver --> EntTier

  subgraph Free_Buttons["Core Gatekeeper Actions (All Tiers)"]
    BtnBoot["🚀 Bootstrap / Verify Workspace"]
    BtnGate["🚦 Run PR Gatekeeper"]
    BtnAudit["🛡️ Verify Merkle Chain"]
    BtnCicd["▶ Autonomous CI/CD Pipeline"]
    BtnVal["🔍 Validate Layered Context"]
    BtnTok["⚡ Token Savings Summary"]
  end

  subgraph Team_Buttons["Team Tier Actions [Team+]"]
    BtnWt["🌿 Manage Worktrees"]
    BtnAgent["🤖 Specialist Agents Registry"]
    BtnDriftChk["🔄 Anti-Drift Parity Check"]
  end

  subgraph Biz_Buttons["Business Tier Actions [Business+]"]
    BtnPack["📦 Package Sealed NBPack"]
    BtnProv["🌐 Gateway Provisioner"]
    BtnDriftRep["🧠 Cognitive Parity Report"]
  end

  subgraph Ent_Buttons["Enterprise Dedicated Actions [Enterprise]"]
    BtnSwarm["🐝 Swarm Triad Orchestrator"]
    BtnVpc["🔒 Private VPC Air-Gapped Sync"]
    BtnWorm["📜 Immutable WORM Cloud Egress"]
  end

  FreeTier --> Free_Buttons
  TeamTier --> Free_Buttons & Team_Buttons
  BizTier --> Free_Buttons & Team_Buttons & Biz_Buttons
  EntTier --> Free_Buttons & Team_Buttons & Biz_Buttons & Ent_Buttons
```

#### Detailed Action Matrix:
| Control Plane Button | CLI Subcommand | Free Community | Team Tier | Business Tier | Enterprise Dedicated |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Bootstrap Workspace** | `bootstrap` | ✅ | ✅ | ✅ | ✅ |
| **Run PR Gatekeeper** | `gate` | ✅ | ✅ | ✅ | ✅ |
| **Verify Merkle Chain** | `audit --enforce-merkle-chain` | ✅ | ✅ | ✅ | ✅ |
| **Autonomous CI/CD** | `cicd run` | ✅ | ✅ | ✅ | ✅ |
| **Validate Layered Context** | `validate --layered` | ✅ | ✅ | ✅ | ✅ |
| **Token Savings Summary** | `tokens summary` | ✅ | ✅ | ✅ | ✅ |
| **Manage Worktrees** | `worktree list` | ❌ | ✅ | ✅ | ✅ |
| **Specialist Agents Registry**| `agent list` | ❌ | ✅ | ✅ | ✅ |
| **Anti-Drift Parity Check** | `drift check` | ❌ | ✅ | ✅ | ✅ |
| **Package Sealed NBPack** | `layer pack` | ❌ | ❌ | ✅ | ✅ |
| **Gateway Provisioner** | `provision --target all` | ❌ | ❌ | ✅ | ✅ |
| **Cognitive Parity Report** | `drift report` | ❌ | ❌ | ✅ | ✅ |
| **Swarm Triad Orchestrator** | `swarm audit` | ❌ | ❌ | ❌ | ✅ |
| **Private VPC Enclave Sync**| `repo status` | ❌ | ❌ | ❌ | ✅ |
| **Immutable WORM Egress** | `egress list` | ❌ | ❌ | ❌ | ✅ |

---\n
## 5. Domain-Specific Surgical Rollback & Poisoning Defense

```mermaid
sequenceDiagram
  autonumber
  participant Agent as agent_jetbrains_plugin_architect
  participant WT as Ephemeral Worktree (.nb/workspaces/mod_intellij_plugin)
  participant Gate as Percipience Gatekeeper (Stage 3 & 4)
  participant Sentinel as Poisoning & Threading Sentinel
  participant Ledger as Context Ledger (.nb/context/ledger)

  Agent->>WT: Introduce synchronous network call on UI Thread inside ToolWindowFactory
  WT->>Gate: Submit PR increment
  Gate->>Sentinel: Run EDT Threading Linter & Thread Sanity Oracle
  Sentinel-->>Gate: DETECTED - EDTBlockingViolation: Network I/O detected on Event Dispatch Thread!
  Gate->>Sentinel: Trigger Surgical Rollback for mod_intellij_plugin
  Sentinel->>WT: Reset mod_intellij_plugin to RP_INTELLIJ_PREV
  Sentinel->>Ledger: Record quarantine event in user/hitl/poisoning_quarantine.md
  Sentinel->>Ledger: Seal Merkle Block RP_POISON_ROLLBACK_INTELLIJ
  Gate-->>Agent: Reject PR with stack trace and mandate Kotlin Coroutine background dispatch
```

---\n
## 6. Encrypted Packaging, Layer Consumption & Separate Tier Bundles

### 6.1. Compiling the Sealed Domain Bundle
```bash
./.nb/bin/percipience layer pack \
  --plan .nb/plan/l1/intellij-pycharm-plugin/concise.md \
  --output .nb/bundles/intellij_pycharm_plugin_domain.nbpack \
  --include-spaces .nb/context/contracts,.nb/context/rules,.nb/agentic/custom
```

### 6.2. Consuming the Encrypted Bundle in Target Repository
```bash
./.nb/bin/percipience layer apply \
  --pack .nb/bundles/intellij_pycharm_plugin_domain.nbpack \
  --in-memory-only \
  --mode multi_module
```

### 6.3. Bundled Free Tier Platform Core Assets & Autonomous Bootstrapping
The IntelliJ/PyCharm plugin ZIP distribution (`.nb/bundles/percipience-intellij-plugin-1.0.0.zip`) packages the entire offline platform engine within the plugin JAR (`percipience/core/` containing all 38 Python modules + `__init__.py`). When initialized via `BootstrapWorkspaceAction` or the interactive startup prompt (`PercipienceProjectStartupActivity`), `WorkspaceBootstrapper.kt` extracts:
1. `percipience/bin/percipience` with Unix `0755` executable permissions.
2. `percipience/core/*.py` into `.nb/core/` (AST optimizer, Merkle engine, CI/CD, token tracker, etc.).
3. `percipience/config/` (`billing_plans.yaml`, `token_compression_rules.yaml`).
4. `percipience/workflows/` (`basic_autonomous_cicd.yaml`).
5. `percipience/plan/` (`claude-context-engineering-parent-master-free_plan.md`).
6. Genesis Merkle state ledger (`.nb/context/ledger/context_ledger.yaml`).

### 6.4. Separate Multi-Tier Plugin Bundles for Permission Verification
To test and verify dynamic permission enforcement across all tiers in staging and automated test harnesses, the packager (`package_plugin.py`) generates dedicated tier-aware plugin distributions in `.nb/bundles/`:
- `percipience-intellij-plugin-free-1.0.0.zip`: Community edition pre-provisioned with `plan_free` license and gatekeeper-only surface.
- `percipience-intellij-plugin-team-1.0.0.zip`: Team edition with worktree and custom agent provisioning.
- `percipience-intellij-plugin-business-1.0.0.zip`: Business edition with full platform tools, NBPack encrypted packaging, and multi-tenant provisioner.
- `percipience-intellij-plugin-enterprise-1.0.0.zip`: Enterprise edition with private VPC isolation, swarm triad orchestrator, and WORM cloud egress.
- `percipience-intellij-plugin-1.0.0.zip`: Universal distribution defaulting to active workspace license.
