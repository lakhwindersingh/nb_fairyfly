use percipience_core::{
    AstPruner, DiagnosticEngine, MerkleLedger, ParityEvaluation,
    SemanticParityVectors,
};

#[test]
fn test_merkle_chain_integrity() {
    let mut ledger = MerkleLedger::with_genesis("a1b2c3d4e5f6");
    assert_eq!(ledger.blocks.len(), 1);
    assert!(ledger.blocks[0].verify_integrity());

    let res = ledger.append(
        "BLOCK_TEST_001",
        "MERKLE_ROOT_001",
        "f6e5d4c3b2a1",
        serde_json::json!({ "action": "test_verification" }),
    );
    assert!(res.is_ok());
    assert_eq!(ledger.blocks.len(), 2);
    assert!(ledger.verify_chain().is_ok());
}

#[test]
fn test_ast_pruner_compression() {
    let raw_source = r#"
def calculate_metrics(data: list) -> dict:
    total = 0
    for item in data:
        total += item.value
        total *= 1.05
    return {"total": total}

def summarize():
    print("Summary done")
"#;

    let (pruned, summary) = AstPruner::prune_source(raw_source);
    assert!(pruned.contains("def calculate_metrics(data: list) -> dict:"));
    assert!(pruned.contains("... [AST_PRUNED]"));
    assert!(summary.compression_ratio_pct > 0.0);
}

#[test]
fn test_semantic_parity_gate() {
    let vectors = SemanticParityVectors::default();
    let eval = ParityEvaluation::evaluate(vectors);
    assert_eq!(eval.gate_status, "PASSED");
    assert!(eval.composite_score >= 0.950);

    let failing_vectors = SemanticParityVectors {
        contract_parity: 0.85,
        ..Default::default()
    };
    let failing_eval = ParityEvaluation::evaluate(failing_vectors);
    assert_eq!(failing_eval.gate_status, "FAILED");
}

#[test]
fn test_diagnostic_self_repair() {
    let report = DiagnosticEngine::analyze_error("SyntaxError: unexpected token at line 12", 1);
    assert_eq!(report.error_category, "STRUCTURAL");
    assert_eq!(report.attempts_remaining, 2);
}
