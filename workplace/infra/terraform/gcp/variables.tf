variable "project_id" {
  type        = string
  description = "GCP Project ID."
  default     = "percipience-enterprise-prod"
}

variable "region" {
  type        = string
  default     = "us-central1"
  description = "Target GCP deployment region."
}

variable "environment" {
  type        = string
  default     = "prod"
  description = "Target environment (dev, staging, prod)."
}

variable "cluster_name" {
  type        = string
  default     = "percipience-gke-cluster"
  description = "Name for the regional GKE Autopilot / Sandbox cluster."
}

variable "gke_version" {
  type        = string
  default     = "1.30"
  description = "Target Kubernetes release channel / minor version for GKE."
}

variable "subnet_cidr" {
  type        = string
  default     = "10.10.0.0/20"
  description = "Primary CIDR range for GKE Nodes subnet."
}

variable "pods_cidr" {
  type        = string
  default     = "10.20.0.0/16"
  description = "Secondary CIDR range for GKE Pods."
}

variable "services_cidr" {
  type        = string
  default     = "10.30.0.0/20"
  description = "Secondary CIDR range for GKE Services."
}

variable "db_tier" {
  type        = string
  default     = "db-custom-4-32768"
  description = "Cloud SQL machine tier for PostgreSQL 16 Enterprise Plus (4 vCPU, 32 GiB RAM for 50-client growth milestone)."
}

variable "sandbox_machine_type" {
  type        = string
  default     = "c2-standard-8"
  description = "Machine type for GKE Sandbox gVisor agent worker nodes (c2-standard-8 Spot VMs)."
}

variable "redis_memory_size_gb" {
  type        = number
  default     = 5
  description = "Memory capacity in GB for Cloud Memorystore Redis."
}

variable "retention_period_days" {
  type        = number
  default     = 365
  description = "Retention lock duration in days for GCS WORM bucket object retention."
}

variable "timescaledb_disk_size_gb" {
  type        = number
  default     = 500
  description = "Regional Hyperdisk Balanced capacity for TimescaleDB telemetry engine on GKE."
}
