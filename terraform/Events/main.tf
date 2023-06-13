# Read the contents of the testModel.json file
data "local_file" "test_model" {
  filename = "../detectorModels/testModel.json"  # Replace with the actual path to your file
}

# Create an IoT Events detector model
resource "aws_iotevents_detector_model" "greenhouse_detector" {
  name                      = "greenhouse-detector"
  detector_model_definition = data.local_file.test_model.content
}

# Create an IoT Events input
resource "aws_iotevents_input" "greenhouse_input" {
  name               = "greenhouse-input"
  input_definition   = <<EOF
    {
      "temperature": "DOUBLE",
      "humidity": "DOUBLE",
      "air_pressure": "DOUBLE",
      "open_window": "BOOLEAN",
      "light_switch": "BOOLEAN"
    }
  EOF
}

# Create an IoT Events rule for temperature
resource "aws_iotevents_rule" "temperature_rule" {
  name                      = "temperature-rule"
  detector_model_name       = aws_iotevents_detector_model.greenhouse_detector.name
  state                     = "ENABLED"
  description               = "Temperature rule"
  action {
    iot_topic_publish {
      mqtt_topic = "temperature-topic"
    }
  }
  rule_condition {
    numeric {
      variable    = "temperature"
      comparison  = "GREATER_THAN"
      threshold   = 30
    }
  }
}

# Create an IoT Events rule for humidity
resource "aws_iotevents_rule" "humidity_rule" {
  name                      = "humidity-rule"
  detector_model_name       = aws_iotevents_detector_model.greenhouse_detector.name
  state                     = "ENABLED"
  description               = "Humidity rule"
  action {
    iot_topic_publish {
      mqtt_topic = "humidity-topic"
    }
  }
  rule_condition {
    numeric {
      variable    = "humidity"
      comparison  = "GREATER_THAN"
      threshold   = 80
    }
  }
}

# Create an IoT Events rule for air pressure
resource "aws_iotevents_rule" "air_pressure_rule" {
  name                      = "air-pressure-rule"
  detector_model_name       = aws_iotevents_detector_model.greenhouse_detector.name
  state                     = "ENABLED"
  description               = "Air pressure rule"
  action {
    iot_topic_publish {
      mqtt_topic = "air-pressure-topic"
    }
  }
  rule_condition {
    numeric {
      variable    = "air_pressure"
      comparison  = "GREATER_THAN"
      threshold   = 1000
    }
  }
}



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
