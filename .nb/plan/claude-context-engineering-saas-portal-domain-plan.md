---
sessionId: session-260915-saas-portal-domain-plan
parent_plan: .nb/plan/claude-context-engineering-parent-master-plan.md
domain: "Enterprise SaaS, Corporate Portals & Web Platform Ecosystem"
tier: "Tier 2 (Enterprise Domain Plan) & Tier 3 (Specialist Subagents)"
---

# Layerable Context Engineering Plan: Enterprise SaaS & Corporate Portal Space

### Executive Overview & Domain Grounding
This document is a **Layerable Domain-Specific Context Engineering Plan** designed to be overlaid onto the generic **Parent Master Context Engineering Framework** (`.nb/plan/claude-context-engineering-parent-master-plan.md`). While the parent plan governs universal multi-module lifecycle orchestration, cryptographic Merkle state verification, AST token compression, and autonomous CI/CD, this plan injects concrete domain contracts, specialized subagents, and web application runtimes required for:

1. **Modern Frontend & Corporate Web Systems**: React, Next.js (App Router), Astro, Tailwind CSS, TypeScript, and accessible UI component design systems conforming to WCAG 2.1 AA and Core Web Vitals (LCP < 2.5s, CLS < 0.1, INP < 200ms).
2. **Multi-Tenant SaaS Portals & Management Dashboards**: Dynamic role-based access control (RBAC), tenant data isolation, customer self-service billing portals, and real-time observability telemetry hubs (`user/outputs/dashboard/index.html`).
3. **Decoupled API Gateways & Webhook Handlers**: High-throughput REST and GraphQL gateways (`workplace/portal/server.py`), Stripe/Paddle billing webhooks, and JWT/OAuth2 session management.
4. **End-to-End Web Verification & Quality Harnesses**: Headless browser automation (Playwright/Puppeteer), Jest/Vitest component testing, and axe-core accessibility regression gates.

---

## 1. Domain-Specific Quad-Space Mapping

When layered onto the Parent Master Plan, the workspace instantiates domain-specialized structures across the four clean directories:

```
.
├── context/
│   ├── contracts/
│   │   ├── portal_openapi_spec.yaml         # REST/JSON API contract between frontend portal & backend services
│   │   ├── billing_webhook_contract.json    # Stripe/Paddle subscription event lifecycle schemas
│   │   └── rbac_permission_matrix.json     # Role-based access control & tenant boundary definitions
│   └── rules/
│       ├── web_performance_invariants.md    # Core Web Vitals (LCP/CLS/INP) and bundle size thresholds (< 150KB gzip)
│       └── wcag_accessibility_rules.md      # WCAG 2.1 AA color contrast, ARIA landmarks, keyboard navigation
├── agentic/
│   ├── custom/agents/
│   │   ├── portal_developer.yaml            # Subagent: React/Next.js/Tailwind frontend & UX specialist
│   │   └── saas_backend_developer.yaml      # Subagent: Python/Node.js microservices, billing & auth specialist
│   └── custom/workflows/
│       └── saas_portal_delivery_flow.yaml   # Orchestrates UI component build -> API gateway -> Playwright E2E
├── workplace/
│   ├── modules/
│   │   ├── mod_portal_marketing/            # Customer-Facing Corporate & Marketing Site (Next.js / Astro)
│   │   │   ├── config/                      # Tailwind theme tokens, next.config.js, SEO sitemaps
│   │   │   ├── src/                         # Landing pages, pricing tables, MDX blogs, lead forms
│   │   │   └── tests/                       # Component tests & Lighthouse CI performance fixtures
│   │   └── mod_portal_admin/                # Multi-Tenant Cloud SaaS Management Console
│   │       ├── config/                      # Route guards, telemetry refresh intervals, auth config
│   │       ├── src/                         # 5-tab observability dashboard, tenant settings, analytics
│   │       └── tests/                       # Playwright E2E authentication & permission test suites
│   ├── portal/
│   │   └── server.py                        # Standalone Python HTTP/API Gateway bridging dashboard & local daemon
│   └── shared/
│       ├── schemas/                         # Shared TypeScript interfaces and JSON schemas
│       └── styles/                          # Global CSS design tokens, utility classes, and font configurations
└── user/
    ├── inputs/
    │   ├── corp_site_mvs_spec.yaml          # Sitemap sketch, brand color hexes, typography, lead fields
    │   └── saas_portal_mvs_spec.yaml        # Tenant roles, dashboard widget metrics, billing tiers, API quotas
    ├── hitl/
    │   └── poisoning_quarantine.md          # Quarantined hallucinated UI routes or invalid CSS token payloads
    └── outputs/
        ├── dashboard/
        │   └── index.html                   # 5-tab zero-dependency interactive context observability portal
        ├── context_maturity_report.md       # Quantitative 6-dimensional scorecard including web performance
        └── token_savings_report.md          # FinOps token metering, AST compression ratio, 15% rev-share ledger
```

