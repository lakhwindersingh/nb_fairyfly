# Percipience Commercial Tier Permissioning & Feature Gate Invariants

> **Governing Plan**: [Layerable SaaS Portal Domain Plan](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/l1/saas-portal-domain/detailed.md)  
> **Enforcement Engine**: `CommercialPackagerProvisioner` & `TenantManager`

## 1. Zero-Trust Tier Boundary Invariants
1. **Free Community Tier (`plan_free`)**:
   - Strictly confined to offline AST token optimization, Tree-Sitter pruning, deterministic Merkle ledgering, and base CLI orchestration.
   - Forbidden actions: `allow_nbpack_compilation`, `allow_custom_agent_creation`, `allow_private_vpc`, `allow_worm_egress`, `allow_multi_tenant_gateway`.
   - Max concurrent worktree allocation: 1. Max monthly PR verification audits: 500.

2. **Team Tier (`plan_team`)**:
   - Unlocks custom agent definition creation (`allow_custom_agent_creation = true`) and ephemeral worktree concurrency up to 5 concurrent worktrees.
   - Forbidden actions: `allow_nbpack_compilation`, `allow_private_vpc`, `allow_worm_egress`.

3. **Business Tier (`plan_business`)**:
   - Unlocks `.nbpack` encrypted enclave compilation, Multi-Tenant Gateway routing, Cognitive Router, and up to 20 concurrent worktrees with 25,000 PR audits.
   - Forbidden actions: `allow_private_vpc`, `allow_worm_egress`.

4. **Enterprise Dedicated Tier (`plan_enterprise`)**:
   - Complete unconstrained capability suite: WORM Egress to AWS S3 Object Lock / GCP Bucket Lock, Air-gapped VPC execution, unlimited seats, 100+ concurrent worktrees, and custom LLM provider brokering.

## 2. Cryptographic License Minting & Tamper Resistance
- Every provisioned target must receive an Ed25519-signed or SHA-256 sealed license manifest (`PERCIPIENCE_LICENSE.json` or `tenant_license.json`).
- If a tenant attempts to execute an engine or capability outside their provisioned tier, `CommercialPackagerProvisioner.verify_permissions` immediately halts execution and flags an audit event in the Merkle ledger.
