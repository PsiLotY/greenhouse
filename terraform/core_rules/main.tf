resource "aws_iot_topic_rule" "test_rule" {
  name        = "test_rule"
  description = "Testing whether the rule works with iotevents"
  enabled     = true
  sql_version = "2016-03-23"
  sql = "SELECT * FROM message_test WHERE sensor_data.temperature <> null"
  iot_events {
    input_name = "device_input"
    role_arn = "arn:aws:iam::413812240765:role/service-role/IoTCoreRole"
  }
}

/*
resource "aws_iam_role" "example" {
  name = "iot_timestream_role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "iot.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "example" {
  role       = aws_iam_role.example.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonTimestreamFullAccess"
}


#rule that listens to the topic and writes down if something comes up
#has a connection to the timestream database
#rule needs to specify the table which data is to be sent

resource "aws_iot_topic_rule" "send_to_timestream" {
  name        = "send_to_timestream_rule"
  description = "Rule to send MQTT messages to Timestream"
  sql = "SELECT * FROM 'my/mqtt/topic'"  # Replace with your desired MQTT topic

  aws_iot_sql_version = "2016-03-23"

  actions {
    timestream_put_record {
      role_arn             = aws_iam_role.mqtt_to_timestream_role.arn
      database_name        = aws_timestreamwrite_database.my_database.database_name  # Replace with your Timestream database name
      table_name           = var.table_name  # Replace with your Timestream table name
      timestamp            = "${timestamp()}"
      dimensions           = {
        "deviceId" = "${new_guid()}"  # Replace with your desired dimension values
      }
      measure_name         = "payload"
      measure_value        = "${rule_payload()}"
      measure_value_type   = "STRING"
      measure_value_format = "RAW"
    }
  }
}

#Q: Are the variables created already? If so, what are the names?
#Q: 

resource "aws_iam_role" "mqtt_to_timestream_role" {
  name = "mqtt_to_timestream_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "iot.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}*/




