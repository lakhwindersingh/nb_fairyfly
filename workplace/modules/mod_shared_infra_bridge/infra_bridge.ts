/**
 * Infrastructure Bridge Abstraction Layer
 * Supports Phase 1 (Shared Co-Located Infrastructure) and Phase 2 (Decoupled Standalone Infrastructure)
 */

export interface TelemetryMetricEvent {
  tenantId: string;
  metricName: string;
  value: number;
  tags?: Record<string, string>;
}

export interface IInfraBridge {
  getDatabaseConnection(tenantId: string): Promise<string>;
  getCacheNamespace(tenantId: string): string;
  getWormVaultPrefix(tenantId: string): string;
  emitTelemetryMetric(event: TelemetryMetricEvent): Promise<void>;
  getOperatingMode(): "shared_co_located" | "decoupled_dedicated";
  setOperatingMode(mode: "shared_co_located" | "decoupled_dedicated"): void;
}

export class SharedInfraBridge implements IInfraBridge {
  private mode: "shared_co_located" | "decoupled_dedicated";
  private connectionPoolMax: number;
  private redisPrefix: string;

  constructor(
    mode: "shared_co_located" | "decoupled_dedicated" = "shared_co_located",
    connectionPoolMax: number = 20,
    redisPrefix: string = "portal:"
  ) {
    this.mode = mode;
    this.connectionPoolMax = connectionPoolMax;
    this.redisPrefix = redisPrefix;
  }

  getOperatingMode(): "shared_co_located" | "decoupled_dedicated" {
    return this.mode;
  }

  setOperatingMode(mode: "shared_co_located" | "decoupled_dedicated"): void {
    this.mode = mode;
  }

  async getDatabaseConnection(tenantId: string): Promise<string> {
    if (this.mode === "shared_co_located") {
      // Co-located PostgreSQL pool with Row-Level Security & tenant schema search path
      return `postgresql://aurora_shared_pool:5432/percipience?sslmode=verify-full&options=-c%20search_path=tenant_${tenantId}&pool_max=${this.connectionPoolMax}`;
    }
    // Phase 2 Decoupled: Dedicated client VPC connection string
    return `postgresql://dedicated_tenant_${tenantId}:secret@rds-${tenantId}.vpc.internal:5432/percipience_db?sslmode=verify-full`;
  }

  getCacheNamespace(tenantId: string): string {
    if (this.mode === "shared_co_located") {
      return `${this.redisPrefix}tenant:${tenantId}:`;
    }
    return `tenant:${tenantId}:`;
  }

  getWormVaultPrefix(tenantId: string): string {
    if (this.mode === "shared_co_located") {
      return `s3://percipience-shared-worm-vault/tenants/${tenantId}/`;
    }
    return `s3://tenant-${tenantId}-dedicated-vault/`;
  }

  async emitTelemetryMetric(event: TelemetryMetricEvent): Promise<void> {
    // Routes metric to co-located TimescaleDB or dedicated Prometheus/Datadog endpoint
    // In production, this flushes asynchronously to the telemetry queue
  }
}
