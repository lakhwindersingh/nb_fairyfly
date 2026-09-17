output "vpc_id" {
  description = "Percipience GCP VPC network ID."
  value       = google_compute_network.percipience_vpc.id
}

output "gke_cluster_endpoint" {
  description = "Regional GKE Cluster endpoint."
  value       = google_container_cluster.percipience_gke.endpoint
}

output "gke_cluster_name" {
  description = "Regional GKE Cluster name."
  value       = google_container_cluster.percipience_gke.name
}

output "cloud_sql_connection_name" {
  description = "Cloud SQL PostgreSQL 16 Enterprise Plus instance connection name."
  value       = google_sql_database_instance.percipience_db.connection_name
}

output "cloud_sql_private_ip" {
  description = "Cloud SQL private IP address."
  value       = google_sql_database_instance.percipience_db.private_ip_address
}

output "memorystore_redis_host" {
  description = "Cloud Memorystore Redis primary host."
  value       = google_redis_instance.percipience_redis.host
}

output "memorystore_redis_port" {
  description = "Cloud Memorystore Redis port."
  value       = google_redis_instance.percipience_redis.port
}

output "gcs_worm_bucket_name" {
  description = "Immutable GCS WORM Object Retention bucket name."
  value       = google_storage_bucket.worm_ledger.name
}

output "kms_cryptokey_id" {
  description = "Google Cloud KMS CMEK CryptoKey ID."
  value       = google_kms_crypto_key.percipience_key.id
}
