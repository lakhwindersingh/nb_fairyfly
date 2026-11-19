use percipience_core::PlanParityComparator;
use percipience_orchestrator::{
    BootstrapOrchestrator, FinOpsReconciler, WorkflowStateLedger,
};
use std::path::Path;
use tempfile::tempdir;

fn get_repo_root() -> std::path::PathBuf {
    let mut cur = Path::new(env!("CARGO_MANIFEST_DIR")).to_path_buf();
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
fn test_bootstrap_orchestrator_execution() {
    let repo_root = get_repo_root();
    let report = BootstrapOrchestrator::execute_bootstrap(&repo_root, None::<&str>, true)
        .expect("Bootstrap sequence execution failed");

    assert_eq!(report.sequence_id, "percipience_quad_space_bootstrap");
    assert_eq!(report.total_phases, 5);
    assert_eq!(report.passed_phases, 5);
    assert_eq!(report.overall_status, "SUCCESS");

    // Idempotency check: running again produces identical success
    let report2 = BootstrapOrchestrator::execute_bootstrap(&repo_root, None::<&str>, true)
        .expect("Second bootstrap run failed");
    assert_eq!(report2.passed_phases, 5);
    assert_eq!(report2.overall_status, "SUCCESS");
}

#[test]
fn test_dynamic_plan_parity_recalculation() {
    let repo_root = get_repo_root();
    let plan_dir = repo_root.join(".nb/plan/master/enterprise-ui-design-system");

    let report = PlanParityComparator::compare_plan_dir(&plan_dir)
        .expect("Plan parity comparison failed");

    assert_eq!(report.plan_name, "enterprise-ui-design-system");
    assert!(report.line_ratio_valid);
    assert!(report.concise_lines < report.detailed_lines);
    assert!(report.evaluation.composite_score >= 0.950);
    assert_eq!(report.evaluation.gate_status, "PASSED");
}

#[test]
fn test_workflow_state_ledger_persistence_and_replay() {
    let repo_root = get_repo_root();
    let ledger_path = repo_root.join(".nb/context/ledger/agent_workflow_state.yaml");

    let ledger = WorkflowStateLedger::load_from_yaml(&ledger_path)
        .expect("Failed to load agent workflow state ledger");

    assert_eq!(ledger.version, "1.0.0");
    assert_eq!(ledger.completed_runs, 1);

    // Replay check for matching hash:
    let match_step = ledger.check_replay_eligible(
        "pr_gatekeeper",
        "step_registry_sync",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    );
    assert!(match_step.is_some());
    let step = match_step.unwrap();
    assert_eq!(step.status, "SUCCESS");
    assert_eq!(step.handoff_token, "hnd_a3f890c4e1b72389d5f0");

    // Replay check for non-matching hash:
    let mismatch_step = ledger.check_replay_eligible(
        "pr_gatekeeper",
        "step_registry_sync",
        "0000000000000000000000000000000000000000000000000000000000000000",
    );
    assert!(mismatch_step.is_none());

    // Test saving ledger in temp directory:
    let temp_dir = tempdir().unwrap();
    let temp_ledger_path = temp_dir.path().join("saved_state.yaml");
    let mut cloned = ledger.clone();
    assert!(cloned.save_to_yaml(&temp_ledger_path).is_ok());
    assert!(temp_ledger_path.exists());
}

#[test]
fn test_finops_token_reconciliation() {
    let repo_root = get_repo_root();
    let projected_path = repo_root.join(".nb/context/ledger/token_savings_ledger.yaml");
    let actual_path = repo_root.join(".nb/context/ledger/agent_token_consumption.yaml");

    let report = FinOpsReconciler::reconcile_ledgers(&projected_path, &actual_path)
        .expect("FinOps reconciliation failed");

    assert_eq!(report.status, "ON_BUDGET");
    assert!(report.projected_saved_tokens > 50_000_000);
    assert!(report.actual_consumed_tokens > 50_000_000);
    assert!(report.effective_compression_ratio > 0.40);
    assert!(report.net_savings_usd > 100.0);
}
