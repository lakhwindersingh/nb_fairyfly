---
plan_type: "layerable_domain_plan"
plan_id: "domain_saas_portal"
name: "Enterprise SaaS, Corporate Portals & Web Platform Ecosystem"
parent_master_plan: "master/parent-master-plan/concise.md"
tier_mapping:
  tier_2: "Enterprise Domain Rules & Wire Contracts (.nb/context/contracts/, .nb/context/rules/)"
  tier_3: "Specialist Subagents & Delivery Workflows (.nb/agentic/custom/agents/, .nb/agentic/custom/workflows/)"
model_tiering_policy:
  provider_agnostic: true
  tier_a_model: "claude-3-7-sonnet / pro"
  tier_b_model: "claude-3-5-haiku / flash"
---

# Layerable Context Engineering Plan: Enterprise SaaS & Corporate Portal Space (Concise Plan)

### Executive Overview & Domain Grounding

This document is a **Layerable Domain-Specific Context Engineering Plan** designed to overlay onto the generic **Parent Master Context Engineering Framework**. It injects web frontend systems, SaaS customer portals, billing gateways, commercial package provisioners, and real-time observability telemetry dashboards:

1. **Modern Frontend & Corporate Web Systems**: Next.js 14 App Router, dynamic MDX documentation, and Core Web Vitals ($< 1.2\text{s}$ LCP).
2. **Multi-Tenant SaaS Portals & Access Control**: PostgreSQL Row-Level Security (RLS), tenant isolation, and CMEK key brokerage.
3. **Commercial Package Provisioner & Licensing**: Automated tier packaging (`CommercialPackagerProvisioner`), cryptographic Ed25519 license minting, and cross-IDE/SaaS provisioning.
4. **Decoupled API Gateways & Billing Handlers**: Stripe billing webhooks and automated 15% token savings revenue-share calculation.
5. **Observability Hub Dashboard**: Live WebSocket and REST telemetry feed (`user/outputs/dashboard/index.html`) with interactive commercial provisioner console.

```mermaid
graph TD
  subgraph Frontend_Layer["Frontend & Corporate Portal Layer"]
    NextApp["Next.js 14 App Router / React"]
    ObservabilityUI["Observability Hub Dashboard"]
    CommercialUI["Commercial Provisioner Console"]
  end

  subgraph API_Gateway_Layer["API Gateway & Services (Rust Axum / Tokio)"]
    PortalServer["Portal Server (crates/percipience-server)"]
    KmsBroker["KMS & RLS Tenant Broker"]
    PackagerEngine["crates/percipience-packager"]
  end

  subgraph Platform_Core_Layer["Percipience Rust Platform"]
    PlatformCli["./percipience"]
    LedgerEngine["Merkle State Ledger"]
  end

  NextApp --> PortalServer
  ObservabilityUI --> PortalServer
  CommercialUI --> PortalServer
  PortalServer --> KmsBroker
  PortalServer --> PackagerEngine
  PortalServer --> PlatformCli
  PackagerEngine --> LedgerEngine
  PlatformCli --> LedgerEngine
```

---

## 1. Domain-Specific Quad-Space Mapping

- `.nb/context/contracts/`: `onboarding_contract.yaml`, `billing_meter_contract.yaml`, `commercial_provisioning_contract.yaml`, `observability_contract.yaml`
- `.nb/context/rules/`: `web_accessibility_rules.md`, `tenant_isolation_invariants.md`, `commercial_tier_permissioning_rules.md`
- `.nb/agentic/custom/agents/`: `agent_saas_portal_architect.yaml`, `agent_commercial_packager_provisioner.yaml`, `agent_billing_integration_engineer.yaml`, `agent_observability_frontend_specialist.yaml`
- `.nb/agentic/custom/workflows/`: `saas_portal_delivery_flow.yaml`, `commercial_packaging_provisioning_flow.yaml`
- `crates/percipience-server/`: Rust Axum & Tokio web/API server, WebSocket telemetry bus, and Connect-RPC endpoints
- `crates/percipience-packager/`: Multi-tier binary compiler, Ed25519 license minter, and multi-IDE provisioner
- `workplace/portal/`: Frontend corporate portal and UI assets embedded via `rust-embed`
- `workplace/modules/`: `mod_corp_site/`, `mod_saas_portal/`, `mod_billing_engine/`, `mod_api_gateway/`
- `user/outputs/`: Maturity reports, commercial bundle packages, and live dashboard feeds.

---

## 2. CLI & Layer Management

```bash
# Package layer bundle
./percipience layer pack --plan .nb/plan/l1/saas-portal-domain/concise.md --output .nb/bundles/saas_portal_domain.nbpack

# Apply layer bundle
./percipience layer apply --pack .nb/bundles/saas_portal_domain.nbpack --in-memory-only

# Commercial packaging & provisioning
./percipience commercial package --tier enterprise --tenant tenant_acme_fintech
./percipience commercial provision --tenant tenant_acme_fintech --tier enterprise --target all
```

## 4. Visual Delivery Pipelines & Stage Handled Contracts Governance

- **Portal Visualizer**: `resources.html` provides a dedicated subtab for inspecting the 7 delivery flows with interactive DAG progression, executor chips, and stage-handled contract schemas.
- **Endpoints**: `/api/observability/workflows` and `/api/observability/contract-detail` serve workflow metadata, stage DAGs, and raw contract contents.
