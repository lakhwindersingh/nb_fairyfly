use percipience_core::{MerkleLedger, SemanticParityVectors};
use percipience_orchestrator::{DagScheduler, LifecycleHookManager, PlanNode};

#[test]
fn test_topological_dag_resolution() {
    let nodes = vec![
        PlanNode {
            id: "master_parent_framework".to_string(),
            dependencies: vec![],
        },
        PlanNode {
            id: "domain_intellij_pycharm_plugin".to_string(),
            dependencies: vec!["master_parent_framework".to_string()],
        },
        PlanNode {
            id: "domain_saas_portal".to_string(),
            dependencies: vec!["master_parent_framework".to_string()],
        },
        PlanNode {
            id: "percipience_master_test_plan".to_string(),
            dependencies: vec![
                "domain_intellij_pycharm_plugin".to_string(),
                "domain_saas_portal".to_string(),
            ],
        },
    ];

    let order = DagScheduler::resolve_execution_order(&nodes).expect("DAG resolution failed");
    assert_eq!(order.len(), 4);
    assert_eq!(order[0], "master_parent_framework");
    assert_eq!(order[3], "percipience_master_test_plan");

    let waves = DagScheduler::partition_waves(&nodes).expect("Wave partition failed");
    assert_eq!(waves.len(), 3);
    assert_eq!(waves[0], vec!["master_parent_framework"]);
    assert_eq!(waves[1].len(), 2);
    assert_eq!(waves[2], vec!["percipience_master_test_plan"]);
}

#[test]
fn test_circular_dag_rejection() {
    let circular_nodes = vec![
        PlanNode {
            id: "plan_a".to_string(),
            dependencies: vec!["plan_b".to_string()],
        },
        PlanNode {
            id: "plan_b".to_string(),
            dependencies: vec!["plan_a".to_string()],
        },
    ];

    assert!(DagScheduler::resolve_execution_order(&circular_nodes).is_err());
}

#[test]
fn test_pre_merge_gate_and_seal() {
    let vectors = SemanticParityVectors::default();
    let gate_res = LifecycleHookManager::execute_pre_merge_gate(vectors);
    assert!(gate_res.is_ok());

    let mut ledger = MerkleLedger::with_genesis("112233445566");
    let seal_res = LifecycleHookManager::execute_post_merge_seal(&mut ledger, "BLOCK_TEST_SEAL", "665544332211");
    assert!(seal_res.is_ok());
    assert_eq!(ledger.blocks.len(), 2);
}
