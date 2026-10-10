# Percipience Cloud SaaS Portal Sitemap & Route Specifications

> **Governing Spec:** [`.nb/plan/master/parent-master-free-plan/detailed.md`](/.nb/plan/master/parent-master-free-plan/detailed.md)  
> **Server Implementation:** [`workplace/portal/server.py`](/workplace/portal/server.py)  
> **Default Port:** `http://localhost:3000` (Local) / Container Port `3000` (`percipience-portal`)

---

## 1. Public & Interactive Portal Navigation Tabs (15 Tabs)

1. **`/` (Hero & AST Pruning Simulator)**: Interactive hero experience with real-time AST pruning demonstration, customer validation metrics, and token arbitrage calculators.
2. **`/tier-matrix` (`#tier-matrix`)**: **Plan Tier Matrix & Boundary Ceilings** &mdash; Full comparative matrix across Free Community (`plan_free`), Team (`plan_team`), Business (`plan_business`), and Enterprise (`plan_enterprise`). Deep dives into 6 boundary ceilings, capability allotments, and live tier ceiling validator.
3. **`/capabilities` (`#capabilities`)**: **SDLC Capabilities Catalog** &mdash; Interactive catalog of all 52 engineering capabilities (CAP-01 through CAP-52), organized across Core Context, Autonomous CI/CD, Multi-Tenant Governance, and Agent Coordination Swarms.
4. **`/comparatives` (`#comparatives`)**: **5-Way Competitive Matrix** &mdash; Comparative differentiation against Cursor, LangSmith, Arize Phoenix, AutoGen/CrewAI, and GitHub Actions.
5. **`/gateway` (`#gateway`)**: **Context Gateway Console** &mdash; In-flight prompt injection simulator, zero client-side plan exposure demonstrator, and `.nbpack` encryption console.
6. **`/roi-calculator` (`#roi-calculator`)**: **FinOps ROI & Token Savings Calculator** &mdash; Dynamic 15% performance fee calculator, model arbitrage savings estimator, and gross/net financial projections.
7. **`/sandboxes` (`#sandboxes`)**: **Ephemeral Worktree Sandboxes** &mdash; Real-time status of active subagent git worktree leases (`.nb/workspaces/wt_*`), lease expiration timers, and manual purge controls.
8. **`/infrastructure` (`#infrastructure`)**: **Cloud Infrastructure & WORM Vault** &mdash; Architectural layout, multi-region immutable storage topologies, and OpEx breakdown.
9. **`/pricing` (`#pricing`)**: **Commercial Pricing Plans** &mdash; Transparent tier costs (Free Community $0.00, Team $1,499/mo, Business $4,499/mo, Enterprise $9,999+/mo) and licensing terms.
10. **`/docs` (`#docs`)**: **Embedded Developer Documentation** &mdash; In-portal documentation viewer for quickstart guides, CI/CD gatekeeper setup, and IDE integration tutorials.
11. **`/reports` (`#reports`)**: **Engineering Reports & Whitepapers** &mdash; Interactive view of SDLC architecture reviews, AST pruning benchmarks, and token savings whitepapers.
12. **`/observability` (`#observability`)**: **GenAI Observability Hub** &mdash; OpenTelemetry W3C distributed traces (`gen_ai.request.model`, `gen_ai.usage.input_tokens`), 5D G-Eval radar scoring, and semantic KV prompt cache hit rate analytics.
13. **`/governance` (`#governance`)**: **Multi-Tenant Governance Console** &mdash; Tenant isolation management, policy sliders, KMS hardware enclave verification, and emergency kill switches.
14. **`/commercial-provisioner` (`#commercial-provisioner`)**: **Commercial Provisioner & License Engine** &mdash; Automated plan entitlement provisioning, dynamic module slicing, cryptographic license key generation, and tier upgrade workflow.
15. **`/swarm-governance` (`#swarm-governance`)**: **Agent Swarm & Coordination Governance** &mdash; Dynamic DAG orchestrator visualizer, 5-pillar reflexion critic scoring, 3-tier persistent memory inspector, tool contract schema validator, and capability-based access control (CBAC) token console.

