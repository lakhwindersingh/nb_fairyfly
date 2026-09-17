# -----------------------------------------------------------------------------
# Google Cloud KMS CMEK KeyRing & CryptoKey (Automated 90-Day Rotation)
# -----------------------------------------------------------------------------

resource "google_kms_key_ring" "percipience_keyring" {
  name     = "percipience-${var.environment}-keyring"
  location = var.region
}

resource "google_kms_crypto_key" "percipience_key" {
  name            = "percipience-${var.environment}-cmek"
  key_ring        = google_kms_key_ring.percipience_keyring.id
  rotation_period = "7776000s" # 90 days

  lifecycle {
    prevent_destroy = true
  }
}

# IAM bindings for Cloud SQL and GCS Service Agents
data "google_project" "project" {}

resource "google_kms_crypto_key_iam_member" "gcs_kms" {
  crypto_key_id = google_kms_crypto_key.percipience_key.id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member        = "serviceAccount:service-${data.google_project.project.number}@gs-project-accounts.iam.gserviceaccount.com"
}

resource "google_kms_crypto_key_iam_member" "cloudsql_kms" {
  crypto_key_id = google_kms_crypto_key.percipience_key.id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member        = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-cloud-sql.iam.gserviceaccount.com"
}
