package com.neutronbinary.percipience.toolwindow

import com.intellij.openapi.application.ApplicationManager
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
import com.neutronbinary.percipience.ledger.TierInfo
import com.neutronbinary.percipience.security.SandboxPermissionBroker
import com.neutronbinary.percipience.services.PercipienceExecutionService
import kotlinx.coroutines.runBlocking
import java.awt.*
import java.io.File
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
        tabbedPane.addTab("Terminal Agents & FinOps", createTerminalAgentsPanel(project))
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

        val headerPanel = JPanel(GridLayout(8, 1, 4, 4))
        headerPanel.background = headerBg
        headerPanel.border = BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(headerBorder, 1),
            EmptyBorder(10, 12, 10, 12)
        )

        val titleLabel = JLabel("⚡ PERCIPIENCE CONTROL PLANE")
        titleLabel.font = titleLabel.font.deriveFont(Font.BOLD, 13.0f)
        titleLabel.foreground = titleCyan

        val planTierLabel = JLabel("💳 Tier: Resolving...")
        planTierLabel.font = planTierLabel.font.deriveFont(Font.BOLD, 11.5f)
        planTierLabel.foreground = JBColor(Color(100, 116, 139), Color(148, 163, 184))

        val statusLabel = JLabel("● Status: Initializing...")
        statusLabel.font = statusLabel.font.deriveFont(Font.BOLD, 12.0f)
        statusLabel.foreground = statusGreen

        val finopsLabel = JLabel("💰 Token Compression: Calculating...")
        finopsLabel.font = finopsLabel.font.deriveFont(Font.PLAIN, 11.5f)

        val savingsUsdLabel = JLabel("💵 Value Saved: Calculating...")
        savingsUsdLabel.font = savingsUsdLabel.font.deriveFont(Font.PLAIN, 11.5f)

        val cicdLabel = JLabel("🔄 CI/CD Engine: Initializing...")
        cicdLabel.font = cicdLabel.font.deriveFont(Font.PLAIN, 11.5f)

        val layerLabel = JLabel("🌐 Active Binary: .nb/bin/percipience (Executable)")
        layerLabel.font = layerLabel.font.deriveFont(Font.PLAIN, 11.5f)

        val toolsLabel = JLabel("🛠️ Tools Exposure: Initializing...")
        toolsLabel.font = toolsLabel.font.deriveFont(Font.PLAIN, 11.5f)

        val actionsContainer = JPanel(BorderLayout())
        actionsContainer.background = UIUtil.getPanelBackground()
        val actionsPanel = JPanel()
        actionsContainer.add(actionsPanel, BorderLayout.NORTH)

        val execService = PercipienceExecutionService.getInstance(project)

        fun rebuildActionsPanel(tierInfo: TierInfo) {
            actionsPanel.removeAll()

            // Count buttons to dynamically size grid
            var buttonCount = 7 // Base buttons: Bootstrap, Gate, Merkle Audit, CI/CD, Validate, Token Summary, Refresh, Portal

            if (tierInfo.canUseWorktrees || tierInfo.canCreateCustomAgents) {
                buttonCount += 3 // Worktrees, Custom Agent, Anti-Drift Parity Check
            }
            if (tierInfo.canPackNbpack) {
                buttonCount += 3 // NBPack layer pack, Provision Portal, Cognitive Router Report
            }
            if (tierInfo.canUseSwarmOrchestrator || tierInfo.canUsePrivateVpc || tierInfo.canUseWormEgress) {
                buttonCount += 3 // Swarm Orchestrator, Private VPC Enclave, WORM Egress
            }
            buttonCount += 1 // Observability Portal

            actionsPanel.layout = GridLayout(buttonCount, 1, 6, 6)
            actionsPanel.border = EmptyBorder(10, 0, 10, 0)

            // --- 1. Universal / Free Tier Core Action Buttons ---
            val btnBootstrap = JButton("🚀 Bootstrap / Verify Workspace Setup")
            btnBootstrap.addActionListener {
                val basePath = project.basePath ?: return@addActionListener
                val res = WorkspaceBootstrapper.bootstrapWorkspace(basePath)
                if (res.alreadyConfigured) {
                    Messages.showInfoMessage(
                        "Workspace is already fully bootstrapped with Master Plan, Merkle ledger, .nb/bin/percipience binary, and CI/CD.",
                        "Percipience Workspace Status"
                    )
                } else {
                    Messages.showInfoMessage(
                        "Bootstrapped ${res.createdFiles.size} files and ${res.createdDirectories.size} directories successfully for ${tierInfo.tierName}.\n\nPercipience CLI executable (.nb/bin/percipience) is now installed.",
                        "Percipience Bootstrap Complete"
                    )
                }
            }
            actionsPanel.add(btnBootstrap)

            val btnGate = JButton("🚦 Run PR Gatekeeper (`.nb/bin/percipience gate`)")
            btnGate.addActionListener {
                ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Running Percipience PR Gatekeeper...", false) {
                    override fun run(indicator: ProgressIndicator) {
                        indicator.isIndeterminate = true
                        indicator.text = "Executing .nb/bin/percipience gate..."
                        val res = runBlocking { execService.runGatekeeper() }
                        ApplicationManager.getApplication().invokeLater {
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
                    }
                })
            }
            actionsPanel.add(btnGate)

            val btnVerifyChain = JButton("🛡️ Verify Merkle Chain (`.nb/bin/percipience audit`)")
            btnVerifyChain.addActionListener {
                ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Auditing Merkle Ledger...", false) {
                    override fun run(indicator: ProgressIndicator) {
                        indicator.isIndeterminate = true
                        indicator.text = "Executing .nb/bin/percipience audit..."
                        val res = runBlocking { execService.runMerkleAudit(enforceMerkleChain = true, minMaturity = 0.85) }
                        ApplicationManager.getApplication().invokeLater {
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
                    }
                })
            }
            actionsPanel.add(btnVerifyChain)

            val btnRunWorkflow = JButton("▶ Execute Autonomous CI/CD Pipeline (`.nb/bin/percipience cicd run`)")
            btnRunWorkflow.addActionListener {
                ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Running Autonomous CI/CD...", false) {
                    override fun run(indicator: ProgressIndicator) {
                        indicator.isIndeterminate = true
                        indicator.text = "Executing .nb/bin/percipience cicd run..."
                        val res = runBlocking { execService.runBasicCicd() }
                        ApplicationManager.getApplication().invokeLater {
                            if (res.success) {
                                Messages.showInfoMessage(
                                    project,
                                    "CI/CD Executed Successfully!\n\n${res.stdout.takeLast(400)}",
                                    "Autonomous CI/CD Pipeline"
                                )
                            } else {
                                Messages.showErrorDialog(
                                    project,
                                    "CI/CD Failed:\n\n${res.stderr.ifEmpty { res.stdout }.takeLast(600)}",
                                    "CI/CD Failure"
                                )
                            }
                        }
                    }
                })
            }
            actionsPanel.add(btnRunWorkflow)

            val btnValidateLayered = JButton("🔍 Validate Layered Context (`.nb/bin/percipience validate --layered`)")
            btnValidateLayered.addActionListener {
                ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Validating Layered Context...", false) {
                    override fun run(indicator: ProgressIndicator) {
                        indicator.isIndeterminate = true
                        indicator.text = "Executing .nb/bin/percipience validate --layered..."
                        val res = runBlocking { execService.runValidateLayered() }
                        ApplicationManager.getApplication().invokeLater {
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
                    }
                })
            }
            actionsPanel.add(btnValidateLayered)

            val btnTokensSummary = JButton("⚡ Token Savings Summary (`.nb/bin/percipience tokens summary`)")
            btnTokensSummary.addActionListener {
                ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Loading Token Savings Summary...", false) {
                    override fun run(indicator: ProgressIndicator) {
                        indicator.isIndeterminate = true
                        val res = runBlocking { execService.runTokensSummary() }
                        ApplicationManager.getApplication().invokeLater {
                            if (res.success) {
                                Messages.showInfoMessage(project, res.stdout, "Token Savings & FinOps Summary")
                            } else {
                                Messages.showErrorDialog(project, res.stderr.ifEmpty { res.stdout }, "Error")
                            }
                        }
                    }
                })
            }
            actionsPanel.add(btnTokensSummary)

            // --- 2. Team Tier Entitled Buttons ---
            if (tierInfo.canUseWorktrees || tierInfo.canCreateCustomAgents) {
                val btnWorktrees = JButton("🌿 Manage Worktrees (`.nb/bin/percipience worktree list`) [Team+]")
                btnWorktrees.addActionListener {
                    ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Listing Worktrees...", false) {
                        override fun run(indicator: ProgressIndicator) {
                            val res = runBlocking { execService.runWorktreeList() }
                            ApplicationManager.getApplication().invokeLater {
                                Messages.showInfoMessage(project, res.stdout.ifEmpty { "No active worktrees" }, "Worktree Manager")
                            }
                        }
                    })
                }
                actionsPanel.add(btnWorktrees)

                val btnCustomAgent = JButton("🤖 Specialist Agents Registry (`.nb/bin/percipience agent list`) [Team+]")
                btnCustomAgent.addActionListener {
                    ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Listing Agents...", false) {
                        override fun run(indicator: ProgressIndicator) {
                            val res = runBlocking { execService.runAgentList() }
                            ApplicationManager.getApplication().invokeLater {
                                Messages.showInfoMessage(project, res.stdout.ifEmpty { "Registered agents active" }, "Agent Registry")
                            }
                        }
                    })
                }
                actionsPanel.add(btnCustomAgent)

                val btnDriftCheck = JButton("🔄 Anti-Drift Parity Check (`.nb/bin/percipience drift check`) [Team+]")
                btnDriftCheck.addActionListener {
                    ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Checking Semantic Parity...", false) {
                        override fun run(indicator: ProgressIndicator) {
                            val res = runBlocking { execService.runDriftCheck() }
                            ApplicationManager.getApplication().invokeLater {
                                Messages.showInfoMessage(project, res.stdout, "Anti-Drift Parity Check")
                            }
                        }
                    })
                }
                actionsPanel.add(btnDriftCheck)
            }

            // --- 3. Business Tier Entitled Buttons ---
            if (tierInfo.canPackNbpack) {
                val btnLayerPack = JButton("📦 Package Sealed NBPack (`.nb/bin/percipience layer pack`) [Business+]")
                btnLayerPack.addActionListener {
                    ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Packaging NBPack Layer...", false) {
                        override fun run(indicator: ProgressIndicator) {
                            val planPath = ".nb/plan/l1/intellij-pycharm-plugin/detailed.md"
                            val outPath = ".nb/bundles/intellij_pycharm_plugin_domain.nbpack"
                            val res = runBlocking { execService.runLayerPack(planPath, outPath) }
                            ApplicationManager.getApplication().invokeLater {
                                if (res.success) {
                                    Messages.showInfoMessage(project, "Layer package compiled successfully!\n\n${res.stdout}", "NBPack Sealed")
                                } else {
                                    Messages.showErrorDialog(project, res.stderr.ifEmpty { res.stdout }, "Packaging Error")
                                }
                            }
                        }
                    })
                }
                actionsPanel.add(btnLayerPack)

                val btnProvisionPortal = JButton("🌐 Multi-Tenant Gateway Provisioner (`.nb/bin/percipience provision`) [Business+]")
                btnProvisionPortal.addActionListener {
                    ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Provisioning Gateway...", false) {
                        override fun run(indicator: ProgressIndicator) {
                            val res = runBlocking { execService.runProvisionPortal("all") }
                            ApplicationManager.getApplication().invokeLater {
                                Messages.showInfoMessage(project, res.stdout, "Gateway Provisioning")
                            }
                        }
                    })
                }
                actionsPanel.add(btnProvisionPortal)

                val btnDriftReport = JButton("🧠 Cognitive Router & Parity Report (`.nb/bin/percipience drift report`) [Business+]")
                btnDriftReport.addActionListener {
                    ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Generating Parity Report...", false) {
                        override fun run(indicator: ProgressIndicator) {
                            val res = runBlocking { execService.runDriftReport() }
                            ApplicationManager.getApplication().invokeLater {
                                Messages.showInfoMessage(project, res.stdout, "Cognitive Parity Breakdown")
                            }
                        }
                    })
                }
                actionsPanel.add(btnDriftReport)
            }

            // --- 4. Enterprise Tier Entitled Buttons ---
            if (tierInfo.canUseSwarmOrchestrator || tierInfo.canUsePrivateVpc || tierInfo.canUseWormEgress) {
                val btnSwarm = JButton("🐝 Swarm Triad Orchestrator (`.nb/bin/percipience swarm audit`) [Enterprise]")
                btnSwarm.addActionListener {
                    ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Auditing Swarm Triad...", false) {
                        override fun run(indicator: ProgressIndicator) {
                            val res = runBlocking { execService.runSwarmAudit() }
                            ApplicationManager.getApplication().invokeLater {
                                Messages.showInfoMessage(project, res.stdout, "Swarm Triad Governance")
                            }
                        }
                    })
                }
                actionsPanel.add(btnSwarm)

                val btnVpcSync = JButton("🔒 Private VPC Air-Gapped Sync (`.nb/bin/percipience repo status`) [Enterprise]")
                btnVpcSync.addActionListener {
                    ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Syncing Private VPC Enclave...", false) {
                        override fun run(indicator: ProgressIndicator) {
                            val res = runBlocking { execService.runRepoStatus() }
                            ApplicationManager.getApplication().invokeLater {
                                Messages.showInfoMessage(project, res.stdout, "Private VPC Enclave Status")
                            }
                        }
                    })
                }
                actionsPanel.add(btnVpcSync)

                val btnWormEgress = JButton("📜 Immutable WORM Cloud Egress Export (`.nb/bin/percipience egress list`) [Enterprise]")
                btnWormEgress.addActionListener {
                    ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Fetching WORM Egress Audit...", false) {
                        override fun run(indicator: ProgressIndicator) {
                            val res = runBlocking { execService.runEgressList() }
                            ApplicationManager.getApplication().invokeLater {
                                Messages.showInfoMessage(project, res.stdout, "Immutable WORM Audit Trail")
                            }
                        }
                    })
                }
                actionsPanel.add(btnWormEgress)
            }

            // --- 5. Utilities ---
            val btnRefresh = JButton("🔄 Refresh Metrics & Permissions")
            btnRefresh.addActionListener {
                val metrics = WorkspaceLedgerReader.readWorkspaceMetrics(project.basePath)
                updateLabels()
                rebuildActionsPanel(metrics.tierInfo)
                Messages.showInfoMessage("Workspace metrics and permissions successfully reloaded for ${metrics.tierInfo.tierName}.", "Ledger Re-synced")
            }
            actionsPanel.add(btnRefresh)

            val btnOpenPortal = JButton("🌐 Open Percipience Observability Portal")
            btnOpenPortal.addActionListener {
                try {
                    Desktop.getDesktop().browse(URI("http://localhost:3000"))
                } catch (e: Exception) {
                    Messages.showErrorDialog("Unable to open browser: ${e.message}", "Error")
                }
            }
            actionsPanel.add(btnOpenPortal)

            actionsPanel.revalidate()
            actionsPanel.repaint()
        }

        fun updateLabels() {
            val basePath = project.basePath
            val isConfigured = if (basePath != null) WorkspaceBootstrapper.isWorkspaceConfigured(basePath) else false

            val metrics = WorkspaceLedgerReader.readWorkspaceMetrics(basePath)
            val tok = metrics.tokenSavings
            val mer = metrics.merkleLedger
            val tierInfo = metrics.tierInfo

            planTierLabel.text = "💳 Tier: ${tierInfo.tierName} (${tierInfo.formatQuota()})"

            val merkleHeightStr = if (mer.exists && mer.merkleBlockHeight > 0) "#${mer.merkleBlockHeight}" else "Genesis"
            val configStr = if (isConfigured) "Active" else "Not Initialized"
            statusLabel.text = "● Workspace: $configStr | Merkle Chain: $merkleHeightStr Verified (${tierInfo.tierName})"

            if (tok.exists && tok.totalTokensSaved > 0) {
                finopsLabel.text = "💰 Token Compression: ${tok.formatReductionPct()} Reduction (${tok.formatTokensSaved()} Tokens Saved)"
                savingsUsdLabel.text = "💵 Gross Value Saved: ${tok.formatGrossSavingsUsd()} | Net FinOps: ${tok.formatNetSavingsUsd()} (${tok.totalEvents} Events)"
            } else {
                finopsLabel.text = "💰 Token Compression: ~70.0% Target Reduction | AST Skeletonizer Active"
                savingsUsdLabel.text = "💵 Gross Value Saved: $0.0000 | Net FinOps: $0.0000 (0 Events)"
            }

            cicdLabel.text = "🔄 CI/CD Engine: Autonomous CI/CD (${tierInfo.tierName})"
            toolsLabel.text = if (tierInfo.exposeBasicPlatformTools) {
                "🛠️ Tools Exposure: Standard & Full Platform Tool APIs (Active)"
            } else {
                "🛠️ Tools Exposure: Gatekeeper Actions Only (Basic Platform Tools Unexposed on Free/Team Tier)"
            }
        }

        val initialMetrics = WorkspaceLedgerReader.readWorkspaceMetrics(project.basePath)
        updateLabels()
        rebuildActionsPanel(initialMetrics.tierInfo)

        headerPanel.add(titleLabel)
        headerPanel.add(planTierLabel)
        headerPanel.add(statusLabel)
        headerPanel.add(finopsLabel)
        headerPanel.add(savingsUsdLabel)
        headerPanel.add(cicdLabel)
        headerPanel.add(layerLabel)
        headerPanel.add(toolsLabel)

        mainPanel.add(headerPanel, BorderLayout.NORTH)
        mainPanel.add(actionsContainer, BorderLayout.CENTER)

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
        val metrics = WorkspaceLedgerReader.readWorkspaceMetrics(project.basePath)
        val tierInfo = metrics.tierInfo

        val sb = StringBuilder()
        sb.append("<html><head>").append(getThemeCss(isDark)).append("</head><body>")
        sb.append("<h2>🚀 Percipience OS Capabilities &amp; Tier Governance</h2>")
        sb.append("<p>Engineered context operating system built for JetBrains IDEs and autonomous LLM agent execution. Active Tier: <b>${tierInfo.tierName}</b>.</p>")

        sb.append("<h3>🌟 Included Free Community Tier Capabilities</h3>")
        sb.append("<ul>")
        sb.append("<li><b>AST Token Pruning:</b> 60%–80% context reduction via AST traversal.</li>")
        sb.append("<li><b>Merkle Chain Audit:</b> Real-time linear SHA-256 cryptographic chain continuity.</li>")
        sb.append("<li><b>Basic Autonomous CI/CD:</b> Bounded auto-healing (1-retry heal) and hygiene workflows.</li>")
        sb.append("<li><b>Percipience CLI:</b> Direct execution in workspace via <code>.nb/bin/percipience</code>.</li>")
        sb.append("<li><b>Included Quota:</b> 1 Seat | 1 Concurrent Worktree | 500 PR Audits/mo.</li>")
        sb.append("</ul>")

        sb.append("<h3>🛠️ Basic Platform Tools Exposure Governance</h3>")
        sb.append("<ul>")
        sb.append("<li><b>Free Community Tier:</b> <span class='muted'>❌ Unexposed (No Plan to Expose Basic Tools)</span>. Low-level internal developer utilities, raw packaging binaries (<code>percipience pack</code>), internal AST rule compilers, and agent toolkits are restricted from direct Free Tier exposure.</li>")
        sb.append("<li><b>Safe Gatekeeper Surface:</b> Free Tier users execute exclusively through high-level gatekeeper actions (<code>gate</code>, <code>audit</code>, <code>cicd run</code>, <code>validate --layered</code>, <code>tokens summary</code>) and the IntelliJ / PyCharm UI.</li>")
        sb.append("<li><b>Business &amp; Enterprise Tiers:</b> <span class='badge-success'>✅ Standard &amp; Full Platform Tool APIs</span>. Unrestricted access to raw CLI tool suites, custom tool compilers, and agent development SDKs.</li>")
        sb.append("</ul>")

        sb.append("<h3>🔒 Encryption &amp; Obfuscation Architecture</h3>")
        sb.append("<ul>")
        sb.append("<li><b>Platform Core Assets:</b> 🔒 Sealed &amp; Encrypted. Platform schemas (<code>.nb/context/</code>), configs (<code>.nb/config/</code>), core engines (<code>.nb/core/</code>), and master plans remain encrypted, obfuscated, and strictly readable by the <code>percipience</code> binary.</li>")
        sb.append("<li><b>Free Tier User Plans:</b> 📄 Strictly Plaintext (Non-Encryptable). Free Tier user plans in <code>workplace/</code> remain unencrypted.</li>")
        sb.append("<li><b>Paid Tiers (Business &amp; Enterprise):</b> 🔒 <code>.nbpack</code> AES-256 and RAM Enclave zero-disk plaintext execution for user domain plans and schemas.</li>")
        sb.append("</ul>")

        sb.append("<h3>⚡ Tier-Aware Entitlements Matrix</h3>")
        sb.append("<ul>")
        sb.append("<li><b>Team Tier:</b> Git Worktree Leasing, Custom Agent Creation SDK, Anti-Drift Parity Checking.</li>")
        sb.append("<li><b>Business Tier:</b> Encrypted <code>.nbpack</code> Layer Packaging, Multi-Tenant Gateway Provisioning, Cognitive Router.</li>")
        sb.append("<li><b>Enterprise Dedicated Tier:</b> Swarm Triad Orchestration (Redis Redlock), Private VPC Enclave, WORM Cloud Egress.</li>")
        sb.append("</ul>")

        sb.append("</body></html>")

        val editorPane = JEditorPane("text/html", sb.toString())
        editorPane.isEditable = false
        editorPane.background = UIUtil.getPanelBackground()
        return JBScrollPane(editorPane)
    }

    private fun createAgentsAndFlowsPanel(project: Project): JComponent {
        val isDark = UIUtil.isUnderDarcula()
        val metrics = WorkspaceLedgerReader.readWorkspaceMetrics(project.basePath)
        val tierInfo = metrics.tierInfo

        val sb = StringBuilder()
        sb.append("<html><head>").append(getThemeCss(isDark)).append("</head><body>")
        sb.append("<h2>🤖 Specialist Agents &amp; Delivery Flows</h2>")
        sb.append("<p>Pre-configured agents and workflows active for <b>${tierInfo.tierName}</b>:</p>")

        sb.append("<h3>Active Specialist Agents</h3>")
        sb.append("<ul>")
        sb.append("<li><code>agent_psi_ast_bridge_specialist</code> - Fast AST skeletonization</li>")
        sb.append("<li><code>agent_jetbrains_plugin_architect</code> - Plugin structure and threading</li>")
        sb.append("<li><code>agent_autonomous_healer</code> - Bounded TDD auto-healing</li>")
        sb.append("<li><code>agent_merkle_ledger</code> - Cryptographic state blocks</li>")
        if (tierInfo.canCreateCustomAgents) {
            sb.append("<li><code>agent_commercial_packager_provisioner</code> - Tier packaging and license provisioning [Team+]</li>")
        }
        if (tierInfo.canUseSwarmOrchestrator) {
            sb.append("<li><code>agent_enterprise_saas_portal_architect</code> - Full swarm orchestration [Enterprise]</li>")
        }
        sb.append("</ul>")

        sb.append("<h3>Active Workflows</h3>")
        sb.append("<ul>")
        sb.append("<li><code>basic_autonomous_cicd.yaml</code> - Free community autonomous CI/CD</li>")
        sb.append("<li><code>intellij_pycharm_plugin_delivery_flow.yaml</code> - IDE plugin delivery pipeline</li>")
        if (tierInfo.canPackNbpack) {
            sb.append("<li><code>commercial_packaging_provisioning_flow.yaml</code> - Multi-tier packaging workflow [Business+]</li>")
        }
        if (tierInfo.canUseSwarmOrchestrator) {
            sb.append("<li><code>enterprise_sdlc.yaml</code> - Enterprise multi-stage closed loop swarm [Enterprise]</li>")
        }
        sb.append("</ul>")

        sb.append("</body></html>")

        val editorPane = JEditorPane("text/html", sb.toString())
        editorPane.isEditable = false
        editorPane.background = UIUtil.getPanelBackground()
        return JBScrollPane(editorPane)
    }

    private fun createTerminalAgentsPanel(project: Project): JComponent {
        val mainPanel = JPanel(BorderLayout(10, 10))
        mainPanel.border = EmptyBorder(12, 12, 12, 12)
        mainPanel.background = UIUtil.getPanelBackground()

        val isDark = UIUtil.isUnderDarcula()
        val sb = StringBuilder()
        sb.append("<html><head>").append(getThemeCss(isDark)).append("</head><body>")
        sb.append("<h2>💻 Terminal Mode Agents & AST Token Compression</h2>")
        sb.append("<p>Integrate autonomous CLI agents (<b>Claude Code</b>, <b>Gemini CLI</b>, <b>Aider</b>) directly inside IntelliJ / PyCharm terminal tool windows with automatic AST skeletonization and token optimization.</p>")
        sb.append("<h3>⚡ How It Works</h3>")
        sb.append("<ul>")
        sb.append("<li><b>AST Structural Skeletons:</b> Strips function and class implementation bodies while preserving full signatures, type hints, docstrings, and DOM tags (40-70% token savings).</li>")
        sb.append("<li><b>Dynamic Context Injection:</b> Generates compact context files (<code>.percipience_claude_context.md</code>, <code>.percipience_gemini_context.md</code>) loaded directly into CLI prompts.</li>")
        sb.append("<li><b>FinOps Ledger Metering:</b> All terminal prompt invocations are recorded into <code>token_savings_ledger.yaml</code> to calculate gross USD saved and net customer ROI.</li>")
        sb.append("</ul>")
        sb.append("<h3>🚀 Quick Commands</h3>")
        sb.append("<pre><code># Wrap Claude Code with AST compression\n./.nb/bin/percipience agent wrap --agent claude\n\n# Wrap Gemini CLI\n./.nb/bin/percipience agent wrap --agent gemini\n\n# Install Shell Hook into zsh / bash\neval \"$(./.nb/bin/percipience terminal hook --shell zsh)\"</code></pre>")
        sb.append("</body></html>")

        val editorPane = JEditorPane("text/html", sb.toString())
        editorPane.isEditable = false
        editorPane.background = UIUtil.getPanelBackground()

        val buttonPanel = JPanel(FlowLayout(FlowLayout.LEFT, 8, 8))
        val btnClaude = JButton("⚡ Prepare Claude Code Context")
        btnClaude.addActionListener {
            val execService = PercipienceExecutionService.getInstance(project)
            ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Exporting Claude Code AST Context...", false) {
                override fun run(indicator: ProgressIndicator) {
                    val res = runBlocking { execService.runContextExport("claude-code", ".percipience_claude_context.md") }
                    ApplicationManager.getApplication().invokeLater {
                        Messages.showInfoMessage(project, res.stdout, "Claude Code Context Export")
                    }
                }
            })
        }

        val btnGemini = JButton("✨ Prepare Gemini CLI Context")
        btnGemini.addActionListener {
            val execService = PercipienceExecutionService.getInstance(project)
            ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Exporting Gemini CLI AST Context...", false) {
                override fun run(indicator: ProgressIndicator) {
                    val res = runBlocking { execService.runContextExport("gemini-cli", ".percipience_gemini_context.md") }
                    ApplicationManager.getApplication().invokeLater {
                        Messages.showInfoMessage(project, res.stdout, "Gemini CLI Context Export")
                    }
                }
            })
        }

        val btnStatus = JButton("📊 Terminal FinOps Status")
        btnStatus.addActionListener {
            val execService = PercipienceExecutionService.getInstance(project)
            ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Loading Terminal FinOps Status...", false) {
                override fun run(indicator: ProgressIndicator) {
                    val res = runBlocking { execService.runTerminalStatus() }
                    ApplicationManager.getApplication().invokeLater {
                        Messages.showInfoMessage(project, res.stdout, "Terminal Agent FinOps Status")
                    }
                }
            })
        }

        buttonPanel.add(btnClaude)
        buttonPanel.add(btnGemini)
        buttonPanel.add(btnStatus)

        mainPanel.add(JBScrollPane(editorPane), BorderLayout.CENTER)
        mainPanel.add(buttonPanel, BorderLayout.SOUTH)
        return mainPanel
    }

    private fun createUserGuidePanel(project: Project): JComponent {
        val isDark = UIUtil.isUnderDarcula()
        val sb = StringBuilder()
        sb.append("<html><head>").append(getThemeCss(isDark)).append("</head><body>")
        sb.append("<h2>📖 Percipience User Guide &amp; Quickstart</h2>")
        sb.append("<h3>1. Running Commands</h3>")
        sb.append("<p>You can execute commands either through the Control Plane buttons above or directly from the terminal:</p>")
        sb.append("<pre><code># Run PR Gatekeeper\n./.nb/bin/percipience gate\n\n# Audit Merkle Ledger\n./.nb/bin/percipience audit --enforce-merkle-chain\n\n# Run Basic CI/CD\n./.nb/bin/percipience cicd run\n\n# Validate Layered Context\n./.nb/bin/percipience validate --layered\n\n# View Token Savings\n./.nb/bin/percipience tokens summary</code></pre>")

        sb.append("<h3>2. New Workspace Initialization &amp; Tier Awareness</h3>")
        sb.append("<p>When opening a project, Percipience detects your active license tier (<code>tenant_license.json</code> or <code>context_ledger.yaml</code>) and dynamically renders the entitled action buttons in the Control Plane tab.</p>")

        sb.append("<h3>3. Tooling Exposure &amp; Encryption Boundaries</h3>")
        sb.append("<p>Free Tier workspaces operate under strict governance: low-level packaging tools and internal rule compilers remain unexposed, user plans remain plaintext, while the underlying platform core remains encrypted and readable by the percipience command.</p>")

        sb.append("</body></html>")

        val editorPane = JEditorPane("text/html", sb.toString())
        editorPane.isEditable = false
        editorPane.background = UIUtil.getPanelBackground()
        return JBScrollPane(editorPane)
    }
}
