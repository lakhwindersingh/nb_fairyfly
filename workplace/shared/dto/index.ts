/**
 * Shared Data Transfer Objects (DTOs) for Percipience Multi-Module Platform
 */

export interface TenantProfile {
  tenantId: string;
  organizationName: string;
  adminEmail: string;
  subscriptionTier: "plan_team" | "plan_business" | "plan_enterprise";
  cmekKeyArn?: string;
  createdAt: string;
}

export interface BillingUsageEvent {
  eventId: string;
  tenantId: string;
  timestamp: string;
  eventType: "pr_gate_verified" | "worktree_hour_consumed" | "token_savings_realized";
  payload: {
    prNumber?: number;
    gitCommitSha?: string;
    tokensUncompressed?: number;
    tokensPruned?: number;
    grossTokenSavingsUsd?: number;
    revShareDueUsd?: number;
    worktreeId?: string;
    merkleBlockHash: string;
  };
}

export interface ObservabilityMetric {
  telemetryId: string;
  tenantId: string;
  timestamp: string;
  metricType: "token_velocity" | "prompt_cache_hit_rate" | "ast_pruning_ratio" | "merkle_block_sealed";
  data: Record<string, unknown>;
}

export interface MerkleBlockHeader {
  blockId: number;
  blockType: string;
  prevBlockHash: string;
  currentBlockHash: string;
  merkleRoot: string;
  timestamp: string;
  action: string;
}
