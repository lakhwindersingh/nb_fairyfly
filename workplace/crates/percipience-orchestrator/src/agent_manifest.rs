use anyhow::{bail, Result};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentSpec {
    pub tier: String,
    pub models: Vec<String>,
    pub token_budget: u64,
    pub timeout_seconds: u64,
    pub capabilities: Vec<String>,
    pub fail_action: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ManifestDefaults {
    pub token_budget_per_invocation: u64,
    pub timeout_seconds: u64,
    pub max_retries: u32,
    pub fail_action: String,
    pub sliding_window_tokens: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentManifest {
    pub version: String,
    pub schema_version: String,
    pub manifest_id: String,
    pub defaults: ManifestDefaults,
    pub agents: HashMap<String, AgentSpec>,
}

impl AgentManifest {
    pub fn load_from_yaml<P: AsRef<Path>>(path: P) -> Result<Self> {
        let content = fs::read_to_string(path)?;
        let manifest: Self = serde_yaml::from_str(&content)?;
        Ok(manifest)
    }

    pub fn enforce_quota(&self, agent_name: &str, requested_tokens: u64) -> Result<()> {
        let budget = if let Some(spec) = self.agents.get(agent_name) {
            spec.token_budget
        } else {
            self.defaults.token_budget_per_invocation
        };

        if requested_tokens > budget {
            bail!(
                "QuotaExceededError: Agent '{}' requested {} tokens, exceeding budget limit of {}",
                agent_name,
                requested_tokens,
                budget
            );
        }

        Ok(())
    }

    pub fn validate_capability(&self, agent_name: &str, capability: &str) -> Result<()> {
        if let Some(spec) = self.agents.get(agent_name) {
            if !spec.capabilities.iter().any(|c| c == capability) {
                bail!(
                    "UnauthorizedCapabilityError: Agent '{}' lacks required capability '{}'",
                    agent_name,
                    capability
                );
            }
        }
        Ok(())
    }
}
