provider "aws" {
  region = local.region
}

locals {
  name    = "home-budget"
  region  = "ap-southeast-2"
}

################################################################################
# RDS Module
################################################################################

resource "aws_db_instance" "home-budget" {
  identifier_prefix = local.name
  # All available versions: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html#PostgreSQL.Concepts
  engine               = "postgres"
  instance_class       = "db.t3.micro"
  allocated_storage    = 5

  # NOTE: Do NOT use 'user' as the value for 'username' as it throws:
  # "Error creating DB Instance: InvalidParameterValue: MasterUsername
  # user cannot be used as it is a reserved word used by the engine"
  db_name  = "homeBudget"
  username = "gundalai"
  port     = 5432
  publicly_accessible = true
  vpc_security_group_ids = [aws_security_group.postgres_homeBudget.id]
  manage_master_user_password   = true
}

################################################################################
# Supporting Resources
################################################################################

# Fetch the default VPC
resource "aws_default_vpc" "default" {
}

resource "aws_security_group" "postgres_homeBudget" {
  name        = "allow-all-inbound"
  description = "Security group allowing all inbound traffic"

  vpc_id = aws_default_vpc.default.id

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  // Allow traffic from any IPv4 address
  }

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]  // Allow traffic from any IPv4 address
  }

  ingress {
    from_port   = -1
    to_port     = -1
    protocol    = "icmp"
    cidr_blocks = ["0.0.0.0/0"]  // Allow ICMP traffic from any IPv4 address
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]  // Allow all outbound traffic to any IPv4 address
  }
}
