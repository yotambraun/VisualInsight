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

# ---------------------------------------
# 1. S3 Bucket (no public access block here, or remove policy)
# ---------------------------------------
resource "aws_s3_bucket" "documents" {
  bucket = var.bucket_name
}

/*
  If you truly need a public policy with Principal = "*", you must either
  remove "Block Public Access" at the account/bucket level,
  or remove the public policy resource below.
  
  Alternatively, remove the entire aws_s3_bucket_policy resource if
  you do NOT want/need a publicly readable bucket.
*/

# Comment this out or remove entirely if you don't need public read:
# resource "aws_s3_bucket_policy" "documents" {
#   bucket = aws_s3_bucket.documents.id

#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Sid       = "AllowGetObject"
#         Effect    = "Allow"
#         Principal = "*"
#         Action    = "s3:GetObject"
#         Resource  = "${aws_s3_bucket.documents.arn}/*"
#       }
#     ]
#   })
# }


# ---------------------------------------
# 2. ECR Repository
# ---------------------------------------
resource "aws_ecr_repository" "app" {
  name = "document-analyzer"
}

# ---------------------------------------
# 3. ECS Cluster
# ---------------------------------------
resource "aws_ecs_cluster" "main" {
  name = "document-analyzer-cluster"
}

# ---------------------------------------
# 4. IAM Role for ECS Task Execution
# ---------------------------------------
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecs-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# ---------------------------------------
# 5. ECS Task Definition
# ---------------------------------------
resource "aws_ecs_task_definition" "app" {
  family                   = "document-analyzer"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn

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

# ---------------------------------------
# 6. Security Group for ECS
# ---------------------------------------
resource "aws_security_group" "ecs_sg" {
  name        = "ecs-service-sg"
  description = "Security group for ECS Fargate tasks"
  vpc_id      = "vpc-0c39ffe1c5dbcd319"  # Must match subnets' VPC

  # Allow inbound to port 8501 (Streamlit)
  ingress {
    description = "Allow Streamlit inbound"
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound to anywhere
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ecs-service-sg"
  }
}

# ---------------------------------------
# 7. ECS Service
# ---------------------------------------
resource "aws_ecs_service" "app" {
  name            = "document-analyzer"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.subnet_ids
    # Directly reference the SG we just created:
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }

  deployment_controller {
    type = "ECS"
  }
}
