# -----------------------------------------------------------------------------
# AWS Aurora PostgreSQL Serverless v2 Cluster (Multi-AZ & Row-Level Security)
# -----------------------------------------------------------------------------

resource "aws_db_subnet_group" "aurora_subnet_group" {
  name       = "percipience-${var.environment}-aurora-subnet-group"
  subnet_ids = aws_subnet.database[*].id

  tags = {
    Name = "percipience-${var.environment}-aurora-subnet-group"
  }
}

resource "aws_security_group" "aurora_sg" {
  name        = "percipience-${var.environment}-aurora-sg"
  description = "Allow inbound PostgreSQL traffic from private EKS worker nodes"
  vpc_id      = aws_vpc.percipience_vpc.id

  ingress {
    description = "PostgreSQL from Private Subnets"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = aws_subnet.private[*].cidr_block
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "percipience-${var.environment}-aurora-sg"
  }
}

resource "aws_rds_cluster_parameter_group" "aurora_pg_params" {
  name        = "percipience-${var.environment}-aurora-pg16-params"
  family      = "aurora-postgresql16"
  description = "Percipience Parameter Group enforcing RLS, SSL, and connection pooling"

  parameter {
    name  = "rds.force_ssl"
    value = "1"
  }

  parameter {
    name  = "log_connections"
    value = "1"
  }

  parameter {
    name  = "log_disconnections"
    value = "1"
  }

  parameter {
    name  = "shared_preload_libraries"
    value = "pg_stat_statements"
  }
}

resource "random_password" "db_master_password" {
  length           = 32
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_rds_cluster" "percipience_aurora" {
  cluster_identifier          = "percipience-${var.environment}-aurora"
  engine                      = "aurora-postgresql"
  engine_mode                 = "provisioned"
  engine_version              = "16.1"
  database_name               = "percipience_db"
  master_username             = "percipience_admin"
  master_password             = random_password.db_master_password.result
  db_subnet_group_name        = aws_db_subnet_group.aurora_subnet_group.name
  vpc_security_group_ids      = [aws_security_group.aurora_sg.id]
  db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.aurora_pg_params.name
  kms_key_id                  = aws_kms_key.percipience_cmek.arn
  storage_encrypted           = true
  deletion_protection         = true
  backup_retention_period     = 30
  preferred_backup_window     = "02:00-03:00"
  preferred_maintenance_window = "sun:04:00-sun:05:00"
  copy_tags_to_snapshot       = true
  allow_major_version_upgrade = false

  serverlessv2_scaling_configuration {
    min_capacity = var.aurora_min_acu
    max_capacity = var.aurora_max_acu
  }

  tags = {
    Name        = "percipience-${var.environment}-aurora-cluster"
    Architecture = "Multi-Tenant RLS Control Plane"
  }
}

resource "aws_rds_cluster_instance" "aurora_instances" {
  count               = 2
  identifier          = "percipience-${var.environment}-aurora-instance-${count.index + 1}"
  cluster_identifier  = aws_rds_cluster.percipience_aurora.id
  instance_class      = "db.serverless"
  engine              = aws_rds_cluster.percipience_aurora.engine
  engine_version      = aws_rds_cluster.percipience_aurora.engine_version
  db_subnet_group_name = aws_db_subnet_group.aurora_subnet_group.name
  publicly_accessible = false
  monitoring_interval = 60
  auto_minor_version_upgrade = true

  tags = {
    Name = "percipience-${var.environment}-aurora-node-${count.index + 1}"
  }
}
