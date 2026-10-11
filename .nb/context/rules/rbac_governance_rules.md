# Enterprise RBAC & Governance Rules

## 1. 5-Tier Role Taxonomy
The platform enforces a five-tier tenant role taxonomy:
1. `ENTERPRISE_SUPER_ADMIN`: Full sovereign authority across all projects, KMS enclaves, policies, and billing.
2. `PROJECT_ADMIN`: Administrative control scoped to specific projects and repositories.
3. `SECURITY_AUDITOR`: Read-only access to audit trails, WORM ledgers, and PII access logs.
4. `DEVELOPER`: Read-write access to code, micro-modules, and verification runs within assigned projects.
5. `VIEWER`: Read-only observability over telemetry, public metrics, and dashboards.

## 2. Least Privilege Default
All permissions are denied by default. Explicit relationship tuples or role grants are required for every action.
Privilege escalation attempts trigger automated alerting and session quarantine.
