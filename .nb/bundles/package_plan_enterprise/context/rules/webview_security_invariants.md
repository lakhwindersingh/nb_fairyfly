# VSCode Webview Security & Activation Invariants

1. **Strict Content-Security-Policy (CSP)**:
   - Every Webview instance must render a dynamic CSP header:
     `default-src 'none'; img-src ${webview.cspSource} https: data:; script-src 'nonce-${nonce}'; style-src ${webview.cspSource} 'unsafe-inline'; font-src ${webview.cspSource};`.
   - Never load remote scripts directly from unvetted CDNs. All UI libraries (e.g., Mermaid.js, Webview Toolkit) must be locally bundled via `esbuild`.

2. **Asynchronous Bidirectional RPC Protocol**:
   - Communication between the Webview and the Extension Host must use `acquireVsCodeApi().postMessage()` validating a structured JSON-RPC message envelope with typed command routing.
   - Message payloads exceeding 1MB must be streamed via chunked transfer to avoid IPC buffer exhaustion.

3. **Lazy Activation Standard**:
   - The extension must NEVER activate globally on `*`.
   - Activation must strictly bind to precise triggers: `workspaceContains:.nb`, `onCommand:percipience.*`, and language IDs (`onLanguage:yaml`, `onLanguage:json`, `onLanguage:python`).
