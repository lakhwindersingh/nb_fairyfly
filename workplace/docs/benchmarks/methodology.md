# Percipience FinOps, Context Engineering & Swarm Durability Benchmark Methodology

> **Standard Version**: 2.1.0  
> **Status**: Active Reference Harness  
> **Auditable Provenance**: Linked directly to Merkle DAG Ledger Blocks (`.nb/context/ledger/context_ledger.yaml`)  
> **Docker Test Harness:** [`workplace/infra/docker/`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/workplace/infra/docker/)  

---

## 1. Overview & Provenance Contract
All quantitative figures stated across Percipience documentation, whitepapers, and operational dashboards (e.g., 50–70% token reduction, 47.4% empirical savings, sub-1.2s surgical rollback, 0.1ms AST skeleton retrieval, <2ms Kahn acyclicity check, <15ms 3-tier memory recall) are strictly treated as **targets and design goals** until explicitly reproduced and audited by this benchmark harness.

Every empirical measurement records:
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

### Profile D: Dynamic DAG Swarm Orchestration Latency & Scale
- **Scenario**: 10 to 100 node dynamic agentic task DAGs with complex inter-dependencies, parallel forks, and join stages.
- **Measurement**: Runtime graph synthesis, topological sorting via Kahn's algorithm, cycle detection latency ($\le 2.0\text{ms}$ SLA), and topological wave scheduling overhead.

### Profile E: Self-Reflection 5-Pillar Critic Scoring & Iteration Budget
- **Scenario**: 50 candidate code patches evaluated across 5 pillars (Syntax, Contract, Invariant, Security, Efficiency) in an in-memory zero-disk-write sandbox.
- **Measurement**: Composite scoring duration, memory consumption, convergence iterations (bounded $\le 3$), and rate of hallucination quarantine.

### Profile F: 3-Tier Persistent Memory Recall & Token Economy
- **Scenario**: High-throughput query workloads against Short-Term, Working (scratchpad), and Long-Term (semantic) memory tiers.
- **Measurement**: Semantic query latency ($\le 15.0\text{ms}$ SLA), exponential decay decay accuracy, and token savings from episodic context retrieval vs full prompt resubmission.

### Profile G: Containerized Tree-Sitter Daemon IPC Throughput vs Subprocess
- **Scenario**: 500 concurrent AST extraction requests comparing the containerized HTTP Tree-Sitter daemon on port 8585 against cold-start CLI subprocess invocations.
- **Measurement**: Parsing latency, connection concurrency, memory footprint, and throughput speedup ($> 4\times$ design goal).

---

## 3. Metric Calculations

### Token & FinOps Economics
$$\text{Token Savings Percentage} = \frac{\text{Uncompressed Tokens} - \text{Pruned Tokens}}{\text{Uncompressed Tokens}} \times 100$$

$$\text{Gross Financial Savings (USD)} = \frac{\text{Tokens Saved}}{1,000} \times \$0.003$$

$$\text{15\% Performance Fee (USD)} = \text{Gross Savings} \times 0.15$$

$$\text{Net Customer Cash Saved (USD)} = \text{Gross Savings} \times 0.85$$

### Swarm Reflexion Score
$$\text{Score}_{\text{composite}} = \sum_{i=1}^{5} w_i \times S_i \quad \text{where} \quad \sum w_i = 1.0, \; S_i \in [0.0, 1.0]$$

$$\text{Pass Threshold} \iff \text{Score}_{\text{composite}} \ge 0.85$$

### Memory Relevance with Exponential Decay
$$R(t) = R_0 \times e^{-\lambda (t - t_0)} \times \text{sim}(\vec{q}, \vec{k})$$

where $\lambda$ is the decay rate, $(t - t_0)$ is the time elapsed in hours, and $\text{sim}(\vec{q}, \vec{k})$ is the cosine similarity between query and memory vectors.

---

## 4. Benchmark Result Storage
Raw measurements are persisted in:
`workplace/docs/benchmarks/results/<YYYY-MM-DD>_<workload_profile>_<model_or_engine>.json`
