# -----------------------------------------------------------------------------
# Google Cloud Memorystore for Redis (Standard HA Tier)
# -----------------------------------------------------------------------------

resource "random_password" "redis_auth" {
  length  = 32
  special = false
}

resource "google_redis_instance" "percipience_redis" {
  name           = "percipience-${var.environment}-redis"
  tier           = "STANDARD_HA"
  memory_size_gb = var.redis_memory_size_gb
  region         = var.region

  authorized_network = google_compute_network.percipience_vpc.id
  connect_mode       = "PRIVATE_SERVICE_ACCESS"

  redis_version      = "REDIS_7_0"
  display_name       = "Percipience AST Cache & Ephemeral Worktree State"

  auth_enabled       = true
  transit_encryption_mode = "SERVER_AUTHENTICATION"

  maintenance_policy {
    weekly_maintenance_window {
      day = "SUNDAY"
      start_time {
        hours   = 3
        minutes = 0
        seconds = 0
        nanos   = 0
      }
    }
  }

  depends_on = [google_service_networking_connection.private_vpc_connection]
}
