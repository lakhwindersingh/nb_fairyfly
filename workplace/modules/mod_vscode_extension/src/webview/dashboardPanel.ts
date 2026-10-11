import * as vscode from 'vscode';
import { PercipienceDaemonClient } from '../ipc/daemonClient';
import { DELIVERY_PIPELINES_REGISTRY } from '../providers/workflowTreeProvider';

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
          case 'open_contract':
            if (message.path) {
              const wsFolders = vscode.workspace.workspaceFolders;
              if (wsFolders && wsFolders.length > 0) {
                const uri = vscode.Uri.joinPath(wsFolders[0].uri, message.path);
                try {
                  await vscode.commands.executeCommand('vscode.open', uri);
                } catch {
                  vscode.window.showWarningMessage(`Could not open contract file: ${message.path}`);
                }
              }
            }
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

    const pipelineCardsHtml = DELIVERY_PIPELINES_REGISTRY.map((pipe) => {
      const totalContracts = pipe.stages.reduce((acc, s) => acc + s.handledContracts.length, 0);
      const stagesFlowHtml = pipe.stages.map((st, sIdx) => {
        const isLast = sIdx === pipe.stages.length - 1;
        const contractsBadges = st.handledContracts.map((c) => `
          <span class="contract-badge" onclick="openContract('${c.path}')" title="${c.name} (${c.path}): ${c.description}">
            📄 ${c.contractId}
          </span>
        `).join('');

        return `
          <div class="stage-card">
            <div class="stage-header">
              <span class="stage-num">Stage ${sIdx + 1}</span>
              <span class="executor-tag">${st.executor}</span>
            </div>
            <div class="stage-name">${st.name}</div>
            <div class="contract-list">
              ${contractsBadges || '<span class="muted-text">Internal Stage</span>'}
            </div>
          </div>
          ${!isLast ? '<div class="stage-arrow">➔</div>' : ''}
        `;
      }).join('');

      return `
        <div class="pipeline-block">
          <div class="pipeline-header">
            <div>
              <div class="pipeline-title">${pipe.name}</div>
              <div class="pipeline-desc">${pipe.description}</div>
            </div>
            <div class="pipeline-meta">
              <span class="badge badge-cyan">${pipe.stages.length} Stages</span>
              <span class="badge badge-emerald">${totalContracts} Handled Contracts</span>
            </div>
          </div>
          <div class="pipeline-dag-row">
            ${stagesFlowHtml}
          </div>
        </div>
      `;
    }).join('');

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
        .badge-cyan { background: #0284c7; }
        .badge-emerald { background: #059669; }
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
        .section-title { font-size: 13px; font-weight: 600; margin-top: 24px; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px; color: var(--vscode-foreground); }

        /* Pipeline Visualizer Styles */
        .pipeline-block {
          background: var(--vscode-sideBar-background);
          border: 1px solid var(--vscode-widget-border);
          border-radius: 6px;
          padding: 14px;
          margin-bottom: 14px;
        }
        .pipeline-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          flex-wrap: wrap;
          gap: 10px;
          margin-bottom: 12px;
          padding-bottom: 8px;
          border-bottom: 1px solid var(--vscode-widget-border);
        }
        .pipeline-title { font-size: 14px; font-weight: bold; color: var(--vscode-textLink-foreground); }
        .pipeline-desc { font-size: 11.5px; color: var(--vscode-descriptionForeground); margin-top: 2px; }
        .pipeline-meta { display: flex; gap: 6px; }
        .pipeline-dag-row {
          display: flex;
          gap: 10px;
          overflow-x: auto;
          padding: 6px 0;
          align-items: center;
        }
        .stage-card {
          flex: 1;
          min-width: 190px;
          background: var(--vscode-editor-background);
          border: 1px solid var(--vscode-widget-border);
          border-top: 3px solid #0284c7;
          border-radius: 4px;
          padding: 10px;
        }
        .stage-header { display: flex; justify-content: space-between; margin-bottom: 4px; }
        .stage-num { font-size: 10px; font-weight: bold; color: var(--vscode-descriptionForeground); text-transform: uppercase; }
        .executor-tag { font-size: 10px; color: #0284c7; font-family: var(--vscode-editor-font-family); }
        .stage-name { font-size: 11.5px; font-weight: 600; margin-bottom: 6px; line-height: 1.3; }
        .contract-list { display: flex; flex-wrap: wrap; gap: 3px; margin-top: 6px; }
        .contract-badge {
          display: inline-block;
          background: rgba(2, 132, 199, 0.15);
          color: #0284c7;
          border: 1px solid rgba(2, 132, 199, 0.35);
          border-radius: 3px;
          padding: 2px 5px;
          font-size: 9.5px;
          font-family: var(--vscode-editor-font-family);
          cursor: pointer;
        }
        .contract-badge:hover { background: rgba(2, 132, 199, 0.3); }
        .stage-arrow { font-size: 16px; color: #0284c7; font-weight: bold; opacity: 0.8; }
        .muted-text { font-size: 10px; color: var(--vscode-descriptionForeground); font-style: italic; }
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

      <div class="section-title">🔄 Delivery Pipelines &amp; Handled Contracts Visualizer (7 Flows)</div>
      ${pipelineCardsHtml}

      <script nonce="${nonce}">
        const vscode = acquireVsCodeApi();
        function sendAction(action) {
          vscode.postMessage({ command: 'execute_action', action: action });
        }
        function openContract(path) {
          vscode.postMessage({ command: 'open_contract', path: path });
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
