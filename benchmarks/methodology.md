# Percipience FinOps & Context Engineering Benchmark Methodology

> **Standard Version**: 1.0.0  
> **Status**: Active Reference Harness  
> **Auditable Provenance**: Linked directly to Merkle DAG Ledger Blocks

---

## 1. Overview & Provenance Contract
All quantitative figures stated across Percipience documentation, whitepapers, and operational dashboards (e.g., 50–70% token reduction, 62% empirical savings, 90% cost arbitrage, sub-1.2s surgical rollback, 0.1ms AST skeleton retrieval) are strictly treated as **targets and design goals** until explicitly reproduced and audited by this benchmark harness.

Every empirical measurement must record:
1. Workload definition & repository corpus size.
2. Provider, model ID, API version, and temperature.
3. Cold-start vs. warm-cache AST cache policies.
4. Statistical treatment (median across $N \ge 10$ runs with 95% confidence intervals).
5. Exact Merkle ledger block ID and commit SHA producing the benchmark.

---

## 2. Benchmark Workload Profiles

### Profile A: Poly-Module Enterprise Microservices (Standard Repository)
- **Corpus**: 5 TypeScript/Python microservices (`mod_tenant_onboarding`, `mod_billing_metering`, `mod_observability_usage`, `mod_shared_infra_bridge`, `mod_portal_marketing`).
- **Files**: 48 source and contract files.
- **Uncompressed Baseline**: 1,632,800 tokens.
- **Test Invocations**: 50 consecutive agentic PR gatekeeper verification runs.

### Profile B: Surgical Context Poisoning Remediation
- **Scenario**: Simulated secret key leakage and hallucinated dependency injection into a leaf module.
- **Measurement**: Wall-clock time to detect poisoning, trigger worktree isolation, isolate culprit to append-only HITL incident store, and restore sibling modules cleanly.

### Profile C: Cognitive Model-Agnostic Cascading Arbitrage
- **Scenario**: 1,000 mixed-complexity tasks (AST extraction, SemVer contract diffs, security audits, living doc generation).
- **Measurement**: Token distribution across Tier A (Frontier) vs. Tier B (Compact) and total dollar expenditure versus single-tier frontier model execution.

---

## 3. Metric Calculations

$$
\text{Token Savings Percentage} = \frac{\text{Uncompressed Tokens} - \text{Pruned Tokens}}{\text{Uncompressed Tokens}} \times 100
$$

$$
\text{Gross Financial Savings (USD)} = \frac{\text{Tokens Saved}}{1,000} \times \$0.003
$$

$$
\text{15% Performance Fee (USD)} = \text{Gross Savings} \times 0.15
$$

$$
\text{Net Customer Cash Saved (USD)} = \text{Gross Savings} \times 0.85
$$

---

## 4. Benchmark Result Storage
Raw measurements are persisted in:
`benchmarks/results/<YYYY-MM-DD>_<provider>_<model_slug>.json`
