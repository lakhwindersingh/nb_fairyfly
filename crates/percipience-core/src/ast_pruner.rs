use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PruningSummary {
    pub original_characters: usize,
    pub pruned_characters: usize,
    pub compression_ratio_pct: f64,
}

pub struct AstPruner;

impl AstPruner {
    /// Prunes function and method bodies from source code lines while preserving signatures,
    /// type annotations, docstrings, and module declarations.
    pub fn prune_source(source: &str) -> (String, PruningSummary) {
        let lines: Vec<&str> = source.lines().collect();
        let mut pruned_lines = Vec::new();
        let mut in_function_body = false;
        let mut current_indent = 0;

        for line in &lines {
            let trimmed = line.trim_start();
            let indent = line.len() - trimmed.len();

            if trimmed.starts_with("def ")
                || trimmed.starts_with("async def ")
                || trimmed.starts_with("fn ")
                || trimmed.starts_with("pub fn ")
                || trimmed.starts_with("function ")
                || trimmed.starts_with("pub async fn ")
            {
                pruned_lines.push(line.to_string());
                in_function_body = true;
                current_indent = indent;
                let indent_str = " ".repeat(indent + 4);
                pruned_lines.push(format!("{indent_str}... [AST_PRUNED]"));
                continue;
            }

            if in_function_body {
                if trimmed.is_empty() {
                    continue;
                }
                if indent <= current_indent && !trimmed.starts_with("#") && !trimmed.starts_with("//") {
                    in_function_body = false;
                    pruned_lines.push(line.to_string());
                }
                // Skip lines inside the function body
                continue;
            }

            pruned_lines.push(line.to_string());
        }

        let pruned_text = pruned_lines.join("\n");
        let original_chars = source.len();
        let pruned_chars = pruned_text.len();

        let compression_ratio = if original_chars > 0 {
            if original_chars >= pruned_chars {
                ((original_chars - pruned_chars) as f64 / original_chars as f64) * 100.0
            } else {
                0.0
            }
        } else {
            0.0
        };

        (
            pruned_text,
            PruningSummary {
                original_characters: original_chars,
                pruned_characters: pruned_chars,
                compression_ratio_pct: compression_ratio,
            },
        )
    }
}
