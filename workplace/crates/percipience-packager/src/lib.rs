use anyhow::{Context, Result};
use chrono::Utc;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::fs;
use std::path::{Path, PathBuf};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum CommercialTier {
    Free,
    Team,
    Business,
    Enterprise,
}

impl CommercialTier {
    pub fn parse_str(s: &str) -> Self {
        match s.to_lowercase().replace("plan_", "").as_str() {
            "free" | "community" => CommercialTier::Free,
            "team" => CommercialTier::Team,
            "business" => CommercialTier::Business,
            _ => CommercialTier::Enterprise,
        }
    }

    pub fn as_str(&self) -> &'static str {
        match self {
            CommercialTier::Free => "free",
            CommercialTier::Team => "team",
            CommercialTier::Business => "business",
            CommercialTier::Enterprise => "enterprise",
        }
    }

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

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub enum BundleTarget {
    IntelliJ,
    VSCode,
    All,
}

impl std::str::FromStr for BundleTarget {
    type Err = anyhow::Error;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.to_lowercase().as_str() {
            "intellij" | "idea" | "pycharm" => Ok(BundleTarget::IntelliJ),
            "vscode" | "code" => Ok(BundleTarget::VSCode),
            "all" | "both" => Ok(BundleTarget::All),
            _ => anyhow::bail!("Unknown bundle target: {}. Valid: intellij, vscode, all", s),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BundleReport {
    pub target: String,
    pub bundle_dir: String,
    pub binary_path: String,
    pub binary_size_bytes: u64,
    pub binary_sha256: String,
    pub files_copied: usize,
    pub tier: CommercialTier,
    pub tenant_id: String,
    pub success: bool,
    pub clean_pure_rust: bool,
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

    /// Locates the native release binary within the workspace
    pub fn find_native_binary(repo_root: &Path) -> Result<PathBuf> {
        let candidates = [
            repo_root.join("target/release/percipience"),
            repo_root.join(".nb/bin/percipience"),
            repo_root.join("percipience"),
        ];

        for cand in &candidates {
            if cand.is_file() {
                return Ok(cand.clone());
            }
        }

        anyhow::bail!(
            "Could not find native percipience binary in any expected path: {:?}",
            candidates
        );
    }

    /// Recursively copies files from src to dst, excluding Python/pycache artifacts
    pub fn copy_clean_dir(src: &Path, dst: &Path) -> Result<usize> {
        if !src.exists() {
            return Ok(0);
        }

        let mut count = 0;
        fs::create_dir_all(dst)?;

        for entry in fs::read_dir(src)? {
            let entry = entry?;
            let file_type = entry.file_type()?;
            let path = entry.path();
            let file_name = entry.file_name();
            let name_str = file_name.to_string_lossy();

            // Exclude Python, cache, and hidden git files
            if name_str.ends_with(".py")
                || name_str.ends_with(".pyc")
                || name_str == "__pycache__"
                || name_str == ".DS_Store"
                || name_str.starts_with(".git")
            {
                continue;
            }

            let target = dst.join(&file_name);
            if file_type.is_dir() {
                count += Self::copy_clean_dir(&path, &target)?;
            } else if file_type.is_file() {
                fs::copy(&path, &target)?;
                count += 1;
            }
        }

        Ok(count)
    }

    /// Removes legacy python core/ and scripts/ directories and files from a bundle directory
    pub fn purge_legacy_python_artifacts(bundle_dir: &Path) -> Result<()> {
        if !bundle_dir.exists() {
            return Ok(());
        }

        let legacy_dirs = ["core", "__pycache__", "core_legacy"];
        for d in &legacy_dirs {
            let p = bundle_dir.join(d);
            if p.exists() {
                let _ = fs::remove_dir_all(&p);
            }
        }

        // Recursively remove any dangling .py or .pyc files
        let mut dirs_to_visit = vec![bundle_dir.to_path_buf()];
        while let Some(current_dir) = dirs_to_visit.pop() {
            if let Ok(entries) = fs::read_dir(&current_dir) {
                for entry in entries.flatten() {
                    let path = entry.path();
                    if let Ok(ft) = entry.file_type() {
                        if ft.is_dir() {
                            let name = entry.file_name();
                            let s = name.to_string_lossy();
                            if s == "__pycache__" || s == "core" {
                                let _ = fs::remove_dir_all(&path);
                            } else {
                                dirs_to_visit.push(path);
                            }
                        } else if ft.is_file() {
                            let s = entry.file_name().to_string_lossy().to_string();
                            if s.ends_with(".py") || s.ends_with(".pyc") {
                                let _ = fs::remove_file(&path);
                            }
                        }
                    }
                }
            }
        }

        Ok(())
    }

    pub fn is_workflow_allowed_for_tier(wf_name: &str, tier: &CommercialTier) -> bool {
        match tier {
            CommercialTier::Free => matches!(
                wf_name,
                "basic_autonomous_cicd.yaml"
                    | "intellij_pycharm_plugin_delivery_flow.yaml"
            ),
            CommercialTier::Team => matches!(
                wf_name,
                "basic_autonomous_cicd.yaml"
                    | "intellij_pycharm_plugin_delivery_flow.yaml"
                    | "vscode_plugin_delivery_flow.yaml"
            ),
            CommercialTier::Business => matches!(
                wf_name,
                "basic_autonomous_cicd.yaml"
                    | "intellij_pycharm_plugin_delivery_flow.yaml"
                    | "vscode_plugin_delivery_flow.yaml"
                    | "saas_portal_delivery_flow.yaml"
                    | "iot_mobile_delivery_flow.yaml"
                    | "commercial_packaging_provisioning_flow.yaml"
            ),
            CommercialTier::Enterprise => true,
        }
    }

    /// Packages the IntelliJ IDEA / PyCharm plugin runtime bundle in Rust
    pub fn pack_intellij_bundle(
        repo_root: &Path,
        tier: CommercialTier,
        tenant_id: &str,
    ) -> Result<BundleReport> {
        let bundle_dir = repo_root
            .join("workplace/modules/mod_intellij_plugin/src/main/resources/percipience");
        Self::provision_directory_bundle(repo_root, &bundle_dir, "intellij", tier, tenant_id)
    }

    /// Packages the VSCode extension runtime bundle in Rust
    pub fn pack_vscode_bundle(
        repo_root: &Path,
        tier: CommercialTier,
        tenant_id: &str,
    ) -> Result<BundleReport> {
        let bundle_dir =
            repo_root.join("workplace/modules/mod_vscode_extension/percipience_runtime");
        let report = Self::provision_directory_bundle(repo_root, &bundle_dir, "vscode", tier.clone(), tenant_id)?;

        // Also write .percipience_license.json at the root of mod_vscode_extension
        let ext_license = repo_root
            .join("workplace/modules/mod_vscode_extension/.percipience_license.json");
        let license_src = bundle_dir.join("tenant_license.json");
        if license_src.is_file() {
            fs::copy(&license_src, &ext_license)?;
        }

        Ok(report)
    }

    /// Core provisioning logic for any runtime bundle directory
    pub fn provision_directory_bundle(
        repo_root: &Path,
        bundle_dir: &Path,
        target_name: &str,
        tier: CommercialTier,
        tenant_id: &str,
    ) -> Result<BundleReport> {
        fs::create_dir_all(bundle_dir)?;
        Self::purge_legacy_python_artifacts(bundle_dir)?;

        // Clean tier-sensitive directories so previous provisions don't leak
        for d in &["workflows", "agentic", "hooks", "scripts"] {
            let p = bundle_dir.join(d);
            if p.exists() {
                let _ = fs::remove_dir_all(&p);
            }
        }

        let mut total_files_copied = 0;

        // 1. Locate and deploy native release binary
        let binary_src = Self::find_native_binary(repo_root)
            .context("Failed to locate release percipience binary")?;
        let bin_bytes = fs::read(&binary_src)
            .with_context(|| format!("Failed to read binary at {:?}", binary_src))?;

        let mut hasher = Sha256::new();
        hasher.update(&bin_bytes);
        let binary_sha256 = hex::encode(hasher.finalize());
        let binary_size_bytes = bin_bytes.len() as u64;

        let bin_dest_dir = bundle_dir.join("bin");
        fs::create_dir_all(&bin_dest_dir)?;
        let bin_dest = bin_dest_dir.join("percipience");
        fs::copy(&binary_src, &bin_dest)?;
        total_files_copied += 1;

        #[cfg(unix)]
        {
            use std::os::unix::fs::PermissionsExt;
            if let Ok(meta) = fs::metadata(&bin_dest) {
                let mut perms = meta.permissions();
                perms.set_mode(0o755);
                let _ = fs::set_permissions(&bin_dest, perms);
            }
        }

        // 2. Deploy configuration plane (.nb/config)
        let config_src = repo_root.join(".nb/config");
        let config_dst = bundle_dir.join("config");
        total_files_copied += Self::copy_clean_dir(&config_src, &config_dst)?;

        // 3. Deploy declarative agentic plane (.nb/agentic) with tier gating
        let agentic_src = repo_root.join(".nb/agentic");
        let agentic_dst = bundle_dir.join("agentic");
        fs::create_dir_all(&agentic_dst)?;

        // 3a. Custom agents gating
        let custom_agents_src = agentic_src.join("custom/agents");
        let custom_agents_dst = agentic_dst.join("custom/agents");
        if custom_agents_src.exists() {
            fs::create_dir_all(&custom_agents_dst)?;
            for entry in fs::read_dir(&custom_agents_src)? {
                let entry = entry?;
                let path = entry.path();
                let name = entry.file_name().to_string_lossy().to_string();
                if name.ends_with(".yaml") || name.ends_with(".yml") {
                    if tier == CommercialTier::Free
                        && (name.contains("enterprise") || name.contains("saas_portal") || name.contains("iot_mobile"))
                    {
                        continue;
                    }
                    fs::copy(&path, custom_agents_dst.join(&name))?;
                    total_files_copied += 1;
                }
            }
        }

        // 3b. Custom workflows gating (e.g. delivery flows)
        let custom_wf_src = agentic_src.join("custom/workflows");
        let custom_wf_dst = agentic_dst.join("custom/workflows");
        if custom_wf_src.exists() {
            fs::create_dir_all(&custom_wf_dst)?;
            for entry in fs::read_dir(&custom_wf_src)? {
                let entry = entry?;
                let path = entry.path();
                let name = entry.file_name().to_string_lossy().to_string();
                if (name.ends_with(".yaml") || name.ends_with(".yml")) && Self::is_workflow_allowed_for_tier(&name, &tier) {
                    fs::copy(&path, custom_wf_dst.join(&name))?;
                    total_files_copied += 1;
                }
            }
        }

        // 3c. Canonical workflows gating (e.g. pr_gatekeeper, derivation pipelines)
        let canon_wf_src = agentic_src.join("workflows");
        let canon_wf_dst = agentic_dst.join("workflows");
        if canon_wf_src.exists() {
            fs::create_dir_all(&canon_wf_dst)?;
            for entry in fs::read_dir(&canon_wf_src)? {
                let entry = entry?;
                let path = entry.path();
                let name = entry.file_name().to_string_lossy().to_string();
                if name.ends_with(".yaml") || name.ends_with(".yml") {
                    if tier == CommercialTier::Free && (name.contains("enterprise") || name.contains("security_mesh")) {
                        continue;
                    }
                    fs::copy(&path, canon_wf_dst.join(&name))?;
                    total_files_copied += 1;
                }
            }
        }

        // 3d. Top-level workflows/ directory (for direct IDE execution and tier tests)
        let top_wf_dst = bundle_dir.join("workflows");
        fs::create_dir_all(&top_wf_dst)?;
        if custom_wf_src.exists() {
            for entry in fs::read_dir(&custom_wf_src)? {
                let entry = entry?;
                let path = entry.path();
                let name = entry.file_name().to_string_lossy().to_string();
                if (name.ends_with(".yaml") || name.ends_with(".yml")) && Self::is_workflow_allowed_for_tier(&name, &tier) {
                    fs::copy(&path, top_wf_dst.join(&name))?;
                    total_files_copied += 1;
                }
            }
        }
        // Always ensure basic_autonomous_cicd.yaml is in workflows/ if present
        let basic_cicd_cand = custom_wf_src.join("basic_autonomous_cicd.yaml");
        if basic_cicd_cand.is_file() && !top_wf_dst.join("basic_autonomous_cicd.yaml").exists() {
            fs::copy(&basic_cicd_cand, top_wf_dst.join("basic_autonomous_cicd.yaml"))?;
            total_files_copied += 1;
        }

        // 3e. Copy prompts and schemas if present
        for sub in ["prompts", "schemas"] {
            let src = agentic_src.join(sub);
            let dst = agentic_dst.join(sub);
            if src.exists() {
                total_files_copied += Self::copy_clean_dir(&src, &dst)?;
            }
        }

        // 4. Deploy contracts (.nb/context/contracts)
        let contracts_src = repo_root.join(".nb/context/contracts");
        let contracts_dst = bundle_dir.join("contracts");
        if contracts_src.exists() {
            total_files_copied += Self::copy_clean_dir(&contracts_src, &contracts_dst)?;
        }

        // 4b. Deploy git hooks (hooks/pre-commit.sh)
        let hooks_dst = bundle_dir.join("hooks");
        fs::create_dir_all(&hooks_dst)?;
        let pre_commit_src = repo_root.join(".nb/git_hooks/pre-commit.sh");
        if pre_commit_src.is_file() {
            fs::copy(&pre_commit_src, hooks_dst.join("pre-commit.sh"))?;
            total_files_copied += 1;
        }

        // 4c. Deploy essential scripts (scripts/install_git_hook.sh, scripts/validate.sh)
        let scripts_dst = bundle_dir.join("scripts");
        fs::create_dir_all(&scripts_dst)?;
        let install_hook_src = repo_root.join(".nb/scripts/install_git_hook.sh");
        if install_hook_src.is_file() {
            fs::copy(&install_hook_src, scripts_dst.join("install_git_hook.sh"))?;
            total_files_copied += 1;
        }
        let validate_src = repo_root.join(".nb/scripts/validate.sh");
        if validate_src.is_file() {
            fs::copy(&validate_src, scripts_dst.join("validate.sh"))?;
            total_files_copied += 1;
        }

        // 5. Deploy canonical plan templates
        let plan_dst = bundle_dir.join("plan");
        fs::create_dir_all(&plan_dst)?;

        let master_plan_src = repo_root.join(".nb/plan/master/parent-master-plan/detailed.md");
        if master_plan_src.is_file() {
            fs::copy(
                &master_plan_src,
                plan_dst.join("claude-context-engineering-parent-master-plan.md"),
            )?;
            total_files_copied += 1;
        }

        let free_plan_src =
            repo_root.join(".nb/plan/master/parent-master-free-plan/detailed.md");
        if free_plan_src.is_file() {
            fs::copy(
                &free_plan_src,
                plan_dst.join("claude-context-engineering-parent-master-free_plan.md"),
            )?;
            total_files_copied += 1;
        }

        // 6. Write version.json
        let version_manifest = serde_json::json!({
            "manifest_schema": 1,
            "plugin_version": "1.3.0",
            "platform_version": "7.5.0",
            "runtime_type": "rust_native_static",
            "tier": format!("plan_{}", tier.as_str()),
            "channel": "stable",
            "binary_sha256": binary_sha256,
            "binary_size_bytes": binary_size_bytes,
            "released_at": Utc::now().to_rfc3339(),
            "timestamp": Utc::now().to_rfc3339()
        });
        fs::write(
            bundle_dir.join("version.json"),
            serde_json::to_string_pretty(&version_manifest)?,
        )?;
        total_files_copied += 1;

        // 7. Write tenant_license.json
        let caps = tier.get_capabilities();
        let license_id = uuid::Uuid::new_v4().to_string();
        let mut lic_hasher = Sha256::new();
        lic_hasher.update(format!("{}:{}:{}", tenant_id, tier.as_str(), license_id));
        let license_signature = hex::encode(lic_hasher.finalize());

        let license_manifest = serde_json::json!({
            "tenant_id": tenant_id,
            "tier": tier.as_str(),
            "license_id": license_id,
            "status": "PROVISIONED",
            "capabilities": caps,
            "license_signature": format!("sha256:{}", license_signature),
            "issued_at": Utc::now().to_rfc3339()
        });
        fs::write(
            bundle_dir.join("tenant_license.json"),
            serde_json::to_string_pretty(&license_manifest)?,
        )?;
        total_files_copied += 1;

        // 8. Sanity check: Ensure 0 Python files remain
        let mut clean_pure_rust = true;
        let mut verify_queue = vec![bundle_dir.to_path_buf()];
        while let Some(dir) = verify_queue.pop() {
            if let Ok(entries) = fs::read_dir(&dir) {
                for entry in entries.flatten() {
                    let path = entry.path();
                    if let Ok(ft) = entry.file_type() {
                        if ft.is_dir() {
                            if entry.file_name() == "core" || entry.file_name() == "__pycache__" {
                                clean_pure_rust = false;
                            }
                            verify_queue.push(path);
                        } else if ft.is_file() {
                            let name = entry.file_name().to_string_lossy().to_string();
                            if name.ends_with(".py") || name.ends_with(".pyc") {
                                clean_pure_rust = false;
                            }
                        }
                    }
                }
            }
        }

        Ok(BundleReport {
            target: target_name.to_string(),
            bundle_dir: bundle_dir.to_string_lossy().to_string(),
            binary_path: bin_dest.to_string_lossy().to_string(),
            binary_size_bytes,
            binary_sha256,
            files_copied: total_files_copied,
            tier,
            tenant_id: tenant_id.to_string(),
            success: true,
            clean_pure_rust,
        })
    }

    /// Provision target(s) based on BundleTarget enum
    pub fn provision_target(
        repo_root: &Path,
        target: BundleTarget,
        tier: CommercialTier,
        tenant_id: &str,
    ) -> Result<Vec<BundleReport>> {
        let mut reports = Vec::new();
        match target {
            BundleTarget::IntelliJ => {
                reports.push(Self::pack_intellij_bundle(repo_root, tier, tenant_id)?);
            }
            BundleTarget::VSCode => {
                reports.push(Self::pack_vscode_bundle(repo_root, tier, tenant_id)?);
            }
            BundleTarget::All => {
                reports.push(Self::pack_intellij_bundle(repo_root, tier.clone(), tenant_id)?);
                reports.push(Self::pack_vscode_bundle(repo_root, tier, tenant_id)?);
            }
        }
        Ok(reports)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::tempdir;

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
        let bundle =
            PackagerProvisioner::assemble_bundle(CommercialTier::Business, "tenant_acme_corp").unwrap();
        assert_eq!(bundle["status"], "PROVISIONED");
        assert_eq!(bundle["tenant_id"], "tenant_acme_corp");
    }

    #[test]
    fn test_provision_mock_bundle_pure_rust() {
        let td = tempdir().unwrap();
        let root = td.path();

        // Create mock binary
        let bin_dir = root.join("target/release");
        fs::create_dir_all(&bin_dir).unwrap();
        fs::write(bin_dir.join("percipience"), b"mock-elf-binary").unwrap();

        // Create mock config & agentic
        let cfg_dir = root.join(".nb/config");
        fs::create_dir_all(&cfg_dir).unwrap();
        fs::write(cfg_dir.join("platform_config.yaml"), b"mode: prod").unwrap();

        let ag_dir = root.join(".nb/agentic/workflows");
        fs::create_dir_all(&ag_dir).unwrap();
        fs::write(ag_dir.join("cicd.yaml"), b"name: cicd").unwrap();

        // Bundle
        let out_dir = root.join("out_bundle");
        let report = PackagerProvisioner::provision_directory_bundle(
            root,
            &out_dir,
            "test_target",
            CommercialTier::Enterprise,
            "tenant_test",
        )
        .unwrap();

        assert!(report.success);
        assert!(report.clean_pure_rust);
        assert!(out_dir.join("bin/percipience").exists());
        assert!(out_dir.join("version.json").exists());
        assert!(out_dir.join("tenant_license.json").exists());
        assert!(out_dir.join("config/platform_config.yaml").exists());
    }
}
