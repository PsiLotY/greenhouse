terraform {
  required_providers {
    awscc = {
      source  = "hashicorp/awscc"
      version = ">= 0.5.0"
    }
  }

  required_version = ">= 1.2.0"
}

provider "awscc" {
  region     = "eu-central-1"
  access_key = "AKIAWAWJBWF65CWABPGM"
  secret_key = "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"
}

resource "awscc_iotevents_detector_model" "test" {
  detector_model_definition = {
    states = [{
      state_name = "window_closed"
      on_input = {
        events = [{
          event_name = "too_warm"
          condition  = "$input.sensorData.temperature > 25"
          nextState  = "window_open"
        }]
      }
      on_enter = {
        events = [{
          event_name = "closing_window"
          condition  = "TRUE"
          actions = {
            iot_topic_publish = {
              mqtt_topic = "message_test"
            }
          }
        }]
      }
      on_exit = {
        events = {
          events = []
        }
      }
      }, {
      state_name = "window_open"
      on_input = {
        events = [{
          event_name = "too_cold"
          condition  = "$input.sensorData.temperature <= 25"
          nextState  = "window_closed"
        }]
      }
      on_enter = {
        events = [{
          event_name = "opening_window"
          condition  = "TRUE"
          actions = {
            iot_topic_publish = {
              mqtt_topic = "message_test"
            }
          }
        }]
      }
      on_exit = {
        events = {
          events = []
        }
      }
    }]
    initial_state_name = "window_closed"
  }
  detector_model_name        = "test"
  detector_model_description = "this is a test"
  role_arn                   = "arn:aws:iam::413812240765:role/service-role/Model"
}
