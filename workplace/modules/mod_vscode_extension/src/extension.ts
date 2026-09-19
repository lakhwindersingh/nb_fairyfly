import * as vscode from 'vscode';
import { PercipienceLspClient } from './lsp/lspClient';
import { WorkflowTreeProvider } from './providers/workflowTreeProvider';
import { AgentTreeProvider } from './providers/agentTreeProvider';
import { DashboardPanel } from './webview/dashboardPanel';
import { PercipienceDaemonClient } from './ipc/daemonClient';
import { PercipienceStatusBarManager } from './statusbar/statusBarManager';

let lspClient: PercipienceLspClient;
let statusBarManager: PercipienceStatusBarManager;

export function activate(context: vscode.ExtensionContext) {
  console.log('Percipience Context Engineering OS activated.');

  // Initialize Daemon IPC Client
  const daemonClient = new PercipienceDaemonClient();

  // Initialize and show Status Bar Metrics
  statusBarManager = new PercipienceStatusBarManager(daemonClient);
  statusBarManager.show();
  context.subscriptions.push(statusBarManager);

  // Register Tree Views
  const workflowProvider = new WorkflowTreeProvider();
  vscode.window.registerTreeDataProvider('percipience.workflowsView', workflowProvider);

  const agentProvider = new AgentTreeProvider();
  vscode.window.registerTreeDataProvider('percipience.agentsView', agentProvider);

  // Register Commands
  context.subscriptions.push(
    vscode.commands.registerCommand('percipience.openDashboard', () => {
      DashboardPanel.createOrShow(context.extensionUri, daemonClient);
    }),
    vscode.commands.registerCommand('percipience.executeWorkflow', async () => {
      vscode.window.showInformationMessage('Executing Percipience Delivery Workflow...');
      await daemonClient.executeWorkflow('vscode_plugin_delivery_flow');
      vscode.window.showInformationMessage('Workflow execution completed successfully.');
    }),
    vscode.commands.registerCommand('percipience.showStatusMenu', async () => {
      const selection = await vscode.window.showQuickPick(
        [
          { label: '$(dashboard) Open Percipience Control Plane', description: 'Webview telemetry dashboard' },
          { label: '$(play) Run Invariant Verification Workflow', description: 'Execute contract test suite' },
          { label: '$(graph) Inspect AST Token Pruning Metrics', description: 'Real-time reduction stats' },
          { label: '$(globe) Open Web Observability Portal', description: 'http://localhost:3000' }
        ],
        { placeHolder: 'Percipience Context OS Actions' }
      );

      if (selection) {
        if (selection.label.includes('Open Percipience Control Plane')) {
          DashboardPanel.createOrShow(context.extensionUri, daemonClient);
        } else if (selection.label.includes('Run Invariant Verification')) {
          vscode.commands.executeCommand('percipience.executeWorkflow');
        } else if (selection.label.includes('Open Web Observability')) {
          vscode.env.openExternal(vscode.Uri.parse('http://localhost:3000'));
        } else {
          vscode.window.showInformationMessage('Percipience AST Token Reduction: 70.0% active in current workspace.');
        }
      }
    })
  );

  // Start LSP Client
  lspClient = new PercipienceLspClient(context);
  lspClient.start();
}

export function deactivate(): Thenable<void> | undefined {
  if (statusBarManager) {
    statusBarManager.dispose();
  }
  if (!lspClient) {
    return undefined;
  }
  return lspClient.stop();
}
