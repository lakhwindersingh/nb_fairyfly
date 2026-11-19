# Multi-Tier Rust Binary, Crate & Polyglot Packaging Architecture Plan (L1 Foundation)

> **Plan ID**: `domain_tiered_wheel_packaging`  
> **Capability Rating**: `L1` (Foundation Layer)  
> **Status**: `Active`  
> **Parent Plan**: [`master/parent-master-plan/concise.md`](../../master/parent-master-plan/concise.md)

---

## Overview

This plan defines the **Multi-Tier Rust Binary, Crate and Polyglot Packaging Subsystem** for Percipience. It governs the automated compilation, feature gate boundaries, cryptographic sealing, and distribution of standardized single static binaries, Cargo crates, and optional polyglot bindings (Python wheels via PyO3/maturin, Node via NAPI-RS) across the 4 commercial tiers:
1. **Free Community Edition** (`percipience` with `--features tier_free`)
2. **Team Edition** (`percipience` with `--features tier_team`)
3. **Business Edition** (`percipience` with `--features tier_business`)
4. **Enterprise Dedicated Edition** (`percipience` with `--features tier_enterprise`)

## Document Map

| Document | Purpose | Target Audience |
| :--- | :--- | :--- |
| **[`concise.md`](./concise.md)** | High-density specification of tier binary rules, build hooks, target matrix, and download commands. | Autonomous Agents & Architects |
| **[`detailed.md`](./detailed.md)** | Comprehensive implementation guide covering feature gating, entry points, cryptographic Merkle sealing, and multi-OS binary deployment. | DevOps Engineers & Packaging Specialists |
| **[`MANIFEST.yaml`](./MANIFEST.yaml)** | Cryptographic version manifest, file checksums, and dependency graph. | Automated Build & Audit Tools |

## Key Capabilities

- **Tier-Gated Feature Flags**: Automated build-time feature exclusion of proprietary enterprise modules (NBPack compilers, private VPC enclaves, swarm orchestrators) via Cargo `#[cfg(feature = "...")]`.
- **Single Static Binary Compilation**: Pre-compiled static binaries (< 15MB) for macOS (universal), Linux (static musl), and Windows (.exe) with zero external runtime requirements.
- **Embedded Assets**: Self-contained runtime assets, default configurations, and wire schemas embedded via `rust-embed`.
- **Cryptographic Merkle State Sealing**: Every compiled binary artifact hash is recorded into `context_ledger.yaml` before release.
- **Multi-Channel Distribution Strategy**: GitHub Releases, crates.io, and private enterprise VPC enclaves.
- **Unified CLI Entry Point**: Standardized `./percipience` executable entry point across all tiers.
