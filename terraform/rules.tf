resource "aws_iot_topic_rule" "iot_rule" {
  name        = "iot_rule"
  description = "Testing whether the rule works with iotevents"
  enabled     = true
  sql_version = "2016-03-23"
  sql = "SELECT * FROM 'iot/sensor_data'"
  iot_events {
    input_name = "device_input"
    role_arn = aws_iam_role.core_role.arn
  }
  iot_events {
    input_name = "device_input2"
    role_arn = aws_iam_role.core_role.arn
  }
  iot_events {
    input_name = "device_input3"
    role_arn = aws_iam_role.core_role.arn
  }
  #TODO only for debugging remove this later
  republish {
    role_arn = aws_iam_role.core_role.arn
    topic = "iot/debugging"
  }
  error_action {
    republish {
      role_arn = aws_iam_role.core_role.arn
      topic = "iot/error"
    }
  }
}

resource "aws_iot_topic_rule" "timestream_routing" {
  name = "timestream_routing"
  description = "Test rule to write data to timestream"
  enabled = true
  sql_version = "2016-03-23"
  sql = "SELECT * FROM 'message_test'"
  timestream {
    database_name = "sensorDataDB"
    table_name = "sensorDataTable"
    dimension {
      name = "deviceId"
      value = "${uuid()}"
    }
    role_arn = aws_iam_role.core_role.arn
  }
}




