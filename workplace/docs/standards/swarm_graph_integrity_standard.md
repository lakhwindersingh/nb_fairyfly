# Swarm Graph Integrity & CBAC Security Standard

> **Status**: RATIFIED ARCHITECTURAL STANDARD  
> **Subsystem**: Dynamic Task DAGs (`CAP-AGT-01`), Swarm Governor (`CAP-31`), CBAC Sandboxing (`CAP-AGT-05`)  
> **Classification**: Core Invariant (Zero-Dial Configuration)

---

## 1. Dynamic Task DAG Acyclicity & Bound Invariants

Multi-agent coordination in Percipience relies on runtime topological task graphs (DAGs). To prevent runaway recursion and fork-bomb vulnerabilities:

1. **Kahn Acyclicity Invariant**:
   - Every dynamic sub-goal expansion must satisfy strict acyclicity:
     $$\mathcal{O}(V + E) \text{ topological sorting verification}.$$
   - Any dependency edge introducing a cycle is rejected with immediate `CYCLE_DEADLOCK_DETECTED`.
2. **Depth Ceiling ($D \le 3$)**:
   - Recursive task delegation is strictly bounded to a maximum tree depth of $3$.
3. **Node Ceiling ($N \le 20$)**:
   - Maximum active concurrent task nodes per wave is clamped at $20$.

---

## 2. Capability-Based Access Control (CBAC) Sandboxing

Every subagent spawned within an ephemeral worktree operates under cryptographic CBAC tokens:
- **HMAC-SHA256 Token Minting**: Tokens are cryptographically bound to `(agent_id, worktree_path, expiry)`.
- **Standard 1-Hour Lease**: Eliminates manual TTL configuration. Leases expire automatically after 3600 seconds.
- **Least-Privilege Scoping**: Subagents can read project files and write strictly within their isolated worktree directory (`.nb/workspaces/wt_*`). Direct writes to platform runtime paths (`.nb/core/`, `.nb/bin/`) are blocked at the filesystem kernel boundary.
