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
