package com.neutronbinary.percipience.toolwindow

import com.intellij.openapi.progress.ProgressIndicator
import com.intellij.openapi.progress.ProgressManager
import com.intellij.openapi.progress.Task
import com.intellij.openapi.project.Project
import com.intellij.openapi.ui.Messages
import com.intellij.openapi.wm.ToolWindow
import com.intellij.openapi.wm.ToolWindowFactory
import com.intellij.ui.JBColor
import com.intellij.ui.components.JBScrollPane
import com.intellij.ui.components.JBTabbedPane
import com.intellij.ui.content.ContentFactory
import com.intellij.util.ui.JBUI
import com.intellij.util.ui.UIUtil
import com.neutronbinary.percipience.bootstrap.WorkspaceBootstrapper
import com.neutronbinary.percipience.ledger.WorkspaceLedgerReader
import com.neutronbinary.percipience.ledger.WorkspaceMetrics
import com.neutronbinary.percipience.security.SandboxPermissionBroker
import com.neutronbinary.percipience.services.PercipienceExecutionService
import kotlinx.coroutines.runBlocking
import java.awt.*
import java.net.URI
import javax.swing.*
import javax.swing.border.EmptyBorder

class PercipienceToolWindowFactory : ToolWindowFactory {

    override fun createToolWindowContent(project: Project, toolWindow: ToolWindow) {
        val tabbedPane = JBTabbedPane()

        tabbedPane.addTab("Control Plane", createControlPlanePanel(project))
        tabbedPane.addTab("Sandbox Permissions", createSandboxPermissionsPanel(project))
        tabbedPane.addTab("Capabilities", createCapabilitiesPanel(project))
        tabbedPane.addTab("Agents & Flows", createAgentsAndFlowsPanel(project))
        tabbedPane.addTab("User Guide", createUserGuidePanel(project))

        val content = ContentFactory.getInstance().createContent(tabbedPane, "", false)
        toolWindow.contentManager.addContent(content)
    }

    /**
     * Returns Swing-safe HTML 3.2 / CSS 1.0 compatible stylesheet rules.
     */
    private fun getThemeCss(isDark: Boolean): String {
        val bodyBg = if (isDark) "#1e293b" else "#ffffff"
        val textColor = if (isDark) "#f8fafc" else "#1e293b"
        val headerColor = if (isDark) "#38bdf8" else "#0369a1"
        val tableHeaderBg = if (isDark) "#334155" else "#f1f5f9"
        val codeBg = if (isDark) "#0f172a" else "#f1f5f9"
        val codeColor = if (isDark) "#38bdf8" else "#0f766e"
        val mutedColor = if (isDark) "#94a3b8" else "#64748b"
        val successColor = if (isDark) "#34d399" else "#059669"
        val infoColor = if (isDark) "#38bdf8" else "#0284c7"

        return """
            <style>
                body {
                    font-family: sans-serif;
                    background-color: $bodyBg;
                    color: $textColor;
                    padding: 8px;
                    margin: 0;
                    font-size: 11pt;
                }
                h2 { color: $headerColor; margin-top: 0; margin-bottom: 6px; font-size: 14pt; }
                h3 { color: $headerColor; margin-top: 10px; margin-bottom: 4px; font-size: 12pt; }
                p, li { color: $textColor; font-size: 11pt; margin-top: 3px; margin-bottom: 3px; }
                th {
                    background-color: $tableHeaderBg;
                    color: $headerColor;
                    font-weight: bold;
                    padding: 6px;
                    text-align: left;
                }
                td {
                    padding: 6px;
                    color: $textColor;
                    font-size: 11pt;
                }
                code {
                    background-color: $codeBg;
                    color: $codeColor;
                    font-family: monospaced;
                    font-size: 10pt;
                }
                .muted { color: $mutedColor; }
                .badge-success { color: $successColor; font-weight: bold; }
                .badge-info { color: $infoColor; font-weight: bold; }
            </style>
        """.trimIndent()
    }

    private fun createControlPlanePanel(project: Project): JComponent {
        val mainPanel = JPanel(BorderLayout(10, 10))
        mainPanel.border = EmptyBorder(12, 12, 12, 12)
        mainPanel.background = UIUtil.getPanelBackground()

        val headerBg = JBColor(Color(241, 245, 249), Color(24, 33, 47))
        val headerBorder = JBColor(Color(203, 213, 225), Color(51, 65, 85))
        val titleCyan = JBColor(Color(3, 105, 161), Color(0, 210, 255))
        val statusGreen = JBColor(Color(16, 149, 103), Color(16, 185, 129))

        val headerPanel = JPanel(GridLayout(7, 1, 4, 4))
        headerPanel.background = headerBg
        headerPanel.border = BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(headerBorder, 1),
            EmptyBorder(10, 12, 10, 12)
        )

