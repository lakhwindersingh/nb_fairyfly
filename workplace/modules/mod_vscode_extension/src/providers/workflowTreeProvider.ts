import * as vscode from 'vscode';
import * as path from 'path';

export interface HandledContractInfo {
  contractId: string;
  name: string;
  path: string;
  type: string;
  action: string;
  description: string;
}

export interface WorkflowStageInfo {
  id: string;
  name: string;
  executor: string;
  action?: string;
  dependsOn?: string[];
  handledContracts: HandledContractInfo[];
}

export interface DeliveryPipelineInfo {
  id: string;
  name: string;
  description: string;
  source: string;
  trigger: string;
  version: string;
  status: string;
  stages: WorkflowStageInfo[];
}

export const DELIVERY_PIPELINES_REGISTRY: DeliveryPipelineInfo[] = [
  {
    id: 'basic_autonomous_cicd',
    name: 'Free Community Autonomous CI/CD Pipeline',
    description: 'Automated workspace hygiene, AST token compression, bounded self-repair, and Merkle block sealing.',
    source: '.nb/agentic/custom/workflows/basic_autonomous_cicd.yaml',
    trigger: 'Free Plan / Pre-Commit / Local CLI',
    version: '1.0.0',
    status: 'Active - [✔ HEALTHY]',
    stages: [
      {
        id: 'sustain_maintenance',
        name: 'Self-Sustaining Workspace Hygiene',
        executor: 'platform.self_sustaining_engine',
        action: 'warn_and_continue',
        handledContracts: [
          {
            contractId: 'observability_contract',
            name: 'Observability Telemetry & Log Format Contract',
            path: '.nb/context/contracts/observability_contract.yaml',
            type: 'yaml_schema',
            action: 'validate',
            description: 'Enforces structured logging, health status schema, and hygiene execution metrics.'
          },
          {
            contractId: 'hierarchical_rule_contract',
            name: 'Hierarchical Space Isolation & Scratch Hygiene Contract',
            path: '.nb/context/contracts/hierarchical_rule_contract.json',
            type: 'json_schema',
            action: 'enforce',
            description: 'Verifies boundary rules ensuring scratch directory cleanup does not violate quad-space isolation.'
          }
        ]
      },
      {
        id: 'ast_token_reduction',
        name: 'AST Token Skeletonization & Attention Budgeting',
        executor: 'platform.ast_pruner',
        dependsOn: ['sustain_maintenance'],
        handledContracts: [
          {
            contractId: 'psi_ast_bridge_contract',
            name: 'AST Skeleton & Token Compression Contract',
            path: '.nb/context/contracts/psi_ast_bridge_contract.yaml',
            type: 'yaml_schema',
            action: 'inspect_and_prune',
            description: 'Preserves signatures and docstrings while stripping function bodies for 65% token savings.'
          }
        ]
      },
      {
        id: 'contract_and_test_gate',
        name: 'Basic Contract & Test Verification',
        executor: 'platform.contract_verifier',
        dependsOn: ['ast_token_reduction'],
        handledContracts: [
          {
            contractId: 'rbac_permission_matrix',
            name: 'RBAC Permission Matrix Contract',
            path: '.nb/context/contracts/rbac_permission_matrix.json',
            type: 'json_schema',
            action: 'validate',
            description: 'Asserts baseline permission matrices and role access controls before test execution.'
          },
          {
            contractId: 'data_grid_contract',
            name: 'Data Grid & Table Schema Contract',
            path: '.nb/context/contracts/data_grid_contract.json',
            type: 'json_schema',
            action: 'validate',
            description: 'Validates data structure formats across test payloads and fixture outputs.'
          }
        ]
      },
      {
        id: 'bounded_auto_heal',
        name: 'Basic Single-Attempt Self-Healing',
        executor: 'platform.autonomous_healer',
        dependsOn: ['contract_and_test_gate'],
        handledContracts: [
          {
            contractId: 'hierarchical_rule_contract',
            name: 'Bounded Self-Repair Fallback Policy Contract',
            path: '.nb/context/contracts/hierarchical_rule_contract.json',
            type: 'json_schema',
            action: 'enforce',
            description: 'Bounds repair loops to 1 attempt and activates quarantine fallback on error.'
          }
        ]
      },
      {
        id: 'merkle_state_seal',
        name: 'Cryptographic Merkle State Block Seal',
        executor: 'platform.merkle_ledger',
        action: 'SEAL_BLOCK',
        dependsOn: ['bounded_auto_heal'],
        handledContracts: [
          {
            contractId: 'security_four_eyes_contract',
            name: 'Cryptographic Four-Eyes State Sealing Contract',
            path: '.nb/context/contracts/security_four_eyes_contract.json',
            type: 'json_schema',
            action: 'seal_block',
            description: 'Signs block hash with SHA-256 and records immutable state transition in context ledger.'
          }
        ]
      }
    ]
  },
  {
    id: 'commercial_packaging_provisioning_flow',
    name: 'Commercial Packaging, Multi-IDE Provisioning & Tier Permissions Flow',
    description: 'Tier entitlement bundling, multi-IDE provisioning, and RBAC feature gating.',
    source: '.nb/agentic/custom/workflows/commercial_packaging_provisioning_flow.yaml',
    trigger: 'Billing Event / Tier Packaging Request',
    version: '1.0.0',
    status: 'Ready - [✔ HEALTHY]',
    stages: [
      {
        id: 'step_validate_billing_rules',
        name: 'Validate Pricing Matrix & Billing Plans Schema',
        executor: 'agent_commercial_packager_provisioner',
        action: 'validate_schema',
        handledContracts: [
          {
            contractId: 'billing_meter_contract',
            name: 'Billing Meter & Tier Quotas Contract',
            path: '.nb/context/contracts/billing_meter_contract.yaml',
            type: 'yaml_schema',
            action: 'validate',
            description: 'Verifies subscription tiers, feature flags, and token budget ceilings against billing specs.'
          }
        ]
      },
      {
        id: 'step_filter_and_package_tier',
        name: 'Filter Runtime Assets & Build Tier Distribution Bundle',
        executor: 'agent_commercial_packager_provisioner',
        action: 'package_tier',
        handledContracts: [
          {
            contractId: 'commercial_provisioning_contract',
            name: 'Commercial Provisioning & Asset Filter Contract',
            path: '.nb/context/contracts/commercial_provisioning_contract.yaml',
            type: 'yaml_schema',
            action: 'filter_and_bundle',
            description: 'Enforces platform core encryption and plaintext user plans per distribution tier.'
          }
        ]
      },
      {
        id: 'step_sign_and_seal_license',
        name: 'Generate Cryptographically Signed License & Merkle Seal',
        executor: 'agent_commercial_packager_provisioner',
        action: 'seal_license',
        handledContracts: [
          {
            contractId: 'security_tenant_profile_contract',
            name: 'Tenant Identity & Cryptographic Licensing Contract',
            path: '.nb/context/contracts/security_tenant_profile_contract.json',
            type: 'json_schema',
            action: 'seal_license',
            description: 'Encodes tenant profile attributes, tier expiration, and cryptographic signature in license payload.'
          }
        ]
      },
      {
        id: 'step_provision_ide_and_portal',
        name: 'Provision Runtime Bundle to IntelliJ, VSCode, and SaaS Portal',
        executor: 'agent_commercial_packager_provisioner',
        action: 'provision_target',
        handledContracts: [
          {
            contractId: 'intellij_plugin_manifest_contract',
            name: 'IntelliJ IDEA Plugin Manifest Contract',
            path: '.nb/context/contracts/intellij_plugin_manifest_contract.json',
            type: 'json_schema',
            action: 'verify_manifest',
            description: 'Validates plugin.xml extension point compatibility and bundled toolwindow components.'
          },
          {
            contractId: 'package_json_manifest_contract',
            name: 'VS Code Package Manifest Contract',
            path: '.nb/context/contracts/package_json_manifest_contract.json',
            type: 'json_schema',
            action: 'verify_manifest',
            description: 'Validates package.json contributes layout, commands, and activation events for the extension.'
          }
        ]
      },
      {
        id: 'step_verify_tier_permissions',
        name: 'Verify Cross-Platform Feature Gating & RBAC Permissions',
        executor: 'agent_commercial_packager_provisioner',
        action: 'verify_permissions',
        handledContracts: [
          {
            contractId: 'sandbox_permission_contract',
            name: 'Sandbox Capability Broker Contract',
            path: '.nb/context/contracts/sandbox_permission_contract.json',
            type: 'json_schema',
            action: 'verify_security_sandbox',
            description: 'Enforces read/write sandboxing policies and AST token pruning constraints on LLM plugins.'
          },
          {
            contractId: 'rbac_permission_matrix',
            name: 'Role-Based Access Control Entitlement Matrix',
            path: '.nb/context/contracts/rbac_permission_matrix.json',
            type: 'json_schema',
            action: 'enforce_entitlements',
            description: 'Guarantees Free Community users cannot execute unexposed basic platform tools.'
          }
        ]
      }
    ]
  },
  {
    id: 'enterprise_sdlc',
    name: 'Enterprise PR Gate with Infosec & FinOps Audit',
    description: 'Hybrid composition of sealed platform executors with infosec, banking, and FinOps audit agents.',
    source: '.nb/agentic/custom/workflows/enterprise_sdlc.yaml',
    trigger: 'Enterprise Branch Merge Event',
    version: '1.0.0',
    status: 'Ready - [✔ HEALTHY]',
    stages: [
      {
        id: 'ast_prune',
        name: 'Structural AST Token Pruner',
        executor: 'platform.ast_pruner',
        handledContracts: [
          {
            contractId: 'psi_ast_bridge_contract',
            name: 'Structural AST Bridge & Token Slicing Contract',
            path: '.nb/context/contracts/psi_ast_bridge_contract.yaml',
            type: 'yaml_schema',
            action: 'prune_ast',
            description: 'Extracts function declarations and docstrings while pruning implementation blocks.'
          }
        ]
      },
      {
        id: 'token_savings_audit',
        name: 'Autonomous Token FinOps & Metering Verification',
        executor: 'agent_token_finops_auditor',
        dependsOn: ['ast_prune'],
        handledContracts: [
          {
            contractId: 'billing_meter_contract',
            name: 'Token Savings FinOps Metering Contract',
            path: '.nb/context/contracts/billing_meter_contract.yaml',
            type: 'yaml_schema',
            action: 'audit_metering',
            description: 'Verifies cumulative token savings, calculates USD value, and checks billing ceilings.'
          }
        ]
      },
      {
        id: 'custom_security_audit',
        name: 'Enterprise Infosec & Banking Rule Audit',
        executor: 'agent_security_auditor',
        dependsOn: ['token_savings_audit'],
        handledContracts: [
          {
            contractId: 'security_rebac_policy_contract',
            name: 'Relationship-Based Access Control (ReBAC) Contract',
            path: '.nb/context/contracts/security_rebac_policy_contract.json',
            type: 'json_schema',
            action: 'audit_policy',
            description: 'Verifies multi-tenant graph relationships and enterprise access boundaries.'
          },
          {
            contractId: 'security_pii_vault_contract',
            name: 'PII Vault & Data Protection Contract',
            path: '.nb/context/contracts/security_pii_vault_contract.json',
            type: 'json_schema',
            action: 'inspect_payload',
            description: 'Scans payloads for unredacted sensitive tokens, cryptographic secrets, or customer PII.'
          }
        ]
      },
      {
        id: 'contract_verification',
        name: 'Cross-Module Schema Verification',
        executor: 'platform.contract_verifier',
        dependsOn: ['custom_security_audit'],
        handledContracts: [
          {
            contractId: 'portal_openapi_spec',
            name: 'OpenAPI 3.1 REST Wire Specification Contract',
            path: '.nb/context/contracts/portal_openapi_spec.yaml',
            type: 'openapi_spec',
            action: 'verify_endpoints',
            description: 'Enforces backward compatibility and route invariants across all exposed REST endpoints.'
          },
          {
            contractId: 'rbac_permission_matrix',
            name: 'Cross-Module RBAC Matrix Contract',
            path: '.nb/context/contracts/rbac_permission_matrix.json',
            type: 'json_schema',
            action: 'verify_matrix',
            description: 'Validates access scopes across modules to prevent privilege escalation.'
          }
        ]
      },
      {
        id: 'merkle_seal',
        name: 'Merkle State DAG Block Sealer',
        executor: 'platform.merkle_ledger',
        action: 'SEAL_BLOCK',
        dependsOn: ['contract_verification'],
        handledContracts: [
          {
            contractId: 'security_four_eyes_contract',
            name: 'Cryptographic Four-Eyes Merkle Seal Contract',
            path: '.nb/context/contracts/security_four_eyes_contract.json',
            type: 'json_schema',
            action: 'seal_dag_block',
            description: 'Validates dual signoffs before sealing state transition block into Merkle DAG.'
          }
        ]
      }
    ]
  },
  {
    id: 'intellij_pycharm_plugin_delivery_flow',
    name: 'IntelliJ IDEA & PyCharm Plugin Delivery Flow',
    description: 'Multi-stage delivery pipeline for JetBrains IntelliJ & PyCharm plugins.',
    source: '.nb/agentic/custom/workflows/intellij_pycharm_plugin_delivery_flow.yaml',
    trigger: 'JetBrains Platform Release Event',
    version: '1.0.0',
    status: 'Ready - [✔ HEALTHY]',
    stages: [
      {
        id: 'stage_1_manifest_and_contracts',
        name: 'Manifest & Wire Contract Validation',
        executor: 'agent_jetbrains_plugin_architect',
        handledContracts: [
          {
            contractId: 'intellij_plugin_manifest_contract',
            name: 'JetBrains plugin.xml Manifest Contract',
            path: '.nb/context/contracts/intellij_plugin_manifest_contract.json',
            type: 'json_schema',
            action: 'validate_manifest',
            description: 'Verifies plugin ID, depends tags, toolWindow declarations, and external annotators.'
          },
          {
            contractId: 'psi_ast_bridge_contract',
            name: 'JetBrains PSI-to-AST Protocol Bridge Contract',
            path: '.nb/context/contracts/psi_ast_bridge_contract.yaml',
            type: 'yaml_schema',
            action: 'verify_protocol',
            description: 'Specifies in-memory PyFile/PsiFile AST traversal and token reduction invariants.'
          }
        ]
      },
      {
        id: 'stage_2_psi_engine_and_token_meter',
        name: 'PSI AST Engine & Token Compression',
        executor: 'agent_psi_ast_bridge_specialist',
        handledContracts: [
          {
            contractId: 'psi_ast_bridge_contract',
            name: 'PSI AST Extraction & Token Compression Contract',
            path: '.nb/context/contracts/psi_ast_bridge_contract.yaml',
            type: 'yaml_schema',
            action: 'benchmark_ast_pruner',
            description: 'Ensures >60% token compression ratio across Python & Kotlin ASTs.'
          }
        ]
      },
      {
        id: 'stage_3_toolwindow_and_ui',
        name: 'ToolWindow, JCEF & Action Integration',
        executor: 'agent_intellij_ui_ux_engineer',
        handledContracts: [
          {
            contractId: 'ui_theme_token_contract',
            name: 'Enterprise UI Design System & Theme Token Contract',
            path: '.nb/context/contracts/ui_theme_token_contract.json',
            type: 'json_schema',
            action: 'audit_theme_tokens',
            description: 'Enforces Corporate Light & Enterprise Dark tokens and WCAG AA contrast.'
          },
          {
            contractId: 'data_grid_contract',
            name: 'Interactive Data Grid & Table Schema Contract',
            path: '.nb/context/contracts/data_grid_contract.json',
            type: 'json_schema',
            action: 'validate_ui_grid',
            description: 'Validates high-density audit grids and telemetry views in ToolWindow tab panels.'
          }
        ]
      },
      {
        id: 'stage_4_daemon_rpc_and_merkle_seal',
        name: 'Daemon IPC Bridge & Merkle Seal',
        executor: 'agent_jetbrains_plugin_architect',
        handledContracts: [
          {
            contractId: 'daemon_rpc_contract',
            name: 'Percipience Daemon JSON-RPC Protocol Contract',
            path: '.nb/context/contracts/daemon_rpc_contract.json',
            type: 'json_schema',
            action: 'test_ipc_bridge',
            description: 'Verifies bidirectional UNIX socket/IPC communication between IDE and CLI binary.'
          },
          {
            contractId: 'security_four_eyes_contract',
            name: 'Cryptographic Merkle State Seal Contract',
            path: '.nb/context/contracts/security_four_eyes_contract.json',
            type: 'json_schema',
            action: 'seal_recovery_block',
            description: 'Cryptographically seals verified build hash into local Merkle ledger before deployment.'
          }
        ]
      },
      {
        id: 'stage_5_terminal_agent_interceptor',
        name: 'Terminal Mode Agent Interceptor & FinOps Optimizer',
        executor: 'agent_terminal_mode_specialist',
        handledContracts: [
          {
            contractId: 'terminal_agent_ast_contract',
            name: 'Terminal Mode AST Proxy & Prompt Interceptor Contract',
            path: '.nb/context/contracts/terminal_agent_ast_contract.yaml',
            type: 'yaml_schema',
            action: 'verify_terminal_hook',
            description: 'Injects AST-compressed context into Claude Code, Gemini CLI, and Aider sessions.'
          }
        ]
      }
    ]
  },
  {
    id: 'iot_mobile_delivery_flow',
    name: 'Connected IoT, Embedded Firmware & Mobile Delivery Flow',
    description: 'BLE GATT contract verification, FreeRTOS/Zephyr firmware, and KMP mobile client orchestration.',
    source: '.nb/agentic/custom/workflows/iot_mobile_delivery_flow.yaml',
    trigger: 'Embedded Firmware & KMP Release',
    version: '1.0.0',
    status: 'Ready - [✔ HEALTHY]',
    stages: [
      {
        id: 'step_ble_gatt_contract_gate',
        name: 'BLE GATT Service Contract Compatibility Gate',
        executor: 'agent_contract_compatibility_checker',
        handledContracts: [
          {
            contractId: 'ble_gatt_spec',
            name: 'Bluetooth Low Energy GATT Specification Contract',
            path: '.nb/context/contracts/ble_gatt_spec.yaml',
            type: 'yaml_schema',
            action: 'verify_gatt_services',
            description: 'Validates primary UUIDs, MTU constraints, and characteristic permission profiles.'
          }
        ]
      },
      {
        id: 'step_mobile_kmp_client',
        name: 'KMP Shared BLE Client & UI Verification',
        executor: 'agent_mobile_developer',
        handledContracts: [
          {
            contractId: 'ota_firmware_manifest',
            name: 'OTA Firmware Package Manifest Contract',
            path: '.nb/context/contracts/ota_firmware_manifest.json',
            type: 'json_schema',
            action: 'verify_ota_payload',
            description: 'Verifies cryptographic hash, firmware semver, and hardware architecture metadata.'
          },
          {
            contractId: 'ui_theme_token_contract',
            name: 'Enterprise UI Design System Tokens',
            path: '.nb/context/contracts/ui_theme_token_contract.json',
            type: 'json_schema',
            action: 'audit_mobile_tokens',
            description: 'Enforces design token consistency and WCAG compliance for Kotlin Multiplatform mobile screens.'
          }
        ]
      },
      {
        id: 'step_iot_ecosystem_audit',
        name: 'BLE Mesh, Power & Security Invariant Audit',
        executor: 'agent_iot_mobile_ecosystem_architect',
        handledContracts: [
          {
            contractId: 'security_pii_vault_contract',
            name: 'PII Redaction & IoT Payload Sanitization Contract',
            path: '.nb/context/contracts/security_pii_vault_contract.json',
            type: 'json_schema',
            action: 'sanitize_telemetry',
            description: 'Guarantees sensor and location metrics sent from embedded nodes do not leak PII.'
          },
          {
            contractId: 'security_four_eyes_contract',
            name: 'Cryptographic Four-Eyes Release Seal Contract',
            path: '.nb/context/contracts/security_four_eyes_contract.json',
            type: 'json_schema',
            action: 'seal_firmware_release',
            description: 'Cryptographically seals binary firmware payload hash and KMP client artifacts.'
          }
        ]
      }
    ]
  },
  {
    id: 'saas_portal_delivery_flow',
    name: 'Enterprise SaaS Portal Multi-Module Delivery Flow',
    description: 'Next.js frontend, API gateway, Stripe billing webhooks, and security audit orchestration.',
    source: '.nb/agentic/custom/workflows/saas_portal_delivery_flow.yaml',
    trigger: 'Portal Webhook / Production Gate',
    version: '1.0.0',
    status: 'Ready - [✔ HEALTHY]',
    stages: [
      {
        id: 'step_openapi_contract_gate',
        name: 'OpenAPI 3.1 Contract Compatibility Gate',
        executor: 'agent_contract_compatibility_checker',
        handledContracts: [
          {
            contractId: 'portal_openapi_spec',
            name: 'OpenAPI 3.1 REST API Specification Contract',
            path: '.nb/context/contracts/portal_openapi_spec.yaml',
            type: 'openapi_spec',
            action: 'verify_api_contract',
            description: 'Validates REST route schemas, response codes, and request bodies for SaaS portal endpoints.'
          }
        ]
      },
      {
        id: 'step_portal_frontend_scaffold',
        name: 'Build Responsive React/Tailwind Frontend',
        executor: 'agent_portal_developer',
        handledContracts: [
          {
            contractId: 'ui_theme_token_contract',
            name: 'Enterprise UI Design System Tokens Contract',
            path: '.nb/context/contracts/ui_theme_token_contract.json',
            type: 'json_schema',
            action: 'audit_theme_tokens',
            description: 'Ensures zero dark-grey tints in Light mode, 4.5:1 WCAG contrast, and zero mobile frames.'
          },
          {
            contractId: 'data_grid_contract',
            name: 'Interactive Data Grid & Table Schema Contract',
            path: '.nb/context/contracts/data_grid_contract.json',
            type: 'json_schema',
            action: 'validate_grid_components',
            description: 'Validates responsive data table rendering, pagination, and sorting structures in the portal UI.'
          }
        ]
      },
      {
        id: 'step_saas_backend_gateway',
        name: 'Gateway & Stripe Webhook Integration',
        executor: 'agent_saas_backend_developer',
        handledContracts: [
          {
            contractId: 'billing_webhook_contract',
            name: 'Billing Webhook & Event Schema Contract',
            path: '.nb/context/contracts/billing_webhook_contract.json',
            type: 'json_schema',
            action: 'verify_webhook_signatures',
            description: 'Enforces HMAC SHA-256 signature verification and webhook event payloads for billing.'
          },
          {
            contractId: 'billing_meter_contract',
            name: 'Subscription Entitlements & Metering Contract',
            path: '.nb/context/contracts/billing_meter_contract.yaml',
            type: 'yaml_schema',
            action: 'verify_metering_limits',
            description: 'Enforces tenant seat quotas, token consumption limits, and tier feature gates.'
          }
        ]
      },
      {
        id: 'step_saas_security_audit',
        name: 'Multi-Tenant SOC 2 & RLS Security Audit',
        executor: 'agent_enterprise_saas_portal_architect',
        handledContracts: [
          {
            contractId: 'security_tenant_profile_contract',
            name: 'Multi-Tenant Profile & Isolation Contract',
            path: '.nb/context/contracts/security_tenant_profile_contract.json',
            type: 'json_schema',
            action: 'verify_tenant_isolation',
            description: 'Verifies database row-level security (RLS) tenant isolation and JWT tenant claims.'
          },
          {
            contractId: 'security_rebac_policy_contract',
            name: 'Relationship-Based Access Control Policy Contract',
            path: '.nb/context/contracts/security_rebac_policy_contract.json',
            type: 'json_schema',
            action: 'enforce_rebac_policies',
            description: 'Asserts role relationships and admin workspace boundaries before gateway deployment.'
          }
        ]
      }
    ]
  },
  {
    id: 'vscode_plugin_delivery_flow',
    name: 'Visual Studio Code Extension End-to-End Delivery Flow',
    description: 'Multi-stage delivery pipeline for VS Code Extension & LSP Server.',
    source: '.nb/agentic/custom/workflows/vscode_plugin_delivery_flow.yaml',
    trigger: 'VSIX Publish & LSP Verification',
    version: '1.0.0',
    status: 'Active - [✔ HEALTHY]',
    stages: [
      {
        id: 'stage_1_manifest_and_activation',
        name: 'Package Manifest & Lazy Activation Gate',
        executor: 'agent_vscode_extension_architect',
        handledContracts: [
          {
            contractId: 'package_json_manifest_contract',
            name: 'VS Code package.json Extension Manifest Contract',
            path: '.nb/context/contracts/package_json_manifest_contract.json',
            type: 'json_schema',
            action: 'validate_manifest',
            description: 'Verifies contributes schemas, views, commands, and activationEvents configuration.'
          },
          {
            contractId: 'sandbox_permission_contract',
            name: 'Extension Sandbox & Zero Wildcard Activation Contract',
            path: '.nb/context/contracts/sandbox_permission_contract.json',
            type: 'json_schema',
            action: 'enforce_sandbox_isolation',
            description: 'Prohibits wildcard onStartupFinished activation, requiring explicit onCommand triggers.'
          }
        ]
      },
      {
        id: 'stage_2_lsp_subsystem',
        name: 'LSP 3.17 Server & Diagnostic Verification',
        executor: 'agent_lsp_language_features_specialist',
        handledContracts: [
          {
            contractId: 'lsp_protocol_contract',
            name: 'Language Server Protocol 3.17 Specification Contract',
            path: '.nb/context/contracts/lsp_protocol_contract.yaml',
            type: 'yaml_schema',
            action: 'test_lsp_compliance',
            description: 'Tests publishDiagnostics, codeLens, and incremental synchronization latency (<50ms).'
          }
        ]
      },
      {
        id: 'stage_3_webview_dashboard',
        name: 'Webview Dashboard & Theme Sync',
        executor: 'agent_vscode_webview_ux_engineer',
        handledContracts: [
          {
            contractId: 'webview_message_rpc_contract',
            name: 'Webview RPC & Nonce-Based CSP Contract',
            path: '.nb/context/contracts/webview_message_rpc_contract.json',
            type: 'json_schema',
            action: 'verify_csp_and_rpc',
            description: 'Ensures zero inline script execution without cryptographic nonces, and validates postMessage RPC.'
          },
          {
            contractId: 'ui_theme_token_contract',
            name: 'Enterprise UI Design System Tokens Contract',
            path: '.nb/context/contracts/ui_theme_token_contract.json',
            type: 'json_schema',
            action: 'audit_theme_sync',
            description: 'Synchronizes VS Code CSS variables with corporate design tokens for light and dark modes.'
          }
        ]
      },
      {
        id: 'stage_4_ipc_and_gate_seal',
        name: 'Socket IPC Bridge & Merkle Seal',
        executor: 'agent_vscode_extension_architect',
        handledContracts: [
          {
            contractId: 'daemon_rpc_contract',
            name: 'Percipience Daemon IPC Protocol Contract',
            path: '.nb/context/contracts/daemon_rpc_contract.json',
            type: 'json_schema',
            action: 'test_socket_ipc',
            description: 'Verifies UNIX socket IPC throughput and error handling between extension and CLI daemon.'
          },
          {
            contractId: 'security_four_eyes_contract',
            name: 'Cryptographic Four-Eyes Release Seal Contract',
            path: '.nb/context/contracts/security_four_eyes_contract.json',
            type: 'json_schema',
            action: 'seal_recovery_block',
            description: 'Signs VSIX package distribution hash into the local Merkle ledger before publication.'
          }
        ]
      }
    ]
  }
];

