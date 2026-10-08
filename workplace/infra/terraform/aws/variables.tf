variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "Target AWS deployment region."
}

variable "environment" {
  type        = string
  default     = "prod"
  description = "Target deployment environment (dev, staging, prod)."
}

variable "cluster_name" {
  type        = string
  default     = "percipience-cluster"
  description = "Identifier for the EKS Cluster and Karpenter discovery tags."
}

variable "eks_version" {
  type        = string
  default     = "1.30"
  description = "Kubernetes control plane version for EKS."
}

variable "vpc_cidr" {
  type        = string
  default     = "10.0.0.0/16"
  description = "Base IPv4 CIDR block for the Percipience VPC."
}

variable "aurora_min_acu" {
  type        = number
  default     = 4.0
  description = "Minimum Aurora Capacity Units (ACU) for Serverless v2 scaling (4.0 ACU for 50-client growth milestone)."
}

variable "aurora_max_acu" {
  type        = number
  default     = 32.0
  description = "Maximum Aurora Capacity Units (ACU) for Serverless v2 scaling (32.0 ACU peak)."
}

variable "redis_node_type" {
  type        = string
  default     = "cache.m6g.large"
  description = "Node instance type for the multi-AZ ElastiCache Redis replication group."
}

variable "kms_deletion_window_in_days" {
  type        = number
  default     = 30
  description = "Key deletion waiting period in days for CMEK destruction prevention."
}

variable "retention_period_days" {
  type        = number
  default     = 365
  description = "Retention lock duration in days for S3 WORM Compliance Mode object locking."
}

variable "timescaledb_disk_size_gb" {
  type        = number
  default     = 500
  description = "Dedicated EBS gp3 volume capacity for TimescaleDB telemetry engine."
}
