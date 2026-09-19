import * as vscode from 'vscode';

export class AgentTreeProvider implements vscode.TreeDataProvider<AgentItem> {
  getTreeItem(element: AgentItem): vscode.TreeItem {
    return element;
  }

  getChildren(_element?: AgentItem): Thenable<AgentItem[]> {
    return Promise.resolve([
      new AgentItem('agent_vscode_extension_architect', 'Tier_A (Expert)', vscode.TreeItemCollapsibleState.None),
      new AgentItem('agent_lsp_language_features_specialist', 'Tier_B (Specialist)', vscode.TreeItemCollapsibleState.None),
      new AgentItem('agent_vscode_webview_ux_engineer', 'Tier_A (UI/UX)', vscode.TreeItemCollapsibleState.None),
      new AgentItem('agent_jetbrains_plugin_architect', 'Tier_A (Expert)', vscode.TreeItemCollapsibleState.None)
    ]);
  }
}

export class AgentItem extends vscode.TreeItem {
  constructor(
    public readonly label: string,
    private readonly tier: string,
    public readonly collapsibleState: vscode.TreeCollapsibleState
  ) {
    super(label, collapsibleState);
    this.description = this.tier;
  }
}
