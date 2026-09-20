# Visual Studio Code Extension Space Architecture

> **Autonomously Maintained by**: `agent_vscode_extension_architect`  
> **Status**: ✅ Verified Valid Mermaid  
> **Canonical Target**: `workplace/modules/mod_vscode_extension/`

## 1. System Topology & Component Layout

```mermaid
graph TD
  subgraph VSCode_Host["VSCode Extension Host"]
    Ext["Extension Entrypoint<br/>(src/extension.ts)"]
    LSP["Language Server Client<br/>(vscode-languageclient/node)"]
    TreeViews["TreeDataProvider Views<br/>(Workflows, Agents, Merkle)"]
    StatusBar["StatusBar Item<br/>(Live Token Savings & Merkle Seal)"]
    Webview["Webview Panel<br/>(percipience.dashboard)"]
  end

  subgraph LanguageServer["LSP 3.17 Server Process"]
    LSPServer["LanguageServer Daemon<br/>(CodeLens, Diagnostics, Hovers)"]
    SchemaVal["Contract Schema Validator<br/>(JSON/YAML AST Validator)"]
  end

  subgraph Local_Daemon["Local Percipience Control Plane"]
    Daemon["JSON-RPC Socket Client<br/>(daemonClient.ts)"]
    Merkle["Merkle State Chain<br/>(context_ledger.yaml)"]
  end

  Ext --> LSP
  Ext --> TreeViews
  Ext --> StatusBar
  Ext --> Webview
  LSP --> LSPServer
  LSPServer --> SchemaVal
  Ext --> Daemon
  Daemon --> Merkle
```