---

## 2. Wire Contracts & Invariant Enforcements

The domain plan supplies three non-overridable wire contracts verified by the pre-commit gatekeeper:

### 1. `context/contracts/portal_openapi_spec.yaml`
```yaml
openapi: 3.1.0
info:
  title: "Enterprise SaaS Portal & Gateway API"
  version: "1.0.0"
paths:
  /api/v1/telemetry/maturity:
    get:
      summary: "Retrieve 6-dimensional context maturity score"
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MaturityScoreResponse'
  /api/v1/agents/plugins:
    get:
      summary: "List registered autonomous custom agents"
    post:
      summary: "Register new custom agent plugin"
  /api/v1/cicd/pipeline/run:
    post:
      summary: "Trigger autonomous self-sustaining CI/CD verification cycle"
```

### 2. `context/contracts/billing_webhook_contract.json`
Enforces idempotency and payload schema verification for customer subscription events (`customer.subscription.created`, `invoice.payment_succeeded`, `invoice.payment_failed`) ensuring zero double-charging or billing race conditions.

---

## 3. Domain Specialist Subagents

### `agentic/custom/agents/portal_developer.yaml`
```yaml
agent_id: "agent_portal_developer"
name: "SaaS Portal & Corporate Web Specialist"
version: "1.0.0"
category: "frontend_engineering"
model_tier: "sonnet"
system_prompt_ref: "agentic/prompts/portal_developer_prompt.md"
budget_limits:
  max_tokens_per_turn: 25000
  max_ast_pruned_tokens: 12000
permissions:
  allow_worktree_isolation: true
  allowed_module_paths:
    - "workplace/modules/mod_portal_marketing"
    - "workplace/modules/mod_portal_admin"
    - "user/outputs/dashboard"
enforced_invariants:
  - "Zero uncompressed context leaks (> 50% AST compression required)"
  - "Lighthouse Performance Score >= 90 / Accessibility Score >= 95"
  - "Strict responsive breakpoints (mobile, tablet, desktop) on all UI components"
```

---

## 4. Multi-Module Surgical Rollback Scenario

In a multi-module SaaS deployment with `mod_portal_marketing` and `mod_portal_admin`:

```mermaid
sequenceDiagram
    autonumber
    participant Dev as agent_portal_developer
    participant WT as Ephemeral Worktree (.workspaces/portal_admin)
    participant Gate as Percipience Gatekeeper
    participant Sentinel as Poisoning Sentinel
    participant Ledger as Context Ledger (Merkle Chain)

    Dev->>WT: Modify admin dashboard routes & charts
    WT->>Gate: Submit PR increment
    Gate->>Sentinel: Scan for invalid API contracts & hardcoded client secrets
    Sentinel-->>Gate: DETECTED: Hallucinated /api/v2/superadmin route violating portal_openapi_spec.yaml
    Gate->>Sentinel: Trigger Surgical Rollback for mod_portal_admin
    Sentinel->>WT: Reset mod_portal_admin to RP_PORTAL_ADMIN_004
    Note over WT: mod_portal_marketing remains untouched at RP_PORTAL_MKTG_002!
    Sentinel->>Ledger: Log quarantine event in user/hitl/poisoning_quarantine.md
    Sentinel->>Ledger: Seal Merkle Block RP_POISON_ROLLBACK_PORTAL_ADMIN
    Gate-->>Dev: Halt turn with remediation diff; unaffected marketing site unaffected
```

---

## 5. Layering Recipe & Integration Commands

To instantiate or layer this SaaS Portal domain onto a fresh repository using the Percipience CLI:

```bash
# 1. Initialize repository with multi-module SaaS configuration
./bin/percipience init --mode multi_module --domain saas_portal

# 2. Register the domain subagents into the gatekeeper DAG
./bin/percipience agent register --manifest agentic/custom/agents/portal_developer.yaml
./bin/percipience agent integrate --agent-id agent_portal_developer --workflow wf_pr_gatekeeper --after step_contract_compat

# 3. Launch local real-time telemetry API gateway and dashboard
python3 workplace/portal/server.py --port 8080 &
open user/outputs/dashboard/index.html

# 4. Execute autonomous CI/CD closed-loop validation
./bin/percipience cicd --full-cycle
```
