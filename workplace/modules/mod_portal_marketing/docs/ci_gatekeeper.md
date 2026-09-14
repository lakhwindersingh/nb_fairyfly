# CI/CD Gatekeeper & PR Verification Integration

Percipience acts as an autonomous gatekeeper across GitHub Actions, GitLab CI, and Bitbucket Pipelines.

## Core Gatekeeper Steps
1. **AST Symbol Pruning**: Strips function bodies from diffs to verify structural signatures in under 15ms.
2. **Contract Compatibility**: Validates that producer and consumer data models align in `context/contracts/`.
3. **Bounded TDD Loop**: Executes tests up to 3 retries; isolates failing tests into quarantine.
4. **Merkle Block Sealing**: Appends a SHA-256 block hash to `context/ledger/context_ledger.yaml`.

## GitHub Actions Example
```yaml
- name: Run Percipience Gatekeeper
  run: |
    percipience gate
    percipience audit --enforce-merkle-chain --min-maturity 0.85
```
