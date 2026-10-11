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
import com.neutronbinary.percipience.services.ExecutionResult
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
        tabbedPane.addTab("Swarm & Fleet", createSwarmGovernancePanel(project))
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
                updateLabels()
                if (res.alreadyConfigured) {
                    Messages.showInfoMessage(
                        project,
                        "Workspace is already fully bootstrapped with Master Plan, Merkle ledger, .nb/bin/percipience binary, and CI/CD.",
                        "Percipience Workspace Status"
                    )
                } else {
                    Messages.showInfoMessage(
                        project,
                        "Bootstrapped ${res.createdFiles.size} files and ${res.createdDirectories.size} directories successfully for ${tierInfo.tierName}.\n\nPercipience CLI executable (.nb/bin/percipience) is now installed.",
                        "Percipience Bootstrap Complete"
                    )
                }
            }
            actionsPanel.add(btnBootstrap)

            val btnGate = JButton("🚦 Run PR Gatekeeper (`.nb/bin/percipience gate`)")
            btnGate.addActionListener {
                ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Running Percipience PR Gatekeeper...", false) {
                    private var result: ExecutionResult? = null

                    override fun run(indicator: ProgressIndicator) {
                        indicator.isIndeterminate = true
                        indicator.text = "Executing .nb/bin/percipience gate..."
                        result = runBlocking { execService.runGatekeeper() }
                    }

                    override fun onSuccess() {
                        updateLabels()
                        val res = result ?: return
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

                    override fun onThrowable(error: Throwable) {
                        Messages.showErrorDialog(project, "Gatekeeper Execution Error:\n\n${error.message}", "Gatekeeper Error")
                    }
                })
            }
            actionsPanel.add(btnGate)

            val btnVerifyChain = JButton("🛡️ Verify Merkle Chain (`.nb/bin/percipience audit`)")
            btnVerifyChain.addActionListener {
                ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Auditing Merkle Ledger...", false) {
                    private var result: ExecutionResult? = null

                    override fun run(indicator: ProgressIndicator) {
                        indicator.isIndeterminate = true
                        indicator.text = "Executing .nb/bin/percipience audit..."
                        result = runBlocking { execService.runMerkleAudit(enforceMerkleChain = true, minMaturity = 0.85) }
                    }

                    override fun onSuccess() {
                        updateLabels()
                        val res = result ?: return
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

                    override fun onThrowable(error: Throwable) {
                        Messages.showErrorDialog(project, "Audit Execution Error:\n\n${error.message}", "Merkle Audit Error")
                    }
                })
            }
            actionsPanel.add(btnVerifyChain)

            val btnRunWorkflow = JButton("▶ Execute Autonomous CI/CD Pipeline (`.nb/bin/percipience cicd run`)")
            btnRunWorkflow.addActionListener {
                ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Running Autonomous CI/CD...", false) {
                    private var result: ExecutionResult? = null

                    override fun run(indicator: ProgressIndicator) {
                        indicator.isIndeterminate = true
                        indicator.text = "Executing .nb/bin/percipience cicd run..."
                        result = runBlocking { execService.runBasicCicd() }
                    }

                    override fun onSuccess() {
                        updateLabels()
                        val res = result ?: return
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

                    override fun onThrowable(error: Throwable) {
                        Messages.showErrorDialog(project, "CI/CD Execution Error:\n\n${error.message}", "CI/CD Failure")
                    }
                })
            }
            actionsPanel.add(btnRunWorkflow)

            val btnValidateLayered = JButton("🔍 Validate Layered Context (`.nb/bin/percipience validate --layered`)")
            btnValidateLayered.addActionListener {
                ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Validating Layered Context...", false) {
                    private var result: ExecutionResult? = null

                    override fun run(indicator: ProgressIndicator) {
                        indicator.isIndeterminate = true
                        indicator.text = "Executing .nb/bin/percipience validate --layered..."
                        result = runBlocking { execService.runValidateLayered() }
                    }

                    override fun onSuccess() {
                        updateLabels()
                        val res = result ?: return
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

                    override fun onThrowable(error: Throwable) {
                        Messages.showErrorDialog(project, "Validation Error:\n\n${error.message}", "Validation Failed")
                    }
                })
            }
            actionsPanel.add(btnValidateLayered)

            val btnTokensSummary = JButton("⚡ Token Savings Summary (`.nb/bin/percipience tokens summary`)")
            btnTokensSummary.addActionListener {
                ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Loading Token Savings Summary...", false) {
                    private var result: ExecutionResult? = null

                    override fun run(indicator: ProgressIndicator) {
                        indicator.isIndeterminate = true
                        result = runBlocking { execService.runTokensSummary() }
                    }

                    override fun onSuccess() {
                        updateLabels()
                        val res = result ?: return
                        if (res.success) {
                            Messages.showInfoMessage(project, res.stdout, "Token Savings & FinOps Summary")
                        } else {
                            Messages.showErrorDialog(project, res.stderr.ifEmpty { res.stdout }, "Error")
                        }
                    }

                    override fun onThrowable(error: Throwable) {
                        Messages.showErrorDialog(project, "Summary Error:\n\n${error.message}", "Error")
                    }
                })
            }
            actionsPanel.add(btnTokensSummary)

            // --- 2. Team Tier Entitled Buttons ---
            if (tierInfo.canUseWorktrees || tierInfo.canCreateCustomAgents) {
                val btnWorktrees = JButton("🌱 Manage Worktrees (`.nb/bin/percipience worktree list`) [Team+]")
                btnWorktrees.addActionListener {
                    ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Listing Worktrees...", false) {
                        private var result: ExecutionResult? = null

                        override fun run(indicator: ProgressIndicator) {
                            result = runBlocking { execService.runWorktreeList() }
                        }

                        override fun onSuccess() {
                            val res = result ?: return
                            Messages.showInfoMessage(project, res.stdout.ifEmpty { "No active worktrees" }, "Worktree Manager")
                        }

                        override fun onThrowable(error: Throwable) {
                            Messages.showErrorDialog(project, error.message ?: "Failed to list worktrees", "Error")
                        }
                    })
                }
                actionsPanel.add(btnWorktrees)

                val btnCustomAgent = JButton("🤖 Specialist Agents Registry (`.nb/bin/percipience agent list`) [Team+]")
                btnCustomAgent.addActionListener {
                    ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Listing Agents...", false) {
                        private var result: ExecutionResult? = null

                        override fun run(indicator: ProgressIndicator) {
                            result = runBlocking { execService.runAgentList() }
                        }

                        override fun onSuccess() {
                            val res = result ?: return
                            Messages.showInfoMessage(project, res.stdout.ifEmpty { "Registered agents active" }, "Agent Registry")
                        }

                        override fun onThrowable(error: Throwable) {
                            Messages.showErrorDialog(project, error.message ?: "Failed to list agents", "Error")
                        }
                    })
                }
                actionsPanel.add(btnCustomAgent)

                val btnDriftCheck = JButton("🔄 Anti-Drift Parity Check (`.nb/bin/percipience drift check`) [Team+]")
                btnDriftCheck.addActionListener {
                    ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Checking Semantic Parity...", false) {
                        private var result: ExecutionResult? = null

                        override fun run(indicator: ProgressIndicator) {
                            result = runBlocking { execService.runDriftCheck() }
                        }

                        override fun onSuccess() {
                            val res = result ?: return
                            Messages.showInfoMessage(project, res.stdout, "Anti-Drift Parity Check")
                        }

                        override fun onThrowable(error: Throwable) {
                            Messages.showErrorDialog(project, error.message ?: "Parity check failed", "Error")
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
                        private var result: ExecutionResult? = null

                        override fun run(indicator: ProgressIndicator) {
                            val planPath = ".nb/plan/l1/intellij-pycharm-plugin/detailed.md"
                            val outPath = ".nb/bundles/intellij_pycharm_plugin_domain.nbpack"
                            result = runBlocking { execService.runLayerPack(planPath, outPath) }
                        }

                        override fun onSuccess() {
                            val res = result ?: return
                            if (res.success) {
                                Messages.showInfoMessage(project, "Layer package compiled successfully!\n\n${res.stdout}", "NBPack Sealed")
                            } else {
                                Messages.showErrorDialog(project, res.stderr.ifEmpty { res.stdout }, "Packaging Error")
                            }
                        }

                        override fun onThrowable(error: Throwable) {
                            Messages.showErrorDialog(project, error.message ?: "Packaging error", "Error")
                        }
                    })
                }
                actionsPanel.add(btnLayerPack)

                val btnProvisionPortal = JButton("🌐 Multi-Tenant Gateway Provisioner (`.nb/bin/percipience provision`) [Business+]")
                btnProvisionPortal.addActionListener {
                    ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Provisioning Gateway...", false) {
                        private var result: ExecutionResult? = null

                        override fun run(indicator: ProgressIndicator) {
                            result = runBlocking { execService.runProvisionPortal("all") }
                        }

                        override fun onSuccess() {
                            val res = result ?: return
                            Messages.showInfoMessage(project, res.stdout, "Gateway Provisioning")
                        }

                        override fun onThrowable(error: Throwable) {
                            Messages.showErrorDialog(project, error.message ?: "Provisioning error", "Error")
                        }
                    })
                }
                actionsPanel.add(btnProvisionPortal)

                val btnDriftReport = JButton("🧠 Cognitive Router & Parity Report (`.nb/bin/percipience drift report`) [Business+]")
                btnDriftReport.addActionListener {
                    ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Generating Parity Report...", false) {
                        private var result: ExecutionResult? = null

                        override fun run(indicator: ProgressIndicator) {
                            result = runBlocking { execService.runDriftReport() }
                        }

                        override fun onSuccess() {
                            val res = result ?: return
                            Messages.showInfoMessage(project, res.stdout, "Cognitive Parity Breakdown")
                        }

                        override fun onThrowable(error: Throwable) {
                            Messages.showErrorDialog(project, error.message ?: "Report error", "Error")
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
                        private var result: ExecutionResult? = null

                        override fun run(indicator: ProgressIndicator) {
                            result = runBlocking { execService.runSwarmAudit() }
                        }

                        override fun onSuccess() {
                            val res = result ?: return
                            Messages.showInfoMessage(project, res.stdout, "Swarm Triad Governance")
                        }

                        override fun onThrowable(error: Throwable) {
                            Messages.showErrorDialog(project, error.message ?: "Swarm audit error", "Error")
                        }
                    })
                }
                actionsPanel.add(btnSwarm)

                val btnVpcSync = JButton("🔒 Private VPC Air-Gapped Sync (`.nb/bin/percipience repo status`) [Enterprise]")
                btnVpcSync.addActionListener {
                    ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Syncing Private VPC Enclave...", false) {
                        private var result: ExecutionResult? = null

                        override fun run(indicator: ProgressIndicator) {
                            result = runBlocking { execService.runRepoStatus() }
                        }

                        override fun onSuccess() {
                            val res = result ?: return
                            Messages.showInfoMessage(project, res.stdout, "Private VPC Enclave Status")
                        }

                        override fun onThrowable(error: Throwable) {
                            Messages.showErrorDialog(project, error.message ?: "VPC sync error", "Error")
                        }
                    })
                }
                actionsPanel.add(btnVpcSync)

                val btnWormEgress = JButton("📜 Immutable WORM Cloud Egress Export (`.nb/bin/percipience egress list`) [Enterprise]")
                btnWormEgress.addActionListener {
                    ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Fetching WORM Egress Audit...", false) {
                        private var result: ExecutionResult? = null

                        override fun run(indicator: ProgressIndicator) {
                            result = runBlocking { execService.runEgressList() }
                        }

                        override fun onSuccess() {
                            val res = result ?: return
                            Messages.showInfoMessage(project, res.stdout, "Immutable WORM Audit Trail")
                        }

                        override fun onThrowable(error: Throwable) {
                            Messages.showErrorDialog(project, error.message ?: "Egress fetch error", "Error")
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
                Messages.showInfoMessage(
                    project,
                    "Workspace metrics and permissions successfully reloaded for ${metrics.tierInfo.tierName}.",
                    "Ledger Re-synced"
                )
            }
            actionsPanel.add(btnRefresh)

            val btnOpenPortal = JButton("🌐 Open Percipience Observability Portal")
            btnOpenPortal.addActionListener {
                try {
                    Desktop.getDesktop().browse(URI("http://localhost:3000"))
                } catch (e: Exception) {
                    Messages.showErrorDialog(project, "Unable to open browser: ${e.message}", "Error")
                }
            }
            actionsPanel.add(btnOpenPortal)

            actionsPanel.revalidate()
            actionsPanel.repaint()
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
        val borderColor = if (isDark) "#334155" else "#cbd5e1"
        val dagBg = if (isDark) "#0f172a" else "#f1f5f9"

        val sb = StringBuilder()
        sb.append("<html><head>").append(getThemeCss(isDark)).append("</head><body>")
        sb.append("<h2>🔄 Visual Delivery Pipelines &amp; Stage Contract Governance</h2>")
        sb.append("<p>Interactive multi-stage DAG workflow visualizer detailing stage execution progressions, assigned agent executors, and cryptographic contracts handled across all 7 autonomous delivery flows. Active Tier: <b>${tierInfo.tierName}</b>.</p>")

        // Helper lambda for rendering a pipeline block
        fun renderPipelineSection(
            title: String,
            wfFile: String,
            desc: String,
            trigger: String,
            stagesFlow: String,
            stagesTableHtml: String
        ) {
            sb.append("<hr style='border:0; border-top:1px solid $borderColor; margin:14px 0;'>")
            sb.append("<table width='100%' cellpadding='0' cellspacing='0'><tr>")
            sb.append("<td><h3 style='margin-bottom:2px;'>⚡ $title</h3></td>")
            sb.append("<td align='right'><span class='badge-info'>$wfFile</span></td>")
            sb.append("</tr></table>")
            sb.append("<p class='muted' style='margin-top:0;'><b>Trigger:</b> $trigger &bull; <b>Description:</b> $desc</p>")

            // Visual DAG flow box
            sb.append("<div style='background-color:$dagBg; border:1px solid $borderColor; padding:8px; margin:6px 0 10px 0;'>")
            sb.append("<p style='margin:0; font-size:10.5pt;'><b>Execution DAG:</b> $stagesFlow</p>")
            sb.append("</div>")

            // Handled contracts table
            sb.append("<table border='1' cellspacing='0' cellpadding='5' style='border-color:$borderColor; width:100%; margin-bottom:12px;'>")
            sb.append("<tr>")
            sb.append("<th width='24%'>Stage / Executor</th>")
            sb.append("<th width='26%'>Handled Contract</th>")
            sb.append("<th width='14%'>Type / Action</th>")
            sb.append("<th width='36%'>Description &amp; Invariants</th>")
            sb.append("</tr>")
            sb.append(stagesTableHtml)
            sb.append("</table>")
        }

        // 1. Basic Autonomous CI/CD Pipeline
        renderPipelineSection(
            "Free Community Autonomous CI/CD Pipeline",
            ".nb/agentic/custom/workflows/basic_autonomous_cicd.yaml",
            "Automated maintenance, AST token compression, bounded self-repair, and Merkle block sealing for the Free Plan.",
            "Free Plan / Pre-Commit / Local CLI",
            "[1. Workspace Hygiene] ➔ [2. AST Token Reduction] ➔ [3. Contract & Test Gate] ➔ [4. Single-Attempt Auto-Heal] ➔ [5. Merkle Block Seal]",
            """
            <tr>
              <td><b>sustain_maintenance</b><br><code>platform.self_sustaining_engine</code></td>
              <td><b>observability_contract.yaml</b><br><code class='muted'>.nb/context/contracts/observability_contract.yaml</code><br><br><b>hierarchical_rule_contract.json</b><br><code class='muted'>.nb/context/contracts/hierarchical_rule_contract.json</code></td>
              <td><span class='badge-info'>yaml_schema</span> [validate]<br><br><span class='badge-info'>json_schema</span> [enforce]</td>
              <td>Enforces structured logging, health status schema, and hygiene execution metrics.<br><br>Verifies boundary rules ensuring scratch directory cleanup does not violate quad-space isolation.</td>
            </tr>
            <tr>
              <td><b>ast_token_reduction</b><br><code>platform.ast_pruner</code></td>
              <td><b>psi_ast_bridge_contract.yaml</b><br><code class='muted'>.nb/context/contracts/psi_ast_bridge_contract.yaml</code></td>
              <td><span class='badge-info'>yaml_schema</span> [inspect_and_prune]</td>
              <td>Preserves function signatures and type annotations while stripping execution bodies to achieve 65% token compression.</td>
            </tr>
            <tr>
              <td><b>contract_and_test_gate</b><br><code>platform.contract_verifier</code></td>
              <td><b>rbac_permission_matrix.json</b><br><code class='muted'>.nb/context/contracts/rbac_permission_matrix.json</code><br><br><b>data_grid_contract.json</b><br><code class='muted'>.nb/context/contracts/data_grid_contract.json</code></td>
              <td><span class='badge-info'>json_schema</span> [validate]<br><br><span class='badge-info'>json_schema</span> [validate]</td>
              <td>Asserts baseline permission matrices and role access controls before test execution.<br><br>Validates data structure formats across test payloads and fixture outputs.</td>
            </tr>
            <tr>
              <td><b>bounded_auto_heal</b><br><code>platform.autonomous_healer</code></td>
              <td><b>hierarchical_rule_contract.json</b><br><code class='muted'>.nb/context/contracts/hierarchical_rule_contract.json</code></td>
              <td><span class='badge-info'>json_schema</span> [enforce]</td>
              <td>Bounds repair loops to a single attempt and triggers quarantine on second failure.</td>
            </tr>
            <tr>
              <td><b>merkle_state_seal</b><br><code>platform.merkle_ledger</code></td>
              <td><b>security_four_eyes_contract.json</b><br><code class='muted'>.nb/context/contracts/security_four_eyes_contract.json</code></td>
              <td><span class='badge-success'>json_schema</span> [seal_block]</td>
              <td>Signs block hash with SHA-256 and records immutable state transition in context ledger.</td>
            </tr>
            """.trimIndent()
        )

        // 2. Commercial Packaging & Provisioning Flow
        renderPipelineSection(
            "Commercial Packaging, Multi-IDE Provisioning & Tier Permissions Flow",
            ".nb/agentic/custom/workflows/commercial_packaging_provisioning_flow.yaml",
            "End-to-end commercial packaging, multi-IDE provisioning, and cross-platform RBAC feature gating.",
            "Billing Plan Update / Tier Packaging Request",
            "[1. Validate Billing Plans] ➔ [2. Filter Runtime Assets] ➔ [3. Seal License & Merkle] ➔ [4. Provision Multi-IDE/Portal] ➔ [5. Verify RBAC Permissions]",
            """
            <tr>
              <td><b>step_validate_billing_rules</b><br><code>agent_commercial_packager_provisioner</code></td>
              <td><b>billing_meter_contract.yaml</b><br><code class='muted'>.nb/context/contracts/billing_meter_contract.yaml</code></td>
              <td><span class='badge-info'>yaml_schema</span> [validate]</td>
              <td>Verifies subscription tiers, feature flags, and token budget ceilings against billing specifications.</td>
            </tr>
            <tr>
              <td><b>step_filter_and_package_tier</b><br><code>agent_commercial_packager_provisioner</code></td>
              <td><b>commercial_provisioning_contract.yaml</b><br><code class='muted'>.nb/context/contracts/commercial_provisioning_contract.yaml</code></td>
              <td><span class='badge-info'>yaml_schema</span> [filter_and_bundle]</td>
              <td>Governs selective file packaging per tier, enforcing platform core encryption and plaintext user plans.</td>
            </tr>
            <tr>
              <td><b>step_sign_and_seal_license</b><br><code>agent_commercial_packager_provisioner</code></td>
              <td><b>security_tenant_profile_contract.json</b><br><code class='muted'>.nb/context/contracts/security_tenant_profile_contract.json</code></td>
              <td><span class='badge-success'>json_schema</span> [seal_license]</td>
              <td>Encodes tenant profile attributes, tier expiration, and cryptographic signature in license payload.</td>
            </tr>
            <tr>
              <td><b>step_provision_ide_and_portal</b><br><code>agent_commercial_packager_provisioner</code></td>
              <td><b>intellij_plugin_manifest_contract.json</b><br><code class='muted'>.nb/context/contracts/intellij_plugin_manifest_contract.json</code><br><br><b>package_json_manifest_contract.json</b><br><code class='muted'>.nb/context/contracts/package_json_manifest_contract.json</code></td>
              <td><span class='badge-info'>json_schema</span> [verify_manifest]<br><br><span class='badge-info'>json_schema</span> [verify_manifest]</td>
              <td>Validates plugin.xml extension point compatibility and bundled toolwindow components.<br><br>Validates package.json contributes layout, commands, and activation events for the extension.</td>
            </tr>
            <tr>
              <td><b>step_verify_tier_permissions</b><br><code>agent_commercial_packager_provisioner</code></td>
              <td><b>sandbox_permission_contract.json</b><br><code class='muted'>.nb/context/contracts/sandbox_permission_contract.json</code><br><br><b>rbac_permission_matrix.json</b><br><code class='muted'>.nb/context/contracts/rbac_permission_matrix.json</code></td>
              <td><span class='badge-info'>json_schema</span> [verify_security_sandbox]<br><br><span class='badge-info'>json_schema</span> [enforce_entitlements]</td>
              <td>Enforces read/write sandboxing policies and AST token pruning constraints on LLM plugins.<br><br>Guarantees Free Community users cannot execute unexposed basic platform tools or enterprise private VPC endpoints.</td>
            </tr>
            """.trimIndent()
        )

        // 3. Enterprise SDLC PR Gate
        renderPipelineSection(
            "Enterprise PR Gate with Infosec & FinOps Audit",
            ".nb/agentic/custom/workflows/enterprise_sdlc.yaml",
            "Demonstrates hybrid composition of sealed platform executors with customer custom agents.",
            "Enterprise Branch Merge Event",
            "[1. AST Prune] ➔ [2. Token FinOps Audit] ➔ [3. Infosec & Banking Security] ➔ [4. Cross-Module Contracts] ➔ [5. Merkle DAG Block Seal]",
            """
            <tr>
              <td><b>ast_prune</b><br><code>platform.ast_pruner</code></td>
              <td><b>psi_ast_bridge_contract.yaml</b><br><code class='muted'>.nb/context/contracts/psi_ast_bridge_contract.yaml</code></td>
              <td><span class='badge-info'>yaml_schema</span> [prune_ast]</td>
              <td>Extracts function declarations and docstrings while pruning implementation blocks to maximize prompt cache hits.</td>
            </tr>
            <tr>
              <td><b>token_savings_audit</b><br><code>agent_token_finops_auditor</code></td>
              <td><b>billing_meter_contract.yaml</b><br><code class='muted'>.nb/context/contracts/billing_meter_contract.yaml</code></td>
              <td><span class='badge-info'>yaml_schema</span> [audit_metering]</td>
              <td>Verifies cumulative token savings, calculates USD economic value, and compares against billing tier ceilings.</td>
            </tr>
            <tr>
              <td><b>custom_security_audit</b><br><code>agent_security_auditor</code></td>
              <td><b>security_rebac_policy_contract.json</b><br><code class='muted'>.nb/context/contracts/security_rebac_policy_contract.json</code><br><br><b>security_pii_vault_contract.json</b><br><code class='muted'>.nb/context/contracts/security_pii_vault_contract.json</code></td>
              <td><span class='badge-info'>json_schema</span> [audit_policy]<br><br><span class='badge-info'>json_schema</span> [inspect_payload]</td>
              <td>Verifies multi-tenant graph relationships and enterprise access boundaries.<br><br>Scans payloads for unredacted sensitive tokens, cryptographic secrets, or customer PII.</td>
            </tr>
            <tr>
              <td><b>contract_verification</b><br><code>platform.contract_verifier</code></td>
              <td><b>portal_openapi_spec.yaml</b><br><code class='muted'>.nb/context/contracts/portal_openapi_spec.yaml</code><br><br><b>rbac_permission_matrix.json</b><br><code class='muted'>.nb/context/contracts/rbac_permission_matrix.json</code></td>
              <td><span class='badge-info'>openapi_spec</span> [verify_endpoints]<br><br><span class='badge-info'>json_schema</span> [verify_matrix]</td>
              <td>Enforces backward compatibility, schema validation, and route invariants across all exposed REST endpoints.<br><br>Validates access scopes across modules to prevent privilege escalation.</td>
            </tr>
            <tr>
              <td><b>merkle_seal</b><br><code>platform.merkle_ledger</code></td>
              <td><b>security_four_eyes_contract.json</b><br><code class='muted'>.nb/context/contracts/security_four_eyes_contract.json</code></td>
              <td><span class='badge-success'>json_schema</span> [seal_dag_block]</td>
              <td>Validates dual cryptographic signoffs before sealing the state transition block into the immutable Merkle DAG.</td>
            </tr>
            """.trimIndent()
        )

        // 4. IntelliJ & PyCharm Plugin Delivery Flow
        renderPipelineSection(
            "IntelliJ IDEA & PyCharm Plugin End-to-End Delivery Flow",
            ".nb/agentic/custom/workflows/intellij_pycharm_plugin_delivery_flow.yaml",
            "Multi-stage automated delivery pipeline for JetBrains IntelliJ & PyCharm IDE plugins.",
            "JetBrains Platform Release Event",
            "[1. Manifest & Contracts] ➔ [2. PSI Engine & Token Meter] ➔ [3. ToolWindow & UI] ➔ [4. Daemon RPC & Merkle] ➔ [5. Terminal Mode Interceptor]",
            """
            <tr>
              <td><b>stage_1_manifest_and_contracts</b><br><code>agent_jetbrains_plugin_architect</code></td>
              <td><b>intellij_plugin_manifest_contract.json</b><br><code class='muted'>.nb/context/contracts/intellij_plugin_manifest_contract.json</code><br><br><b>psi_ast_bridge_contract.yaml</b><br><code class='muted'>.nb/context/contracts/psi_ast_bridge_contract.yaml</code></td>
              <td><span class='badge-info'>json_schema</span> [validate_manifest]<br><br><span class='badge-info'>yaml_schema</span> [verify_protocol]</td>
              <td>Verifies plugin ID, depends tags (platform, lang), toolWindow declarations, and external annotators.<br><br>Specifies in-memory PyFile/PsiFile AST traversal and token reduction invariants (&lt;35ms latency).</td>
            </tr>
            <tr>
              <td><b>stage_2_psi_engine_and_token_meter</b><br><code>agent_psi_ast_bridge_specialist</code></td>
              <td><b>psi_ast_bridge_contract.yaml</b><br><code class='muted'>.nb/context/contracts/psi_ast_bridge_contract.yaml</code></td>
              <td><span class='badge-info'>yaml_schema</span> [benchmark_ast_pruner]</td>
              <td>Evaluates symbol extraction accuracy and ensures &gt;60% token compression ratio across Python &amp; Kotlin ASTs.</td>
            </tr>
            <tr>
              <td><b>stage_3_toolwindow_and_ui</b><br><code>agent_intellij_ui_ux_engineer</code></td>
              <td><b>ui_theme_token_contract.json</b><br><code class='muted'>.nb/context/contracts/ui_theme_token_contract.json</code><br><br><b>data_grid_contract.json</b><br><code class='muted'>.nb/context/contracts/data_grid_contract.json</code></td>
              <td><span class='badge-info'>json_schema</span> [audit_theme_tokens]<br><br><span class='badge-info'>json_schema</span> [validate_ui_grid]</td>
              <td>Enforces Corporate Light &amp; Enterprise Dark color tokens, WCAG AA contrast (&gt;= 4.5:1), and terminology-neutral styling.<br><br>Validates high-density audit grids and telemetry views in the ToolWindow tab panels.</td>
            </tr>
            <tr>
              <td><b>stage_4_daemon_rpc_and_merkle_seal</b><br><code>agent_jetbrains_plugin_architect</code></td>
              <td><b>daemon_rpc_contract.json</b><br><code class='muted'>.nb/context/contracts/daemon_rpc_contract.json</code><br><br><b>security_four_eyes_contract.json</b><br><code class='muted'>.nb/context/contracts/security_four_eyes_contract.json</code></td>
              <td><span class='badge-info'>json_schema</span> [test_ipc_bridge]<br><br><span class='badge-success'>json_schema</span> [seal_recovery_block]</td>
              <td>Verifies bidirectional UNIX socket/IPC communication between IDE ToolWindow and .nb/bin/percipience binary.<br><br>Cryptographically seals verified build hash into local Merkle ledger before deployment.</td>
            </tr>
            <tr>
              <td><b>stage_5_terminal_agent_interceptor</b><br><code>agent_terminal_mode_specialist</code></td>
              <td><b>terminal_agent_ast_contract.yaml</b><br><code class='muted'>.nb/context/contracts/terminal_agent_ast_contract.yaml</code></td>
              <td><span class='badge-info'>yaml_schema</span> [verify_terminal_hook]</td>
              <td>Injects AST-compressed context into Claude Code, Gemini CLI, and Aider sessions with zero disk contamination.</td>
            </tr>
            """.trimIndent()
        )

        // 5. Connected IoT & Mobile Delivery Flow
        renderPipelineSection(
            "Connected IoT, Embedded Firmware & Mobile Delivery Flow",
            ".nb/agentic/custom/workflows/iot_mobile_delivery_flow.yaml",
            "Orchestrates BLE GATT contract verification, FreeRTOS/Zephyr firmware, and KMP mobile client.",
            "Embedded Firmware & KMP Release",
            "[1. BLE GATT Contract Gate] ➔ [2. Mobile KMP Client & UI] ➔ [3. IoT Ecosystem Invariant Audit]",
            """
            <tr>
              <td><b>step_ble_gatt_contract_gate</b><br><code>agent_contract_compatibility_checker</code></td>
              <td><b>ble_gatt_spec.yaml</b><br><code class='muted'>.nb/context/contracts/ble_gatt_spec.yaml</code></td>
              <td><span class='badge-info'>yaml_schema</span> [verify_gatt_services]</td>
              <td>Validates primary UUIDs, MTU constraints (up to 512 bytes), and characteristic read/write/notify permission profiles.</td>
            </tr>
            <tr>
              <td><b>step_mobile_kmp_client</b><br><code>agent_mobile_developer</code></td>
              <td><b>ota_firmware_manifest.json</b><br><code class='muted'>.nb/context/contracts/ota_firmware_manifest.json</code><br><br><b>ui_theme_token_contract.json</b><br><code class='muted'>.nb/context/contracts/ui_theme_token_contract.json</code></td>
              <td><span class='badge-info'>json_schema</span> [verify_ota_payload]<br><br><span class='badge-info'>json_schema</span> [audit_mobile_tokens]</td>
              <td>Verifies cryptographic hash, firmware version semver, and target hardware architecture metadata.<br><br>Enforces design token consistency and WCAG compliance for Kotlin Multiplatform mobile screens.</td>
            </tr>
            <tr>
              <td><b>step_iot_ecosystem_audit</b><br><code>agent_iot_mobile_ecosystem_architect</code></td>
              <td><b>security_pii_vault_contract.json</b><br><code class='muted'>.nb/context/contracts/security_pii_vault_contract.json</code><br><br><b>security_four_eyes_contract.json</b><br><code class='muted'>.nb/context/contracts/security_four_eyes_contract.json</code></td>
              <td><span class='badge-info'>json_schema</span> [sanitize_telemetry]<br><br><span class='badge-success'>json_schema</span> [seal_firmware_release]</td>
              <td>Guarantees sensor and location metrics sent from embedded nodes do not leak unredacted PII.<br><br>Cryptographically seals binary firmware payload hash and KMP client artifacts before publication.</td>
            </tr>
            """.trimIndent()
        )

        // 6. Enterprise SaaS Portal Multi-Module Delivery Flow
        renderPipelineSection(
            "Enterprise SaaS & Portal Multi-Module Delivery Flow",
            ".nb/agentic/custom/workflows/saas_portal_delivery_flow.yaml",
            "Orchestrates Next.js/Tailwind frontend, API gateway, Stripe billing webhooks, and security audit.",
            "Portal Webhook / Production Gate",
            "[1. OpenAPI 3.1 Contract Gate] ➔ [2. Frontend UI Scaffold] ➔ [3. SaaS Backend Gateway] ➔ [4. Multi-Tenant Security Audit]",
            """
            <tr>
              <td><b>step_openapi_contract_gate</b><br><code>agent_contract_compatibility_checker</code></td>
              <td><b>portal_openapi_spec.yaml</b><br><code class='muted'>.nb/context/contracts/portal_openapi_spec.yaml</code></td>
              <td><span class='badge-info'>openapi_spec</span> [verify_api_contract]</td>
              <td>Validates REST route schemas, response codes, and request bodies for SaaS portal endpoints.</td>
            </tr>
            <tr>
              <td><b>step_portal_frontend_scaffold</b><br><code>agent_portal_developer</code></td>
              <td><b>ui_theme_token_contract.json</b><br><code class='muted'>.nb/context/contracts/ui_theme_token_contract.json</code><br><br><b>data_grid_contract.json</b><br><code class='muted'>.nb/context/contracts/data_grid_contract.json</code></td>
              <td><span class='badge-info'>json_schema</span> [audit_theme_tokens]<br><br><span class='badge-info'>json_schema</span> [validate_grid_components]</td>
              <td>Ensures zero dark-grey tints in Corporate Light mode, 4.5:1 WCAG contrast, and zero mobile frame restrictions.<br><br>Validates responsive data table rendering, pagination, and sorting structures in the portal UI.</td>
            </tr>
            <tr>
              <td><b>step_saas_backend_gateway</b><br><code>agent_saas_backend_developer</code></td>
              <td><b>billing_webhook_contract.json</b><br><code class='muted'>.nb/context/contracts/billing_webhook_contract.json</code><br><br><b>billing_meter_contract.yaml</b><br><code class='muted'>.nb/context/contracts/billing_meter_contract.yaml</code></td>
              <td><span class='badge-info'>json_schema</span> [verify_webhook_signatures]<br><br><span class='badge-info'>yaml_schema</span> [verify_metering_limits]</td>
              <td>Enforces HMAC SHA-256 signature verification and webhook event payloads for subscription lifecycle events.<br><br>Enforces tenant seat quotas, token consumption limits, and tier feature gates.</td>
            </tr>
            <tr>
              <td><b>step_saas_security_audit</b><br><code>agent_enterprise_saas_portal_architect</code></td>
              <td><b>security_tenant_profile_contract.json</b><br><code class='muted'>.nb/context/contracts/security_tenant_profile_contract.json</code><br><br><b>security_rebac_policy_contract.json</b><br><code class='muted'>.nb/context/contracts/security_rebac_policy_contract.json</code></td>
              <td><span class='badge-info'>json_schema</span> [verify_tenant_isolation]<br><br><span class='badge-info'>json_schema</span> [enforce_rebac_policies]</td>
              <td>Verifies database row-level security (RLS) tenant isolation and JWT tenant claims.<br><br>Asserts role relationships and admin workspace boundaries before gateway deployment.</td>
            </tr>
            """.trimIndent()
        )

        // 7. Visual Studio Code Extension Delivery Flow
        renderPipelineSection(
            "Visual Studio Code Extension End-to-End Delivery Flow",
            ".nb/agentic/custom/workflows/vscode_plugin_delivery_flow.yaml",
            "Multi-stage automated delivery pipeline for Visual Studio Code VSIX Extension &amp; LSP Client.",
            "VSIX Publish & LSP Verification",
            "[1. Package Manifest Gate] ➔ [2. LSP 3.17 Subsystem] ➔ [3. Webview Dashboard] ➔ [4. Socket IPC & Merkle Seal]",
            """
            <tr>
              <td><b>stage_1_manifest_and_activation</b><br><code>agent_vscode_extension_architect</code></td>
              <td><b>package_json_manifest_contract.json</b><br><code class='muted'>.nb/context/contracts/package_json_manifest_contract.json</code><br><br><b>sandbox_permission_contract.json</b><br><code class='muted'>.nb/context/contracts/sandbox_permission_contract.json</code></td>
              <td><span class='badge-info'>json_schema</span> [validate_manifest]<br><br><span class='badge-info'>json_schema</span> [enforce_sandbox_isolation]</td>
              <td>Verifies contributes schemas, views, commands, and activationEvents configuration.<br><br>Prohibits wildcard onStartupFinished activation, requiring explicit onCommand or onLanguage triggers.</td>
            </tr>
            <tr>
              <td><b>stage_2_lsp_subsystem</b><br><code>agent_lsp_language_features_specialist</code></td>
              <td><b>lsp_protocol_contract.yaml</b><br><code class='muted'>.nb/context/contracts/lsp_protocol_contract.yaml</code></td>
              <td><span class='badge-info'>yaml_schema</span> [test_lsp_compliance]</td>
              <td>Tests textDocument/publishDiagnostics, codeLens, and incremental synchronization latency (&lt;50ms).</td>
            </tr>
            <tr>
              <td><b>stage_3_webview_dashboard</b><br><code>agent_vscode_webview_ux_engineer</code></td>
              <td><b>webview_message_rpc_contract.json</b><br><code class='muted'>.nb/context/contracts/webview_message_rpc_contract.json</code><br><br><b>ui_theme_token_contract.json</b><br><code class='muted'>.nb/context/contracts/ui_theme_token_contract.json</code></td>
              <td><span class='badge-info'>json_schema</span> [verify_csp_and_rpc]<br><br><span class='badge-info'>json_schema</span> [audit_theme_sync]</td>
              <td>Ensures zero inline script execution without cryptographic nonces, and validates postMessage RPC schemas.<br><br>Synchronizes VS Code CSS variables (--vscode-*) with corporate design tokens for light and dark modes.</td>
            </tr>
            <tr>
              <td><b>stage_4_ipc_and_gate_seal</b><br><code>agent_vscode_extension_architect</code></td>
              <td><b>daemon_rpc_contract.json</b><br><code class='muted'>.nb/context/contracts/daemon_rpc_contract.json</code><br><br><b>security_four_eyes_contract.json</b><br><code class='muted'>.nb/context/contracts/security_four_eyes_contract.json</code></td>
              <td><span class='badge-info'>json_schema</span> [test_socket_ipc]<br><br><span class='badge-success'>json_schema</span> [seal_recovery_block]</td>
              <td>Verifies UNIX socket IPC throughput and error handling between extension and CLI daemon.<br><br>Signs VSIX package distribution hash into the local Merkle ledger before publication.</td>
            </tr>
            """.trimIndent()
        )

        sb.append("<h3>🤖 Active Specialist Agents Registry</h3>")
        sb.append("<ul>")
        sb.append("<li><code>agent_psi_ast_bridge_specialist</code> - Fast AST skeletonization &amp; signature preservation</li>")
        sb.append("<li><code>agent_jetbrains_plugin_architect</code> - Plugin structure, threading, and toolwindow registration</li>")
        sb.append("<li><code>agent_autonomous_healer</code> - Bounded TDD auto-healing (1-attempt bound)</li>")
        sb.append("<li><code>agent_merkle_ledger</code> - Cryptographic SHA-256 state DAG block sealing</li>")
        sb.append("<li><code>agent_commercial_packager_provisioner</code> - Tier packaging and license provisioning [Team+]</li>")
        sb.append("<li><code>agent_vscode_extension_architect</code> - VS Code extension packaging and IPC bridge [Team+]</li>")
        sb.append("<li><code>agent_enterprise_saas_portal_architect</code> - Multi-tenant SaaS and swarm orchestration [Enterprise]</li>")
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
        sb.append("<li><b>Dynamic Context Injection:</b> Generates compact context files (<code>.nb/context/percipience_claude_context.md</code>, <code>.nb/context/percipience_gemini_context.md</code>) loaded directly into CLI prompts.</li>")
        sb.append("<li><b>FinOps Ledger Metering:</b> All terminal prompt invocations are recorded into <code>token_savings_ledger.yaml</code> to calculate gross USD saved and net customer ROI.</li>")
        sb.append("</ul>")
        sb.append("<h3>🚀 Quick Commands</h3>")
        sb.append("<ul>")
        sb.append("<li><code>percipience wrap claude-code</code> - Injects AST stripped skeletons directly into Claude Code.</li>")
        sb.append("<li><code>percipience wrap gemini-cli</code> - Injects AST stripped skeletons directly into Gemini CLI.</li>")
        sb.append("<li><code>percipience terminal hook</code> - Outputs dynamic eval hook for zsh/bash shell startup.</li>")
        sb.append("</ul>")
        sb.append("</body></html>")

        val editorPane = JEditorPane("text/html", sb.toString())
        editorPane.isEditable = false
        editorPane.background = UIUtil.getPanelBackground()

        val buttonPanel = JPanel(FlowLayout(FlowLayout.LEFT, 8, 8))
        val btnClaude = JButton("⚡ Prepare Claude Code Context")
        btnClaude.addActionListener {
            val execService = PercipienceExecutionService.getInstance(project)
            ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Exporting Claude Code AST Context...", false) {
                private var result: ExecutionResult? = null

                override fun run(indicator: ProgressIndicator) {
                    result = runBlocking { execService.runContextExport("claude-code", ".nb/context/percipience_claude_context.md") }
                }

                override fun onSuccess() {
                    val res = result ?: return
                    Messages.showInfoMessage(project, res.stdout, "Claude Code Context Export")
                }

                override fun onThrowable(error: Throwable) {
                    Messages.showErrorDialog(project, error.message ?: "Export failed", "Error")
                }
            })
        }

        val btnGemini = JButton("✨ Prepare Gemini CLI Context")
        btnGemini.addActionListener {
            val execService = PercipienceExecutionService.getInstance(project)
            ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Exporting Gemini CLI AST Context...", false) {
                private var result: ExecutionResult? = null

                override fun run(indicator: ProgressIndicator) {
                    result = runBlocking { execService.runContextExport("gemini-cli", ".nb/context/percipience_gemini_context.md") }
                }

                override fun onSuccess() {
                    val res = result ?: return
                    Messages.showInfoMessage(project, res.stdout, "Gemini CLI Context Export")
                }

                override fun onThrowable(error: Throwable) {
                    Messages.showErrorDialog(project, error.message ?: "Export failed", "Error")
                }
            })
        }

        val btnStatus = JButton("📊 Terminal FinOps Status")
        btnStatus.addActionListener {
            val execService = PercipienceExecutionService.getInstance(project)
            ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Loading Terminal FinOps Status...", false) {
                private var result: ExecutionResult? = null

                override fun run(indicator: ProgressIndicator) {
                    result = runBlocking { execService.runTerminalStatus() }
                }

                override fun onSuccess() {
                    val res = result ?: return
                    Messages.showInfoMessage(project, res.stdout, "Terminal Agent FinOps Status")
                }

                override fun onThrowable(error: Throwable) {
                    Messages.showErrorDialog(project, error.message ?: "Status error", "Error")
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

    private fun createSwarmGovernancePanel(project: Project): JComponent {
        val mainPanel = JPanel(BorderLayout(10, 10))
        mainPanel.border = EmptyBorder(12, 12, 12, 12)
        mainPanel.background = UIUtil.getPanelBackground()

        val isDark = UIUtil.isUnderDarcula()
        val sb = StringBuilder()
        sb.append("<html><head>").append(getThemeCss(isDark)).append("</head><body>")
        sb.append("<h2>🐝 Swarm Governance &amp; Fleet Management</h2>")
        sb.append("<p>Orchestrate distributed autonomous multi-agent swarms with topological DAG wave execution, multi-pillar self-reflection critics, 2-of-3 Byzantine model consensus, capability token enforcement (CBAC), and workstation fleet monitoring.</p>")

        sb.append("<h3>⚡ Key Swarm Subsystems</h3>")
        sb.append("<ul>")
        sb.append("<li><b>Dynamic DAG Orchestrator:</b> Runtime goal-expansion and topological wave execution (<code>.nb/bin/percipience swarm dag</code>).</li>")
        sb.append("<li><b>Autonomous Self-Reflection Critic:</b> Zero-disk-write critique verifying architecture, security, and schema invariants (<code>.nb/bin/percipience swarm reflexion</code>).</li>")
        sb.append("<li><b>Multi-Model Consensus Quorum:</b> 2-of-3 model voting attestation across Claude, GPT-4, and Gemini with cryptographic signatures (<code>.nb/bin/percipience swarm consensus</code>).</li>")
        sb.append("<li><b>Capability-Based Access Control (CBAC):</b> HMAC-SHA256 minted capability envelopes constraining agent file, network, and tool rights (<code>.nb/bin/percipience swarm cbac</code>).</li>")
        sb.append("<li><b>Workstation &amp; Fleet FinOps:</b> Multi-node telemetry tracking CPU/RAM load, task progress, and 15% platform rev-share fee / 85% customer net ROI (<code>.nb/bin/percipience swarm fleet</code>).</li>")
        sb.append("</ul>")

        sb.append("<h3>🛠️ Swarm Operations</h3>")
        sb.append("<p>Use the action buttons below to trigger real-time swarm orchestrations directly in your IDE workspace.</p>")
        sb.append("</body></html>")

        val editorPane = JEditorPane("text/html", sb.toString())
        editorPane.isEditable = false
        editorPane.background = UIUtil.getPanelBackground()

        val buttonPanel = JPanel(FlowLayout(FlowLayout.LEFT, 8, 8))

        val btnDag = JButton("🌊 Execute Swarm DAG Wave")
        btnDag.addActionListener {
            val execService = PercipienceExecutionService.getInstance(project)
            ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Executing Swarm Wave...", false) {
                private var result: ExecutionResult? = null

                override fun run(indicator: ProgressIndicator) {
                    result = runBlocking { execService.runSwarmDag("exec") }
                }

                override fun onSuccess() {
                    val res = result ?: return
                    if (res.success) {
                        Messages.showInfoMessage(project, "Swarm Wave Execution Succeeded!\n\n${res.stdout}", "Swarm DAG")
                    } else {
                        Messages.showErrorDialog(project, "Swarm Wave Failed:\n\n${res.stderr.ifEmpty { res.stdout }}", "Swarm Wave Error")
                    }
                }

                override fun onThrowable(error: Throwable) {
                    Messages.showErrorDialog(project, error.message ?: "DAG execution error", "Error")
                }
            })
        }

        val btnReflexion = JButton("🔍 Self-Reflection Critic")
        btnReflexion.addActionListener {
            val execService = PercipienceExecutionService.getInstance(project)
            ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Running Reflexion Critic...", false) {
                private var result: ExecutionResult? = null

                override fun run(indicator: ProgressIndicator) {
                    result = runBlocking { execService.runSwarmReflexion() }
                }

                override fun onSuccess() {
                    val res = result ?: return
                    if (res.success) {
                        Messages.showInfoMessage(project, "Reflexion Invariants Passed!\n\n${res.stdout}", "Swarm Reflexion")
                    } else {
                        Messages.showErrorDialog(project, "Reflexion Violated Invariants:\n\n${res.stderr.ifEmpty { res.stdout }}", "Reflexion Violated")
                    }
                }

                override fun onThrowable(error: Throwable) {
                    Messages.showErrorDialog(project, error.message ?: "Reflexion error", "Error")
                }
            })
        }

        val btnConsensus = JButton("⚖️ Consensus Quorum")
        btnConsensus.addActionListener {
            val execService = PercipienceExecutionService.getInstance(project)
            ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Verifying Multi-Model Consensus...", false) {
                private var result: ExecutionResult? = null

                override fun run(indicator: ProgressIndicator) {
                    result = runBlocking { execService.runSwarmConsensus("PR Gate Approval") }
                }

                override fun onSuccess() {
                    val res = result ?: return
                    if (res.success) {
                        Messages.showInfoMessage(project, "Consensus Quorum Passed!\n\n${res.stdout}", "Consensus Quorum")
                    } else {
                        Messages.showErrorDialog(project, "Consensus Quorum Failed:\n\n${res.stderr.ifEmpty { res.stdout }}", "Consensus Rejected")
                    }
                }

                override fun onThrowable(error: Throwable) {
                    Messages.showErrorDialog(project, error.message ?: "Consensus error", "Error")
                }
            })
        }

        val btnCbac = JButton("🛡️ Mint CBAC Token")
        btnCbac.addActionListener {
            val execService = PercipienceExecutionService.getInstance(project)
            ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Minting CBAC Token...", false) {
                private var result: ExecutionResult? = null

                override fun run(indicator: ProgressIndicator) {
                    result = runBlocking { execService.runSwarmCbac("agent_sandbox_coder") }
                }

                override fun onSuccess() {
                    val res = result ?: return
                    if (res.success) {
                        Messages.showInfoMessage(project, "CBAC Token Minted:\n\n${res.stdout}", "CBAC Minted")
                    } else {
                        Messages.showErrorDialog(project, "CBAC Minting Failed:\n\n${res.stderr.ifEmpty { res.stdout }}", "CBAC Error")
                    }
                }

                override fun onThrowable(error: Throwable) {
                    Messages.showErrorDialog(project, error.message ?: "CBAC error", "Error")
                }
            })
        }

        val btnFleet = JButton("🚀 Workstation & Fleet Status")
        btnFleet.addActionListener {
            val execService = PercipienceExecutionService.getInstance(project)
            ProgressManager.getInstance().run(object : Task.Backgroundable(project, "Querying Fleet Status...", false) {
                private var result: ExecutionResult? = null

                override fun run(indicator: ProgressIndicator) {
                    result = runBlocking { execService.runSwarmFleet(simulatePulse = true) }
                }

                override fun onSuccess() {
                    val res = result ?: return
                    if (res.success) {
                        Messages.showInfoMessage(project, "Fleet Status & FinOps:\n\n${res.stdout}", "Fleet Status")
                    } else {
                        Messages.showErrorDialog(project, "Fleet Inspection Failed:\n\n${res.stderr.ifEmpty { res.stdout }}", "Fleet Error")
                    }
                }

                override fun onThrowable(error: Throwable) {
                    Messages.showErrorDialog(project, error.message ?: "Fleet query error", "Error")
                }
            })
        }

        buttonPanel.add(btnDag)
        buttonPanel.add(btnReflexion)
        buttonPanel.add(btnConsensus)
        buttonPanel.add(btnCbac)
        buttonPanel.add(btnFleet)

        mainPanel.add(JBScrollPane(editorPane), BorderLayout.CENTER)
        mainPanel.add(buttonPanel, BorderLayout.SOUTH)
        return mainPanel
    }

    private fun createUserGuidePanel(project: Project): JComponent {
        val isDark = UIUtil.isUnderDarcula()
        val sb = StringBuilder()
        sb.append("<html><head>").append(getThemeCss(isDark)).append("</head><body>")
        sb.append("<h2>📘 Percipience Platform User Guide</h2>")
        sb.append("<p>Welcome to <b>Percipience</b> — the contextual engineering operating system for JetBrains IDEs.</p>")

        sb.append("<h3>1. Core Architecture</h3>")
        sb.append("<p>Percipience structures software development into a deterministic, layered hierarchy of invariants, schemas, and execution plans.</p>")
        sb.append("<ul>")
        sb.append("<li><b>Layer 0 (L0) - Master Governance:</b> Platform rules, Merkle chain validation, and sandbox policies.</li>")
        sb.append("<li><b>Layer 1 (L1) - Domain Engine:</b> Feature specifications, AST pruning routines, and tool integrations.</li>")
        sb.append("<li><b>Layer 2 (L2) - Deployment:</b> Packaging, tier bundles, and CI/CD automation.</li>")
        sb.append("</ul>")

        sb.append("<h3>2. Key Operations</h3>")
        sb.append("<ul>")
        sb.append("<li><b>Run PR Gatekeeper:</b> Validates tests, static analysis, and seals a cryptographic Merkle block.</li>")
        sb.append("<li><b>Verify Merkle Chain:</b> Verifies the integrity of the linear SHA-256 block sequence.</li>")
        sb.append("<li><b>Autonomous CI/CD:</b> Runs automated test suites with bounded auto-healing retry logic.</li>")
        sb.append("<li><b>AST Token Pruning:</b> Strips unnecessary implementation bodies before feeding context to LLM agents.</li>")
        sb.append("</ul>")

        sb.append("<h3>3. JetBrains Threading Model</h3>")
        sb.append("<p>All background CLI commands and coroutines run asynchronously off the Event Dispatch Thread (EDT) via <code>Task.Backgroundable</code>. UI updates, label refreshes, and modal dialogs are dispatched safely on the EDT via <code>onSuccess()</code> callbacks.</p>")

        sb.append("</body></html>")

        val editorPane = JEditorPane("text/html", sb.toString())
        editorPane.isEditable = false
        editorPane.background = UIUtil.getPanelBackground()
        return JBScrollPane(editorPane)
    }
}
