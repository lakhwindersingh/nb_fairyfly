terraform {
  required_version = ">= 1.7.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.20"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.20"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

# -----------------------------------------------------------------------------
# VPC Network & Cloud NAT
# -----------------------------------------------------------------------------

resource "google_compute_network" "percipience_vpc" {
  name                    = "percipience-${var.environment}-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "gke_subnet" {
  name                     = "percipience-${var.environment}-gke-subnet"
  ip_cidr_range            = var.subnet_cidr
  region                   = var.region
  network                  = google_compute_network.percipience_vpc.id
  private_ip_google_access = true

  secondary_ip_range {
    range_name    = "gke-pods"
    ip_cidr_range = var.pods_cidr
  }

  secondary_ip_range {
    range_name    = "gke-services"
    ip_cidr_range = var.services_cidr
  }
}

resource "google_compute_router" "nat_router" {
  name    = "percipience-${var.environment}-router"
  region  = var.region
  network = google_compute_network.percipience_vpc.id
}

resource "google_compute_router_nat" "cloud_nat" {
  name                               = "percipience-${var.environment}-nat"
  router                             = google_compute_router.nat_router.name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}

# Private Service Access for Cloud SQL & Cloud Memorystore
resource "google_compute_global_address" "private_ip_alloc" {
  name          = "percipience-${var.environment}-private-ip"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.percipience_vpc.id
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.percipience_vpc.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_alloc.name]
}
