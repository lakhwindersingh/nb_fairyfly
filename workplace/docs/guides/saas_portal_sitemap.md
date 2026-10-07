# Percipience Cloud SaaS Portal Sitemap & Route Specifications

> **Governing Spec:** [`.nb/plan/master/parent-master-free-plan/detailed.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/master/parent-master-free-plan/detailed.md)  
> **Server Implementation:** [`workplace/portal/server.py`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/portal/server.py)  
> **Default Port:** `http://localhost:3000` (Local) / Container Port `3000` (`percipience-portal`)

---

## 1. Public & Interactive Portal Navigation Tabs (15 Tabs)

1. **`/` (Hero & AST Pruning Simulator)**: Interactive hero experience with real-time AST pruning demonstration, customer validation metrics, and token arbitrage calculators.
2. **`/tier-matrix` (`#tier-matrix`)**: **Plan Tier Matrix & Boundary Ceilings** &mdash; Full comparative matrix across Free Community (`plan_free`), Team (`plan_team`), Business (`plan_business`), and Enterprise (`plan_enterprise`). Deep dives into 6 boundary ceilings, capability allotments, and live tier ceiling validator.
3. **`/capabilities` (`#capabilities`)**: **SDLC Capabilities Catalog** &mdash; Interactive catalog of all 47 engineering capabilities (CAP-01 through CAP-47), organized across Core Context, Autonomous CI/CD, Multi-Tenant Governance, and Agent Coordination Swarms.
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

## 2. Authenticated Client Space (`#client`)

- **`/client` (`#client`)**: Dedicated authenticated client dashboard for enterprise tenant organizations.
  - **Module Architecture View**: Protected view of multi-module workspace structure and module health.
  - **FinOps Ledger**: Itemized token savings and 15% performance fee invoice ledger.
  - **WORM Audit Log**: SEC 17a-4 / FINRA compliance audit trail linked to cryptographic Merkle blocks.
  - **Surgical Micro-Module Rollback**: One-click rollback triggering rewind of specific poisoned modules to prior recovery points ($\text{RP}_k$) in under 1.2s without sibling disruption.

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