        val titleLabel = JLabel("⚡ PERCIPIENCE CONTROL PLANE")
        titleLabel.font = titleLabel.font.deriveFont(Font.BOLD, 13.0f)
        titleLabel.foreground = titleCyan

        val planTierLabel = JLabel("💳 Tier: Free Community Tier (Included: 1 Seat | 1 Worktree | 500 Audits/mo)")
        planTierLabel.font = planTierLabel.font.deriveFont(Font.BOLD, 11.5f)
        planTierLabel.foreground = JBColor(Color(100, 116, 139), Color(148, 163, 184))

        val statusLabel = JLabel("● Status: Initializing...")
        statusLabel.font = statusLabel.font.deriveFont(Font.BOLD, 12.0f)
        statusLabel.foreground = statusGreen

        val finopsLabel = JLabel("💰 Token Compression: Calculating...")
        finopsLabel.font = finopsLabel.font.deriveFont(Font.PLAIN, 11.5f)

        val savingsUsdLabel = JLabel("💵 Value Saved: Calculating...")
        savingsUsdLabel.font = savingsUsdLabel.font.deriveFont(Font.PLAIN, 11.5f)

        val cicdLabel = JLabel("🔄 CI/CD Engine: Basic Autonomous CI/CD (Free Edition)")
        cicdLabel.font = cicdLabel.font.deriveFont(Font.PLAIN, 11.5f)

        val layerLabel = JLabel("🌐 Active Binary: .nb/bin/percipience (Executable Workspace-Wide)")
        layerLabel.font = layerLabel.font.deriveFont(Font.PLAIN, 11.5f)

        fun updateLabels() {
            val basePath = project.basePath
            val isConfigured = if (basePath != null) WorkspaceBootstrapper.isWorkspaceConfigured(basePath) else false

            val metrics = WorkspaceLedgerReader.readWorkspaceMetrics(basePath)
            val tok = metrics.tokenSavings
            val mer = metrics.merkleLedger

            val merkleHeightStr = if (mer.exists && mer.merkleBlockHeight > 0) "#${mer.merkleBlockHeight}" else "Genesis"
            val configStr = if (isConfigured) "Active" else "Not Initialized"
            statusLabel.text = "● Workspace: $configStr | Merkle Chain: $merkleHeightStr Verified (Free Edition)"

            if (tok.exists && tok.totalTokensSaved > 0) {
                finopsLabel.text = "💰 Token Compression: ${tok.formatReductionPct()} Reduction (${tok.formatTokensSaved()} Tokens Saved)"
                savingsUsdLabel.text = "💵 Gross Value Saved: ${tok.formatGrossSavingsUsd()} | Net FinOps: ${tok.formatNetSavingsUsd()} (${tok.totalEvents} Events)"
            } else {
                finopsLabel.text = "💰 Token Compression: ~70.0% Target Reduction | AST Skeletonizer Active"
                savingsUsdLabel.text = "💵 Gross Value Saved: $0.0000 | Net FinOps: $0.0000 (0 Events)"
            }
        }

        updateLabels()

        headerPanel.add(titleLabel)
        headerPanel.add(planTierLabel)
        headerPanel.add(statusLabel)
        headerPanel.add(finopsLabel)
        headerPanel.add(savingsUsdLabel)
        headerPanel.add(cicdLabel)
        headerPanel.add(layerLabel)

        val actionsPanel = JPanel(GridLayout(8, 1, 8, 8))
        actionsPanel.background = UIUtil.getPanelBackground()
        actionsPanel.border = EmptyBorder(10, 0, 10, 0)

        val execService = PercipienceExecutionService.getInstance(project)

        val btnBootstrap = JButton("🚀 Bootstrap / Verify Free Workspace Setup")
        btnBootstrap.addActionListener {
            val basePath = project.basePath ?: return@addActionListener
            val res = WorkspaceBootstrapper.bootstrapWorkspace(basePath)
            if (res.alreadyConfigured) {
                Messages.showInfoMessage(
                    "Workspace is already fully bootstrapped with Free Master Plan, Merkle ledger, .nb/bin/percipience binary, and Basic CI/CD.",
                    "Percipience Workspace Status"
                )
            } else {
                Messages.showInfoMessage(
                    "Bootstrapped ${res.createdFiles.size} files and ${res.createdDirectories.size} directories successfully for Free Community Tier.\n\nPercipience CLI executable (.nb/bin/percipience) is now installed.",
                    "Percipience Bootstrap Complete"
                )
            }
            updateLabels()
        }

