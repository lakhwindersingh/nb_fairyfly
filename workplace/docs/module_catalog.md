# Poly-Module Interface Catalog & Responsibilities

> **Autonomously Synchronized**: 2026-09-16T21:17:16.346275+00:00  
> **Engine**: `agent_living_doc_architect` (CAP-21)  
> **Diagram Validation**: ✅ Valid Mermaid

## Module Dependency Graph
```mermaid
graph TD
  M_Onboarding["mod_tenant_onboarding<br/>(Tenant Provisioning, BYOR Wizard, Auth)"]
  M_Billing["mod_billing_metering<br/>(Usage Aggregator, 15% Rev-Share, Stripe)"]
  M_Observability["mod_observability_usage<br/>(Telemetry Stream, Merkle Explorer, Leases)"]
  M_Bridge["mod_shared_infra_bridge<br/>(Mock Service Daemon, Loopback Socket)"]
  M_Marketing["mod_portal_marketing<br/>(Capabilities Catalog, ROI Calculator)"]

  M_Onboarding -->|"Emit Provisioned Event"| M_Billing
  M_Billing -->|"Stream FinOps Metrics"| M_Observability
  M_Bridge -->|"Synthetic Telemetry"| M_Observability
  M_Marketing -->|"Showcase Live Architecture"| M_Observability
```

## Public Interface Catalog
| Module Name | Responsibilities | Public Interfaces / Symbols | Wire Contract Binding |
| :--- | :--- | :--- | :--- |
| `mod_tenant_onboarding` | Multi-tenant organization provisioning, BYOR VCS binding (GitHub/GitLab/Bitbucket), OAuth2 auth | `provisionTenant()`, `generateByorManifest()`, `authenticateRequest()` | `context/contracts/onboarding_contract.yaml` |
| `mod_billing_metering` | Real-time AST token savings tracking, gross savings conversion ($0.003/1K tokens), 15% performance fee calculation | `aggregateTenantUsage()`, `calculatePerformanceFee()`, `createStripeInvoice()` | `context/contracts/billing_meter_contract.yaml` |
| `mod_observability_usage` | Live Merkle block DAG explorer, ephemeral worktree lease monitor, append-only quarantine console | `streamTelemetry()`, `getMerkleNode()`, `listActiveLeases()`, `getQuarantineEntries()` | `context/contracts/observability_contract.yaml` |
| `mod_shared_infra_bridge` | Zero-dependency virtual service loopback bridge, async socket emulator, synthetic telemetry stream | `initBridge()`, `dispatchMockRequest()`, `simulateTelemetryEvent()` | `context/contracts/service_contract.yaml` |
| `mod_portal_marketing` | Enterprise interactive capabilities catalog, 4-way competitive matrix, real-time ROI calculator | `renderCapabilities()`, `calculateFinOpsROI()`, `renderCompetitiveMatrix()` | None (Frontend Client View) |

