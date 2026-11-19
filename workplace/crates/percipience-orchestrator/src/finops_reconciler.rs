use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProjectedLedgerSummary {
    #[serde(default)]
    pub total_events: u64,
    #[serde(default)]
    pub total_uncompressed_tokens: u64,
    #[serde(default)]
    pub total_pruned_tokens: u64,
    #[serde(default)]
    pub total_tokens_saved: u64,
    #[serde(default)]
    pub total_net_savings_usd: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProjectedLedger {
    pub summary: ProjectedLedgerSummary,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ActualLedgerSummary {
    #[serde(default)]
    pub total_events: u64,
    #[serde(default)]
    pub total_consumed_tokens: u64,
    #[serde(default)]
    pub total_cost_usd: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ActualLedger {
    pub total_actual_consumption: ActualLedgerSummary,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FinOpsReconciliationReport {
    pub status: String,
    pub projected_saved_tokens: u64,
    pub actual_consumed_tokens: u64,
    pub token_variance: i64,
    pub net_savings_usd: f64,
    pub actual_cost_usd: f64,
    pub cost_variance_usd: f64,
    pub effective_compression_ratio: f64,
    pub reconciled_at: String,
}

pub struct FinOpsReconciler;

impl FinOpsReconciler {
    pub fn reconcile_ledgers<P1: AsRef<Path>, P2: AsRef<Path>>(
        projected_path: P1,
        actual_path: P2,
    ) -> Result<FinOpsReconciliationReport> {
        let proj_content = fs::read_to_string(projected_path.as_ref())
            .with_context(|| format!("Failed to read projected ledger at {:?}", projected_path.as_ref()))?;
        let proj: ProjectedLedger = serde_yaml::from_str(&proj_content)
            .with_context(|| "Failed to parse projected ledger YAML")?;

        let actual_content = fs::read_to_string(actual_path.as_ref())
            .with_context(|| format!("Failed to read actual consumption ledger at {:?}", actual_path.as_ref()))?;
        let actual: ActualLedger = serde_yaml::from_str(&actual_content)
            .with_context(|| "Failed to parse actual consumption ledger YAML")?;

        let projected_saved = proj.summary.total_tokens_saved;
        let actual_consumed = actual.total_actual_consumption.total_consumed_tokens;
        let token_variance = actual_consumed as i64 - proj.summary.total_pruned_tokens as i64;

        let net_savings_usd = proj.summary.total_net_savings_usd;
        let actual_cost_usd = actual.total_actual_consumption.total_cost_usd;
        let cost_variance_usd = actual_cost_usd - net_savings_usd;

        let effective_compression_ratio = if proj.summary.total_uncompressed_tokens > 0 {
            (proj.summary.total_tokens_saved as f64) / (proj.summary.total_uncompressed_tokens as f64)
        } else {
            0.0
        };

        let status = if cost_variance_usd <= 20.0 {
            "ON_BUDGET".to_string()
        } else if cost_variance_usd <= 50.0 {
            "OVER_BUDGET_WARNING".to_string()
        } else {
            "CRITICAL_OVERRUN".to_string()
        };

        Ok(FinOpsReconciliationReport {
            status,
            projected_saved_tokens: projected_saved,
            actual_consumed_tokens: actual_consumed,
            token_variance,
            net_savings_usd: (net_savings_usd * 1000.0).round() / 1000.0,
            actual_cost_usd: (actual_cost_usd * 1000.0).round() / 1000.0,
            cost_variance_usd: (cost_variance_usd * 1000.0).round() / 1000.0,
            effective_compression_ratio: (effective_compression_ratio * 1000.0).round() / 1000.0,
            reconciled_at: chrono::Utc::now().to_rfc3339(),
        })
    }
}
