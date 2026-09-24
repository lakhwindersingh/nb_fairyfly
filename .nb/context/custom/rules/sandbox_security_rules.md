# JetBrains Sandbox & LLM Cross-Plugin Security Invariants

> **Governing Plan**: [Parent Master Context Engineering Plan](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/claude-context-engineering-parent-master-plan.md)  
> **Enforcement Engine**: `SandboxPermissionBroker` (IntelliJ Platform Plugin)

## 1. Token Reduction by Default
- All cross-plugin source code read requests from sandboxed LLM plugins (`com.intellij.ai`, `com.github.copilot`, `com.continue.continue`, `com.sourcegraph.cody`) MUST receive **AST-pruned token representations** (`READ_PRUNED_AST`) by default.
- Implementation function bodies are stripped in memory, returning symbol signatures, class hierarchies, and docstrings (yielding 60%–80% token savings).

## 2. Merkle Ledger & Platform Invariant WORM Protection
- Write access to `.nb/context/ledger/`, `context/ledger/`, `.nb/context/invariants/`, and governing plans is strictly prohibited for third-party sandboxed plugins.
- Any attempt to modify ledger files from a sandboxed plugin is immediately blocked (`DENIED`) and recorded as a security audit violation.

## 3. Sandboxed Worktree Isolation for Agent Writes
- Sandboxed LLM agents generating code modifications must write to isolated ephemeral review worktrees (`.nb/workspaces/`) or provide unified diffs, never mutating main branch files directly without verification gate approval.
