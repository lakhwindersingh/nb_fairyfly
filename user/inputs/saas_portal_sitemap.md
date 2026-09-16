# Percipience Cloud SaaS Portal Sitemap & Route Specifications

## Public Routes (`mod_portal_marketing`)
- `/`: Homepage, Hero, Real-Time AST Pruning Simulator, Customer Testimonials.
- `/roi-calculator`: Interactive Token Savings & 15% Performance Fee Calculator.
- `/pricing`: Transparent pricing tiers (Team $1,499, Business $4,499, Enterprise $9,999+).
- `/docs`: MDX Developer Documentation, CLI Quickstart, CI/CD Gatekeeper setup.

## Authenticated Tenant Routes
- `/onboard` (`mod_tenant_onboarding`): Organization signup, WorkOS SSO, CMEK key setup.
- `/billing` (`mod_billing_metering`): Stripe billing portal, invoice history, token savings proof ledger.
- `/app` (`mod_observability_usage`): Real-time token burn graph, Merkle DAG explorer, surgical rollback manager.

## API & Simulation Endpoints (`workplace/portal/server.py`)
- `/api/health`: Platform status, version, and Merkle continuity.
- `/api/tokens/savings`: Real-time token pruning events and FinOps metrics.
- `/api/observability/agents`: Active agent swarm registry including all 4 specialist plugins.
- `/api/observability/plugins`: Custom specialist agent plugin manifests (`agentic/custom/agents/`).
- `/api/observability/flaky`: Flaky test quarantine tracking (`user/hitl/flaky_quarantine.yaml`).
- `/api/observability/ast-cache`: Content-addressable AST cache metrics and retrieval latency.
- `/api/observability/cognitive-router`: Model-agnostic tier routing policies and cost arbitrage.
- `/api/merkle/epochs`: Checkpointed epoch archives in `context/ledger/archive/`.
- `/api/marketing/cognitive-route` (POST): Interactive cognitive tier dispatch simulation.
- `/api/marketing/flaky-check` (POST): Multi-run test determinism verification.
- `/dashboard`: Direct embed of the comprehensive 5-tab Enterprise Observability Hub.
