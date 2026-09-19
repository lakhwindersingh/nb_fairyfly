import * as vscode from 'vscode';
import { PercipienceLspClient } from './lsp/lspClient';
import { WorkflowTreeProvider } from './providers/workflowTreeProvider';
import { AgentTreeProvider } from './providers/agentTreeProvider';
import { DashboardPanel } from './webview/dashboardPanel';
import { PercipienceDaemonClient } from './ipc/daemonClient';

let lspClient: PercipienceLspClient;

export function activate(context: vscode.ExtensionContext) {
  console.log('Percipience Context Engineering OS activated.');

  // Initialize Daemon IPC Client
  const daemonClient = new PercipienceDaemonClient();

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
    })
  );

  // Start LSP Client
  lspClient = new PercipienceLspClient(context);
  lspClient.start();
}

export function deactivate(): Thenable<void> | undefined {
  if (!lspClient) {
    return undefined;
  }
  return lspClient.stop();
}
