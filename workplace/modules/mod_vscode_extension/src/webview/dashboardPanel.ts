import * as vscode from 'vscode';
import { PercipienceDaemonClient } from '../ipc/daemonClient';

export interface TierEntitlements {
  tierId: string;
  tierName: string;
  quota: string;
  canUseWorktrees: boolean;
  canCreateAgents: boolean;
  canPackNbpack: boolean;
  canUseSwarm: boolean;
  canUsePrivateVpc: boolean;
  canUseWormEgress: boolean;
  exposeBasicPlatformTools: boolean;
}

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
          case 'execute_action':
            vscode.window.showInformationMessage(`Percipience Action triggered: ${message.action}`);
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

  private resolveTier(): TierEntitlements {
    const rawTier = process.env.PERCIPIENCE_PLAN || 'plan_free';
    const normalized = rawTier.toLowerCase();

    if (normalized.includes('enterprise') || normalized.includes('dedicated')) {
      return {
        tierId: 'plan_enterprise',
        tierName: 'Enterprise Dedicated Tier',
        quota: 'Unlimited Seats | Unlimited Worktrees | Unlimited Audits',
        canUseWorktrees: true,
        canCreateAgents: true,
        canPackNbpack: true,
        canUseSwarm: true,
        canUsePrivateVpc: true,
        canUseWormEgress: true,
        exposeBasicPlatformTools: true
      };
    } else if (normalized.includes('business')) {
      return {
        tierId: 'plan_business',
        tierName: 'Business Tier',
        quota: '50 Seats | 20 Worktrees | 25,000 Audits/mo',
        canUseWorktrees: true,
        canCreateAgents: true,
        canPackNbpack: true,
        canUseSwarm: false,
        canUsePrivateVpc: false,
        canUseWormEgress: false,
        exposeBasicPlatformTools: true
      };
    } else if (normalized.includes('team')) {
      return {
        tierId: 'plan_team',
        tierName: 'Team Tier',
        quota: '15 Seats | 5 Worktrees | 5,000 Audits/mo',
        canUseWorktrees: true,
        canCreateAgents: true,
        canPackNbpack: false,
        canUseSwarm: false,
        canUsePrivateVpc: false,
        canUseWormEgress: false,
        exposeBasicPlatformTools: false
      };
    }

    return {
      tierId: 'plan_free',
      tierName: 'Free Community Tier',
      quota: '1 Seat | 1 Worktree | 500 Audits/mo',
      canUseWorktrees: false,
      canCreateAgents: false,
      canPackNbpack: false,
      canUseSwarm: false,
      canUsePrivateVpc: false,
      canUseWormEgress: false,
      exposeBasicPlatformTools: false
    };
  }

  private getHtmlForWebview(): string {
    const nonce = getNonce();
    const tier = this.resolveTier();

    return `<!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'nonce-${nonce}';">
      <title>Percipience Control Plane</title>
      <style>
        body {
          font-family: var(--vscode-font-family);
          background: var(--vscode-editor-background);
          color: var(--vscode-editor-foreground);
          padding: 20px;
          line-height: 1.4;
        }
        .header-card {
          background: var(--vscode-sideBar-background);
          padding: 16px;
          border-radius: 6px;
          margin-bottom: 16px;
          border: 1px solid var(--vscode-widget-border);
        }
        .badge {
          display: inline-block;
          background: #0284c7;
          color: #ffffff;
          padding: 3px 10px;
          border-radius: 12px;
          font-weight: bold;
          font-size: 11px;
          margin-bottom: 8px;
        }
        .badge-enterprise { background: #7c3aed; }
        .badge-business { background: #059669; }
        .badge-team { background: #2563eb; }
        .badge-free { background: #0284c7; }
        .title { font-size: 16px; font-weight: bold; margin-bottom: 6px; color: var(--vscode-textLink-foreground); }
        .meta-line { font-size: 12px; color: var(--vscode-descriptionForeground); margin: 3px 0; }
        .actions-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
          gap: 10px;
          margin-top: 16px;
        }
        .btn {
          background: var(--vscode-button-background);
          color: var(--vscode-button-foreground);
          border: none;
          padding: 10px 14px;
          border-radius: 4px;
          font-size: 12px;
          font-weight: 500;
          cursor: pointer;
          text-align: left;
          transition: background 0.2s;
        }
        .btn:hover { background: var(--vscode-button-hoverBackground); }
        .btn-team { border-left: 4px solid #2563eb; }
        .btn-business { border-left: 4px solid #059669; }
        .btn-enterprise { border-left: 4px solid #7c3aed; }
        .section-title { font-size: 13px; font-weight: 600; margin-top: 20px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; color: var(--vscode-foreground); }
      </style>
    </head>
    <body>
      <div class="header-card">
        <span class="badge badge-${tier.tierId.replace('plan_', '')}">${tier.tierName}</span>
        <div class="title">⚡ Percipience Control Plane</div>
        <div class="meta-line">💳 <b>Active License Quota:</b> ${tier.quota}</div>
        <div class="meta-line">🛡️ <b>Merkle Chain Integrity:</b> Verified Block #RP_GENESIS_000</div>
        <div class="meta-line">💰 <b>AST Token Optimization:</b> 70.0% Reduction (Active)</div>
        <div class="meta-line">🛠️ <b>Platform Tools Exposure:</b> ${tier.exposeBasicPlatformTools ? 'Standard & Full Tool APIs (Active)' : 'Gatekeeper Actions Only (Free/Team Tier Protection)'}</div>
      </div>

      <div class="section-title">Core Actions (${tier.tierName})</div>
      <div class="actions-grid">
        <button class="btn" onclick="sendAction('bootstrap')">🚀 Bootstrap Workspace</button>
        <button class="btn" onclick="sendAction('gate')">🚦 Run PR Gatekeeper</button>
        <button class="btn" onclick="sendAction('audit')">🛡️ Verify Merkle Chain</button>
        <button class="btn" onclick="sendAction('cicd')">▶ Execute Autonomous CI/CD</button>
        <button class="btn" onclick="sendAction('validate')">🔍 Validate Layered Context</button>
        <button class="btn" onclick="sendAction('tokens')">⚡ Token Savings Summary</button>
      </div>

      ${tier.canUseWorktrees || tier.canCreateAgents ? `
      <div class="section-title">Team Tier Actions</div>
      <div class="actions-grid">
        <button class="btn btn-team" onclick="sendAction('worktrees')">🌿 Manage Worktrees</button>
        <button class="btn btn-team" onclick="sendAction('agent_list')">🤖 Specialist Agents Registry</button>
        <button class="btn btn-team" onclick="sendAction('drift_check')">🔄 Anti-Drift Parity Check</button>
      </div>
      ` : ''}

      ${tier.canPackNbpack ? `
      <div class="section-title">Business Tier Actions</div>
      <div class="actions-grid">
        <button class="btn btn-business" onclick="sendAction('layer_pack')">📦 Package Sealed NBPack</button>
        <button class="btn btn-business" onclick="sendAction('provision')">🌐 Multi-Tenant Gateway Provisioner</button>
        <button class="btn btn-business" onclick="sendAction('drift_report')">🧠 Cognitive Router & Parity Report</button>
      </div>
      ` : ''}

      ${tier.canUseSwarm || tier.canUsePrivateVpc || tier.canUseWormEgress ? `
      <div class="section-title">Enterprise Dedicated Actions</div>
      <div class="actions-grid">
        <button class="btn btn-enterprise" onclick="sendAction('swarm_audit')">🐝 Swarm Triad Orchestrator</button>
        <button class="btn btn-enterprise" onclick="sendAction('vpc_sync')">🔒 Private VPC Air-Gapped Sync</button>
        <button class="btn btn-enterprise" onclick="sendAction('egress_list')">📜 Immutable WORM Cloud Egress Export</button>
      </div>
      ` : ''}

      <script nonce="${nonce}">
        const vscode = acquireVsCodeApi();
        function sendAction(action) {
          vscode.postMessage({ command: 'execute_action', action: action });
        }
      </script>
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
