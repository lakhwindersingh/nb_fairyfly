use anyhow::Result;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum CommercialTier {
    Free,
    Team,
    Business,
    Enterprise,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TierCapabilities {
    pub tier: CommercialTier,
    pub max_seats: u32,
    pub max_worktrees: u32,
    pub max_monthly_audits: u32,
    pub allows_custom_agents: bool,
    pub allows_sealed_nbpack: bool,
    pub allows_multi_cloud: bool,
}

impl CommercialTier {
    pub fn get_capabilities(&self) -> TierCapabilities {
        match self {
            CommercialTier::Free => TierCapabilities {
                tier: CommercialTier::Free,
                max_seats: 1,
                max_worktrees: 1,
                max_monthly_audits: 500,
                allows_custom_agents: false,
                allows_sealed_nbpack: false,
                allows_multi_cloud: false,
            },
            CommercialTier::Team => TierCapabilities {
                tier: CommercialTier::Team,
                max_seats: 15,
                max_worktrees: 5,
                max_monthly_audits: 5_000,
                allows_custom_agents: true,
                allows_sealed_nbpack: false,
                allows_multi_cloud: false,
            },
            CommercialTier::Business => TierCapabilities {
                tier: CommercialTier::Business,
                max_seats: 50,
                max_worktrees: 20,
                max_monthly_audits: 25_000,
                allows_custom_agents: true,
                allows_sealed_nbpack: true,
                allows_multi_cloud: false,
            },
            CommercialTier::Enterprise => TierCapabilities {
                tier: CommercialTier::Enterprise,
                max_seats: u32::MAX,
                max_worktrees: u32::MAX,
                max_monthly_audits: u32::MAX,
                allows_custom_agents: true,
                allows_sealed_nbpack: true,
                allows_multi_cloud: true,
            },
        }
    }
}

pub struct PackagerProvisioner;

impl PackagerProvisioner {
    pub fn assemble_bundle(tier: CommercialTier, tenant_id: &str) -> Result<serde_json::Value> {
        let caps = tier.get_capabilities();
        Ok(serde_json::json!({
            "tenant_id": tenant_id,
            "tier": caps.tier,
            "max_seats": caps.max_seats,
            "max_worktrees": caps.max_worktrees,
            "allows_custom_agents": caps.allows_custom_agents,
            "allows_sealed_nbpack": caps.allows_sealed_nbpack,
            "status": "PROVISIONED"
        }))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tier_matrix_boundaries() {
        let free_caps = CommercialTier::Free.get_capabilities();
        assert_eq!(free_caps.max_seats, 1);
        assert!(!free_caps.allows_custom_agents);

        let ent_caps = CommercialTier::Enterprise.get_capabilities();
        assert!(ent_caps.allows_multi_cloud);
        assert!(ent_caps.allows_sealed_nbpack);
    }

    #[test]
    fn test_assemble_bundle() {
        let bundle = PackagerProvisioner::assemble_bundle(CommercialTier::Business, "tenant_acme_corp").unwrap();
        assert_eq!(bundle["tenant_id"], "tenant_acme_corp");
        assert_eq!(bundle["status"], "PROVISIONED");
    }
}
