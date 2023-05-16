terraform {
    required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

providers {
  aws = {
    region  = "eu-central-1"
    access_key = "insert access_key"
    secret_key = "insert secret_key"
  }
}

#Resources are AWS services
resource "aws_iot_thing" "iot_thing" {
name = "thing"
}

resource "aws_iot_topic_rule" "rule" {
  name        = "MyRule"
  description = "This is an example rule"
  enabled     = true
  sql         = "SELECT * FROM 'topic/test'"
  sql_version = "2016-03-23" #this is the default version automatically set by AWS
  rule_disabled = false
  #The rule sends all data from the topic "topic/test" to dynamoDB
    "actions": [{
      "dynamoDB": {
          "tableName": "my-dynamodb-table",
          "roleArn": "arn:aws:iam::123456789012:role/my-iot-role",
          "hashKeyField": "topic",
          "hashKeyValue": "${topic(2)}",
          "rangeKeyField": "timestamp",
          "rangeKeyValue": "${timestamp()}"
      }
  }]
}
resource "aws_iotevents_detector_model" "my_detector"  {

}
