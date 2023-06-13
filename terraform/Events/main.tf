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
    region = "eu-central-1"
    access_key = "AKIAWAWJBWF65CWABPGM"
  secret_key = "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"
}

resource "awscc_iotevents_detector_model" "test" {
  detector_model_definition = {
    states = [ {
      state_name = "state1"
      on_input = {
        events = [ {
          event_name = "event1"
          condition = "$input.sensorData.temperature > 25"
          nextState = "state2"
        } ]
      }
    }, {
      state_name = "state2"
      on_input = {
        events = [ {
          event_name = "event2"
          condition = "$input.sensorData.temperature < 10"
          nextState = "state1"
        } ]
      }
    } ]
    initial_state_name = "state1"
  }
  detector_model_name = "test"
  detector_model_description = "this is a test"
  role_arn = "arn:aws:iam::413812240765:role/service-role/Model"
}