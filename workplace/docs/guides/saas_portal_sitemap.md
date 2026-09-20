# Percipience Cloud SaaS Portal Sitemap & Route Specifications

## Public Routes (`mod_portal_marketing` / `portal.server`)
- `/`: Homepage, Hero, Real-Time AST Pruning Simulator, Customer Testimonials.
- `/tier-matrix` (`#tier-matrix`): **Plan Tier Matrix & Boundary Ceilings (Section 2)** &mdash; Full comparative matrix across Free Community (`plan_free`), Team (`plan_team`), Business (`plan_business`), and Enterprise (`plan_enterprise`), 6 Boundary Ceilings deep-dive, full 35-capability mapping (CAP-01 through CAP-35), and Live Boundary Ceiling & Tier Validator.
- `/capabilities` (`#capabilities`): Deep dive into the 35 SDLC capabilities and architectural engines.
- `/comparatives` (`#comparatives`): 5-way comparative matrix vs Cursor, LangSmith, Arize Phoenix, and GitHub Actions.
- `/gateway` (`#gateway`): Context Gateway (Option 1: In-Flight Prompt Injection) simulator and `.nbpack` encryption console.
- `/roi-calculator` (`#roi-calculator`): Interactive Token Savings & 15% Performance Fee Calculator.
- `/sandboxes` (`#sandboxes`): Live worktree sandbox status and active developer leases.
- `/infrastructure` (`#infrastructure`): Cloud infrastructure, multi-region WORM vaults, and OpEx breakdown.
- `/pricing` (`#pricing`): Transparent pricing tiers (Free Community $0.00, Team $1,499, Business $4,499, Enterprise $9,999+).
- `/docs` (`#docs`): Embedded MDX Developer Documentation, CLI Quickstart, CI/CD Gatekeeper setup, and IntelliJ/VSCode guides.
- `/reports` (`#reports`): Embedded engineering reports, AST benchmarks, and token savings whitepapers.
- `/observability` (`#observability`): OpenTelemetry W3C GenAI distributed traces, 5D G-Eval radar, and semantic cache explorer.
- `/client` (`#client`): Secure Client Space for tenant organizations (project details, finops invoices, WORM compliance, and surgical rollback).

## Authenticated Tenant & Security API Endpoints (`workplace/portal/server.py`)
- `/api/auth/login` (POST): Tenant authentication via Client ID and API key, issuing secure session tokens.
- `/api/auth/session` (GET): Validates active session token and returns client profile metadata.
- `/api/auth/logout` (POST): Revokes active session token.
- `/api/client/project-details` (GET): Protected multi-module workspace architecture and module health.
- `/api/client/finops-invoices` (GET): Itemized token savings and 15% performance fee billing ledger.
- `/api/client/worm-audit` (GET): SEC 17a-4 / FINRA WORM storage compliance audit.
- `/api/client/surgical-rollback` (POST): On-demand surgical micro-module rollback to previous recovery points (RP_k).

## Telemetry, Observability & Gateway API Endpoints
- `/api/health`: Platform status, version, and Merkle continuity.
- `/api/tokens/savings`: Real-time token pruning events and FinOps metrics.
- `/api/observability/otel-traces`: OpenTelemetry W3C GenAI distributed traces (`gen_ai.request.model`, `gen_ai.usage.input_tokens`, TTFT).
- `/api/observability/evals`: Continuous quantitative G-Eval scoring across Faithfulness, Context Relevancy, Hallucination Immunity, and Invariance.
- `/api/observability/semantic-cache`: Bit-for-bit KV prompt cache hit rate and latency savings.
- `/api/observability/agents`: Active agent swarm registry including all specialist plugins.
- `/api/observability/flaky`: Flaky test quarantine tracking (`user/hitl/flaky_quarantine.yaml`).
- `/api/merkle/epochs`: Checkpointed epoch archives in `.nb/context/ledger/archive/`.
- `/v1/chat/completions`: OpenAI/Claude drop-in compatible completions endpoint. Injects proprietary plan invariants in-flight while maintaining 0.0% client-side plan exposure.
