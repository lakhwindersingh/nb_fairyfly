use percipience_orchestrator::{
    AgentManifest, RegistryProjection, RegistrySynchronizer, SubmoduleOrchestrator,
};
use std::collections::BTreeMap;
use tempfile::tempdir;

fn find_repo_root() -> std::path::PathBuf {
    let mut cur = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).to_path_buf();
    while !cur.join(".nb").exists() {
        if let Some(parent) = cur.parent() {
            cur = parent.to_path_buf();
        } else {
            break;
        }
    }
    cur
}

#[test]
fn test_agent_manifest_and_quota_enforcement() {
    let repo_root = find_repo_root();
    let manifest_path = repo_root.join(".nb/agentic/agents/agent_manifest.yaml");
    let manifest = AgentManifest::load_from_yaml(&manifest_path).expect("Failed to load agent manifest");

    assert_eq!(manifest.version, "1.0.0");
    assert!(manifest.agents.contains_key("agent_parent_framework_architect"));

    // Enforce quota within budget:
    assert!(manifest.enforce_quota("agent_parent_framework_architect", 25000).is_ok());

    // Exceed quota:
    assert!(manifest.enforce_quota("agent_parent_framework_architect", 35000).is_err());

    // Validate capability:
    assert!(manifest.validate_capability("agent_parent_framework_architect", "merkle_sealing").is_ok());
    assert!(manifest.validate_capability("agent_parent_framework_architect", "unauthorized_hack").is_err());
}

#[test]
fn test_registry_sync_and_binding_validation() {
    let mut agents = BTreeMap::new();
    agents.insert("agent_architect".to_string(), serde_json::json!({ "id": "agent_architect" }));
    agents.insert("agent_coder".to_string(), serde_json::json!({ "id": "agent_coder" }));

    let mut hooks = BTreeMap::new();
    hooks.insert("pre_execution".to_string(), "agent_architect".to_string());
    hooks.insert("handover".to_string(), "agent_coder".to_string());

    assert!(RegistrySynchronizer::validate_hook_bindings(&agents, &hooks).is_ok());

    // Hook pointing to unknown agent must fail:
    hooks.insert("unknown_hook".to_string(), "agent_ghost".to_string());
    assert!(RegistrySynchronizer::validate_hook_bindings(&agents, &hooks).is_err());
}

#[test]
fn test_multi_llm_projection() {
    let temp_dir = tempdir().unwrap();
    let root = temp_dir.path();

    let projection = RegistryProjection::default();
    assert!(RegistrySynchronizer::project_multi_llm(&projection, root).is_ok());

    assert!(root.join("settings.json").exists());
    assert!(root.join(".claude/settings.json").exists());
    assert!(root.join(".gemini/settings.json").exists());
    assert!(root.join(".cursor/settings.json").exists());
    assert!(root.join(".aider.conf.yml").exists());
}

#[test]
fn test_submodule_orchestration_state() {
    let repo_root = find_repo_root();
    let temp_dir = tempdir().unwrap();
    let ledger_out = temp_dir.path().join("orchestrator_state.json");
    let plan_dir = repo_root.join(".nb/plan/master/enterprise-ui-design-system");

    let state = SubmoduleOrchestrator::orchestrate_plan(
        &plan_dir,
        &ledger_out,
    )
    .expect("Plan orchestration failed");

    assert_eq!(state.plan_id, "master_enterprise_ui_design_system");
    assert!(ledger_out.exists());
    assert_eq!(state.submodules.len(), 3);
}
