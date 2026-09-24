# Percipience Context Engineering OS — IntelliJ IDEA & PyCharm Plugin Guide

The **Percipience Context Engineering OS** plugin bridges JetBrains IDEs (IntelliJ IDEA Ultimate/Community and PyCharm Professional/Community) directly with the Percipience multi-agent autonomous SDLC, AST token compression engine, cryptographic Merkle ledger, cross-plugin sandbox permission broker, and dynamic tier-aware Control Plane.

---

## 🌟 1. Core Capabilities & Tier Governance

### 1.1 Automated Workspace Bootstrapping
- **Zero-Click Onboarding**: Automatically detects unconfigured project workspaces on startup.
- **Scaffolding & Core Engine Hydration**: Automatically deploys the full suite of 38 essential platform core engines (`.nb/core/*.py`), the canonical gatekeeper CLI (`.nb/bin/percipience` with executable `0755` permissions), the Quad-Space directory structure (`.nb/`, `workplace/`, `user/`), the Master Plan, default token compression rules, basic CI/CD pipeline, and genesis Merkle state block (`RP_GENESIS_000`).
- **Complete Offline Autonomy**: Because the plugin JAR embeds all platform core files (`percipience/core/`), newly created projects operate fully offline with zero external network downloads.
- **Manual Trigger**: Available via **Tools → Percipience OS → Bootstrap Workspace Setup** or the ToolWindow button.

### 1.2 Dynamic Tier-Aware Control Plane
The Control Plane panel dynamically detects your active billing tier (`tenant_license.json`, `.percipience_license.json`, `context_ledger.yaml`, or `PERCIPIENCE_PLAN` environment variable) and configures available actions:

| Action Button | CLI Subcommand | Free Community | Team Tier | Business Tier | Enterprise Dedicated |
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

### 1.3 Real-Time PSI AST Token Pruning & Local Agent Optimization
- **Native Program Structure Interface (PSI) Integration**: Traverses the JetBrains PSI in-memory AST in **under 35ms** without writing to disk.
- **Skeletonization**: Strips implementation logic (function/method bodies) while preserving full type signatures, docstrings, imports, class hierarchies, and type hints.
- **Supported Languages**: Python (`PyFile`), Kotlin (`KtFile`), Java (`PsiJavaFile`), TypeScript, and JavaScript.

### 1.4 Cross-Plugin Sandbox Permission Broker
- **Sandboxed LLM Governance**: Governs source code access when third-party AI plugins (e.g. JetBrains AI Assistant, GitHub Copilot, Continue, Cody) execute in separate sandboxes or classloaders.
- **Token Pruning by Default (`READ_PRUNED_AST`)**: Automatically intercepts cross-plugin source read requests and returns token-pruned AST skeletons, preventing token exhaustion and exfiltration of internal implementations.
- **Merkle Ledger WORM Protection**: Modifications to `.nb/context/ledger/` and invariant contracts are strictly blocked (`DENIED`).

---

## 🛠️ 2. User Interface & Controls

### Tool Window ("Percipience OS")
Located on the right-hand sidebar of the IDE:
- **Tab 1: Control Plane**: Live status, tier quota badge, Merkle chain height, token compression metrics, dynamic tier action buttons, and CI/CD workflow launcher.
- **Tab 2: Sandbox Permissions**: Registry of sandboxed LLM plugins, active read/write policies, and token pruning enforcement status.
- **Tab 3: Capabilities**: In-depth documentation of PSI AST traversal, Merkle security, and tier tooling isolation.
- **Tab 4: Agents & Flows**: Registry of active specialist agents and execution pipelines for the active tier.
- **Tab 5: Terminal Agents & FinOps**: Interactive integration with Claude Code, Gemini CLI, and Aider with AST context generation.
- **Tab 6: User Guide**: Quick commands, configuration tips, and shortcuts.

### Status Bar Widget
Located on the bottom right of the IDE status bar:
- Displays `⚡ Percipience (<Tier>): <Reduction>% Saved | 🛡️ Merkle: #<Height> OK`.
- Click on the status widget to open a quick action popup tailored to your active tier.

---

## 📦 3. Separate Tier Bundles for Permission Testing

Dedicated plugin distributions are available in `.nb/bundles/` to verify behavior across each tier:
- `percipience-intellij-plugin-free-1.0.0.zip`: Community edition with gatekeeper-only surface.
- `percipience-intellij-plugin-team-1.0.0.zip`: Team edition with worktrees and custom agents.
- `percipience-intellij-plugin-business-1.0.0.zip`: Business edition with sealed `.nbpack` compiler and gateway.
- `percipience-intellij-plugin-enterprise-1.0.0.zip`: Enterprise edition with full private VPC and swarm orchestrator.
- `percipience-intellij-plugin-1.0.0.zip`: Universal distribution defaulting to workspace license.

### Installation for Local Testing
1. Open **Settings / Preferences** in IntelliJ IDEA or PyCharm (<kbd>Cmd</kbd> + <kbd>,</kbd> on macOS / <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>S</kbd> on Windows/Linux).
2. Go to **Plugins** $\rightarrow$ Click ⚙️ (**Gear icon**) $\rightarrow$ **Install Plugin from Disk...**.
3. Select any desired tier bundle from `.nb/bundles/`.
4. Restart the IDE to activate.
