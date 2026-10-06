# Neutron Binary Percipience - Claude Code Guidelines

## Quad-Space Architecture & Hierarchy
This repository strictly adheres to the **Quad-Space context engineering architecture**:
- **`.nb/`**: Platform core engines, wire contracts, Merkle ledger, and CLI gatekeeper tooling.
- **`workplace/`**: Active modules, application packages, integration tests, and business logic.
- **`user/`**: Formal requests, input parameters, brand tokens, and audit artifacts.
- **`.claude/`**: Claude Code configurations, MCP server definitions, and custom commands.

## Mandatory AST Context Injection
- **Canonical Context Location**: The pre-computed, AST-pruned structural project context is maintained at:
  `[percipience_claude_context.md](file://.nb/context/percipience_claude_context.md)`
- **Schema & Contract Adherence**: Always respect the wire contracts, public API interfaces, and type schemas defined in `.nb/context/percipience_claude_context.md`.
- **Implementation Inspection**: Because `.nb/context/percipience_claude_context.md` contains AST-pruned skeletons to optimize token usage (~50–70% savings), full function bodies are omitted. When surgical refactoring or debugging deep logic is required, inspect specific target files directly in `workplace/` using file viewing tools.

## Platform Invariants & Tooling
- **Percipience CLI**: All platform operations are governed by `./.nb/bin/percipience`:
  - `percipience audit` - Cryptographic Merkle DAG audit & scorecard evaluation.
  - `percipience gate` - 7-stage CI/CD gatekeeper validating wire contracts and security invariants.
  - `percipience context sync` - Synchronizes and regenerates AST-pruned context.
  - `percipience tokens summary` - Displays token savings and FinOps metrics.
- **In-Session Context Refresh**: Run `/refresh-context` to refresh the active AST context if codebase structures change during a session.
