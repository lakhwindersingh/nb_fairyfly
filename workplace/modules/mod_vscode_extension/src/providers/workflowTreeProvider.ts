import * as vscode from 'vscode';

export class WorkflowTreeProvider implements vscode.TreeDataProvider<WorkflowItem> {
  getTreeItem(element: WorkflowItem): vscode.TreeItem {
    return element;
  }

  getChildren(_element?: WorkflowItem): Thenable<WorkflowItem[]> {
    return Promise.resolve([
      new WorkflowItem('vscode_plugin_delivery_flow', 'Active - [✔ HEALTHY]', vscode.TreeItemCollapsibleState.None),
      new WorkflowItem('intellij_pycharm_plugin_delivery_flow', 'Ready - [✔ HEALTHY]', vscode.TreeItemCollapsibleState.None),
      new WorkflowItem('pr_gatekeeper', 'Idle', vscode.TreeItemCollapsibleState.None)
    ]);
  }
}

export class WorkflowItem extends vscode.TreeItem {
  constructor(
    public readonly label: string,
    private readonly status: string,
    public readonly collapsibleState: vscode.TreeCollapsibleState
  ) {
    super(label, collapsibleState);
    this.description = this.status;
    this.tooltip = `${this.label} - ${this.status}`;
  }
}
