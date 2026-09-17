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

variable "vpc_cidr" {
  type        = string
  default     = "10.0.0.0/16"
  description = "Base IPv4 CIDR block for the Percipience VPC."
}

variable "aurora_min_acu" {
  type        = number
  default     = 0.5
  description = "Minimum Aurora Capacity Units (ACU) for Serverless v2 scaling."
}

variable "aurora_max_acu" {
  type        = number
  default     = 16.0
  description = "Maximum Aurora Capacity Units (ACU) for Serverless v2 scaling."
}

variable "redis_node_type" {
  type        = string
  default     = "cache.t4g.medium"
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
