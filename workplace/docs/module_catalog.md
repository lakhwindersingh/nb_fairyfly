# Poly-Module Interface Catalog & Responsibilities

> **Autonomously Synchronized**: 2026-09-19T16:00:00+00:00  
> **Engine**: `agent_living_doc_architect` (CAP-21)  
> **Diagram Validation**: ✅ Valid Mermaid

## Module Dependency Graph
```mermaid
graph TD
  M_IntelliJ["mod_intellij_plugin<br/>(IntelliJ ToolWindow, Status Bar, PSI AST Bridge)"]
  M_VSCode["mod_vscode_extension<br/>(VSCode Status Bar, LSP IPC, Webview)"]
  M_Onboarding["mod_tenant_onboarding<br/>(Tenant Provisioning, BYOR Wizard, Auth)"]
  M_Billing["mod_billing_metering<br/>(Usage Aggregator, 15% Rev-Share, Stripe)"]
  M_Observability["mod_observability_usage<br/>(Telemetry Stream, Merkle Explorer, Leases)"]
  M_Bridge["mod_shared_infra_bridge<br/>(Mock Service Daemon, Loopback Socket)"]
  M_Marketing["mod_portal_marketing / portal.server<br/>(Tier Matrix, Capabilities Catalog, ROI Calculator)"]

  M_IntelliJ -->|"Read Metrics & Enforce Broker"| M_Observability
  M_VSCode -->|"LSP IPC Telemetry"| M_Observability
  M_Onboarding -->|"Emit Provisioned Event"| M_Billing
  M_Billing -->|"Stream FinOps Metrics"| M_Observability
  M_Bridge -->|"Synthetic Telemetry"| M_Observability
  M_Marketing -->|"Showcase Live Architecture"| M_Observability
```

## Public Interface Catalog
| Module Name | Responsibilities | Public Interfaces / Symbols | Wire Contract Binding |
| :--- | :--- | :--- | :--- |
| `mod_intellij_plugin` | Native Kotlin IntelliJ/PyCharm plugin; Swing-safe ToolWindow (5 tabs), status bar widget, PSI AST traversal (&lt;35ms), `SandboxPermissionBroker`, `WorkspaceBootstrapper` | `PercipienceToolWindowFactory`, `PercipienceStatusBarWidgetFactory`, `WorkspaceBootstrapper`, `SandboxPermissionBroker`, `PsiAstBridge` | `.nb/context/contracts/sandbox_permission_contract.json` |
| `mod_vscode_extension` | TypeScript VSCode extension; status bar metrics, virtual LSP IPC host, webview RPC bridge | `activate()`, `statusBarManager`, `MockVsCodeIpcHost`, `VirtualLspFixture` | `.nb/context/contracts/sandbox_permission_contract.json` |
| `mod_tenant_onboarding` | Multi-tenant organization provisioning, BYOR VCS binding (GitHub/GitLab/Bitbucket), OAuth2 auth | `provisionTenant()`, `generateByorManifest()`, `authenticateRequest()` | `context/contracts/onboarding_contract.yaml` |
| `mod_billing_metering` | Real-time AST token savings tracking, gross savings conversion ($0.003/1K tokens), 15% performance fee calculation | `aggregateTenantUsage()`, `calculatePerformanceFee()`, `createStripeInvoice()` | `context/contracts/billing_meter_contract.yaml` |
| `mod_observability_usage` | Live Merkle block DAG explorer, ephemeral worktree lease monitor, append-only quarantine console, OpenTelemetry GenAI W3C traces | `streamTelemetry()`, `getMerkleNode()`, `listActiveLeases()`, `getQuarantineEntries()` | `context/contracts/observability_contract.yaml` |
| `mod_shared_infra_bridge` | Zero-dependency virtual service loopback bridge, async socket emulator, synthetic telemetry stream | `initBridge()`, `dispatchMockRequest()`, `simulateTelemetryEvent()` | `context/contracts/service_contract.yaml` |
| `mod_portal_marketing` / `portal.server` | Enterprise interactive capabilities catalog, Plan Tier Matrix & Boundary Ceilings (Section 2), 4-way competitive matrix, real-time ROI calculator, Context Gateway, Secure Client Space | `renderCapabilities()`, `calculateFinOpsROI()`, `renderCompetitiveMatrix()`, `calculateCeilings()` | None (Frontend Client & Gateway View) |
