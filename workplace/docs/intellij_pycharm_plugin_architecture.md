# IntelliJ IDEA & PyCharm Plugin Space Architecture

> **Autonomously Maintained by**: `agent_jetbrains_plugin_architect`  
> **Status**: ✅ Verified Valid Mermaid  
> **Canonical Target**: `workplace/modules/mod_intellij_plugin/`

## 1. System Topology & Component Layout

```mermaid
graph TD
  subgraph IDE_Platform["JetBrains Platform (IntelliJ IDEA / PyCharm)"]
    TW["PercipienceToolWindowFactory<br/>(5-Tab Swing Control Plane)"]
    SB["PercipienceStatusBarWidgetFactory<br/>(Live Token FinOps & Merkle Height)"]
    Boot["WorkspaceBootstrapper<br/>(Zero-Click Free Workspace Setup)"]
    Broker["SandboxPermissionBroker<br/>(AST Skeletonization & Classloader Shield)"]
    Bridge["PsiAstBridge<br/>(In-Memory PSI Tree Traversal <35ms)"]
  end

  subgraph Local_Daemon["Local Percipience Control Plane"]
    Daemon["JSON-RPC Daemon Bridge<br/>(daemon_rpc_contract.json)"]
    Merkle["Merkle State Chain<br/>(context_ledger.yaml)"]
    TokenFinOps["Token Savings Tracker<br/>(token_savings_ledger.yaml)"]
  end

  TW --> Bridge
  TW --> Boot
  SB --> TokenFinOps
  Bridge --> Broker
  Broker --> Daemon
  Daemon --> Merkle
```

## 2. Component Specifications
- **`PercipienceToolWindowFactory`**: Swing-safe multi-tab tool window presenting Control Plane, Sandbox Permissions, Capabilities, Agent Swarms, and User Guides without CSS parser NPEs.
- **`PercipienceStatusBarWidgetFactory`**: Real-time status bar widget tracking token savings ($0.003/1K tokens) and Merkle block height.
- **`SandboxPermissionBroker`**: Classloader-level permission broker routing third-party IDE AI plugins to skeletonized AST signatures.
- **`PsiAstBridge`**: High-performance PSI visitor traversing Python, Kotlin, Java, and TypeScript files in under 35ms.
