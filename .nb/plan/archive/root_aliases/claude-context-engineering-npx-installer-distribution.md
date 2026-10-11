---
plan_type: "layerable_domain_plan"
plan_id: "domain_npx_installer"
name: "NPX Instant Execution & Bootstrapping Architecture Plan"
parent_master_plan: "master/parent-master-plan/concise.md"
tier_mapping:
  tier_2: "Enterprise Domain Rules & Wire Contracts (.nb/context/contracts/, .nb/context/rules/)"
  tier_3: "Specialist Subagents & Delivery Workflows (.nb/agentic/custom/agents/, .nb/agentic/custom/workflows/)"
model_tiering_policy:
  provider_agnostic: true
  tier_a_model: "claude-3-7-sonnet / pro"
  tier_b_model: "claude-3-5-haiku / flash"
---

# Layerable Context Engineering Plan: NPX Instant Execution & Bootstrapping Space — Root Navigation Link

This root-level alias points directly to the authoritative L1 Foundation plan documents:

- **Concise Specification**: [`l1/npx-installer/concise.md`](./l1/npx-installer/concise.md)
- **Detailed Architecture Guide**: [`l1/npx-installer/detailed.md`](./l1/npx-installer/detailed.md)
- **Directory Overview & Map**: [`l1/npx-installer/README.md`](./l1/npx-installer/README.md)
- **Cryptographic Manifest**: [`l1/npx-installer/MANIFEST.yaml`](./l1/npx-installer/MANIFEST.yaml)

### Summary of Coverage
- Instant single-command Quad-Space bootstrapping (`npx @neutronbinary/percipience init`).
- Zero-installation ephemeral CI PR Gatekeeper validation (`npx @neutronbinary/percipience gate`).
- Automatic Model Context Protocol (MCP) server provisioning for Claude Code & Cursor (`.claude/mcp.json`).
- Platform prebuilt binary resolution with Python bridge fallback.
- Corporate proxy, private npm registry (`.npmrc`), and air-gapped tarball installation flows.
