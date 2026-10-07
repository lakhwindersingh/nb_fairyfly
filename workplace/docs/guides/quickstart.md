# Percipience Quickstart Guide

Get up and running with **Neutron Binary Percipience** in less than 90 seconds using your favorite IDE (IntelliJ IDEA / PyCharm / VSCode), the native CLI control plane, or the isolated local Docker testing harness.

---

## 1. Local Docker Testing Harness (Recommended for Hermetic Validation)

Percipience provides an isolated, multi-container Docker testing harness in [`workplace/infra/docker/`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/infra/docker/) that spins up the SaaS Portal, the Tree-Sitter AST parsing daemon, and hermetic test runners with zero host pollution:

```bash
# 1. Inspect environment and container readiness
./workplace/infra/docker/docker-test.sh status

# 2. Build images and start services in the background (Portal on 3000, Tree-Sitter Daemon on 8585)
./workplace/infra/docker/docker-test.sh up

# 3. Run hermetic health check and unit/integration tests
./workplace/infra/docker/docker-test.sh test

# 4. Execute the complete 7-stage PR Gatekeeper inside the test runner container
./workplace/infra/docker/docker-test.sh gate

# 5. Shut down container topology cleanly
./workplace/infra/docker/docker-test.sh down
```

For complete details on container architecture, IPC endpoints, and volume mounts, see the [Docker Testing Guide](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/docs/guides/docker_testing_guide.md).

---

## 2. IDE Plugin Quickstart (Zero-Click Auto-Bootstrapping)

### IntelliJ IDEA / PyCharm Plugin
1. Install the plugin from `.nb/bundles/percipience-intellij-plugin-1.0.0.zip` via **Settings &rarr; Plugins &rarr; Install Plugin from Disk...**
2. Open the **Percipience Context OS** ToolWindow on the right or bottom sidebar.
3. Click **"🚀 Bootstrap / Verify Free Workspace Setup"** in the **Control Plane** tab.
4. The plugin automatically scaffolds `.nb/`, verifies the cryptographic Merkle chain, configures `basic_autonomous_cicd.yaml`, and activates the `SandboxPermissionBroker`.
5. Press <kbd>Shift</kbd> + <kbd>Alt</kbd> + <kbd>P</kbd> on any open file to inspect real-time AST token pruning and compression metrics.
6. Check your status bar on the bottom-right for live token savings and Merkle block height.

### VSCode Extension
1. Install the extension from `.nb/bundles/percipience-vscode-extension-1.0.0.vsix` via **Extensions &rarr; Install from VSIX...**
2. The extension automatically connects to the Percipience Language Server and starts tracking active token savings and Merkle seals in the bottom status bar.

---

## 3. CLI Control Plane Quickstart

### Installation & Initialization
```bash
# Verify CLI execution
chmod +x .nb/bin/percipience
./.nb/bin/percipience --help
```

### Bootstrapping Your Repository (Quad-Space Architecture)
```bash
# Initialize workspace into Quad-Space structure with Master Plan:
./.nb/bin/percipience init --mode multi_module --parent-plan .nb/plan/master/parent-master-free-plan/detailed.md
```

### Auditing Context Health & Merkle Chain
```bash
./.nb/bin/percipience audit --enforce-merkle-chain --min-maturity 0.85
```

### Running Autonomous 7-Stage CI/CD Gatekeeper
```bash
# Execute PR gatekeeper, verify AST signatures, and seal block into WORM vault:
./.nb/bin/percipience gate
```

---

## 4. Launching the Observability & Management Portal

```bash
# Start the local SaaS Portal server on http://localhost:3000
python3 workplace/portal/server.py
```

Open [http://localhost:3000](http://localhost:3000) to inspect:
- **📊 Plan Matrix & Ceilings (`#tier-matrix`)**: Full 4-tier matrix and live boundary ceiling simulator.
- **⚡ SDLC Capabilities (`#capabilities`)**: Deep dive into the 47 architectural engines and capabilities.
- **🛡️ Multi-Tenant Governance (`#governance`)**: Fine-grained tenant policies, KMS isolation, and kill switches.
- **💼 Commercial Provisioner (`#commercial-provisioner`)**: Tier licensing, dynamic module slicing, and hardware enclaves.
- **🤖 Swarm Governance (`#swarm-governance`)**: Dynamic DAG orchestrator, 5-pillar reflexion loop, 3-tier memory engine, and CBAC tokens.
- **📈 Observability (`#observability`)**: OpenTelemetry GenAI traces, 5D G-Eval radar, and token burn charts.
- **🔒 Client Space (`#client`)**: Authenticated tenant portal with SEC 17a-4 / FINRA WORM storage audits and sub-1.2s surgical rollback.
