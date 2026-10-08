# -----------------------------------------------------------------------------
# AWS TimescaleDB Telemetry Storage (EBS gp3 with KMS CMEK Encryption)
# -----------------------------------------------------------------------------

resource "aws_ebs_volume" "timescaledb_data" {
  availability_zone = local.azs[0]
  size              = var.timescaledb_disk_size_gb
  type              = "gp3"
  iops              = 3000
  throughput        = 125
  encrypted         = true
  kms_key_id        = aws_kms_key.percipience_cmek.arn

  tags = {
    Name        = "percipience-${var.environment}-timescaledb-telemetry"
    Subsystem   = "Telemetry & Timeseries Storage"
    Purpose     = "Real-time token burn, drift metrics, and Merkle DAG visualizer"
    CostCenter  = "Observability"
  }
}
