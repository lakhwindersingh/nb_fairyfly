# Domain Models & Entity-Relationship Schemas

> **Autonomously Synchronized**: 2026-09-16T20:09:28.075582+00:00  
> **Engine**: `agent_living_doc_architect` (CAP-21)  
> **Diagram Validation**: ✅ Valid Mermaid

## Core Relational Schema & State Entities
```mermaid
erDiagram
  TENANT {
    string tenant_id PK
    string name
    string slug
    string vcs_provider
    string repo_url
    timestamp created_at
  }

  SUBSCRIPTION {
    string subscription_id PK
    string tenant_id FK
    string tier
    float monthly_budget_usd
    float rev_share_pct
    string status
  }

  BILLING_EVENT {
    string event_id PK
    string subscription_id FK
    timestamp timestamp
    string file_path
    int uncompressed_tokens
    int pruned_tokens
    int tokens_saved
    float gross_savings_usd
    float rev_share_fee_usd
    float net_savings_usd
  }

  MERKLE_BLOCK {
    int block_id PK
    string prev_block_hash
    string current_block_hash
    string merkle_root
    timestamp timestamp
    string action
  }

  LIVING_DOC_ENTRY {
    string doc_id PK
    int block_id FK
    string file_path
    string doc_title
    string source_ast_hash
    string diagram_type
    string status
  }

  RECOVERY_POINT {
    string recovery_point_id PK
    int block_id FK
    string target_module
    string git_commit_sha
    timestamp created_at
  }

  TENANT ||--o{ SUBSCRIPTION : holds
  SUBSCRIPTION ||--o{ BILLING_EVENT : incurs
  MERKLE_BLOCK ||--o{ LIVING_DOC_ENTRY : commits
  MERKLE_BLOCK ||--o{ RECOVERY_POINT : contains
```
