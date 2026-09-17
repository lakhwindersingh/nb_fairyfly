# -----------------------------------------------------------------------------
# AWS KMS Customer-Managed Encryption Key (CMEK) with Automatic Annual Rotation
# -----------------------------------------------------------------------------

data "aws_caller_identity" "current" {}

resource "aws_kms_key" "percipience_cmek" {
  description             = "Percipience Enclave KMS Root Key for Aurora, S3 WORM, ElastiCache, and EKS Secrets"
  deletion_window_in_days = var.kms_deletion_window_in_days
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow CloudWatch Logs & AWS Services"
        Effect = "Allow"
        Principal = {
          Service = [
            "logs.${var.aws_region}.amazonaws.com",
            "rds.amazonaws.com",
            "s3.amazonaws.com",
            "elasticache.amazonaws.com"
          ]
        }
        Action = [
          "kms:Encrypt*",
          "kms:Decrypt*",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:Describe*"
        ]
        Resource = "*"
      }
    ]
  })

  tags = {
    Name = "percipience-${var.environment}-cmek"
  }
}

resource "aws_kms_alias" "percipience_cmek_alias" {
  name          = "alias/percipience-${var.environment}-cmek"
  target_key_id = aws_kms_key.percipience_cmek.key_id
}
