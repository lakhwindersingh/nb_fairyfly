# Multi-Tier Python Wheel Packaging & Distribution Architecture Plan (L1 Foundation)

> **Plan ID**: `domain_tiered_wheel_packaging`  
> **Capability Rating**: `L1` (Foundation Layer)  
> **Status**: `Active`  
> **Parent Plan**: [`master/parent-master-plan/concise.md`](../../master/parent-master-plan/concise.md)

---

## Overview

This plan defines the **Multi-Tier Python Wheel Packaging and Distribution Subsystem** for Percipience. It governs the automated compilation, code exclusion boundaries, cryptographic sealing, and index publishing of standardized Python Wheels (`.whl` adhering to PEP 427, PEP 517, PEP 621) across the 4 commercial tiers:
1. **Free Community Edition** (`percipience-free` / `plan_free`)
2. **Team Edition** (`percipience-team` / `plan_team`)
3. **Business Edition** (`percipience-business` / `plan_business`)
4. **Enterprise Dedicated Edition** (`percipience-enterprise` / `plan_enterprise`)

## Document Map

| Document | Purpose | Target Audience |
| :--- | :--- | :--- |
| **[`concise.md`](./concise.md)** | High-density specification of tier engine rules, build hooks, wheel naming, and pip installation commands. | Autonomous Agents & Architects |
| **[`detailed.md`](./detailed.md)** | Comprehensive implementation guide covering code exclusion, entry points, cryptographic Merkle sealing, and enterprise private index deployment. | DevOps Engineers & Packaging Specialists |
| **[`MANIFEST.yaml`](./MANIFEST.yaml)** | Cryptographic version manifest, file checksums, and dependency graph. | Automated Build & Audit Tools |

## Key Capabilities

- **Tier-Gated Engine Exclusion**: Automated build-time exclusion of proprietary enterprise modules (NBPack compilers, private VPC enclaves, swarm orchestrators) from community distributions.
- **PEP 517/621 Compliant Packaging**: Dynamic `pyproject.toml` and wheel assembly supporting pure-Python (`py3-none-any.whl`) and pre-compiled extensions.
- **Cryptographic Merkle State Sealing**: Every compiled wheel artifact hash is recorded into `context_ledger.yaml` before release.
- **Multi-Index Distribution Strategy**: Public PyPI distribution for community packages; authenticated private registries (AWS CodeArtifact, Artifactory, Cloudsmith) for paid enterprise tiers.
- **Unified CLI Entry Points**: Standardized `percipience` and `percipience-agent` console scripts across all tiers.
