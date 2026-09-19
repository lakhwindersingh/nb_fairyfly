# Percipience Context Engineering Space (`context/`)

> **Governing Plan**: [Parent Master Context Engineering Plan](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/claude-context-engineering-parent-master-plan.md)  
> **Architecture**: Quad-Space Partitioning | Mode: Hybrid Coexistence  

## Purpose & Structure
This directory serves as the immutable single source of truth for governance, schemas, recovery points, and state integrity across all application modules.

```text
context/
├── contracts/                            # Formal cross-module schemas (YAML)
│   ├── onboarding_contract.yaml          # Tenant onboarding payload spec
│   ├── billing_meter_contract.yaml       # High-throughput usage & Stripe event spec
│   └── observability_contract.yaml       # Telemetry & Merkle DAG visualizer spec
├── ledger/
│   ├── context_ledger.yaml               # Master Merkle DAG state ledger (Single Source of Truth)
│   └── context_ledger.public.yaml        # Sanitized disk-safe projection
├── recovery_points/                      # Snapshot commits for surgical rollback
├── schemas/                              # Zod & JSON schema validation models
└── custom/                               # [UNENCRYPTED CUSTOMER EXTENSIBLE CONTEXT]
    ├── rules/                            # Enterprise domain rules & compliance policies
    └── schemas/                          # Custom business contracts & API schemas
```

## Context Layering Precedence
1. **Tier 1 (Base Platform Invariants)**: Merkle chain rules, `CHK_CONTEXT_POISONING_FREE` sentinel, AST pruner rules.
2. **Tier 2 (Enterprise Global Context)**: `context/custom/rules/` (company-wide security, coding standards).
3. **Tier 3 (Module Domain Context)**: `context/custom/schemas/` (custom API schemas and data dictionaries).
