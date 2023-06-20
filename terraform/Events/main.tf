resource "awscc_iotevents_input" "test_input" {
  input_definition = {
    attributes = [ {
      json_path = "messageId"
    },{
      json_path = "sensor_data.humidity"
    }, {
      json_path = "sensor_data.temperature"
    }, {
      json_path = "sensor_data.light"
    } ]
  }
  input_name        = "device_input"
}

resource "awscc_iotevents_detector_model" "window" {
  detector_model_name        = "window_events"
  detector_model_description = "window events"
  evaluation_method          = "BATCH"
  role_arn                   = "arn:aws:iam::413812240765:role/service-role/Model"

  detector_model_definition = {
    states = [
      {
        state_name = "window_closed"
        on_input = {
          events = []
          transition_events = [
            {
              event_name  = "open_window"
              condition   = "$input.device_input.sensor_data.temperature > 38"
              actions     = []
              next_state  = "window_open"
            }
          ]
        }
        on_enter = {
          events = []
        }
        on_exit = {
          events = []
        }
      },
      {
        state_name = "window_open"
        on_input = {
          events = []
          transition_events = [
            {
              event_name  = "close_window"
              condition   = "$input.device_input.sensor_data.temperature < 30"
              actions     = []
              next_state  = "window_closed"
            }
          ]
        }
        on_enter = {
          events = []
        }
        on_exit = {
          events = []
        }
      }
    ]
    initial_state_name = "window_closed"
  }
}

