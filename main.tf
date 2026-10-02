# TEST FILE ONLY — Deliberate IaC misconfigurations for Aikido IaC scanner validation.
# Public S3 bucket and open SSH port included intentionally. DO NOT USE IN PRODUCTION.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# IaC trigger 1: S3 bucket with public-read ACL
resource "aws_s3_bucket" "test_bucket" {
  bucket = "aikido-iac-test-bucket"
  acl    = "public-read"
}

resource "aws_s3_bucket_public_access_block" "test_bucket" {
  bucket = aws_s3_bucket.test_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# IaC trigger 2: Security group with SSH open to the world
resource "aws_security_group" "test_sg" {
  name        = "aikido-iac-test-sg"
  description = "Test security group for Aikido IaC scanner validation"

  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