        val btnGate = JButton("🚦 Run PR Gatekeeper (`.nb/bin/percipience gate`)")
        btnGate.addActionListener {
            ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Running Percipience PR Gatekeeper...", false) {
                override fun run(indicator: ProgressIndicator) {
                    indicator.isIndeterminate = true
                    indicator.text = "Executing .nb/bin/percipience gate..."
                    val res = runBlocking { execService.runGatekeeper() }
                    updateLabels()
                    if (res.success) {
                        Messages.showInfoMessage(
                            project,
                            "PR Gatekeeper Passed Successfully!\n\n${res.stdout.takeLast(400)}",
                            "Gatekeeper Passed"
                        )
                    } else {
                        Messages.showErrorDialog(
                            project,
                            "PR Gatekeeper Failed:\n\n${res.stderr.ifEmpty { res.stdout }.takeLast(600)}",
                            "Gatekeeper Failed"
                        )
                    }
                }
            })
        }

        val btnVerifyChain = JButton("🛡️ Verify Merkle Chain (`.nb/bin/percipience audit`)")
        btnVerifyChain.addActionListener {
            ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Auditing Merkle Ledger...", false) {
                override fun run(indicator: ProgressIndicator) {
                    indicator.isIndeterminate = true
                    indicator.text = "Executing .nb/bin/percipience audit..."
                    val res = runBlocking { execService.runMerkleAudit(enforceMerkleChain = true, minMaturity = 0.85) }
                    updateLabels()
                    if (res.success) {
                        Messages.showInfoMessage(
                            project,
                            "Merkle Chain Audit Validated!\n\n${res.stdout.takeLast(400)}",
                            "Merkle Audit"
                        )
                    } else {
                        Messages.showErrorDialog(
                            project,
                            "Merkle Audit Failed:\n\n${res.stderr.ifEmpty { res.stdout }.takeLast(600)}",
                            "Merkle Audit Error"
                        )
                    }
                }
            })
        }

        val btnRunWorkflow = JButton("▶ Execute Basic CI/CD Pipeline (`.nb/bin/percipience cicd run`)")
        btnRunWorkflow.addActionListener {
            ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Running Basic Autonomous CI/CD...", false) {
                override fun run(indicator: ProgressIndicator) {
                    indicator.isIndeterminate = true
                    indicator.text = "Executing .nb/bin/percipience cicd run..."
                    val res = runBlocking { execService.runBasicCicd() }
                    updateLabels()
                    if (res.success) {
                        Messages.showInfoMessage(
                            project,
                            "Basic CI/CD Executed Successfully!\n\n${res.stdout.takeLast(400)}",
                            "Basic CI/CD Pipeline"
                        )
                    } else {
                        Messages.showErrorDialog(
                            project,
                            "Basic CI/CD Failed:\n\n${res.stderr.ifEmpty { res.stdout }.takeLast(600)}",
                            "CI/CD Failure"
                        )
                    }
                }
            })
        }

        val btnValidateLayered = JButton("🔍 Validate Layered Context (`.nb/bin/percipience validate --layered`)")
        btnValidateLayered.addActionListener {
            ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Validating Layered Context...", false) {
                override fun run(indicator: ProgressIndicator) {
                    indicator.isIndeterminate = true
                    indicator.text = "Executing .nb/bin/percipience validate --layered..."
                    val res = runBlocking { execService.runValidateLayered() }
                    if (res.success) {
                        Messages.showInfoMessage(
                            project,
                            "Layered Context Validation Passed:\n\n${res.stdout}",
                            "Layered Context Valid"
                        )
                    } else {
                        Messages.showErrorDialog(
                            project,
                            "Layered Context Validation Failed:\n\n${res.stderr.ifEmpty { res.stdout }}",
                            "Validation Failed"
                        )
                    }
                }
            })
        }

        val btnTokensSummary = JButton("⚡ Token Savings Summary (`.nb/bin/percipience tokens summary`)")
        btnTokensSummary.addActionListener {
            ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Loading Token Savings Summary...", false) {
                override fun run(indicator: ProgressIndicator) {
                    indicator.isIndeterminate = true
                    val res = runBlocking { execService.runTokensSummary() }
                    if (res.success) {
                        Messages.showInfoMessage(project, res.stdout, "Token Savings & FinOps Summary")
                    } else {
                        Messages.showErrorDialog(project, res.stderr.ifEmpty { res.stdout }, "Error")
                    }
                }
            })
        }

        val btnRefresh = JButton("🔄 Refresh Metrics from Workspace Ledger")
        btnRefresh.addActionListener {
            updateLabels()
            Messages.showInfoMessage("Workspace metrics successfully reloaded from ledger files.", "Ledger Re-synced")
        }

        val btnOpenPortal = JButton("🌐 Open Percipience Observability Portal")
        btnOpenPortal.addActionListener {
            try {
                Desktop.getDesktop().browse(URI("http://localhost:3000"))
            } catch (e: Exception) {
                Messages.showErrorDialog("Unable to open browser: ${e.message}", "Error")
            }
        }

        actionsPanel.add(btnBootstrap)
        actionsPanel.add(btnGate)
        actionsPanel.add(btnVerifyChain)
        actionsPanel.add(btnRunWorkflow)
        actionsPanel.add(btnValidateLayered)
        actionsPanel.add(btnTokensSummary)
        actionsPanel.add(btnRefresh)
        actionsPanel.add(btnOpenPortal)

        mainPanel.add(headerPanel, BorderLayout.NORTH)
        mainPanel.add(actionsPanel, BorderLayout.CENTER)

        return JBScrollPane(mainPanel)
    }

    private fun createSandboxPermissionsPanel(project: Project): JComponent {
        val isDark = UIUtil.isUnderDarcula()
        val broker = SandboxPermissionBroker.instance
        val policies = broker.getAllPolicies().values
        val borderColor = if (isDark) "#475569" else "#cbd5e1"

        val sb = StringBuilder()
        sb.append("<html><head>").append(getThemeCss(isDark)).append("</head><body>")
        sb.append("<h2>🛡️ Sandbox &amp; LLM Plugin Permissions</h2>")
        sb.append("<p>Governs access rights when LLM agents or third-party AI plugins run in separate sandboxes within IntelliJ.</p>")

        sb.append("<table border='1' cellspacing='0' cellpadding='5' style='border-color: $borderColor; width: 100%;'>")
        sb.append("<tr><th>Plugin ID</th><th>Name</th><th>Read Level</th><th>AST Token Pruning</th><th>Direct Write</th></tr>")

        for (p in policies) {
            val badge = if (p.enforceTokenPruning) "<span class='badge-success'>Active (60-80% saved)</span>" else "<span class='muted'>Disabled</span>"
            val writeBadge = if (p.canWriteDirect) "<span class='badge-info'>Allowed</span>" else "<span class='muted'>Blocked (WORM)</span>"
            sb.append("<tr>")
            sb.append("<td><code>${p.pluginId}</code></td>")
            sb.append("<td>${p.pluginName}</td>")
            sb.append("<td><b>${p.defaultReadLevel}</b></td>")
            sb.append("<td>$badge</td>")
            sb.append("<td>$writeBadge</td>")
            sb.append("</tr>")
        }
        sb.append("</table>")

        sb.append("<h3>⚡ Real-Time Invariant Enforcement</h3>")
        sb.append("<ul>")
        sb.append("<li><b>In-Memory PSI Pruning:</b> Compresses AST syntax trees to function signatures, docstrings, and contracts in &lt;35ms before feeding to sandboxed plugins.</li>")
        sb.append("<li><b>Cryptographic Immutability:</b> Every generation, prompt diff, and action is hashed into SHA-256 Merkle chain blocks.</li>")
        sb.append("<li><b>Free Plan Sandbox SLA:</b> Unlimited local PSI AST token pruning and Merkle chain auditing included.</li>")
        sb.append("</ul>")

        sb.append("</body></html>")

        val editorPane = JEditorPane("text/html", sb.toString())
        editorPane.isEditable = false
        editorPane.background = UIUtil.getPanelBackground()
        return JBScrollPane(editorPane)
    }

    private fun createCapabilitiesPanel(project: Project): JComponent {
        val isDark = UIUtil.isUnderDarcula()
        val sb = StringBuilder()
        sb.append("<html><head>").append(getThemeCss(isDark)).append("</head><body>")
        sb.append("<h2>🚀 Percipience OS Capabilities (Free Community Tier)</h2>")
        sb.append("<p>Engineered context operating system built for JetBrains IDEs and autonomous LLM agent execution.</p>")

        sb.append("<h3>🌟 Included Free Features (billing_plans.yaml)</h3>")
        sb.append("<ul>")
        sb.append("<li><b>AST Token Pruning:</b> 60%–80% context reduction via AST traversal.</li>")
        sb.append("<li><b>Merkle Chain Audit:</b> Real-time linear SHA-256 cryptographic chain continuity.</li>")
        sb.append("<li><b>Basic Autonomous CI/CD:</b> Bounded auto-healing and hygiene workflows.</li>")
        sb.append("<li><b>Percipience CLI:</b> Direct execution in workspace via <code>.nb/bin/percipience</code>.</li>")
        sb.append("<li><b>Included Quota:</b> 1 Seat | 1 Concurrent Worktree | 500 PR Audits/mo.</li>")
        sb.append("</ul>")

        sb.append("<h3>🔒 Enterprise Features (Available on Upgrade)</h3>")
        sb.append("<ul>")
        sb.append("<li><b>Encrypted NBPack Distribution:</b> Proprietary plan and schema bytecode obfuscation.</li>")
        sb.append("<li><b>Private VPC & Cloud Gatekeeper:</b> Air-gapped on-premise infrastructure.</li>")
        sb.append("<li><b>Dedicated Slack Support & SLA:</b> 15-minute response time.</li>")
        sb.append("</ul>")

        sb.append("</body></html>")

        val editorPane = JEditorPane("text/html", sb.toString())
        editorPane.isEditable = false
        editorPane.background = UIUtil.getPanelBackground()
        return JBScrollPane(editorPane)
    }

    private fun createAgentsAndFlowsPanel(project: Project): JComponent {
        val isDark = UIUtil.isUnderDarcula()
        val sb = StringBuilder()
        sb.append("<html><head>").append(getThemeCss(isDark)).append("</head><body>")
        sb.append("<h2>🤖 Specialist Agents &amp; Delivery Flows</h2>")
        sb.append("<p>Pre-configured agents and workflows active for the Free Community Tier:</p>")

        sb.append("<h3>Active Agents</h3>")
        sb.append("<ul>")
        sb.append("<li><code>agent_psi_ast_bridge_specialist</code> - Fast AST skeletonization</li>")
        sb.append("<li><code>agent_jetbrains_plugin_architect</code> - Plugin structure and threading</li>")
        sb.append("<li><code>agent_autonomous_healer</code> - Bounded TDD auto-healing</li>")
        sb.append("<li><code>agent_merkle_ledger</code> - Cryptographic state blocks</li>")
        sb.append("</ul>")

        sb.append("<h3>Active Workflows</h3>")
        sb.append("<ul>")
        sb.append("<li><code>basic_autonomous_cicd.yaml</code> - Free community autonomous CI/CD</li>")
        sb.append("<li><code>intellij_pycharm_plugin_delivery_flow.yaml</code> - IDE plugin delivery pipeline</li>")
        sb.append("</ul>")

        sb.append("</body></html>")

        val editorPane = JEditorPane("text/html", sb.toString())
        editorPane.isEditable = false
        editorPane.background = UIUtil.getPanelBackground()
        return JBScrollPane(editorPane)
    }

    private fun createUserGuidePanel(project: Project): JComponent {
        val isDark = UIUtil.isUnderDarcula()
        val sb = StringBuilder()
        sb.append("<html><head>").append(getThemeCss(isDark)).append("</head><body>")
        sb.append("<h2>📖 Percipience User Guide &amp; Quickstart</h2>")
        sb.append("<h3>1. Running Commands</h3>")
        sb.append("<p>You can execute commands either through the Control Plane buttons above or directly from the terminal:</p>")
        sb.append("<pre><code># Run PR Gatekeeper\n./.nb/bin/percipience gate\n\n# Audit Merkle Ledger\n./.nb/bin/percipience audit --enforce-merkle-chain\n\n# Run Basic CI/CD\n./.nb/bin/percipience cicd run\n\n# Validate Layered Context\n./.nb/bin/percipience validate --layered\n\n# View Token Savings\n./.nb/bin/percipience tokens summary</code></pre>")

        sb.append("<h3>2. New Workspace Initialization</h3>")
        sb.append("<p>When creating or opening a new project, Percipience prompts you to initialize the workspace with the Free Community Tier. You can also click <b>Bootstrap / Verify Free Workspace</b> at any time.</p>")

        sb.append("</body></html>")

        val editorPane = JEditorPane("text/html", sb.toString())
        editorPane.isEditable = false
        editorPane.background = UIUtil.getPanelBackground()
        return JBScrollPane(editorPane)
    }
}
