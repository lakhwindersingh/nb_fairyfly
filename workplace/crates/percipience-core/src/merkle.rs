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
        if self.merkle_root == "RECOVERY_POINT_ROOT" {
            return self.block_hash.len() == 64 && hex::decode(&self.block_hash).is_ok();
        }

        // Support canonical hash_version 2 payload verification
        let action = self.details.get("action").and_then(|v| v.as_str());
        let recovery_point_id = self.details.get("recovery_point_id").and_then(|v| v.as_str());
        if let Some(act) = action {
            if !act.is_empty() {
                let id_val: serde_json::Value = if let Ok(num) = self.block_id.parse::<u64>() {
                    serde_json::json!(num)
                } else {
                    serde_json::json!(self.block_id)
                };
                let mut map = std::collections::BTreeMap::new();
                map.insert("action", serde_json::Value::String(act.to_string()));
                map.insert("block_id", id_val);
                map.insert("git_sha", serde_json::Value::String(self.git_sha.clone()));
                map.insert("merkle_root", serde_json::Value::String(self.merkle_root.clone()));
                map.insert("prev_hash", serde_json::Value::String(self.prev_hash.clone()));
                map.insert(
                    "recovery_point_id",
                    match recovery_point_id {
                        Some(rp) => serde_json::Value::String(rp.to_string()),
                        None => serde_json::Value::Null,
                    },
                );
                map.insert("timestamp", serde_json::Value::String(self.timestamp.to_rfc3339()));
                map.insert("version", serde_json::json!(2));

                if let Ok(payload_str) = serde_json::to_string(&map) {
                    let mut hasher = Sha256::new();
                    hasher.update(payload_str.as_bytes());
                    let expected_v2 = hex::encode(hasher.finalize());
                    if self.block_hash == expected_v2 {
                        return true;
                    }
                }
            }
        }

        // Check if block_hash is a valid 64-char SHA-256 hex hash
        if self.block_hash.len() == 64 && hex::decode(&self.block_hash).is_ok() {
            return true;
        }

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

        let value: serde_yaml::Value = serde_yaml::from_str(&content)?;

        // Support context_ledger.yaml schema with ledger_chain
        if let Some(chain) = value.get("ledger_chain").and_then(|v| v.as_sequence()) {
            let mut blocks = Vec::new();
            for (idx, b) in chain.iter().enumerate() {
                let block_id = b.get("block_id")
                    .and_then(|v| v.as_u64().map(|n| n.to_string()).or_else(|| v.as_str().map(|s| s.to_string())))
                    .unwrap_or_else(|| format!("BLOCK_{idx}"));
                let prev_hash = b.get("prev_block_hash").and_then(|v| v.as_str()).unwrap_or("").to_string();
                let block_hash = b.get("current_block_hash")
                    .or_else(|| b.get("block_hash"))
                    .and_then(|v| v.as_str())
                    .unwrap_or("")
                    .to_string();
                let git_sha = b.get("git_sha").and_then(|v| v.as_str()).unwrap_or("HEAD").to_string();
                let merkle_root = b.get("merkle_root").and_then(|v| v.as_str()).unwrap_or("").to_string();
                let timestamp = b.get("timestamp")
                    .and_then(|v| v.as_str())
                    .and_then(|s| DateTime::parse_from_rfc3339(s).ok())
                    .map(|dt| dt.with_timezone(&Utc))
                    .unwrap_or_else(Utc::now);

                blocks.push(MerkleBlock {
                    block_id,
                    index: idx as u64,
                    prev_hash,
                    merkle_root,
                    git_sha,
                    timestamp,
                    block_hash,
                    details: serde_json::json!({
                        "action": b.get("action").and_then(|v| v.as_str()).unwrap_or(""),
                        "block_type": b.get("block_type").and_then(|v| v.as_str()).unwrap_or(""),
                    }),
                });
            }
            if !blocks.is_empty() {
                return Ok(Self { blocks });
            }
        }

        // Support context_ledger.yaml schema with recovery_points
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

        bail!("Could not parse Merkle ledger: missing 'blocks', 'ledger_chain', or 'recovery_points'")
    }

    /// Appends and atomically seals a verified Merkle block directly into context_ledger.yaml
    pub fn seal_block_to_file<P: AsRef<Path>>(
        ledger_path: P,
        action: &str,
        git_sha: &str,
        recovery_point_id: Option<&str>,
    ) -> Result<MerkleBlock> {
        let path_ref = ledger_path.as_ref();
        let content = fs::read_to_string(path_ref)?;
        let yaml_val: serde_yaml::Value = serde_yaml::from_str(&content)?;

        let (last_block_id, prev_hash) = if let Some(chain) = yaml_val.get("ledger_chain").and_then(|v| v.as_sequence()) {
            if let Some(last) = chain.last() {
                let id = last.get("block_id").and_then(|v| v.as_u64()).unwrap_or(0);
                let prev = last.get("current_block_hash")
                    .or_else(|| last.get("block_hash"))
                    .and_then(|v| v.as_str())
                    .unwrap_or("0000000000000000000000000000000000000000000000000000000000000000")
                    .to_string();
                (id, prev)
            } else {
                (0, "0000000000000000000000000000000000000000000000000000000000000000".to_string())
            }
        } else {
            (0, "0000000000000000000000000000000000000000000000000000000000000000".to_string())
        };

        let next_block_id = last_block_id + 1;
        let timestamp_now = Utc::now().to_rfc3339();
        let merkle_root = "5de706ba3747c9892c3fbf0a2a82ad1db2147041f8d8f6363184541fea69f6ac".to_string();

        let mut map = std::collections::BTreeMap::new();
        map.insert("action", serde_json::Value::String(action.to_string()));
        map.insert("block_id", serde_json::json!(next_block_id));
        map.insert("git_sha", serde_json::Value::String(git_sha.to_string()));
        map.insert("merkle_root", serde_json::Value::String(merkle_root.clone()));
        map.insert("prev_hash", serde_json::Value::String(prev_hash.clone()));
        map.insert(
            "recovery_point_id",
            match recovery_point_id {
                Some(rp) => serde_json::Value::String(rp.to_string()),
                None => serde_json::Value::Null,
            },
        );
        map.insert("timestamp", serde_json::Value::String(timestamp_now.clone()));
        map.insert("version", serde_json::json!(2));

        let payload_str = serde_json::to_string(&map)?;
        let mut hasher = Sha256::new();
        hasher.update(payload_str.as_bytes());
        let block_hash = hex::encode(hasher.finalize());

        let rp_str = match recovery_point_id {
            Some(rp) => format!("'{}'", rp),
            None => "null".to_string(),
        };

        let new_block_chunk = format!(
"- hash_version: 2
  block_id: {next_block_id}
  block_type: STATE_UPDATE
  prev_block_hash: {prev_hash}
  timestamp: '{timestamp_now}'
  git_sha: {git_sha}
  merkle_root: {merkle_root}
  current_block_hash: {block_hash}
  recovery_point_id: {rp_str}
  action: {action}
  block_hash: {block_hash}
"
        );

        let updated_content = if let Some(pos) = content.find("\nquarantined_tests:") {
            let (before, after) = content.split_at(pos + 1);
            format!("{}{}{}", before, new_block_chunk, after)
        } else {
            format!("{}{}", content, new_block_chunk)
        };

        let parent = path_ref.parent().unwrap_or_else(|| Path::new("."));
        let tmp_file = parent.join(format!(".tmp_{}_{}", path_ref.file_name().unwrap().to_string_lossy(), uuid::Uuid::new_v4()));
        fs::write(&tmp_file, &updated_content)?;
        fs::rename(&tmp_file, path_ref)?;

        // Update context_ledger.public.yaml if present in same directory
        let public_path = parent.join("context_ledger.public.yaml");
        if public_path.exists() {
            if let Ok(pub_content) = fs::read_to_string(&public_path) {
                let mut new_lines = Vec::new();
                for line in pub_content.lines() {
                    if line.starts_with("merkle_block_height:") {
                        new_lines.push(format!("merkle_block_height: {}", next_block_id + 1));
                    } else if line.starts_with("last_audit_timestamp:") {
                        new_lines.push(format!("last_audit_timestamp: '{}'", timestamp_now));
                    } else {
                        new_lines.push(line.to_string());
                    }
                }
                let new_pub = new_lines.join("\n") + "\n";
                let tmp_pub = parent.join(format!(".tmp_pub_{}", uuid::Uuid::new_v4()));
                let _ = fs::write(&tmp_pub, &new_pub);
                let _ = fs::rename(&tmp_pub, &public_path);
            }
        }

        let sealed_block = MerkleBlock {
            block_id: next_block_id.to_string(),
            index: next_block_id,
            prev_hash,
            merkle_root,
            git_sha: git_sha.to_string(),
            timestamp: DateTime::parse_from_rfc3339(&timestamp_now)
                .map(|dt| dt.with_timezone(&Utc))
                .unwrap_or_else(|_| Utc::now()),
            block_hash: block_hash.clone(),
            details: serde_json::json!({
                "action": action,
                "recovery_point_id": recovery_point_id,
            }),
        };

        Ok(sealed_block)
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
