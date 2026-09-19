# JetBrains Platform Threading & PSI Invariants

1. **Absolute Event Dispatch Thread (EDT) Freedom**:
   - Network requests, JSON-RPC IPC calls, and heavy AST token calculations MUST NEVER run on the EDT.
   - All external execution must use Kotlin Coroutines (`withContext(Dispatchers.Default)`) or `ProgressManager.getInstance().run(Task.Backgroundable)`.
   - UI updates to ToolWindows and editor popups MUST be dispatched via `Dispatchers.EDT` or `ApplicationManager.getApplication().invokeLater()`.

2. **Read/Write Lock Synchronization**:
   - All PSI tree reads must occur inside a read action (`runReadAction`).
   - All modifications to documents or workspace files must execute inside a write action (`runWriteAction`) within a Command (`CommandProcessor.getInstance().executeCommand()`).
   - If the IDE is in "Dumb Mode" (indexing), PSI resolution features must either defer execution via `DumbService.getInstance(project).runWhenSmart()` or display informative placeholder badges.

3. **JCEF Webview Security Constraints**:
   - Java Chromium Embedded Framework (JCEF) browser instances hosting the Percipience Dashboard must enforce strict Content-Security-Policy (CSP) with `script-src 'self'`.
   - Communication between JCEF JavaScript and the Kotlin plugin layer must use asynchronous query handlers (`CefMessageRouterHandlerAdapter`) with verified request nonce validation.
