# Plan Space Reorganization Mapping

This document maps all original legacy flat plan files to their new plan-centric folder locations, defining their plan types, capability tiers, and dual-format distribution.

| Old Path | New Plan Directory | Plan ID | Capability Tier | Plan Type | Migration Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `claude-context-engineering-parent-master-plan.md` | `master/parent-master-plan/` | `master_parent_framework` | Master | Orchestration | `[SPLIT]` Detailed (1624 lines) + Concise (~600 lines) |
| `claude-context-engineering-parent-master-free_plan.md` | `master/parent-master-free-plan/` | `master_parent_free_community` | Free Community | Orchestration | `[EXPAND]` Concise (362 lines) + Detailed (~800 lines) |
| `claude-context-engineering-intellij-pycharm-plugin-space.md` | `l1/intellij-pycharm-plugin/` | `domain_intellij_pycharm_plugin` | L1 | Foundation / IDE Space | `[EXPAND]` Concise (331 lines) + Detailed (~900 lines) |
| `claude-context-engineering-vscode-plugin-space.md` | `l1/vscode-plugin/` | `domain_vscode_plugin` | L1 | Foundation / IDE Space | `[EXPAND]` Concise (325 lines) + Detailed (~900 lines) |
| `claude-context-engineering-saas-portal-domain-plan.md` | `l1/saas-portal-domain/` | `domain_saas_portal` | L1 | Foundation / Web & SaaS | `[EXPAND]` Concise (344 lines) + Detailed (~900 lines) |
| `CEaasS/play_3_enterprise_context_engineering_os_plan.md` | `l2/enterprise-context-engineering-os/` | `play_3_enterprise_os` | L2 | Commercial / Self-Evolution | `[SPLIT]` Detailed (1065 lines) + Concise (~450 lines) |
| `CEaasS/play_3_corp_site_saas_portal_plan.md` | `l2/corp-site-saas-portal/` | `play_3_corp_site_saas` | L2 | Commercial / Portal Platform | `[SPLIT]` Detailed (508 lines) + Concise (~300 lines) |
| `templates/custom_domain_layer_template.md` | `templates/custom_domain_layer_template.md` | `template_domain_layer` | Template | Template | `[PRESERVE]` Standardized template |

## Archive Location
All original legacy files are preserved identically under:
`archive/old_structure/`
