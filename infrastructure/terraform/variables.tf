variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "app_name" {
  description = "Application name"
  type        = string
  default     = "document-analyzer"
}

variable "subnet_ids" {
  type        = list(string)
  description = "List of subnets for ECS tasks."
  default     = [
    "subnet-034b2070ba239b16c",
    "subnet-0aef24f578143107f"
  ]
}

variable "security_group_ids" {
  type        = list(string)
  description = "Security group(s) for ECS tasks."
  default     = []
}