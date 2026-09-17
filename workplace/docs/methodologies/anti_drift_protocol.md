# Anti-Drift & Semantic Parity Protocol

## Metrics
- **Semantic Parity Score ($S_{SP}$)**: Range $0.00 \text{ to } 1.00$.
  - Calculated as the ratio of verified AST symbols mapped directly to MVS acceptance criteria.
  - Required gate threshold: $S_{SP} \ge 0.90$.

## Dual-Reconciliation Workflow
1. **Revert Mode (Automated)**:
   - If an agent generates unprompted dependencies or modifies unrelated files, the gatekeeper automatically generates a reverse diff to restore clean state.
2. **Evolve Mode (HITL Gated)**:
   - If the agent discovers a legitimate architectural necessity not covered in the MVS spec, it drafts a specification delta in `user/hitl/proposed_spec_delta.md`. Human approval is required before the delta is merged into `user/inputs/`.
