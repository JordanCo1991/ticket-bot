# ============================================
# Outputs — What Terraform shows after apply
# ============================================

output "ec2_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.app_server.public_ip
}

output "rds_endpoint" {
  description = "RDS PostgreSQL endpoint"
  value       = aws_db_instance.postgres.endpoint
}

output "ecr_repository_url" {
  description = "ECR repository URL"
  value       = aws_ecr_repository.ticket_bot.repository_url
}

output "s3_bucket" {
  description = "S3 bucket name"
  value       = aws_s3_bucket.ticket_files.bucket
}
