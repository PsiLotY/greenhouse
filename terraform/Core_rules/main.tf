

resource "aws_iot_topic_rule" "example_rule" {
  name        = "example-rule"
  description = "Example IoT Core rule"

  sql = "SELECT * FROM 'my/topic'"

  actions {
    republish {
      topic = "processed/topic"
    }
  }
}




