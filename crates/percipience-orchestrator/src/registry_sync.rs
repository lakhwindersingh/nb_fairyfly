use anyhow::{bail, Result};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, HashSet};
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct RegistryProjection {
    pub agent_registry: BTreeMap<String, serde_json::Value>,
    pub workflow_registry: BTreeMap<String, serde_json::Value>,
    pub workflow_hooks: BTreeMap<String, String>,
}

pub struct RegistrySynchronizer;

impl RegistrySynchronizer {
    pub fn discover_agents<P: AsRef<Path>>(agents_dir: P) -> Result<BTreeMap<String, serde_json::Value>> {
        let mut registry = BTreeMap::new();
        if !agents_dir.as_ref().exists() {
            return Ok(registry);
        }

        for entry in fs::read_dir(agents_dir)? {
            let entry = entry?;
            let path = entry.path();
            if path.extension().and_then(|s| s.to_str()) == Some("yaml") {
                if let Some(stem) = path.file_stem().and_then(|s| s.to_str()) {
                    let content = fs::read_to_string(&path)?;
                    let value: serde_json::Value = serde_yaml::from_str(&content).unwrap_or(serde_json::json!({
                        "id": stem,
                        "file": path.to_string_lossy().to_string()
                    }));
                    registry.insert(stem.to_string(), value);
                }
            }
        }

        Ok(registry)
    }

    pub fn discover_workflows<P: AsRef<Path>>(workflows_dir: P) -> Result<BTreeMap<String, serde_json::Value>> {
        let mut registry = BTreeMap::new();
        if !workflows_dir.as_ref().exists() {
            return Ok(registry);
        }

        for entry in fs::read_dir(workflows_dir)? {
            let entry = entry?;
            let path = entry.path();
            if path.extension().and_then(|s| s.to_str()) == Some("yaml") {
                if let Some(stem) = path.file_stem().and_then(|s| s.to_str()) {
                    let content = fs::read_to_string(&path)?;
                    let value: serde_json::Value = serde_yaml::from_str(&content).unwrap_or(serde_json::json!({
                        "id": stem,
                        "file": path.to_string_lossy().to_string()
                    }));
                    registry.insert(stem.to_string(), value);
                }
            }
        }

        Ok(registry)
    }

    pub fn validate_hook_bindings(
        agent_registry: &BTreeMap<String, serde_json::Value>,
        workflow_hooks: &BTreeMap<String, String>,
    ) -> Result<()> {
        let known_agents: HashSet<&str> = agent_registry.keys().map(|k| k.as_str()).collect();

        for (hook, agent) in workflow_hooks {
            if !known_agents.contains(agent.as_str()) && !agent.starts_with("platform.") {
                bail!(
                    "HookBindingError: Workflow hook '{}' binds to unknown agent '{}'",
                    hook,
                    agent
                );
            }
        }

        Ok(())
    }

    pub fn project_multi_llm(projection: &RegistryProjection, repo_root: &Path) -> Result<()> {
        let claude_val = serde_json::json!({
            "agent_registry": projection.agent_registry,
            "workflow_registry": projection.workflow_registry,
            "workflow_hooks": projection.workflow_hooks
        });

        // 1. Claude Code: settings.json and .claude/settings.json
        let claude_dir = repo_root.join(".claude");
        fs::create_dir_all(&claude_dir)?;
        fs::write(claude_dir.join("settings.json"), serde_json::to_string_pretty(&claude_val)?)?;
        fs::write(repo_root.join("settings.json"), serde_json::to_string_pretty(&claude_val)?)?;

        // 2. Gemini CLI: .gemini/settings.json (namespaced percipience)
        let gemini_dir = repo_root.join(".gemini");
        fs::create_dir_all(&gemini_dir)?;
        let gemini_val = serde_json::json!({ "percipience": claude_val });
        fs::write(gemini_dir.join("settings.json"), serde_json::to_string_pretty(&gemini_val)?)?;

        // 3. Cursor CLI: .cursor/settings.json (namespaced percipience)
        let cursor_dir = repo_root.join(".cursor");
        fs::create_dir_all(&cursor_dir)?;
        let cursor_val = serde_json::json!({ "percipience": claude_val });
        fs::write(cursor_dir.join("settings.json"), serde_json::to_string_pretty(&cursor_val)?)?;

        // 4. Aider: .aider.conf.yml (namespaced percipience, YAML)
        let aider_val = serde_json::json!({ "percipience": claude_val });
        let aider_yaml = serde_yaml::to_string(&aider_val)?;
        fs::write(repo_root.join(".aider.conf.yml"), aider_yaml)?;

        Ok(())
    }
}
