use anyhow::{bail, Result};
use chrono::{DateTime, Utc};
use hmac::{Hmac, Mac};
use serde::{Deserialize, Serialize};
use sha2::Sha256;
use std::collections::HashSet;
use std::sync::Mutex;

type HmacSha256 = Hmac<Sha256>;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct HandoffToken {
    pub token_id: String,
    pub workflow_id: String,
    pub stage_id: String,
    pub from_agent: String,
    pub to_agent: String,
    pub artifact_hash: String,
    pub parity_hash: String,
    pub nonce: String,
    pub timestamp: DateTime<Utc>,
    pub signature: String,
}

impl HandoffToken {
    pub const EXPIRATION_SECONDS: i64 = 300;

    pub fn mint(
        secret_key: &[u8],
        workflow_id: &str,
        stage_id: &str,
        from_agent: &str,
        to_agent: &str,
        artifact_hash: &str,
        parity_hash: &str,
        nonce: &str,
    ) -> Result<Self> {
        let token_id = uuid::Uuid::new_v4().to_string();
        let timestamp = Utc::now();
        let payload = format!(
            "{}:{}:{}:{}->{}:{}:{}:{}:{}",
            token_id,
            workflow_id,
            stage_id,
            from_agent,
            to_agent,
            artifact_hash,
            parity_hash,
            nonce,
            timestamp.to_rfc3339()
        );

        let mut mac = HmacSha256::new_from_slice(secret_key)
            .map_err(|e| anyhow::anyhow!("Invalid HMAC key: {e}"))?;
        mac.update(payload.as_bytes());
        let signature = hex::encode(mac.finalize().into_bytes());

        Ok(Self {
            token_id,
            workflow_id: workflow_id.to_string(),
            stage_id: stage_id.to_string(),
            from_agent: from_agent.to_string(),
            to_agent: to_agent.to_string(),
            artifact_hash: artifact_hash.to_string(),
            parity_hash: parity_hash.to_string(),
            nonce: nonce.to_string(),
            timestamp,
            signature,
        })
    }

    pub fn verify_signature(&self, secret_key: &[u8]) -> Result<bool> {
        let payload = format!(
            "{}:{}:{}:{}->{}:{}:{}:{}:{}",
            self.token_id,
            self.workflow_id,
            self.stage_id,
            self.from_agent,
            self.to_agent,
            self.artifact_hash,
            self.parity_hash,
            self.nonce,
            self.timestamp.to_rfc3339()
        );

        let mut mac = HmacSha256::new_from_slice(secret_key)
            .map_err(|e| anyhow::anyhow!("Invalid HMAC key: {e}"))?;
        mac.update(payload.as_bytes());
        let expected = hex::encode(mac.finalize().into_bytes());

        Ok(self.signature == expected)
    }

    pub fn is_expired(&self) -> bool {
        let age = (Utc::now() - self.timestamp).num_seconds();
        age > Self::EXPIRATION_SECONDS
    }
}

pub struct HandoffValidator {
    secret_key: Vec<u8>,
    spent_nonces: Mutex<HashSet<String>>,
}

impl HandoffValidator {
    pub fn new(secret_key: &[u8]) -> Self {
        Self {
            secret_key: secret_key.to_vec(),
            spent_nonces: Mutex::new(HashSet::new()),
        }
    }

    pub fn validate_handoff(&self, token: &HandoffToken) -> Result<()> {
        if token.is_expired() {
            bail!("HandoffToken expired (age > 300 seconds)");
        }

        if !token.verify_signature(&self.secret_key)? {
            bail!("Invalid cryptographic HMAC signature on HandoffToken");
        }

        let mut nonces = self.spent_nonces.lock().unwrap();
        if nonces.contains(&token.nonce) {
            bail!("Replay attack detected: Nonce {} has already been spent", token.nonce);
        }
        nonces.insert(token.nonce.clone());

        Ok(())
    }
}
