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