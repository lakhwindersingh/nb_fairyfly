# -----------------------------------------------------------------------------
# Google Cloud External TCP Proxy / Regional Load Balancer for Edge Ingress
# -----------------------------------------------------------------------------

resource "google_compute_address" "ingress_lb_ip" {
  name   = "percipience-${var.environment}-ingress-ip"
  region = var.region
}

resource "google_compute_region_health_check" "tcp_health_check" {
  name   = "percipience-${var.environment}-tcp-health-check"
  region = var.region

  tcp_health_check {
    port = 443
  }

  check_interval_sec  = 10
  timeout_sec         = 5
  healthy_threshold   = 3
  unhealthy_threshold = 3
}

resource "google_compute_region_backend_service" "ingress_backend_service" {
  name                  = "percipience-${var.environment}-ingress-backend"
  region                = var.region
  protocol              = "TCP"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  health_checks         = [google_compute_region_health_check.tcp_health_check.id]

  connection_draining_timeout_sec = 60
}

resource "google_compute_forwarding_rule" "tcp_forwarding_rule" {
  name                  = "percipience-${var.environment}-tcp-forwarding-rule"
  region                = var.region
  ip_address            = google_compute_address.ingress_lb_ip.address
  ip_protocol           = "TCP"
  port_range            = "443"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  backend_service       = google_compute_region_backend_service.ingress_backend_service.id
  network               = google_compute_network.percipience_vpc.id
  subnetwork            = google_compute_subnetwork.gke_subnet.id
}
