# NPX Instant Execution & Bootstrapping Architecture Plan (L1 Foundation)

> **Plan ID**: `domain_npx_installer`  
> **Capability Rating**: `L1` (Foundation Layer)  
> **Status**: `Active`  
> **Parent Plan**: [`master/parent-master-plan/concise.md`](../../master/parent-master-plan/concise.md)

---

## Overview

This plan defines the architectural, packaging, and execution specifications for **Zero-Installation Instant Onboarding** via Node Package Runner (`npx @neutronbinary/percipience` or `npx percipience`). It bridges JavaScript/Node.js environments with the Percipience Quad-Space Context Engineering OS, allowing developers and CI/CD runners to initialize, audit, and gate projects in seconds without manual repository cloning or environment management.

## Document Map

| Document | Purpose | Target Audience |
| :--- | :--- | :--- |
| **[`concise.md`](./concise.md)** | High-density specification of package layout, CLI subcommands, execution modes, and MCP provisioning. | Autonomous Agents & Architects |
| **[`detailed.md`](./detailed.md)** | Comprehensive implementation guide covering npm distribution, platform binaries, offline caching, and CI workflows. | Implementation Engineers & DevOps |
| **[`MANIFEST.yaml`](./MANIFEST.yaml)** | Cryptographic version manifest, file checksums, and dependency graph. | Automated Build & Audit Tools |

## Key Capabilities

- **Zero-Install Ephemeral Execution**: Execute gatekeeper and audit commands in CI/CD without global package installation.
- **Single-Command Quad-Space Scaffolding**: `npx @neutronbinary/percipience init` bootstraps `.nb/`, `workplace/`, and `user/` in $<3$ seconds.
- **Automated Claude / MCP Provisioning**: Automatically writes and synchronizes `.claude/mcp.json` and `.claude/settings.json`.
- **Platform Binary & Fallback Resolution**: Multi-platform prebuilt binaries with graceful fallback to Python AST engines.
- **Enterprise Air-Gapped & Proxy Support**: Compatible with private npm registries (Artifactory, Nexus, GitHub Packages) and corporate proxies.
