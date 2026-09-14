# Percipience Lifecycle & Delivery Metaprompt

This metaprompt controls the release, packaging, and CI/CD gatekeeper lifecycle.

## Delivery Protocols
1. **Verification Gate Sweep**:
   - `gate_contract_compatibility`: Verify producer/consumer schema alignment.
   - `gate_test_verification`: Confirm 100% test pass rate within 3-retry budget.
   - `gate_security_audit`: Scan for secrets and vulnerable AST patterns.
2. **Ledger Block Sealing**:
   - Calculate Merkle root of touched files: $H_i = \text{SHA256}(H_{i-1} + \Delta_i + T_i)$.
   - Record new recovery point snapshot ($RP_k$) and append block to `context/ledger/context_ledger.yaml`.
3. **Packaging & Obfuscation**:
   - Run `plan_pack_compiler.py` to encrypt proprietary prompt trees and schemas into `.nbpack`.
4. **Git Commit & Push**:
   - Issue semantic Git commit linking SHA to requirement IDs.
