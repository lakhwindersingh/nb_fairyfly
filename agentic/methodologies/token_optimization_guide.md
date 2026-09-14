# Token Optimization & AST Compression Methodology

## Principles
1. **Structural Symbol Extraction**:
   - Transmit symbol declarations (exported classes, method signatures, return types) rather than full method bodies during architectural exploration.
2. **Unified Diff Context Passing**:
   - When modifying files, transmit standard unified diff hunks (`@@ -12,5 +12,6 @@`) instead of full file retransmissions.
3. **Static Prompt Cache Alignment**:
   - Keep system instructions, tool definitions, and baseline architectural contracts strictly in the prefix of the conversation context to achieve $> 85\%$ prompt cache hits.
4. **Three-Tier Context Allocation**:
   - **Tier 1 (Working Memory)**: Active turn AST diffs and immediate unit test output.
   - **Tier 2 (Ledger Summary)**: Merkle chain height, active recovery point, and contract registry.
   - **Tier 3 (Archived Artifacts)**: Raw logs and full code files, stored on disk or WORM storage and loaded only on explicit demand.
