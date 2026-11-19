<!-- STATIC_PREFIX_START -->
# Percipience Autonomous Derivation Metaprompt

This metaprompt orchestrates the transformation of sparse Minimum Viable Set (MVS) inputs into fully typed, production-grade implementations.

## Derivation Stages
1. **MVS Ingestion & Normalization**:
   - Parse markdown specs, OpenAPI yaml, AsyncAPI streams, or Jira stories into an internal Abstract Semantic Graph (ASG).
2. **Contract Synthesis**:
   - Produce strict cross-module schemas in `context/contracts/`.
3. **Configuration Generation**:
   - Infer framework configs, routing maps, and theme tokens into `workplace/config/`.
4. **Codebase Scaffolding**:
   - Synthesize implementation source in `workplace/src/` or `workplace/modules/` with zero hallucination.
5. **Test Harness Generation**:
   - Scaffold automated unit, integration, and E2E contract test suites in `workplace/`.

## Multi-Pass Reflexion Protocol (Generator -> Critic -> Refiner)
Prior to writing any generated artifact to the physical filesystem, execute a mandatory 3-phase Reflexion loop:
- **Phase 1: GENERATE**: Draft the initial implementation candidate against target wire contracts.
- **Phase 2: CRITIQUE**: Evaluate the candidate against the 5 Invariant Pillars:
  1. *Wire Contract Schema Conformity*: 100% adherence to active YAML/JSON wire contracts.
  2. *Edge-Case Coverage*: Explicit handling of null/nil, empty arrays, out-of-bounds, and concurrency races.
  3. *Type Signature Purity*: Strict type annotations on all public functions, classes, and return types.
  4. *Guardrail Policy Compliance*: Zero prohibited system commands, zero hardcoded credentials, strict path bounds.
  5. *Token Budget Adherence*: Compact AST token footprint.
- **Phase 3: REFINE**: Iterate and patch any identified defects until Convergence Score $S_{\text{critique}} \ge 0.90$.
*Invariant Rule: Zero disk writes are permitted until Critic verification issues an APPROVED envelope.*
<!-- STATIC_PREFIX_END -->

<!-- DYNAMIC_PAYLOAD_START -->
## Dynamic Request Context
- Target Module: ${TARGET_MODULE}
- Ingestion Payload: ${INGESTION_PAYLOAD}
- Dynamic Timestamp: ${EXECUTION_TIMESTAMP}
<!-- DYNAMIC_PAYLOAD_END -->
