# -----------------------------------------------------------------------------
# Google Cloud TimescaleDB Telemetry Storage (Regional Disk with CMEK Encryption)
# -----------------------------------------------------------------------------

resource "google_compute_region_disk" "timescaledb_disk" {
  name                      = "percipience-${var.environment}-timescaledb-disk"
  type                      = "pd-balanced"
  region                    = var.region
  size                      = var.timescaledb_disk_size_gb
  replica_zones             = ["${var.region}-a", "${var.region}-b"]

  disk_encryption_key {
    kms_key_name = google_kms_crypto_key.percipience_key.id
  }

  labels = {
    subsystem  = "telemetry-storage"
    compliance = "soc2_type2"
    env        = var.environment
  }
}
