# VSCode Secret Storage Standards

1. **vscode.SecretStorage Integration**:
   - API keys, daemon auth tokens, and cryptographic signing keys MUST be stored exclusively in `context.secrets` (`vscode.SecretStorage`).
   - Plaintext persistence in `workspaceState` or configuration settings files (`settings.json`) is strictly prohibited.
