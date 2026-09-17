# -----------------------------------------------------------------------------
# Google Cloud Storage WORM Bucket (Immutable Compliance Retention)
# -----------------------------------------------------------------------------

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "google_storage_bucket" "worm_ledger" {
  name                        = "percipience-${var.environment}-worm-ledger-${random_id.bucket_suffix.hex}"
  location                    = var.region
  force_destroy               = false
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  retention_policy {
    is_locked        = true
    retention_period = var.retention_period_days * 86400
  }

  encryption {
    default_kms_key_name = google_kms_crypto_key.percipience_key.id
  }

  labels = {
    env        = var.environment
    compliance = "worm_sec17a4"
  }

  depends_on = [google_kms_crypto_key_iam_member.gcs_kms]
}