---

## 2. Authenticated Client Space (`#client`) — Dashflat Vertical-Default-Light Template

- **`/client` (`#client`)**: Dedicated authenticated enterprise client portal structured using the **Dashflat Admin Vertical-Default-Light** template architecture ([Dashflat Reference](https://demo.bootstrapdash.com/dashflat-new/themes/vertical-default-light/)).
  - **Vertical Collapsible Sidebar (`.dashflat-sidebar`)**:
    - **User Profile Widget**: Tenant user avatar, online status indicator, user name (*Acme Global Admin*), and enterprise super admin role badge with quick action buttons.
    - **Categorized Multi-View Navigation**:
      - `NAVIGATION`: Dashboard & FinOps (`#client-overview`) with 15% fee badge.
      - `SOVEREIGN GOVERNANCE`: Multi-Tenant & RLS Policies (`#governance`) with active badge.
      - `COMMERCIAL & LICENSING`: Commercial Provisioner & Slicing (`#commercial-provisioner`) with tier badge.
      - `SWARM ORCHESTRATION`: Swarm Governance & Reflexion (`#swarm-governance`) with node count badge.
      - `INFRASTRUCTURE & FLEET`: Workstation Fleet & Telemetry (`#fleet-monitor`) with health badge.
    - **Direct Enterprise Plans Promo Card**: Dedicated storage allocations (650 GB S3 WORM) and 24/7 Concierge SLA link.
    - **WORM Chain Footer**: Live display of Merkle Block hash continuity (#828 Locked).
  - **Top Navigation Bar (`.dashflat-topbar`)**:
    - Hamburger sidebar collapse toggle (`☰`).
    - Flat global search bar (`🔍 Search micro-modules, recovery points, invoices, WORM blocks...`).
    - Security status pills (`Enterprise RLS Active`, `SOC 2 Type II`, `Enterprise Tier A`).
    - Interactive notifications dropdown (3 system alerts) & advisories dropdown (2 messages).
    - User profile dropdown with quick links to Profile, Billing, Policies, and Session Sign Out.
    - Responsive dark/light theme switch button.
  - **Dashboard Content Canvas (`.df-content-area`)**:
    - **Welcome Banner**: Client ID, Project Name, Tier Badge, and live sync timestamps.
    - **4-Card KPI Metric Grid**:
      - *Active Workspaces*: 4 Micro-Modules / 12 Swarm Nodes (+5.27% MoM).
      - *Recovery Points*: 4 Active Points (100% Deterministic, sub-1.2s rewind).
      - *AST Token Reductions*: 2.63M Tokens (50.3% Compression with zero semantic loss).
      - *Verified Gross Savings*: $15.6974 USD (15% Rev-Share Due: $2.3546 USD, 85% Client Retained: $13.3428 USD).
    - **2-Column Analytics & Direct Services Row**:
      - *Token Flow Breakdown & Resource Compute*: Progress bar visualization of token budget (AST Pruned vs Cache Hits vs Delivered Window), alongside Active Optimized Compute ($123,657), Eliminated Waste ($100,278), Performance Fee (15.0%), and Gate Throughput (142,800/day).
      - *Direct Enterprise Services*: Live status pills for PostgreSQL RLS, S3 WORM, Ed25519 Enclave, and 0 Flaky Quarantine Blockers.
    - **Micro-Modules & Surgical Recovery Datatable**: Sub-1.2s single-click surgical rollback (`POST /api/client/surgical-rollback`) for isolated micro-modules (`mod_auth`, `mod_billing`, `mod_portal_marketing`, `mod_trading`).
    - **Itemized FinOps Invoice & Transaction Ledger**: Mathematical audit breakdown and settled transaction ledger across enterprise tenant nodes (HSBC, G4S, John Lewis & Partners, Clarks, Lush Cosmetics).
  - **Unauthenticated Authentication State**:
    - Centered Dashflat authentication card with client ID, API key, persistent session checkbox, instant demo login, and SOC 2 / SEC 17a-4 compliance badges.

---

## 3. Comprehensive REST API Endpoint Catalog

### Authentication & Tenant Management APIs
- `POST /api/auth/login`: Authenticates tenant via Client ID and API key, returning a secure session token.
- `GET /api/auth/session`: Validates current session token and returns client profile metadata.
- `POST /api/auth/logout`: Invalidates session token.
- `GET /api/tenants`: Returns list of configured tenants with license tier and resource quotas.
- `POST /api/tenants`: Provisions a new tenant with isolated worktree workspace and quota allocations.
- `GET /api/policies`: Retrieves global and tenant-specific governance policies.
- `POST /api/policies`: Updates policy enforcement rules (e.g., maximum token burn, allowed model tiers).

### Commercial Provisioner APIs
- `GET /api/commercial/tiers`: Enumerates all commercial tiers (`plan_free`, `plan_team`, `plan_business`, `plan_enterprise`) with boundary ceilings.
- `POST /api/commercial/provision`: Provisions an organization with dynamic bundle slicing and KMS-signed license.
- `GET /api/commercial/license/verify`: Cryptographically verifies license validity, checksums, and expiration.

### Swarm Governance & Agent Coordination APIs (Section 17.1)
- `GET /api/swarm/dag`: Returns current dynamic DAG state, node execution status, and topological batches.
- `POST /api/swarm/dag`: Submits a new dynamic DAG for execution with Kahn's algorithm cycle validation.
- `GET /api/swarm/memory`: Queries agent memory entries filtered by tier (`short_term`, `working`, `long_term`).
- `POST /api/swarm/memory`: Stores a memory entry with decay parameters and relevance tags.
- `DELETE /api/swarm/memory`: Prunes or purges expired memory entries based on TTL.
- `GET /api/swarm/reflection`: Retrieves reflection evaluation history and 5-pillar critic radar scores.
- `POST /api/swarm/reflection`: Triggers a 5-pillar self-reflection cycle on candidate agent output in a zero-disk-write sandbox.
- `GET /api/swarm/capabilities`: Lists active capability-based access control (CBAC) tokens and issued permissions.
- `POST /api/swarm/capabilities`: Mints or revokes a CBAC capability token with HMAC-SHA256 signature.
- `GET /api/swarm/contracts`: Lists registered tool contracts and their JSON Schema (Draft-07) specifications.
- `POST /api/swarm/contracts`: Validates tool invocation payloads against registered schema contracts.
- `GET /api/swarm/topologies`: Lists available swarm coordination topologies (`hierarchical`, `mesh`, `sequential`, `dynamic_dag`).

### Telemetry, Observability & Gateway APIs
- `GET /api/health`: Platform status, version, uptime, and Merkle chain continuity.
- `GET /api/tokens/savings`: Real-time token pruning telemetry and FinOps cost arbitrage metrics.
- `GET /api/observability/otel-traces`: OpenTelemetry W3C GenAI distributed traces.
- `GET /api/observability/evals`: Continuous quantitative G-Eval radar metrics (Faithfulness, Relevancy, Hallucination Immunity, Invariance).
- `GET /api/observability/semantic-cache`: Bit-for-bit KV prompt cache hit rate and latency arbitrage data.
- `GET /api/observability/agents`: Registered agent swarm manifests and capability tokens.
- `GET /api/observability/flaky`: Quarantined flaky tests (`user/hitl/flaky_quarantine.yaml`).
- `GET /api/merkle/epochs`: Checkpointed epoch archives in `.nb/context/ledger/archive/`.
- `POST /v1/chat/completions`: OpenAI/Anthropic drop-in completions proxy with in-flight context injection.
