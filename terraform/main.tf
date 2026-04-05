# ============================================
# IT Ticket Automation Bot — Terraform
# Infrastructure as Code
# ============================================

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.7.0"
}

provider "aws" {
  region = var.aws_region
}

# --- Data Sources ---

# Get the latest Ubuntu 24.04 AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "state"
    values = ["available"]
  }
}

# --- Security Group ---

resource "aws_security_group" "ticket_bot" {
  name        = "ticket-bot-tf-sg"
  description = "Security group for IT Ticket Bot"

  # SSH
  ingress {
    description = "SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP
  ingress {
    description = "HTTP access"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Flask
  ingress {
    description = "Flask API"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Grafana
  ingress {
    description = "Grafana dashboard"
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Prometheus
  ingress {
    description = "Prometheus"
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "ticket-bot-sg"
    Project = "ticket-bot"
  }
}

# --- EC2 Instance ---

resource "aws_instance" "app_server" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.ticket_bot.id]

  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get install -y docker.io docker-compose awscli
    systemctl enable docker
    systemctl start docker

    # Create app directory
    mkdir -p /home/ubuntu/ticket-bot

    # Log in to ECR
    aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin ${var.aws_account_id}.dkr.ecr.${var.aws_region}.amazonaws.com
  EOF

  tags = {
    Name    = "ticket-bot-server"
    Project = "ticket-bot"
  }
}

# --- ECR Repository ---

resource "aws_ecr_repository" "ticket_bot" {
  name                 = "ticket-bot-tf"
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  tags = {
    Name    = "ticket-bot-ecr"
    Project = "ticket-bot"
  }
}

# --- S3 Bucket ---

resource "aws_s3_bucket" "ticket_files" {
  bucket        = var.s3_bucket_name
  force_destroy = true

  tags = {
    Name    = "ticket-bot-files"
    Project = "ticket-bot"
  }
}

# --- RDS PostgreSQL ---

resource "aws_db_instance" "postgres" {
  identifier     = "ticket-bot-tf-db"
  engine         = "postgres"
  engine_version = "16"
  instance_class = "db.t3.micro"

  allocated_storage = 20
  db_name           = var.db_name
  username          = var.db_username
  password          = var.db_password

  vpc_security_group_ids = [aws_security_group.ticket_bot.id]
  skip_final_snapshot    = true
  backup_retention_period = 0
  multi_az               = false

  tags = {
    Name    = "ticket-bot-db"
    Project = "ticket-bot"
  }
}
