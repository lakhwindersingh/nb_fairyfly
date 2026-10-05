# PSI Read Lock & DumbService Invariants

1. **Smart Mode Guarantee**:
   - Any feature requiring PSI type resolution or index querying must verify `DumbService.isDumb(project)` is false or queue execution via `DumbService.getInstance(project).runWhenSmart()`.

2. **Read Action Lifecycles**:
   - Heavy PSI traversals must check `ProgressIndicator.checkCanceled()` within iteration loops to gracefully yield to write actions requested by the user during typing.
