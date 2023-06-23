terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
    awscc = {
      source  = "hashicorp/awscc"
      version = ">= 0.5.0"
    }
  }
  required_version = ">= 1.2.0"
}

# Define your AWS provider configuration
provider "aws" {
  region = "eu-central-1"  # Update with your desired region
  access_key = var.access_key 
  secret_key = var.secret_key 
}

provider "awscc" {
  region     = "eu-central-1"
  access_key = var.access_key 
  secret_key = var.secret_key 
}


# Call the thing module
module "thing" {
  source = "./thing"

  # Pass any required variables to the module
  thing_name        = "terra_thing"
  thing_attributes  = {
    arn = aws_iam_role.core_role.arn
  }
  providers = {
    aws = aws
  }
  region = "eu-central-1"
}

module "events" {
  source = "./events"
  providers ={
    awscc = awscc
  }

  arn = aws_iam_role.core_role.arn
}


module "timestream" {
  source = "./timestream"

  # Pass any required variables to the module
  database_name = "terra_database"
  table_name  = "terra_table"
  providers = {
    aws = aws
  }
  region = "eu-central-1"
}

module "lambda" {
  source = "./lambda"
}
