# VSCode Activation Invariants

1. **Targeted Activation Events**:
   - `package.json` `activationEvents` MUST explicitly enumerate selective event triggers:
     - `workspaceContains:.nb`
     - `onCommand:percipience.openDashboard`
     - `onCommand:percipience.executeWorkflow`
     - `onLanguage:yaml`
     - `onLanguage:json`
   - Wildcard `"*"` activation is strictly forbidden and rejected at CI gate.
