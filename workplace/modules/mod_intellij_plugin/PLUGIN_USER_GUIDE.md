# Percipience Context Engineering OS — IntelliJ IDEA & PyCharm Plugin Guide

The **Percipience Context Engineering OS** plugin bridges JetBrains IDEs (IntelliJ IDEA Ultimate/Community and PyCharm Professional/Community) directly with the Percipience multi-agent autonomous SDLC, AST token compression engine, cryptographic Merkle ledger, and cross-plugin sandbox permission broker.

---

## 🌟 1. Core Capabilities Overview

### 1.1 Automated Free Workspace Bootstrapping
- **Zero-Click Onboarding**: Automatically detects unconfigured project workspaces on startup.
- **Scaffolding & Core Engine Hydration**: Automatically deploys the full suite of 38 essential platform core engines (`.nb/core/*.py`), the canonical gatekeeper CLI (`.nb/bin/percipience` with executable `0755` permissions), the Quad-Space directory structure (`.nb/`, `workplace/`, `user/`), the Free Community Master Plan (`.nb/plan/claude-context-engineering-parent-master-free_plan.md`), default token compression rules, basic CI/CD pipeline, and genesis Merkle state block (`RP_GENESIS_000`).
- **Complete Offline Autonomy**: Because the plugin JAR embeds all platform core files (`percipience/core/`), newly created projects operate fully offline with zero external network downloads.
- **Manual Trigger**: Available via **Tools → Percipience OS → Bootstrap Free Workspace Setup** or the ToolWindow button.

### 1.2 Real-Time PSI AST Token Pruning & Local Agent Optimization
- **Native Program Structure Interface (PSI) Integration**: Traverses the JetBrains PSI in-memory AST in **under 35ms** without writing to disk.
- **Skeletonization**: Strips implementation logic (function/method bodies) while preserving full type signatures, docstrings, imports, class hierarchies, and type hints.
- **Local Agent Integration (`LocalAgentTokenOptimizer`)**: Enforces 15/25/35/10/15 attention budgeting and static prompt prefix pinning (`<!-- STATIC_PREFIX_START -->`) for local agents, guaranteeing **60% to 80% token savings**.
- **Supported Languages**: Python (`PyFile`), Kotlin (`KtFile`), Java (`PsiJavaFile`), TypeScript, and JavaScript.

### 1.3 Cross-Plugin Sandbox Permission Broker
- **Sandboxed LLM Governance**: Governs source code access when third-party AI plugins (e.g. JetBrains AI Assistant, GitHub Copilot, Continue, Cody) execute in separate sandboxes or classloaders.
- **Token Pruning by Default (`READ_PRUNED_AST`)**: Automatically intercepts cross-plugin source read requests and returns token-pruned AST skeletons, preventing token exhaustion and exfiltration of internal implementations.
- **Merkle Ledger WORM Protection**: Modifications to `.nb/context/ledger/` and invariant contracts are strictly blocked (`DENIED`).

### 1.4 Cryptographic Merkle Ledger & Audit Compliance
- **SHA-256 Hash Chain**: Every file modification, prompt dispatch, contract verification, and agent run is appended to an immutable Merkle DAG ledger (`.nb/context/ledger/context_ledger.yaml`).
- **Recovery Points**: Instant rollback and atomic recovery (e.g., `RP_GENESIS_000`, `RP_INTELLIJ_PLUGIN_001`).
- **Poisoning Defense**: Continuous secret scanning and prompt injection detection with one-click quarantine and surgical rollback.

### 1.5 Basic Autonomous CI/CD Pipeline
- **Out-of-the-Box Pipeline (`basic_autonomous_cicd.yaml`)**:
  1. *Self-Sustaining Hygiene*: Purges temporary scratch diffs and validates Merkle chain continuity.
  2. *AST Token Reduction*: Pre-processes source code and logs token compression metrics.
  3. *Contract & Test Gate*: Verifies wire contracts and runs local tests.
  4. *Bounded Auto-Repair & Merkle Seal*: Single-attempt bounded auto-repair and SHA-256 block sealing.

---

## 🛠️ 2. User Interface & Controls

### Tool Window ("Percipience OS")
Located on the right-hand sidebar of the IDE:
- **Tab 1: Control Plane**: Live status, Merkle chain height, token compression metrics, workspace bootstrapping, and CI/CD workflow launcher.
- **Tab 2: Sandbox Permissions**: Registry of sandboxed LLM plugins, active read/write policies, and token pruning enforcement status.
- **Tab 3: Capabilities**: In-depth documentation of PSI AST traversal, Merkle security, and autonomous CI/CD.
- **Tab 4: Agents & Flows**: Registry of active specialist agents and execution pipelines.
- **Tab 5: User Guide**: Quick commands, configuration tips, and shortcuts.

### Editor Context Menu & Shortcuts
- **Shortcut**: <kbd>Shift</kbd> + <kbd>Alt</kbd> + <kbd>P</kbd> — Inspect AST Token Pruning for the active file.
- **Context Menu**: Right-click in the editor $\rightarrow$ **"Inspect Percipience AST Token Pruning"**.
- **Tools Menu**:
  - **Tools → Bootstrap Percipience Free Workspace**
  - **Tools → Inspect Sandbox & LLM Permissions**

---

## ⚙️ 3. Configuration

Configure your plugin behavior in `user/inputs/intellij_plugin_config.yaml`:

```yaml
ide_target: "intellij_pycharm"
supported_editions:
  - "PyCharm Professional"
  - "PyCharm Community"
  - "IntelliJ IDEA Ultimate"
  - "IntelliJ IDEA Community"
since_build: "241.0"
until_build: "262.*"
daemon_endpoint: "http://127.0.0.1:8585"
features:
  psi_ast_pruning_preview: true
  live_contract_annotator: true
  jcef_control_plane: true
  auto_bootstrap_free_workspace: true
  sandbox_permission_broker: true
  enforce_token_pruning_for_sandboxed_llms: true
sandbox_policies:
  default_read_level: "READ_PRUNED_AST"
  target_token_reduction_pct: 70.0
  protected_paths:
    - ".nb/context/ledger/"
    - ".nb/context/invariants/"
```

---

## 📦 4. Installation for Local Testing

1. Open **Settings / Preferences** in IntelliJ IDEA or PyCharm (<kbd>Cmd</kbd> + <kbd>,</kbd> on macOS / <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>S</kbd> on Windows/Linux).
2. Go to **Plugins** $\rightarrow$ Click ⚙️ (**Gear icon**) $\rightarrow$ **Install Plugin from Disk...**.
3. Select `.nb/bundles/percipience-intellij-plugin-1.0.0.zip`.
4. Restart the IDE to activate.
