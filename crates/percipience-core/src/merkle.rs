use anyhow::{bail, Result};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct MerkleBlock {
    pub block_id: String,
    pub index: u64,
    pub prev_hash: String,
    pub merkle_root: String,
    pub git_sha: String,
    pub timestamp: DateTime<Utc>,
    pub block_hash: String,
    pub details: serde_json::Value,
}

impl MerkleBlock {
    pub fn compute_hash(
        block_id: &str,
        prev_hash: &str,
        merkle_root: &str,
        git_sha: &str,
        timestamp: &DateTime<Utc>,
    ) -> String {
        let mut hasher = Sha256::new();
        hasher.update(block_id.as_bytes());
        hasher.update(prev_hash.as_bytes());
        hasher.update(merkle_root.as_bytes());
        hasher.update(git_sha.as_bytes());
        hasher.update(timestamp.to_rfc3339().as_bytes());
        hex::encode(hasher.finalize())
    }

    pub fn new_genesis(git_sha: &str) -> Self {
        let block_id = "BLOCK_GENESIS_000".to_string();
        let prev_hash = "0000000000000000000000000000000000000000000000000000000000000000".to_string();
        let merkle_root = "GENESIS_ROOT".to_string();
        let timestamp = Utc::now();
        let block_hash = Self::compute_hash(&block_id, &prev_hash, &merkle_root, git_sha, &timestamp);

        Self {
            block_id,
            index: 0,
            prev_hash,
            merkle_root,
            git_sha: git_sha.to_string(),
            timestamp,
            block_hash,
            details: serde_json::json!({ "type": "genesis", "status": "sealed" }),
        }
    }

    pub fn new_next(
        prev: &MerkleBlock,
        block_id: &str,
        merkle_root: &str,
        git_sha: &str,
        details: serde_json::Value,
    ) -> Self {
        let timestamp = Utc::now();
        let block_hash = Self::compute_hash(block_id, &prev.block_hash, merkle_root, git_sha, &timestamp);

        Self {
            block_id: block_id.to_string(),
            index: prev.index + 1,
            prev_hash: prev.block_hash.clone(),
            merkle_root: merkle_root.to_string(),
            git_sha: git_sha.to_string(),
            timestamp,
            block_hash,
            details,
        }
    }

    pub fn verify_integrity(&self) -> bool {
        let expected = Self::compute_hash(
            &self.block_id,
            &self.prev_hash,
            &self.merkle_root,
            &self.git_sha,
            &self.timestamp,
        );
        self.block_hash == expected
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct MerkleLedger {
    pub blocks: Vec<MerkleBlock>,
}

impl MerkleLedger {
    pub fn new() -> Self {
        Self { blocks: Vec::new() }
    }

    pub fn with_genesis(git_sha: &str) -> Self {
        let mut ledger = Self::new();
        ledger.blocks.push(MerkleBlock::new_genesis(git_sha));
        ledger
    }

    pub fn append(&mut self, block_id: &str, merkle_root: &str, git_sha: &str, details: serde_json::Value) -> Result<&MerkleBlock> {
        let last_block = match self.blocks.last() {
            Some(b) => b,
            None => bail!("Cannot append to an empty ledger without genesis block"),
        };

        let new_block = MerkleBlock::new_next(last_block, block_id, merkle_root, git_sha, details);
        self.blocks.push(new_block);
        Ok(self.blocks.last().unwrap())
    }

    pub fn verify_chain(&self) -> Result<()> {
        if self.blocks.is_empty() {
            bail!("Ledger is empty");
        }

        for (i, block) in self.blocks.iter().enumerate() {
            if block.merkle_root == "RECOVERY_POINT_ROOT" {
                if block.block_hash.len() != 64 || hex::decode(&block.block_hash).is_err() {
                    bail!("Recovery point {} has invalid SHA-256 hash {}", block.block_id, block.block_hash);
                }
            } else if !block.verify_integrity() {
                bail!("Block {} (ID: {}) failed hash verification", i, block.block_id);
            }

            if i > 0 {
                let prev = &self.blocks[i - 1];
                if block.prev_hash != prev.block_hash {
                    bail!(
                        "Broken chain at index {}: block.prev_hash {} != prev.block_hash {}",
                        i,
                        block.prev_hash,
                        prev.block_hash
                    );
                }
                if block.index != prev.index + 1 {
                    bail!("Invalid block index at {}: expected {}", i, prev.index + 1);
                }
            }
        }

        Ok(())
    }

    pub fn load_from_yaml<P: AsRef<Path>>(path: P) -> Result<Self> {
        let content = fs::read_to_string(path)?;
        if let Ok(ledger) = serde_yaml::from_str::<Self>(&content) {
            if !ledger.blocks.is_empty() {
                return Ok(ledger);
            }
        }

        // Support context_ledger.yaml schema with recovery_points
        let value: serde_yaml::Value = serde_yaml::from_str(&content)?;
        if let Some(rps) = value.get("recovery_points").and_then(|v| v.as_sequence()) {
            let mut blocks = Vec::new();
            let mut prev_hash = "0000000000000000000000000000000000000000000000000000000000000000".to_string();

            for (idx, rp) in rps.iter().enumerate() {
                let id = rp.get("id").and_then(|v| v.as_str()).unwrap_or("RP_UNKNOWN").to_string();
                let block_id = rp.get("block_id").and_then(|v| v.as_u64()).map(|b| b.to_string())
                    .or_else(|| rp.get("block_id").and_then(|v| v.as_str()).map(|s| s.to_string()))
                    .unwrap_or_else(|| format!("BLOCK_{idx}"));
                let block_hash = rp.get("block_hash").and_then(|v| v.as_str()).unwrap_or("").to_string();
                let git_sha = rp.get("git_commit").and_then(|v| v.as_str()).unwrap_or("HEAD").to_string();
                let timestamp = rp.get("timestamp")
                    .and_then(|v| v.as_str())
                    .and_then(|s| DateTime::parse_from_rfc3339(s).ok())
                    .map(|dt| dt.with_timezone(&Utc))
                    .unwrap_or_else(Utc::now);

                blocks.push(MerkleBlock {
                    block_id: format!("{id}:{block_id}"),
                    index: idx as u64,
                    prev_hash: prev_hash.clone(),
                    merkle_root: "RECOVERY_POINT_ROOT".to_string(),
                    git_sha,
                    timestamp,
                    block_hash: block_hash.clone(),
                    details: serde_json::json!({
                        "id": id,
                        "status": rp.get("status").and_then(|v| v.as_str()).unwrap_or("UNKNOWN"),
                        "description": rp.get("description").and_then(|v| v.as_str()).unwrap_or("")
                    }),
                });

                prev_hash = block_hash;
            }

            return Ok(Self { blocks });
        }

        bail!("Could not parse Merkle ledger: missing 'blocks' or 'recovery_points'")
    }

    pub fn save_to_yaml<P: AsRef<Path>>(&self, path: P) -> Result<()> {
        let content = serde_yaml::to_string(self)?;
        if let Some(parent) = path.as_ref().parent() {
            fs::create_dir_all(parent)?;
        }
        fs::write(path, content)?;
        Ok(())
    }
}
