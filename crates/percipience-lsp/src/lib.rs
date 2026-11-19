use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LspServerCapabilities {
    pub text_document_sync: u8,
    pub hover_provider: bool,
    pub definition_provider: bool,
    pub diagnostic_provider: bool,
}

impl Default for LspServerCapabilities {
    fn default() -> Self {
        Self {
            text_document_sync: 1, // Full sync
            hover_provider: true,
            definition_provider: true,
            diagnostic_provider: true,
        }
    }
}

pub struct PercipienceLspService;

impl PercipienceLspService {
    pub fn initialize() -> LspServerCapabilities {
        LspServerCapabilities::default()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_lsp_initialization() {
        let caps = PercipienceLspService::initialize();
        assert!(caps.diagnostic_provider);
        assert!(caps.hover_provider);
    }
}
