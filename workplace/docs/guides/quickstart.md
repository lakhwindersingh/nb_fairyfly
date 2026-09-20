# Percipience Quickstart Guide

Get up and running with Percipience in less than 90 seconds using either your favorite IDE (IntelliJ IDEA / PyCharm / VSCode) or the CLI control plane.

---

## 1. IDE Plugin Quickstart (Zero-Click Auto-Bootstrapping)

### IntelliJ IDEA / PyCharm Plugin
1. Install the plugin from `.nb/bundles/percipience-intellij-plugin-1.0.0.zip` via **Settings &rarr; Plugins &rarr; Install Plugin from Disk...**
2. Open the **Percipience Context OS** ToolWindow on the right/bottom sidebar.
3. Click **"🚀 Bootstrap / Verify Free Workspace Setup"** in the **Control Plane** tab.
4. The plugin will automatically scaffold `.nb/`, verify the cryptographic Merkle chain, configure `basic_autonomous_cicd.yaml`, and activate the `SandboxPermissionBroker`.
5. Press <kbd>Shift</kbd> + <kbd>Alt</kbd> + <kbd>P</kbd> on any open file to inspect real-time AST token pruning and compression metrics.
6. Check your status bar on the bottom-right for live token savings and Merkle block height.

### VSCode Extension
1. Install the extension from `.nb/bundles/percipience-vscode-extension-1.0.0.vsix` via **Extensions &rarr; Install from VSIX...**
2. The extension automatically connects to the Percipience Language Server and starts tracking active token savings and Merkle seals in the bottom status bar.

---

## 2. CLI Control Plane Quickstart

### Installation & Initialization
```bash
# Verify CLI execution
chmod +x .nb/.nb/bin/percipience
./.nb/.nb/bin/percipience --help
```

### Bootstrapping Your Repository (Quad-Space Architecture)
```bash
# Initialize workspace into Quad-Space structure with Master Plan:
./.nb/.nb/bin/percipience init --mode multi_module --parent-plan .nb/plan/claude-context-engineering-parent-master-free_plan.md
```

### Auditing Context Health & Merkle Chain
```bash
./.nb/.nb/bin/percipience audit --enforce-merkle-chain --min-maturity 0.85
```

### Running Autonomous CI/CD Gates
```bash
# Execute PR gatekeeper and verify AST signatures:
./.nb/.nb/bin/percipience gate
```

---

## 3. Launching the Observability & Plan Matrix Portal
```bash
# Start the local SaaS Portal server on http://localhost:3000
python3 workplace/portal/server.py
```
Open [http://localhost:3000](http://localhost:3000) to inspect:
- **📊 Plan Matrix & Ceilings**: Full 4-tier matrix and live boundary ceiling simulator.
- **📈 Observability**: OpenTelemetry traces, 5D G-Eval radar, and token burn charts.
- **🔐 Client Space**: Authenticated tenant portal with surgical rollback controls.
