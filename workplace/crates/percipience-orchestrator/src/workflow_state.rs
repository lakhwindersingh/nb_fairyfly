use anyhow::{Context, Result};
use chrono::Utc;
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StepExecution {
    pub step_name: String,
    pub agent: String,
    pub status: String,
    pub started_at: String,
    pub completed_at: Option<String>,
    pub handoff_token: String,
    pub input_hash: String,
    pub output_hash: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WorkflowRun {
    pub run_id: String,
    pub workflow_name: String,
    pub status: String,
    pub started_at: String,
    pub completed_at: Option<String>,
    #[serde(default)]
    pub steps: Vec<StepExecution>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WorkflowStateLedger {
    pub version: String,
    pub ledger_type: String,
    pub last_updated: String,
    pub active_runs: usize,
    pub completed_runs: usize,
    #[serde(default)]
    pub runs: Vec<WorkflowRun>,
}

impl Default for WorkflowStateLedger {
    fn default() -> Self {
        Self {
            version: "1.0.0".to_string(),
            ledger_type: "agent_workflow_state".to_string(),
            last_updated: Utc::now().to_rfc3339(),
            active_runs: 0,
            completed_runs: 0,
            runs: Vec::new(),
        }
    }
}

impl WorkflowStateLedger {
    pub fn load_from_yaml<P: AsRef<Path>>(path: P) -> Result<Self> {
        let content = fs::read_to_string(path.as_ref())
            .with_context(|| format!("Failed to read workflow state ledger at {:?}", path.as_ref()))?;
        let ledger: Self = serde_yaml::from_str(&content)
            .with_context(|| "Failed to parse workflow state ledger YAML")?;
        Ok(ledger)
    }

    pub fn save_to_yaml<P: AsRef<Path>>(&mut self, path: P) -> Result<()> {
        self.last_updated = Utc::now().to_rfc3339();
        self.active_runs = self.runs.iter().filter(|r| r.status == "IN_PROGRESS" || r.status == "PENDING").count();
        self.completed_runs = self.runs.iter().filter(|r| r.status == "COMPLETED").count();

        let serialized = serde_yaml::to_string(self)
            .with_context(|| "Failed to serialize workflow state ledger")?;
        fs::write(path.as_ref(), serialized)
            .with_context(|| format!("Failed to write workflow state ledger to {:?}", path.as_ref()))?;
        Ok(())
    }

    pub fn check_replay_eligible(
        &self,
        workflow_name: &str,
        step_name: &str,
        input_hash: &str,
    ) -> Option<&StepExecution> {
        for run in self.runs.iter().rev() {
            if run.workflow_name == workflow_name && run.status == "COMPLETED" {
                for step in &run.steps {
                    if step.step_name == step_name
                        && step.status == "SUCCESS"
                        && step.input_hash == input_hash
                    {
                        return Some(step);
                    }
                }
            }
        }
        None
    }

    pub fn record_run(&mut self, run: WorkflowRun) {
        if let Some(idx) = self.runs.iter().position(|r| r.run_id == run.run_id) {
            self.runs[idx] = run;
        } else {
            self.runs.push(run);
        }
    }
}
