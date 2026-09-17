# -----------------------------------------------------------------------------
# Immutable S3 WORM Storage (Object Lock in COMPLIANCE Mode)
# -----------------------------------------------------------------------------

resource "aws_s3_bucket" "worm_ledger" {
  bucket        = "percipience-${var.environment}-worm-ledger-${data.aws_caller_identity.current.account_id}"
  force_destroy = false

  object_lock_enabled = true

  tags = {
    Name        = "percipience-${var.environment}-worm-ledger"
    Purpose     = "Immutable Merkle DAG Chain & Cryptographic Epoch Archives"
    Compliance  = "SEC Rule 17a-4 / FINRA / SOC2"
  }
}

resource "aws_s3_bucket_versioning" "worm_ledger_versioning" {
  bucket = aws_s3_bucket.worm_ledger.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_object_lock_configuration" "worm_lock_config" {
  bucket = aws_s3_bucket.worm_ledger.id

  rule {
    default_retention {
      mode = "COMPLIANCE"
      days = var.retention_period_days
    }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "worm_encryption" {
  bucket = aws_s3_bucket.worm_ledger.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.percipience_cmek.arn
      sse_algorithm     = "aws:kms"
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "worm_block_public" {
  bucket = aws_s3_bucket.worm_ledger.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "enforce_tls" {
  bucket = aws_s3_bucket.worm_ledger.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "EnforceTLSRequestsOnly"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource = [
          aws_s3_bucket.worm_ledger.arn,
          "${aws_s3_bucket.worm_ledger.arn}/*"
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      }
    ]
  })
}
