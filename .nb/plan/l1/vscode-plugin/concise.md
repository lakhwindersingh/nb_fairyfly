---
plan_type: "layerable_domain_plan"
plan_id: "domain_vscode_plugin"
name: "Visual Studio Code Extension, Language Server Protocol & Percipience Control Plane Space"
parent_master_plan: "master/parent-master-plan/concise.md"
tier_mapping:
  tier_2: "Enterprise Domain Rules & Wire Contracts (.nb/context/contracts/, .nb/context/rules/)"
  tier_3: "Specialist Subagents & Delivery Workflows (.nb/agentic/custom/agents/, .nb/agentic/custom/workflows/)"
model_tiering_policy:
  provider_agnostic: true
  tier_a_model: "claude-3-7-sonnet / pro"
  tier_b_model: "claude-3-5-haiku / flash"
---

# Layerable Context Engineering Plan: Visual Studio Code Extension Space (Concise Plan)

### Executive Overview & Domain Grounding

This document is a **Layerable Domain-Specific Context Engineering Plan** designed to overlay onto the generic **Parent Master Context Engineering Framework**. It injects concrete IDE integration patterns, VSCode Extension API protocols, Language Server Protocol (LSP 3.17) implementations, and Webview UI orchestration required for:

1. **VSCode Extension API & VSIX Packaging Architecture**: TypeScript extension built with `esbuild`, Activity Bar tree views (`agentTreeProvider.ts`, `workflowTreeProvider.ts`), and status bar telemetry (`statusBarManager.ts`).
2. **Language Server Protocol (LSP 3.17) Client-Server Subsystem**: Detached Node.js language server (`lspServer.ts`, `lspClient.ts`) with in-editor CodeLens triggers (`codeLensProvider.ts`), contract validation, and real-time diagnostic annotators (`diagnosticProvider.ts`).
3. **Secure Webview Panel & Interactive Visualizer**: Nonce-based CSP protected visualizer (`dashboardPanel.ts`) matching active VSCode themes.

```mermaid
graph TD
  subgraph VSCode_Extension_Host["VSCode Extension Host Process"]
    ActivityBar["Activity Bar TreeDataProvider"]
    CodeLens["In-Editor CodeLens Providers"]
    StatusBar["Status Bar Merkle & Token Monitors"]
    LspClient["LSP 3.17 Client Layer"]
    WebviewPanel["Isolated Webview Panel"]
  end

  subgraph Detached_LSP_Server["Detached Node.js LSP Server"]
    LspServer["vscode-languageserver/node (lspServer.ts)"]
  end

  subgraph Local_Platform[".nb/ Platform System"]
    PlatformCli[".nb/bin/percipience"]
    LedgerFile[".nb/context/ledger/context_ledger.yaml"]
  end

  LspClient <-->|JSON-RPC via stdio| LspServer
  ActivityBar --> PlatformCli
  WebviewPanel --> PlatformCli
  PlatformCli --> LedgerFile
```

---

## 1. Domain-Specific Quad-Space Mapping

- `.nb/context/contracts/`: `package_json_manifest_contract.json`, `lsp_protocol_contract.yaml`, `webview_message_rpc_contract.json`
- `.nb/context/rules/`: `webview_security_invariants.md`, `vscode_activation_invariants.md`, `secret_storage_rules.md`
- `.nb/agentic/custom/agents/`: `agent_vscode_extension_architect.yaml`, `agent_lsp_language_features_specialist.yaml`, `agent_vscode_webview_ux_engineer.yaml`
- `workplace/modules/mod_vscode_extension/`: TypeScript extension, language server, and VSIX bundle.
- `user/outputs/`: Status telemetry and Webview dashboard feeds.

---

## 2. CLI & Layer Management

```bash
# Package layer bundle
./.nb/bin/percipience layer pack --plan .nb/plan/l1/vscode-plugin/concise.md --output .nb/bundles/vscode_plugin_domain.nbpack

# Apply layer bundle
./.nb/bin/percipience layer apply --pack .nb/bundles/vscode_plugin_domain.nbpack --in-memory-only
```
