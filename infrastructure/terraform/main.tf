terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# S3 Bucket
resource "aws_s3_bucket" "documents" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_public_access_block" "documents" {
  bucket = aws_s3_bucket.documents.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ECR Repository
resource "aws_ecr_repository" "app" {
  name = "document-analyzer"
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "document-analyzer-cluster"
}

# ECS Task Definition
resource "aws_ecs_task_definition" "app" {
  family                   = "document-analyzer"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512

  container_definitions = jsonencode([
    {
      name  = "document-analyzer"
      image = "${aws_ecr_repository.app.repository_url}:latest"
      
      portMappings = [
        {
          containerPort = 8501
          hostPort      = 8501
        }
      ]
      
      environment = [
        {
          name  = "AWS_REGION"
          value = var.aws_region
        }
      ]
    }
  ])
}