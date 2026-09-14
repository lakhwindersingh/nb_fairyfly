/**
 * Infrastructure Hosting Economics & Cloud Equivalence Matrix Data
 */

export interface CloudEquivalenceRow {
  subsystem: string;
  awsAsset: string;
  gcpAsset: string;
  monthlyCost50Clients: {
    aws: number;
    gcp: number;
  };
  sizingNotes: string;
}

export const CLOUD_EQUIVALENCE_DATA: CloudEquivalenceRow[] = [
  {
    subsystem: "K8s Control Plane",
    awsAsset: "AWS EKS (K8s 1.30+ Multi-AZ)",
    gcpAsset: "Google Kubernetes Engine (GKE Multi-Zonal)",
    monthlyCost50Clients: { aws: 73, gcp: 73 },
    sizingNotes: "Cluster management fee, 4 replicas HA"
  },
  {
    subsystem: "Dynamic Worker Sandboxes",
    awsAsset: "Karpenter Spot c6i.2xlarge (gVisor runsc)",
    gcpAsset: "GKE Sandbox dynamic Spot VMs (c2-standard-8)",
    monthlyCost50Clients: { aws: 4320, gcp: 4180 },
    sizingNotes: "60% Spot / 40% On-Demand, auto-scaling microVMs"
  },
  {
    subsystem: "PostgreSQL Database",
    awsAsset: "Aurora Serverless v2 (4-32 ACUs)",
    gcpAsset: "Cloud SQL for PostgreSQL Enterprise Plus HA",
    monthlyCost50Clients: { aws: 1850, gcp: 1780 },
    sizingNotes: "Strict tenant_id Row-Level Security isolation"
  },
  {
    subsystem: "Distributed Cache",
    awsAsset: "ElastiCache Redis 7.x (cache.m6g.large)",
    gcpAsset: "Cloud Memorystore for Redis Cluster",
    monthlyCost50Clients: { aws: 420, gcp: 410 },
    sizingNotes: "Multi-AZ, sub-15ms AST symbol cache & lease locks"
  },
  {
    subsystem: "Immutable WORM Vault",
    awsAsset: "Amazon S3 Object Lock (Compliance Mode)",
    gcpAsset: "Google Cloud Storage Object Retention WORM",
    monthlyCost50Clients: { aws: 280, gcp: 260 },
    sizingNotes: "SHA-256 Merkle block proof archive for SOC 2"
  },
  {
    subsystem: "Telemetry Storage",
    awsAsset: "TimescaleDB on EBS gp3",
    gcpAsset: "TimescaleDB on Regional Hyperdisk Balanced",
    monthlyCost50Clients: { aws: 225, gcp: 215 },
    sizingNotes: "Real-time token burn and drift telemetry"
  },
  {
    subsystem: "Edge WAF & Ingress",
    awsAsset: "Cloudflare Enterprise + AWS NLB",
    gcpAsset: "Cloudflare Enterprise + GCP TCP Proxy",
    monthlyCost50Clients: { aws: 895, gcp: 850 },
    sizingNotes: "mTLS, DDoS protection, Ed25519 JWT injection"
  },
  {
    subsystem: "Observability & APM",
    awsAsset: "Datadog APM Tracing & Pod Logging",
    gcpAsset: "Google Cloud Operations Suite (Trace & Logging)",
    monthlyCost50Clients: { aws: 1150, gcp: 1050 },
    sizingNotes: "MicroVM saturation & PR gatekeeper trace analysis"
  },
  {
    subsystem: "Tier B Verification AI",
    awsAsset: "Claude 3.5 Haiku on Amazon Bedrock",
    gcpAsset: "Gemini 1.5 Flash on Vertex AI",
    monthlyCost50Clients: { aws: 3200, gcp: 3100 },
    sizingNotes: "Automated contract verification & test evaluator"
  },
  {
    subsystem: "Security & KMS Enclave",
    awsAsset: "AWS KMS CMK Key Rotation + GuardDuty",
    gcpAsset: "Cloud KMS CMEK + Security Command Center",
    monthlyCost50Clients: { aws: 767, gcp: 750 },
    sizingNotes: "Envelope encryption keys for .nbpack hydration"
  }
];

export class InfrastructureEconomicsService {
  static getCloudComparison(): CloudEquivalenceRow[] {
    return CLOUD_EQUIVALENCE_DATA;
  }

  static getHostingTotals(clients: 10 | 50 | 200) {
    if (clients === 10) {
      return {
        mrr: 45000,
        awsOpex: 3850,
        gcpOpex: 3690,
        awsGrossMarginPct: 86.8,
        gcpGrossMarginPct: 87.2,
        breakevenCustomers: 1.5
      };
    } else if (clients === 50) {
      return {
        mrr: 225000,
        awsOpex: 12980,
        gcpOpex: 12468,
        awsGrossMarginPct: 91.2,
        gcpGrossMarginPct: 91.5,
        breakevenCustomers: 1.5
      };
    } else {
      return {
        mrr: 900000,
        awsOpex: 39450,
        gcpOpex: 37830,
        awsGrossMarginPct: 94.1,
        gcpGrossMarginPct: 94.3,
        breakevenCustomers: 1.5
      };
    }
  }
}
