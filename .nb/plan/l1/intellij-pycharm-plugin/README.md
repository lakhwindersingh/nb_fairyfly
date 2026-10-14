# L1 Domain Plan: IntelliJ IDEA & PyCharm Plugin Space

**Plan ID**: `domain_intellij_pycharm_plugin`  
**Capability Rating**: `L1 Foundation (IDE Space)`  
**Version**: `1.3.0`  

## Overview

This domain plan specifies the architecture and implementation for the JetBrains Platform SDK plugin (IntelliJ IDEA & PyCharm), enabling PSI-based AST token optimization, embedded JCEF control plane dashboards, dynamic tier-permission-aware Control Plane button rendering, seamless Model Context Protocol (MCP) agent interoperability across all tiers, and seamless background CLI orchestration.

## Quick Links

- **Concise Plan**: [concise.md](./concise.md) — Compact domain specification (~90 lines)
- **Detailed Plan**: [detailed.md](./detailed.md) — Extended JetBrains SDK implementation guide (~450 lines)
- **Version Manifest**: [MANIFEST.yaml](./MANIFEST.yaml) — Cryptographic SHA-256 version ledger

## Key Features

- **JetBrains Platform SDK Integration**: Kotlin-based plugin with Gradle IntelliJ Platform tools.
- **Dynamic Tier-Aware Control Plane**: Dynamic button visibility and action entitlement based on active license (`plan_free`, `plan_team`, `plan_business`, `plan_enterprise`).
- **Separate Tier Plugin Bundles**: Dedicated packaged distributions in `.nb/bundles/` (`free`, `team`, `business`, `enterprise`, and universal) for staging and test verification.
- **Tier-Gated Workflow & Hook Bundling**: Each tier bundle embeds the tier-appropriate autonomous delivery flows (`percipience/workflows/`) and git pre-commit guardrail hooks (`percipience/hooks/pre-commit.sh` + `percipience/scripts/install_git_hook.sh`) directly inside the plugin JAR/ZIP, mirroring the `CORE_TIER_RULES` engine gating.
- **Model Context Protocol (MCP) Interoperability (All Bundles)**: Natively provisions `.claude/mcp.json` and `.claude/settings.json` across all plugin bundles (free or otherwise), enabling instant integration with Claude Desktop, Claude Code, Gemini CLI, Cursor, and terminal agents.
- **PSI AST Token Pruning**: Deep PSI walking for Python, Kotlin, Java, and TypeScript ($60-85\%$ token reduction).
- **Offline Local-Filesystem Auto-Upgrade**: Embeds a `percipience/version.json` manifest and scans local directories (`.nb/bundles`, `.nb/updates`, `~/.percipience/updates`, `PERCIPIENCE_UPDATE_DIR`) for newer builds, then upgrades the workspace runtime in place — fully air-gapped.
- **JCEF ToolWindow**: Dockable embedded Chromium browser rendering real-time Merkle DAG chains and telemetry.
- **Background Execution Coroutines**: Non-blocking process execution via `PercipienceExecutionService`.

## Success Criteria

- 100% passing tests in `workplace/tests/test_ide_plugins_space.py`.
- Non-blocking EDT operations across all PSI and CLI actions.
- Automatic provisioning of `.claude/mcp.json` and `.claude/settings.json` in every bootstrapped workspace.
- Zero-drift Merkle ledger synchronization with IDE ToolWindow.
- Accurate dynamic button rendering matching active license tier.
