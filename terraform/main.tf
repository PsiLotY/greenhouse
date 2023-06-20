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
  source = "./Thing"

  # Pass any required variables to the module
  thing_name        = "terra_thing"
  thing_attributes  = {
    arn = "arn:aws:iam::aws:policy/service-role/AWSIoTThingsRegistration"
  }
  providers = {
    aws = aws
  }
  region = "eu-central-1"
}

module "events" {
  source = "./Events"
  providers ={
    awscc = awscc
  }
}


module "timestream" {
  source = "./Timestream"

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



# terraform {
#   required_providers {
#     aws = {
#       source  = "hashicorp/aws"
#       version = "~> 4.16"
#     }
#   }
  
#   required_version = ">= 1.2.0"
# }

# provider "aws" {
#   region     = "eu-central-1"
#   access_key = "insert access_key"    #insert access key
#   secret_key = "insert secret_key"    #insert secret key
# }

# # Resources are AWS services
# resource "aws_iot_thing" "iot_thing" {
#   name = "thing"
# }

resource "aws_iot_topic_rule" "rule" {
  name        = "MyRule"
  description = "This is an example rule"
  enabled     = true
  sql         = "SELECT * FROM 'topic/test'"
  sql_version = "2016-03-23"
}

# # Call the thing module
# module "thing" {
#   source = "./thing"

#   # Pass any required variables to the module
#   thing_name = "my-thing"
# }


# resource "aws_iot_topic_rule" "rule" {
#   name        = "MyRule"
#   description = "This is an example rule"
#   enabled     = true
#   sql         = "SELECT * FROM 'topic/test'"
#   sql_version = "2016-03-23" # This is the default version automatically set by AWS
#   rule_disabled = false
# }

# variable "tables" {
#   default = [
#     "Antti's Rasp",
#     "Hannes' Rasp",
#     "Anjo's Rasp",
#     "Elisa's Rasp",
#     "Isaac's Rasp",
#     "Firaz's Rasp"
#   ]
# }

# resource "aws_dynamodb_table" "iot_data" {
#   count          = length(var.tables)
#   name           = var.tables[count.index]
#   billing_mode   = "PAY_PER_REQUEST"
#   hash_key       = "device_id"
#   stream_enabled = true
#   stream_view_type = "NEW_AND_OLD_IMAGES"

#   attribute {
#     name = "device_id"
#     type = "S"                        # Replace with your desired attribute type (e.g., "S" for string, "N" for number)
#   }
#   attribute {
#     name = "timestamp"
#     type = "S"
#   }
#   attribute {
#     name = "temperature"
#     type = "N"
#   }
#   attribute {
#     name = "air_quality"
#     type = "N"
#   }
#   attribute {
#     name = "humidity"
#     type = "N"
#   }
#   attribute {
#     name = "light_exposure"
#     type = "N"
#   }

#   ttl {
#     attribute_name = "ttl"
#     enabled        = true
#   }

#   global_secondary_index {
#     name               = "timestamp-index"
#     hash_key           = "timestamp"
#     projection_type    = "ALL"
#     read_capacity      = 5
#     write_capacity     = 5
#     non_key_attributes = ["temperature", "air_quality", "pressure"]
#   }

#   # Add more attribute blocks as needed

#   # Define global secondary indexes (if required)
#   # Example:
#   # global_secondary_index {
#   #   name               = "example_gsi"
#   #   hash_key           = "gsi_hash_key"
#   #   range_key          = "gsi_range_key"
#   #   read_capacity      = 5
#   #   write_capacity     = 5
#   #   projection_type    = "ALL"     # Set the projection type (e.g., "ALL", "INCLUDE", "KEYS_ONLY")
#   # }
# }

# resource "aws_iotevents_detector_model" "my_detector" {
#   name             = "my-detector"
#   role_arn         = "arn:aws:iam::123456789012:role/my-iot-role"
#   detector_model_definition = <<EOF
# {
#   "states": {
#     "state1": {
#       "type": "InitialState",
#       "onInput": {
#         "events": [
#           {
#             "eventName": "my-input",
#             "condition": "TRUE"
#           }
#         ]
#       },
#       "transition": {
#         "nextState": "state2"
#       }
#     },
#     "state2": {
#       "type": "OnInput",
#       "onInput": {
#         "events": [
#           {
#             "eventName": "my-input",
#             "condition": "TRUE"
#           }
#         ]
#       },
#       "transition": {
#         "nextState": "state1"
#       }
#     }
#   }
# }
# EOF
# #End Of File 
# }
