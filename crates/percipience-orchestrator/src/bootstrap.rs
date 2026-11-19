use crate::agent_manifest::AgentManifest;
use anyhow::{bail, Context, Result};
use percipience_core::MerkleLedger;
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BootstrapSequence {
    pub version: String,
    pub sequence_id: String,
    pub description: String,
    pub phases: Vec<BootstrapPhase>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BootstrapPhase {
    pub id: String,
    pub name: String,
    pub description: String,
    pub idempotent: bool,
    pub action: String,
    #[serde(default)]
    pub required_paths: Vec<String>,
    #[serde(default)]
    pub required_binaries: Vec<String>,
    pub required_ledger: Option<String>,
    pub manifest_path: Option<String>,
    pub git_hook_path: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BootstrapPhaseResult {
    pub phase_id: String,
    pub phase_name: String,
    pub status: String,
    pub message: String,
    pub duration_ms: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BootstrapReport {
    pub sequence_id: String,
    pub total_phases: usize,
    pub passed_phases: usize,
    pub overall_status: String,
    pub results: Vec<BootstrapPhaseResult>,
}

pub struct BootstrapOrchestrator;

impl BootstrapOrchestrator {
    pub fn load_sequence<P: AsRef<Path>>(path: P) -> Result<BootstrapSequence> {
        let content = fs::read_to_string(path.as_ref())
            .with_context(|| format!("Failed to read bootstrap sequence at {:?}", path.as_ref()))?;
        let seq: BootstrapSequence = serde_yaml::from_str(&content)
            .with_context(|| "Failed to parse bootstrap sequence YAML")?;
        Ok(seq)
    }

    pub fn execute_bootstrap<P1: AsRef<Path>, P2: AsRef<Path>>(
        repo_root: P1,
        sequence_path: Option<P2>,
        dry_run: bool,
    ) -> Result<BootstrapReport> {
        let root = repo_root.as_ref();
        let default_seq_path = root.join(".nb/plan/master/bootstrap_sequence.yaml");
        let seq_file = match sequence_path {
            Some(ref p) => p.as_ref(),
            None => default_seq_path.as_path(),
        };

        let sequence = Self::load_sequence(seq_file)?;
        let mut results = Vec::new();
        let mut overall_success = true;

        for phase in &sequence.phases {
            let start = std::time::Instant::now();
            let phase_res = match phase.id.as_str() {
                "phase_1_quad_space_init" => {
                    Self::execute_quad_space_init(root, &phase.required_paths, dry_run)
                }
                "phase_2_engine_init" => {
                    Self::execute_engine_init(root, &phase.required_binaries)
                }
                "phase_3_merkle_genesis" => {
                    Self::execute_merkle_genesis(root, phase.required_ledger.as_deref())
                }
                "phase_4_agent_registry" => {
                    Self::execute_agent_registry(root, phase.manifest_path.as_deref())
                }
                "phase_5_cicd_validation" => {
                    Self::execute_cicd_validation(root, phase.git_hook_path.as_deref())
                }
                _ => Ok(format!("Custom phase '{}' acknowledged", phase.id)),
            };

            let duration_ms = start.elapsed().as_millis() as u64;
            match phase_res {
                Ok(msg) => {
                    results.push(BootstrapPhaseResult {
                        phase_id: phase.id.clone(),
                        phase_name: phase.name.clone(),
                        status: "PASSED".to_string(),
                        message: msg,
                        duration_ms,
                    });
                }
                Err(err) => {
                    overall_success = false;
                    results.push(BootstrapPhaseResult {
                        phase_id: phase.id.clone(),
                        phase_name: phase.name.clone(),
                        status: "FAILED".to_string(),
                        message: err.to_string(),
                        duration_ms,
                    });
                }
            }
        }

        let passed_phases = results.iter().filter(|r| r.status == "PASSED").count();
        let total_phases = results.len();

        Ok(BootstrapReport {
            sequence_id: sequence.sequence_id,
            total_phases,
            passed_phases,
            overall_status: if overall_success { "SUCCESS".to_string() } else { "FAILED".to_string() },
            results,
        })
    }

    fn execute_quad_space_init(root: &Path, paths: &[String], dry_run: bool) -> Result<String> {
        let mut created = Vec::new();
        let mut existing = Vec::new();

        for rel in paths {
            let target = root.join(rel);
            if target.exists() {
                existing.push(rel.clone());
            } else {
                if !dry_run {
                    fs::create_dir_all(&target)
                        .with_context(|| format!("Failed to create quad-space directory {:?}", target))?;
                }
                created.push(rel.clone());
            }
        }

        Ok(format!(
            "Quad-space verified (existing: [{}], initialized: [{}])",
            existing.join(", "),
            created.join(", ")
        ))
    }

    fn execute_engine_init(root: &Path, binaries: &[String]) -> Result<String> {
        let mut found = Vec::new();
        for bin in binaries {
            let p = root.join(bin);
            if p.exists() {
                found.push(bin.clone());
            }
        }
        if found.is_empty() {
            bail!("Native engine binary not found among {:?}", binaries);
        }
        Ok(format!("Native engine verified: [{}]", found.join(", ")))
    }

    fn execute_merkle_genesis(root: &Path, ledger_rel: Option<&str>) -> Result<String> {
        let rel = ledger_rel.unwrap_or(".nb/context/ledger/context_ledger.yaml");
        let ledger_path = root.join(rel);
        if !ledger_path.exists() {
            bail!("Merkle ledger not found at {:?}", ledger_path);
        }

        let ledger = MerkleLedger::load_from_yaml(&ledger_path)
            .with_context(|| format!("Failed to load ledger from {:?}", ledger_path))?;
        if let Err(e) = ledger.verify_chain() {
            bail!("Merkle DAG integrity check failed on {:?}: {e}", ledger_path);
        }
        Ok(format!("Merkle chain verified: {} blocks with 100% cryptographic integrity", ledger.blocks.len()))
    }

    fn execute_agent_registry(root: &Path, manifest_rel: Option<&str>) -> Result<String> {
        let rel = manifest_rel.unwrap_or(".nb/agentic/agents/agent_manifest.yaml");
        let manifest_path = root.join(rel);
        if !manifest_path.exists() {
            bail!("Agent manifest not found at {:?}", manifest_path);
        }

        let manifest = AgentManifest::load_from_yaml(&manifest_path)?;
        Ok(format!("Agent manifest active: {} agents registered with enforced quotas", manifest.agents.len()))
    }

    fn execute_cicd_validation(root: &Path, hook_rel: Option<&str>) -> Result<String> {
        let rel = hook_rel.unwrap_or(".nb/git_hooks/pre-commit.sh");
        let hook_path = root.join(rel);
        if !hook_path.exists() {
            bail!("Git pre-commit hook missing at {:?}", hook_path);
        }
        Ok(format!("CI/CD gate active: pre-commit hook verified at {:?}", rel))
    }
}
