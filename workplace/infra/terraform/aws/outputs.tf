output "vpc_id" {
  description = "Percipience AWS VPC ID."
  value       = aws_vpc.percipience_vpc.id
}

output "eks_cluster_endpoint" {
  description = "EKS API Server Endpoint."
  value       = aws_eks_cluster.percipience_eks.endpoint
}

output "eks_cluster_name" {
  description = "EKS Cluster Name."
  value       = aws_eks_cluster.percipience_eks.name
}

output "eks_oidc_issuer_arn" {
  description = "EKS OpenID Connect Provider ARN."
  value       = aws_iam_openid_connect_provider.eks_oidc.arn
}

output "aurora_cluster_endpoint" {
  description = "Aurora PostgreSQL Serverless v2 writer endpoint."
  value       = aws_rds_cluster.percipience_aurora.endpoint
}

output "aurora_reader_endpoint" {
  description = "Aurora PostgreSQL Serverless v2 reader endpoint."
  value       = aws_rds_cluster.percipience_aurora.reader_endpoint
}

output "elasticache_redis_endpoint" {
  description = "ElastiCache Redis primary replication group endpoint."
  value       = aws_elasticache_replication_group.redis.primary_endpoint_address
}

output "s3_worm_bucket_name" {
  description = "Immutable S3 WORM Compliance Mode bucket name."
  value       = aws_s3_bucket.worm_ledger.id
}

output "s3_worm_bucket_arn" {
  description = "Immutable S3 WORM Compliance Mode bucket ARN."
  value       = aws_s3_bucket.worm_ledger.arn
}

output "kms_cmek_arn" {
  description = "Customer-Managed Encryption Key (CMEK) ARN."
  value       = aws_kms_key.percipience_cmek.arn
}
