/**
 * Infrastructure Bridge Abstraction Layer
 * Allows SaaS Portal to share core infrastructure at launch and decouple seamlessly later.
 */

export interface IInfraBridge {
  getDatabaseConnection(tenantId: string): Promise<string>;
  getCacheNamespace(tenantId: string): string;
  getWormVaultPrefix(tenantId: string): string;
}

export class SharedInfraBridge implements IInfraBridge {
  private mode: "shared_co_located" | "decoupled_dedicated";

  constructor(mode: "shared_co_located" | "decoupled_dedicated" = "shared_co_located") {
    this.mode = mode;
  }

  async getDatabaseConnection(tenantId: string): Promise<string> {
    if (this.mode === "shared_co_located") {
      // Shared Aurora PostgreSQL pool with tenant schema / RLS
      return `postgresql://shared_pool/percipience?options=-c%20search_path=tenant_${tenantId}`;
    }
    // Decoupled dedicated RDS / Neon connection
    return `postgresql://dedicated_${tenantId}:secret@rds.vpc.internal/db`;
  }

  getCacheNamespace(tenantId: string): string {
    return `tenant:${tenantId}:`;
  }

  getWormVaultPrefix(tenantId: string): string {
    return `vaults/${tenantId}/`;
  }
}
