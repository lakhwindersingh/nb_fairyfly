use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DiagnosticReport {
    pub error_category: String,
    pub raw_error: String,
    pub isolated_ast_diff: String,
    pub suggested_patch: Option<String>,
    pub attempts_remaining: u32,
}

pub struct DiagnosticEngine;

impl DiagnosticEngine {
    pub const MAX_HEALING_ATTEMPTS: u32 = 3;

    pub fn analyze_error(raw_error: &str, attempt_number: u32) -> DiagnosticReport {
        let attempts_remaining = Self::MAX_HEALING_ATTEMPTS.saturating_sub(attempt_number);

        let category = if raw_error.contains("SyntaxError") || raw_error.contains("mismatched types") {
            "STRUCTURAL"
        } else if raw_error.contains("timeout") || raw_error.contains("Connection refused") {
            "TRANSIENT"
        } else if raw_error.contains("SchemaValidationError") || raw_error.contains("missing field") {
            "INVARIANT"
        } else {
            "HALLUCINATORY"
        };

        let isolated_diff = format!(">>> Sliced Diagnostic Context:\n{raw_error}\n<<< End Sliced Context");

        DiagnosticReport {
            error_category: category.to_string(),
            raw_error: raw_error.to_string(),
            isolated_ast_diff: isolated_diff,
            suggested_patch: Some("// Automated AST candidate patch".to_string()),
            attempts_remaining,
        }
    }
}
