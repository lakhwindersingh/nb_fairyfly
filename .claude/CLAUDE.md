# Neutron Binary Percipience - Claude Code Guidelines

## Quad-Space Architecture & Hierarchy
This repository strictly adheres to the **Quad-Space context engineering architecture**:
- **`.nb/`**: Platform core engines (54 engines), wire contracts, Merkle DAG ledger, CLI gatekeeper tooling, and centralized configuration ([`.nb/config/platform_config.yaml`](file://.nb/config/platform_config.yaml)).
- **`workplace/`**: Active modules, application packages, living documentation, integration tests, and business logic.
- **`user/`**: Formal MVS requests, input parameters, brand tokens, and audit artifacts.
- **`.claude/`**: Claude Code configurations, MCP server definitions, and custom commands.

## Runtime & System Prerequisites
- **Python**: **3.14+** (3.11+ backward-compatible) with modern virtual environment (`./venv`).
- **Dependencies**: Pinned in [`requirements.txt`](file://requirements.txt) (`pytest 9.1.1`, `pydantic 2.14.0`, `cryptography 50.0.1`, `fastapi 0.143.0`, `redis 8.1.0`).
- **Test Suite**: 320 verified tests with 100% pass rate (`pytest workplace/tests/`).

## Mandatory AST Context Injection
- **Canonical Context Location**: The pre-computed, AST-pruned structural project context is maintained at:
  [`percipience_claude_context.md`](file://.nb/context/percipience_claude_context.md)
- **Schema & Contract Adherence**: Always respect the wire contracts, public API interfaces, and type schemas defined in `.nb/context/percipience_claude_context.md`.
- **Implementation Inspection**: Because `.nb/context/percipience_claude_context.md` contains AST-pruned skeletons to optimize token usage (60–85% savings), full function bodies are omitted. When surgical refactoring or debugging deep logic is required, inspect specific target files directly in `workplace/` using file viewing tools.

## Platform Invariants & Tooling
All platform operations are governed by the unified CLI executable [`.nb/bin/percipience`](file://.nb/bin/percipience):
- `percipience config show / get` - Inspect externalized platform configuration values.
- `percipience audit` - Cryptographic SHA-256 Merkle DAG audit & context maturity scorecard evaluation.
- `percipience gate` - 7-stage CI/CD gatekeeper validating wire contracts, security invariants, and regressions.
- `percipience test --coverage` - Hermetic test pyramid execution with statement/branch coverage reporting.
- `percipience test --total-shards N --shard-index I` - Deterministic parallel test sharding.
- `percipience sandbox exec` - Sub-500ms kernel-isolated MicroVM (Firecracker / gVisor) or process jail execution.
- `percipience oidc token / exchange` - RS256 workload token minting & cloud IAM federation (AWS STS / GCP).
- `percipience license status / mint` - Ed25519 commercial tier license generation, validation, and quotas.
- `percipience worktree acquire / release` - Ephemeral isolated Git worktrees with TTL and POSIX PID probing.
- `percipience daemon status / prune` - High-throughput native Tree-Sitter AST daemon client.
- `percipience tokens summary` - Displays token savings, FinOps gross ROI, and 15% rev-share performance fees.
- `percipience bot deploy / command` - GitOps PR Gatekeeper bot deployment and slash-command automation.

## In-Session Slash Commands
- `/refresh-context`: Synchronize and refresh the active AST context if codebase structures change.
- `/percipience`: Execute standard gatekeeper, audit, and FinOps diagnostics.
