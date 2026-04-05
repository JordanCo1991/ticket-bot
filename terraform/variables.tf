# ============================================
# Variables — Customize your infrastructure
# ============================================

variable "aws_region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "eu-west-1"
}

variable "aws_account_id" {
  description = "AWS account ID"
  type        = string
  default     = "655506454462"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Name of the SSH key pair"
  type        = string
  default     = "ticket-bot-key"
}

variable "s3_bucket_name" {
  description = "S3 bucket name for ticket attachments"
  type        = string
  default     = "jordan-ticket-bot-tf-files"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "ticketbot"
}

variable "db_username" {
  description = "Database master username"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
}
