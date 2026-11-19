use anyhow::{bail, Result};

pub struct SecurityGuardrails;

impl SecurityGuardrails {
    /// Detects prompt injection markers and dangerous shell execution escapes
    pub fn sanitize_prompt(prompt: &str) -> Result<()> {
        let lower = prompt.to_lowercase();
        let dangerous_signatures = [
            "ignore previous instructions",
            "system prompt override",
            "eval(",
            "os.system(",
            "subprocess.call(",
            "/etc/shadow",
            "rm -rf /",
        ];

        for sig in &dangerous_signatures {
            if lower.contains(sig) {
                bail!("SecurityViolation: Prompt contains prohibited pattern: '{}'", sig);
            }
        }
        Ok(())
    }

    /// Redacts PII and confidential keys
    pub fn mask_secrets(input: &str) -> String {
        let mut result = input.to_string();
        let secret_prefixes = ["AKIA", "ghp_", "glpat-", "sk-"];

        for prefix in &secret_prefixes {
            if let Some(pos) = result.find(prefix) {
                let end = result[pos..].find(' ').map(|p| pos + p).unwrap_or(result.len());
                let replacement = "[REDACTED_FPE_TOKEN]";
                result.replace_range(pos..end, replacement);
            }
        }
        result
    }
}
