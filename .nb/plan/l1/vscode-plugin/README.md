# L1 Domain Plan: Visual Studio Code Extension Space

**Plan ID**: `domain_vscode_plugin`  
**Capability Rating**: `L1 Foundation (IDE Space)`  
**Version**: `1.0.0`  

## Overview

This domain plan defines the architecture and implementation for the VSCode extension, delivering Language Server Protocol (LSP 3.17) integration, interactive Webview dashboards, and status bar telemetry.

## Quick Links

- **Concise Plan**: [concise.md](./concise.md) — Compact domain specification (~325 lines)
- **Detailed Plan**: [detailed.md](./detailed.md) — Extended LSP 3.17 & Webview implementation guide (~130 lines)
- **Version Manifest**: [MANIFEST.yaml](./MANIFEST.yaml) — Cryptographic SHA-256 version ledger

## Key Features

- **VSCode Extension API & VSIX Packaging**: TypeScript-based extension bundled with `esbuild`.
- **Language Server Protocol (LSP 3.17)**: Detached Node.js server with CodeLens, diagnostics, and contract validation.
- **Secure Webview Panel**: Nonce-based CSP protected visualizer matching active IDE themes.
- **Activity Bar TreeDataProvider**: Collapsible views for workflows, agent registries, and Merkle recovery points.

## Success Criteria

- 100% passing tests in `workplace/tests/test_ide_plugins_space.py`.
- Strict CSP compliance with zero inline script vulnerabilities.
- Real-time Merkle chain status indicators in the VSCode status bar.