export class WorkflowTreeProvider implements vscode.TreeDataProvider<WorkflowItem> {
  private _onDidChangeTreeData: vscode.EventEmitter<WorkflowItem | undefined | null | void> = new vscode.EventEmitter<WorkflowItem | undefined | null | void>();
  readonly onDidChangeTreeData: vscode.Event<WorkflowItem | undefined | null | void> = this._onDidChangeTreeData.event;

  refresh(): void {
    this._onDidChangeTreeData.fire();
  }

  getTreeItem(element: WorkflowItem): vscode.TreeItem {
    return element;
  }

  getChildren(element?: WorkflowItem): Thenable<WorkflowItem[]> {
    // 1. Root Level: List of Delivery Pipelines
    if (!element) {
      const pipelineItems = DELIVERY_PIPELINES_REGISTRY.map(pipeline => {
        const totalContracts = pipeline.stages.reduce((acc, st) => acc + st.handledContracts.length, 0);
        const item = new WorkflowItem(
          pipeline.name,
          `${pipeline.stages.length} Stages • ${totalContracts} Contracts - ${pipeline.status}`,
          vscode.TreeItemCollapsibleState.Collapsed,
          'workflow',
          pipeline
        );
        item.tooltip = `${pipeline.name} (v${pipeline.version})\n${pipeline.description}\nSource: ${pipeline.source}\nTrigger: ${pipeline.trigger}`;
        item.iconPath = new vscode.ThemeIcon('play-circle');
        return item;
      });
      return Promise.resolve(pipelineItems);
    }

    // 2. Stage Level: Children of a Workflow
    if (element.itemType === 'workflow' && element.pipelineData) {
      const stageItems = element.pipelineData.stages.map((stage, idx) => {
        const stageItem = new WorkflowItem(
          `[Stage ${idx + 1}/${element.pipelineData!.stages.length}] ${stage.name}`,
          `Executor: ${stage.executor} (${stage.handledContracts.length} Handled Contracts)`,
          stage.handledContracts.length > 0 ? vscode.TreeItemCollapsibleState.Collapsed : vscode.TreeItemCollapsibleState.None,
          'stage',
          element.pipelineData,
          stage
        );
        stageItem.tooltip = `Stage ID: ${stage.id}\nExecutor: ${stage.executor}\nAction: ${stage.action || 'execute'}\nDepends On: ${(stage.dependsOn || []).join(', ') || 'None'}\nHandled Contracts: ${stage.handledContracts.length}`;
        stageItem.iconPath = new vscode.ThemeIcon('milestone');
        return stageItem;
      });
      return Promise.resolve(stageItems);
    }

    // 3. Contract Level: Children of a Stage
    if (element.itemType === 'stage' && element.stageData) {
      const contractItems = element.stageData.handledContracts.map(contract => {
        const contractItem = new WorkflowItem(
          `📄 ${contract.name}`,
          `[${contract.type} | ${contract.action}]`,
          vscode.TreeItemCollapsibleState.None,
          'contract',
          element.pipelineData,
          element.stageData,
          contract
        );
        contractItem.tooltip = `Contract ID: ${contract.contractId}\nPath: ${contract.path}\nSchema Type: ${contract.type}\nGate Action: ${contract.action}\n\nDescription:\n${contract.description}`;
        contractItem.iconPath = new vscode.ThemeIcon('file-code');
        
        // Wire click to open the contract file in the editor
        const wsFolders = vscode.workspace.workspaceFolders;
        if (wsFolders && wsFolders.length > 0) {
          const contractUri = vscode.Uri.file(path.join(wsFolders[0].uri.fsPath, contract.path));
          contractItem.command = {
            command: 'vscode.open',
            title: 'Open Contract Schema',
            arguments: [contractUri]
          };
        }
        return contractItem;
      });
      return Promise.resolve(contractItems);
    }

    return Promise.resolve([]);
  }
}

export class WorkflowItem extends vscode.TreeItem {
  constructor(
    public readonly label: string,
    private readonly status: string,
    public readonly collapsibleState: vscode.TreeCollapsibleState,
    public readonly itemType: 'workflow' | 'stage' | 'contract' = 'workflow',
    public readonly pipelineData?: DeliveryPipelineInfo,
    public readonly stageData?: WorkflowStageInfo,
    public readonly contractData?: HandledContractInfo
  ) {
    super(label, collapsibleState);
    this.description = this.status;
  }
}
