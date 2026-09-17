# -----------------------------------------------------------------------------
# AWS ElastiCache for Redis 7.x (Multi-AZ Replication Group)
# -----------------------------------------------------------------------------

resource "aws_elasticache_subnet_group" "redis_subnet_group" {
  name       = "percipience-${var.environment}-redis-subnet-group"
  subnet_ids = aws_subnet.database[*].id

  tags = {
    Name = "percipience-${var.environment}-redis-subnet-group"
  }
}

resource "aws_security_group" "redis_sg" {
  name        = "percipience-${var.environment}-redis-sg"
  description = "Allow inbound Redis traffic from private EKS worker nodes"
  vpc_id      = aws_vpc.percipience_vpc.id

  ingress {
    description = "Redis from Private Subnets"
    from_port   = 6379
    to_port     = 6379
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
    Name = "percipience-${var.environment}-redis-sg"
  }
}

resource "random_password" "redis_auth_token" {
  length           = 32
  special          = false
}

resource "aws_elasticache_replication_group" "redis" {
  replication_group_id          = "percipience-${var.environment}-redis"
  description                   = "Percipience AST Content-Addressable Cache & Worktree Leases"
  node_type                     = var.redis_node_type
  num_cache_clusters            = 2
  parameter_group_name          = "default.redis7"
  port                          = 6379
  subnet_group_name             = aws_elasticache_subnet_group.redis_subnet_group.name
  security_group_ids            = [aws_security_group.redis_sg.id]
  automatic_failover_enabled    = true
  multi_az_enabled              = true
  transit_encryption_enabled    = true
  at_rest_encryption_enabled    = true
  kms_key_id                    = aws_kms_key.percipience_cmek.arn
  auth_token                    = random_password.redis_auth_token.result
  snapshot_retention_limit      = 7
  snapshot_window               = "03:00-04:00"
  maintenance_window            = "sun:05:00-sun:06:00"
  auto_minor_version_upgrade    = true

  tags = {
    Name        = "percipience-${var.environment}-redis"
    Purpose     = "Distributed AST Cache & Ephemeral Worktree State"
  }
}
