---
plan_type: "layerable_domain_plan"
plan_id: "domain_tiered_wheel_packaging"
name: "Multi-Tier Python Wheel Packaging & Distribution Architecture Plan"
parent_master_plan: "master/parent-master-plan/concise.md"
tier_mapping:
  tier_2: "Enterprise Domain Rules & Wire Contracts (.nb/context/contracts/, .nb/context/rules/)"
  tier_3: "Specialist Subagents & Delivery Workflows (.nb/agentic/custom/agents/, .nb/agentic/custom/workflows/)"
model_tiering_policy:
  provider_agnostic: true
  tier_a_model: "claude-3-7-sonnet / pro"
  tier_b_model: "claude-3-5-haiku / flash"
---

# Layerable Context Engineering Plan: Multi-Tier Python Wheel Packaging Space — Root Navigation Link

This root-level alias points directly to the authoritative L1 Foundation plan documents:

- **Concise Specification**: [`l1/tiered-wheel-packaging/concise.md`](./l1/tiered-wheel-packaging/concise.md)
- **Detailed Architecture Guide**: [`l1/tiered-wheel-packaging/detailed.md`](./l1/tiered-wheel-packaging/detailed.md)
- **Directory Overview & Map**: [`l1/tiered-wheel-packaging/README.md`](./l1/tiered-wheel-packaging/README.md)
- **Cryptographic Manifest**: [`l1/tiered-wheel-packaging/MANIFEST.yaml`](./l1/tiered-wheel-packaging/MANIFEST.yaml)

### Summary of Coverage
- Automated compilation of PEP 427 Python Wheels across all 4 commercial tiers (`plan_free`, `plan_team`, `plan_business`, `plan_enterprise`).
- Strict build-time file-level exclusion preventing enterprise code leakage into community wheels.
- Unified console script entry points (`percipience` and `percipience-agent`).
- SHA-256 Merkle block sealing for release artifacts.
- Index hosting and pip installation for public PyPI, AWS CodeArtifact, JFrog Artifactory, and air-gapped VPCs.
