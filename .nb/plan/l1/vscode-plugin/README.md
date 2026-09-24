# L1 Domain Plan: Visual Studio Code Extension Space

**Plan ID**: `domain_vscode_plugin`  
**Capability Rating**: `L1 Foundation (IDE Space)`  
**Version**: `1.0.0`  

## Overview

This domain plan defines the architecture and implementation for the VSCode extension, delivering Language Server Protocol (LSP 3.17) integration, dynamic tier-permission-aware Webview dashboards, synced Control Plane action buttons, and status bar telemetry.

## Quick Links

- **Concise Plan**: [concise.md](./concise.md) — Compact domain specification (~100 lines)
- **Detailed Plan**: [detailed.md](./detailed.md) — Extended LSP 3.17 & Webview implementation guide (~370 lines)
- **Version Manifest**: [MANIFEST.yaml](./MANIFEST.yaml) — Cryptographic SHA-256 version ledger

## Key Features

- **VSCode Extension API & VSIX Packaging**: TypeScript-based extension bundled with `esbuild`.
- **Dynamic Tier-Aware Control Plane**: Synced with IntelliJ plugin, dynamically rendering Free, Team, Business, and Enterprise action buttons.
- **Separate Tier VSIX Bundles**: Dedicated packaged distributions in `.nb/bundles/` (`free`, `team`, `business`, `enterprise`, and universal) for staging and permission verification.
- **Language Server Protocol (LSP 3.17)**: Detached Node.js server with CodeLens, diagnostics, and contract validation.
- **Secure Webview Panel**: Nonce-based CSP protected visualizer matching active IDE themes.
- **Activity Bar TreeDataProvider**: Collapsible views for workflows, agent registries, and Merkle recovery points.

## Success Criteria

- 100% passing tests in `workplace/tests/test_ide_plugins_space.py`.
- Strict CSP compliance with zero inline script vulnerabilities.
- Real-time Merkle chain status indicators in the VSCode status bar.
- Complete action hierarchy parity between VSCode and IntelliJ Control Planes.
