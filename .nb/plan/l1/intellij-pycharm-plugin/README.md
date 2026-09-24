# L1 Domain Plan: IntelliJ IDEA & PyCharm Plugin Space

**Plan ID**: `domain_intellij_pycharm_plugin`  
**Capability Rating**: `L1 Foundation (IDE Space)`  
**Version**: `1.0.0`  

## Overview

This domain plan specifies the architecture and implementation for the JetBrains Platform SDK plugin (IntelliJ IDEA & PyCharm), enabling PSI-based AST token optimization, embedded JCEF control plane dashboards, and seamless background CLI orchestration.

## Quick Links

- **Concise Plan**: [concise.md](./concise.md) — Compact domain specification (~330 lines)
- **Detailed Plan**: [detailed.md](./detailed.md) — Extended JetBrains SDK implementation guide (~140 lines)
- **Version Manifest**: [MANIFEST.yaml](./MANIFEST.yaml) — Cryptographic SHA-256 version ledger

## Key Features

- **JetBrains Platform SDK Integration**: Kotlin-based plugin with Gradle IntelliJ Platform tools.
- **PSI AST Token Pruning**: Deep PSI walking for Python, Kotlin, Java, and TypeScript ($60-85\%$ token reduction).
- **JCEF ToolWindow**: Dockable embedded Chromium browser rendering real-time Merkle DAG chains and telemetry.
- **Background Execution Coroutines**: Non-blocking process execution via `PercipienceExecutionService`.

## Success Criteria

- 100% passing tests in `workplace/tests/test_ide_plugins_space.py`.
- Non-blocking EDT operations across all PSI and CLI actions.
- Zero-drift Merkle ledger synchronization with IDE ToolWindow.
