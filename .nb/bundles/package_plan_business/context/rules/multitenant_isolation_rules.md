# Multi-Tenant Boundary Isolation & RLS Invariants

## 1. Zero-Cross-Tenant Leakage Invariant
Every database query, API dispatch, cache read, and background worker task MUST be scoped to a specific `tenant_id`.
Under NO circumstances may an unpartitioned SQL statement execute against shared enterprise tables (`instruments`, `trades`, `projects`, `users`).

## 2. PostgreSQL Row-Level Security (RLS) Grounding
1. All multi-tenant tables MUST enable Row-Level Security:
   ```sql
   ALTER TABLE <target_table> ENABLE ROW LEVEL SECURITY;
   ```
2. The runtime connection pool MUST inject the active session tenant identity into the PostgreSQL session context before executing domain transactions:
   ```sql
   SET LOCAL app.current_tenant_id = 'tenant_xyz';
   ```
3. Default query behavior for missing session settings MUST return zero records (`NULLIF(current_setting('app.current_tenant_id', true), '') IS NOT NULL`).

## 3. Zanzibar ReBAC Relationship Hierarchy
1. Subject access permissions evaluate hierarchically:
   `Tenant -> Organization -> Project -> Module / Resource`.
2. A subject inheriting permissions through team membership must be evaluated through the ReBAC relation store (`<entity>#<relation>@<subject>`).
3. Deny-overrides prevail across all composite evaluations.
