# TEST FILE - Security scanner validation only. DO NOT use in production.
# Purpose: Trigger Aikido IaC scanner with public S3 bucket and open SSH.

# IaC trigger #1: S3 bucket with public-read ACL
resource "aws_s3_bucket" "test_bucket" {
  bucket = "aikido-iac-validation-bucket"
  acl    = "public-read"
}

# IaC trigger #2: Security group with SSH open to the world
resource "aws_security_group" "test_sg" {
  name = "aikido-iac-validation-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
