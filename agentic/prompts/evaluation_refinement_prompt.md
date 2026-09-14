# Percipience Evaluation & Refinement Metaprompt

This metaprompt evaluates codebase health, audit compliance, and context maturity.

## Evaluation Dimensions
1. **Requirement Coverage**: Validate each Gherkin scenario and acceptance criteria against AST nodes.
2. **Architectural Grounding**: Ensure no module bypasses `context/contracts/` or breaks Quad-Space boundaries.
3. **Code & Config Quality**: Verify linting, typing, zero hardcoded secrets, and cyclomatic complexity limits.
4. **Test & Verification Coverage**: Check unit/integration test pass rates and bounded self-healing logs.
5. **Security & Compliance**: Check Merkle chain integrity, Ed25519 signatures, and zero-knowledge hydration.
6. **Token & GenAI Efficiency**: Measure token compression ratio and prompt cache hit rate.

Output evaluated scorecard to `user/outputs/context_maturity_report.md`.
