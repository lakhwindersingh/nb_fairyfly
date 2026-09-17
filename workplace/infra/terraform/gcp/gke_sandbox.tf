# -----------------------------------------------------------------------------
# Google Kubernetes Engine (GKE) Enterprise Cluster with GVisor Sandbox Isolation
# -----------------------------------------------------------------------------

resource "google_service_account" "gke_sa" {
  account_id   = "percipience-${var.environment}-gke-sa"
  display_name = "Percipience GKE Node Service Account"
}

resource "google_project_iam_member" "gke_sa_log_writer" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.gke_sa.email}"
}

resource "google_project_iam_member" "gke_sa_metric_writer" {
  project = var.project_id
  role    = "roles/monitoring.metricWriter"
  member  = "serviceAccount:${google_service_account.gke_sa.email}"
}

resource "google_container_cluster" "percipience_gke" {
  name     = var.cluster_name
  location = var.region

  network    = google_compute_network.percipience_vpc.id
  subnetwork = google_compute_subnetwork.gke_subnet.id

  # We manage node pools separately
  remove_default_node_pool = true
  initial_node_count       = 1

  ip_allocation_policy {
    cluster_secondary_range_name  = "gke-pods"
    services_secondary_range_name = "gke-services"
  }

  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  release_channel {
    channel = "REGULAR"
  }

  database_encryption {
    state    = "ENCRYPTED"
    key_name = google_kms_crypto_key.percipience_key.id
  }

  addons_config {
    http_load_balancing {
      disabled = false
    }
    gce_persistent_disk_csi_driver_config {
      enabled = true
    }
  }

  lifecycle {
    ignore_changes = [initial_node_count]
  }
}

# System Nodes Pool (Control Plane, Core Ingress, Routing)
resource "google_container_node_pool" "system_nodes" {
  name       = "system-nodes-pool"
  location   = var.region
  cluster    = google_container_cluster.percipience_gke.name
  node_count = 1

  autoscaling {
    min_node_count = 1
    max_node_count = 3
  }

  node_config {
    machine_type = "e2-standard-4"
    disk_size_gb = 50
    disk_type    = "pd-standard"

    service_account = google_service_account.gke_sa.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    labels = {
      role = "system-control"
    }

    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }
  }
}

# Sandboxed Worker Nodes (gVisor Isolated for Ephemeral Agent Worktrees)
resource "google_container_node_pool" "sandbox_nodes" {
  name       = "sandbox-agent-pool"
  location   = var.region
  cluster    = google_container_cluster.percipience_gke.name
  node_count = 1

  autoscaling {
    min_node_count = 1
    max_node_count = 10
  }

  node_config {
    machine_type = "c3-standard-4"
    disk_size_gb = 100
    disk_type    = "pd-ssd"
    spot         = true

    sandbox_config {
      type = "gvisor"
    }

    service_account = google_service_account.gke_sa.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    labels = {
      "percipience.io/workload" = "ephemeral-agent-worktree"
      "sandbox.gke.io/runtime"  = "gvisor"
    }

    taint {
      key    = "percipience.io/untrusted-agent"
      value  = "true"
      effect = "NO_SCHEDULE"
    }

    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }
  }
}
