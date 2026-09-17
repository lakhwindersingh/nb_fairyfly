---
mvs_version: "1.0.0"
format_type: "adr_system_blueprint"
id: "MVS-ADR-004"
title: "Distributed Cache-Aside Layer with Sharded Redis Cluster"
target_module: "mod_cache_layer"
status: "Proposed" # Proposed | Accepted | Deprecated | Superseded
deciders: ["Systems Architect", "Lead Infrastructure Engineer"]
date: "2026-09-13"
---

# Architecture Decision Record (ADR) & System Blueprint

## 1. Context & Problem Statement
High read volume on relational database partitions is degrading p99 query latency during peak market hours ($> 350\text{ ms}$). A distributed caching layer is required to absorb $85\%$ of read traffic while enforcing deterministic cache eviction and preventing stale reads.

## 2. Decision & Architectural Topology
We will implement a Redis 7.x cluster operating in a Cache-Aside pattern with Write-Through invalidation:

```mermaid
flowchart LR
  Client["Application Service"] -->|1. Check Cache| Cache[("Redis 7.x Cluster<br/>(Cluster Sharded)")]
  Cache -->|Cache Hit (Sub-1ms)| Client
  Client -->|2. Cache Miss| DB[("Aurora PostgreSQL<br/>(Read Replica)")]
  DB -->|3. Populate Cache + TTL| Cache
```

### Key Technical Decisions:
1. **TTL Strategy**: Adaptive dynamic TTL (60s default, scaled down to 5s for volatile balance queries).
2. **Key Namespacing**: Strict multi-tenant key prefixes: `tenant_{tenant_id}:session:{session_id}`.
3. **Cache Stampede Prevention**: Distributed Mutex locks via Redlock algorithm on cache misses.

## 3. Database Schema & Data Models
```sql
CREATE TABLE cache_metadata (
    cache_key VARCHAR(255) PRIMARY KEY,
    tenant_id UUID NOT NULL,
    version BIGINT NOT NULL DEFAULT 1,
    invalidation_event VARCHAR(128) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_cache_tenant ON cache_metadata(tenant_id);
```

## 4. Consequences & Compliance
- **Positive**: Reduces database CPU utilization by $65\%$; lowers p99 latency to $< 4\text{ ms}$.
- **Trade-Off**: Requires cache warming logic on container startup and careful eviction invalidation.
- **Compliance**: All cached data in transit is encrypted with TLS 1.3; sensitive customer PII is salted and hashed before storing in cache keys.
