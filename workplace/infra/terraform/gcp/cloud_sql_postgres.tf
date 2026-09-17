# -----------------------------------------------------------------------------
# Google Cloud SQL for PostgreSQL 16 Enterprise Plus HA
# -----------------------------------------------------------------------------

resource "random_password" "cloudsql_password" {
  length  = 32
  special = true
}

resource "google_sql_database_instance" "percipience_db" {
  name             = "percipience-${var.environment}-pg16"
  database_version = "POSTGRES_16"
  region           = var.region
  encryption_key_name = google_kms_crypto_key.percipience_key.id
  deletion_protection = true

  settings {
    tier                        = var.db_tier
    edition                     = "ENTERPRISE_PLUS"
    availability_type           = "REGIONAL"
    disk_type                   = "PD_SSD"
    disk_size                   = 100
    disk_autoresize             = true
    disk_autoresize_limit       = 1000

    ip_configuration {
      ipv4_enabled                                  = false
      private_network                               = google_compute_network.percipience_vpc.id
      enable_private_path_for_google_cloud_services = true
    }

    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      start_time                     = "02:00"
      transaction_log_retention_days = 14
    }

    database_flags {
      name  = "rds.force_ssl"
      value = "on"
    }

    database_flags {
      name  = "log_connections"
      value = "on"
    }

    database_flags {
      name  = "log_disconnections"
      value = "on"
    }

    insights_config {
      query_insights_enabled  = true
      query_string_length     = 1024
      record_application_tags = true
      record_client_address   = false
    }
  }

  depends_on = [
    google_service_networking_connection.private_vpc_connection,
    google_kms_crypto_key_iam_member.cloudsql_kms
  ]
}

resource "google_sql_database" "database" {
  name     = "percipience_db"
  instance = google_sql_database_instance.percipience_db.name
}

resource "google_sql_user" "admin_user" {
  name     = "percipience_admin"
  instance = google_sql_database_instance.percipience_db.name
  password = random_password.cloudsql_password.result
}
