import * as vscode from 'vscode';
import { PercipienceDaemonClient } from '../ipc/daemonClient';

export class DashboardPanel {
  public static currentPanel: DashboardPanel | undefined;
  private readonly panel: vscode.WebviewPanel;
  private disposables: vscode.Disposable[] = [];

  private constructor(
    panel: vscode.WebviewPanel,
    private readonly extensionUri: vscode.Uri,
    private readonly daemonClient: PercipienceDaemonClient
  ) {
    this.panel = panel;
    this.panel.webview.html = this.getHtmlForWebview();
    this.panel.onDidDispose(() => this.dispose(), null, this.disposables);

    this.panel.webview.onDidReceiveMessage(
      async (message) => {
        switch (message.command) {
          case 'fetch_merkle_state':
            const state = await this.daemonClient.getMerkleState();
            this.panel.webview.postMessage({ type: 'MERKLE_STATE_UPDATE', payload: state });
            break;
        }
      },
      null,
      this.disposables
    );
  }

  public static createOrShow(extensionUri: vscode.Uri, daemonClient: PercipienceDaemonClient) {
    const column = vscode.window.activeTextEditor
      ? vscode.window.activeTextEditor.viewColumn
      : undefined;

    if (DashboardPanel.currentPanel) {
      DashboardPanel.currentPanel.panel.reveal(column);
      return;
    }

    const panel = vscode.window.createWebviewPanel(
      'percipienceDashboard',
      'Percipience Control Plane',
      column || vscode.ViewColumn.One,
      {
        enableScripts: true,
        retainContextWhenHidden: true
      }
    );

    DashboardPanel.currentPanel = new DashboardPanel(panel, extensionUri, daemonClient);
  }

  private getHtmlForWebview(): string {
    const nonce = getNonce();
    return `<!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'nonce-${nonce}';">
      <title>Percipience Control Plane</title>
      <style>
        body { font-family: var(--vscode-font-family); background: var(--vscode-editor-background); color: var(--vscode-editor-foreground); padding: 20px; }
        .card { background: var(--vscode-sideBar-background); padding: 15px; border-radius: 6px; margin-bottom: 12px; border: 1px solid var(--vscode-widget-border); }
        .badge { background: #00d2ff; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 11px; }
      </style>
    </head>
    <body>
      <h2>⚡ Percipience Context Engineering OS</h2>
      <div class="card">
        <span class="badge">Merkle Chain Sealed</span>
        <p>Real-time autonomous SDLC governance active in workspace.</p>
      </div>
    </body>
    </html>`;
  }

  public dispose() {
    DashboardPanel.currentPanel = undefined;
    this.panel.dispose();
    while (this.disposables.length) {
      const x = this.disposables.pop();
      if (x) {
        x.dispose();
      }
    }
  }
}

function getNonce() {
  let text = '';
  const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  for (let i = 0; i < 32; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
}
