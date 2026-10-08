# -----------------------------------------------------------------------------
# AWS Network Load Balancer (NLB) for Multi-AZ Edge Ingress
# -----------------------------------------------------------------------------

resource "aws_security_group" "nlb_sg" {
  name        = "percipience-${var.environment}-nlb-sg"
  description = "Security group for external Network Load Balancer ingress"
  vpc_id      = aws_vpc.percipience_vpc.id

  ingress {
    description = "HTTPS Edge traffic from Cloudflare / Public"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP Edge redirect traffic"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "percipience-${var.environment}-nlb-sg"
  }
}

resource "aws_lb" "ingress_nlb" {
  name               = "percipience-${var.environment}-nlb"
  internal           = false
  load_balancer_type = "network"
  subnets            = aws_subnet.public[*].id

  enable_cross_zone_load_balancing = true
  enable_deletion_protection       = false

  tags = {
    Name        = "percipience-${var.environment}-nlb"
    Tier        = "Global Edge & Ingress"
    CostCenter  = "Edge-Networking"
  }
}

resource "aws_lb_target_group" "ingress_https_tg" {
  name        = "percipience-${var.environment}-tg-https"
  port        = 443
  protocol    = "TCP"
  vpc_id      = aws_vpc.percipience_vpc.id
  target_type = "ip"

  health_check {
    enabled             = true
    protocol            = "TCP"
    port                = "traffic-port"
    interval            = 10
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }

  tags = {
    Name = "percipience-${var.environment}-tg-https"
  }
}

resource "aws_lb_listener" "https_listener" {
  load_balancer_arn = aws_lb.ingress_nlb.arn
  port              = 443
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ingress_https_tg.arn
  }
}
