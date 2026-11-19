use anyhow::Result;
use percipience_core::{MerkleLedger, ParityEvaluation, SemanticParityVectors};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum LifecycleStage {
    PreSpawn,
    PreExecution,
    InFlightGuardrail,
    Handover,
    PreMergeGate,
    PostFailure,
    PostMergeSeal,
}

pub struct LifecycleHookManager;

impl LifecycleHookManager {
    pub fn execute_pre_merge_gate(vectors: SemanticParityVectors) -> Result<ParityEvaluation> {
        let eval = ParityEvaluation::evaluate(vectors);
        if eval.gate_status != "PASSED" {
            anyhow::bail!("Pre-Merge Gatekeeper failed: composite score {} < 0.950", eval.composite_score);
        }
        Ok(eval)
    }

    pub fn execute_post_merge_seal(ledger: &mut MerkleLedger, block_id: &str, git_sha: &str) -> Result<String> {
        let block = ledger.append(
            block_id,
            "SEALED_MERKLE_ROOT",
            git_sha,
            serde_json::json!({ "event": "post_merge_seal", "status": "immutable" }),
        )?;
        Ok(block.block_hash.clone())
    }
}
