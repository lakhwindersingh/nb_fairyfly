# IntelliJ IDEA & PyCharm Plugin Contracts Registry

## Machine-Readable Contracts
| Contract File | Schema Standard | Description |
| :--- | :--- | :--- |
| `.nb/context/contracts/intellij_plugin_manifest_contract.json` | JSON Schema Draft-07 | Plugin XML and Gradle configuration metadata |
| `.nb/context/contracts/psi_ast_bridge_contract.yaml` | YAML Spec | In-memory PSI extraction and AST skeletonization interface |
| `.nb/context/contracts/daemon_rpc_contract.json` | JSON-RPC 2.0 | IPC protocol between IntelliJ plugin and CLI daemon |
| `.nb/context/contracts/sandbox_permission_contract.json` | JSON Schema Draft-07 | Multi-tier sandbox source permissions for third-party LLMs |
