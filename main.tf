terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
  
  required_version = ">= 1.2.0"
}

provider "aws" {
  region     = "eu-central-1"
  access_key = "insert access_key"
  secret_key = "insert secret_key"
}

# Resources are AWS services
resource "aws_iot_thing" "iot_thing" {
  name = "thing"
}

resource "aws_iot_topic_rule" "rule" {
  name        = "MyRule"
  description = "This is an example rule"
  enabled     = true
  sql         = "SELECT * FROM 'topic/test'"
  sql_version = "2016-03-23" # This is the default version automatically set by AWS
  rule_disabled = false
  
  action {
    dynamodb {
      table_name      = "my-dynamodb-table"
      role_arn        = "arn:aws:iam::123456789012:role/my-iot-role" #just an example role
      hash_key_field  = "topic"
      hash_key_value  = "${topic(2)}"
      range_key_field = "timestamp"
      range_key_value = "${timestamp()}"
    }
  }
}

resource "aws_iotevents_detector_model" "my_detector" {
  name             = "my-detector"
  role_arn         = "arn:aws:iam::123456789012:role/my-iot-role"
  detector_model_definition = <<EOF
{
  "states": {
    "state1": {
      "type": "InitialState",
      "onInput": {
        "events": [
          {
            "eventName": "my-input",
            "condition": "TRUE"
          }
        ]
      },
      "transition": {
        "nextState": "state2"
      }
    },
    "state2": {
      "type": "OnInput",
      "onInput": {
        "events": [
          {
            "eventName": "my-input",
            "condition": "TRUE"
          }
        ]
      },
      "transition": {
        "nextState": "state1"
      }
    }
  }
}
EOF
#End Of File 
}
