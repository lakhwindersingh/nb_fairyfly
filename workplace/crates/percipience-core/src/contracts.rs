use anyhow::{bail, Result};
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WireContract {
    pub schema_version: String,
    pub contract_id: String,
    pub required_fields: Vec<String>,
    pub properties: serde_json::Value,
}

impl WireContract {
    pub fn load_from_yaml<P: AsRef<Path>>(path: P) -> Result<Self> {
        let content = fs::read_to_string(path)?;
        let contract: Self = serde_yaml::from_str(&content)?;
        Ok(contract)
    }

    pub fn validate_payload(&self, payload: &serde_json::Value) -> Result<()> {
        for field in &self.required_fields {
            if payload.get(field).is_none() {
                bail!("Missing required contract field: {}", field);
            }
        }
        Ok(())
    }
}
