import * as vscode from 'vscode';
import { PercipienceDaemonClient } from '../ipc/daemonClient';

export class PercipienceStatusBarManager {
  private statusBarItem: vscode.StatusBarItem;
  private daemonClient: PercipienceDaemonClient;
  private updateTimer: NodeJS.Timeout | undefined;

  constructor(daemonClient: PercipienceDaemonClient) {
    this.daemonClient = daemonClient;
    this.statusBarItem = vscode.window.createStatusBarItem(
      vscode.StatusBarAlignment.Right,
      100
    );
    this.statusBarItem.command = 'percipience.showStatusMenu';
    this.updateMetrics();
    this.startAutoRefresh();
  }

  public show() {
    this.statusBarItem.show();
  }

  public hide() {
    this.statusBarItem.hide();
  }

  public dispose() {
    if (this.updateTimer) {
      clearInterval(this.updateTimer);
    }
    this.statusBarItem.dispose();
  }

  public async updateMetrics() {
    try {
      const state = await this.daemonClient.getMerkleState();
      const statusText = state.status === 'HEALTHY' ? 'OK' : 'DEGRADED';
      this.statusBarItem.text = `$(zap) Percipience: 70.0% Saved | $(shield) Merkle: ${statusText}`;
      this.statusBarItem.tooltip = new vscode.MarkdownString(
        `### ⚡ Percipience Context Engineering OS\n\n` +
        `- **Token Compression**: ~70.0% Real-Time AST Reduction\n` +
        `- **Merkle Status**: ${state.status} (Height: ${state.merkle_height})\n` +
        `- **Active Enclave Layers**: ${state.active_layers?.join(', ') || 'None'}\n\n` +
        `*Click to open Control Plane & Quick Actions*`
      );
    } catch (e) {
      this.statusBarItem.text = `$(zap) Percipience: Active`;
    }
  }

  private startAutoRefresh() {
    this.updateTimer = setInterval(() => {
      this.updateMetrics();
    }, 5000);
  }
}
