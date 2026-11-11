# 📦 Percipience Workplace Modules Catalog

This directory contains the 7 official application modules of the **Percipience Enterprise SaaS, Developer Tooling & Control Plane** platform. Each module is aligned with the specifications in [`.nb/plan/CAPABILITY_MATRIX.md`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/CAPABILITY_MATRIX.md) and governed by the 13 master and L1 plans.

---

## Subsystem Catalog

| Module | Category | Governing Plan Specification | Core Capabilities & Key Files |
| :--- | :--- | :--- | :--- |
| [`mod_portal_marketing`](./mod_portal_marketing) | Web Platform | [`domain_saas_portal`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/l1/saas-portal-domain/MANIFEST.yaml)<br/>[`master_enterprise_ui_design_system`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/master/enterprise-ui-design-system/MANIFEST.yaml) | Corporate platform, landing page, MDX documentation, AST compression demo, and FinOps ROI calculator ([`roi_calculator.ts`](./mod_portal_marketing/components/roi_calculator.ts)). |
| [`mod_tenant_onboarding`](./mod_tenant_onboarding) | Identity & Auth | [`domain_saas_portal`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/l1/saas-portal-domain/MANIFEST.yaml)<br/>[`generic_multitenant_security_mesh`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/master/security-mesh/MANIFEST.yaml) | Self-serve onboarding, OAuth2/OIDC authentication ([`auth.ts`](./mod_tenant_onboarding/auth.ts)), BYOR repository wizard, and automated Quad-Space tenant provisioning ([`provisioner.ts`](./mod_tenant_onboarding/provisioner.ts)). |
| [`mod_billing_metering`](./mod_billing_metering) | FinOps & Billing | [`domain_saas_portal`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/l1/saas-portal-domain/MANIFEST.yaml) | Stripe billing service ([`stripe_service.ts`](./mod_billing_metering/stripe_service.ts)), real-time token savings metering ([`usage_aggregator.ts`](./mod_billing_metering/usage_aggregator.ts)), and 15% performance fee calculation ([`rev_share_calculator.ts`](./mod_billing_metering/rev_share_calculator.ts)). |
| [`mod_observability_usage`](./mod_observability_usage) | Observability | [`domain_saas_portal`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/l1/saas-portal-domain/MANIFEST.yaml)<br/>[`master_parent_framework`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/master/parent-master-plan/MANIFEST.yaml) | OpenTelemetry telemetry stream ([`telemetry_stream.ts`](./mod_observability_usage/telemetry_stream.ts)), cryptographic Merkle DAG explorer ([`merkle_explorer.ts`](./mod_observability_usage/merkle_explorer.ts)), lease monitor, and quarantine console. |
| [`mod_shared_infra_bridge`](./mod_shared_infra_bridge) | Infrastructure | [`master_cloud_agnostic_infrastructure_substrate`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/master/cloud-agnostic-infrastructure-substrate/MANIFEST.yaml) | Substrate bridge adapter ([`infra_bridge.ts`](./mod_shared_infra_bridge/infra_bridge.ts)), multi-cloud deployment orchestration (K8s, EKS, Cloud Run, Azure), and multi-tenant schema routing. |
| [`mod_vscode_extension`](./mod_vscode_extension) | IDE Extension | [`domain_vscode_plugin`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/l1/vscode-plugin/MANIFEST.yaml) | VS Code extension source, Language Server Protocol (LSP 3.17) client ([`extension.ts`](./mod_vscode_extension/src/extension.ts)), embedded Webview dashboard, IPC socket, and multi-tier VSIX distributions (`free`, `team`, `business`, `enterprise`). |
| [`mod_intellij_plugin`](./mod_intellij_plugin) | IDE Plugin | [`domain_intellij_pycharm_plugin`](file:///Users/lakhwinder/PycharmProjects/nb_fairyfly/.nb/plan/l1/intellij-pycharm-plugin/MANIFEST.yaml) | JetBrains Platform SDK IntelliJ IDEA & PyCharm plugin, PSI AST analysis proxy, in-editor annotators, Gradle distribution build ([`package_plugin.py`](./mod_intellij_plugin/package_plugin.py)), and user guide. |

---

## Architectural Isolation

- **Application Logic (`workplace/modules/`)**: High-velocity customer-facing features, microservices, UI components, and developer tooling.
- **Platform Execution OS (`.nb/core/`)**: Cryptographically sealed runtime, Merkle provenance engine, AST token pruner, and CI/CD gatekeepers.
- **Cross-Module Wire Contracts (`context/contracts/`)**: SemVer wire contracts governing inter-module communication verified at every CI gate.
