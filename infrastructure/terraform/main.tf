terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

# Example VPC configuration (Commented out so it doesn't incur costs or run by default)
# module "vpc" {
#   source = "terraform-aws-modules/vpc/aws"
#   version = "5.0.0"
#   ...
# }

# This project uses local Docker Compose for development to avoid unintended cloud expenditure.
# See README.md for cloud deployment documentation.
