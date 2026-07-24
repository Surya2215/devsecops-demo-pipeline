terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

# --- Intentional demo misconfiguration, clearly labeled ---
# This bucket is deliberately left without encryption/versioning/public-access
# block configuration so the IaC scanning stage (Checkov) has something real
# to flag on the first pipeline run. Fix these before using this as a real
# template — see the corrected block commented below.
resource "aws_s3_bucket" "demo_bucket" {
  bucket = "devsecops-demo-bucket-example"
}

# --- Corrected version, for reference ---
# resource "aws_s3_bucket" "demo_bucket_secure" {
#   bucket = "devsecops-demo-bucket-example"
# }
#
# resource "aws_s3_bucket_versioning" "demo_bucket_versioning" {
#   bucket = aws_s3_bucket.demo_bucket_secure.id
#   versioning_configuration {
#     status = "Enabled"
#   }
# }
#
# resource "aws_s3_bucket_server_side_encryption_configuration" "demo_bucket_encryption" {
#   bucket = aws_s3_bucket.demo_bucket_secure.id
#   rule {
#     apply_server_side_encryption_by_default {
#       sse_algorithm = "AES256"
#     }
#   }
# }
#
# resource "aws_s3_bucket_public_access_block" "demo_bucket_public_access" {
#   bucket                  = aws_s3_bucket.demo_bucket_secure.id
#   block_public_acls       = true
#   block_public_policy     = true
#   ignore_public_acls      = true
#   restrict_public_buckets = true
# }
