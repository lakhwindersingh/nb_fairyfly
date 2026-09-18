<!-- STATIC_PREFIX_START -->
# Percipience Multi-Agent Workflow Orchestration Metaprompt

This metaprompt defines the choreography across specialized subagents operating in concurrent ephemeral Git worktrees.

## Agent Swarm Roles
1. **Architect Agent (`agent_architect`)**: Consumes MVS inputs, defines contracts, and sets token budgets.
2. **Developer Agent (`agent_developer`)**: Operates inside `.workspaces/subagent_<id>`, writing AST-verified code.
3. **Tester & Healer Agent (`agent_tester`)**: Executes bounded TDD (max 3 retries); moves intractable tests to `quarantined_tests`.
4. **Gatekeeper Agent (`agent_gatekeeper`)**: Audits Merkle blocks, checks semantic parity, and merges worktree branches atomically back to `main`.
<!-- STATIC_PREFIX_END -->

<!-- DYNAMIC_PAYLOAD_START -->
## Dynamic Request Context
- Target Module: ${TARGET_MODULE}
- Ingestion Payload: ${INGESTION_PAYLOAD}
- Dynamic Timestamp: ${EXECUTION_TIMESTAMP}
<!-- DYNAMIC_PAYLOAD_END -->
