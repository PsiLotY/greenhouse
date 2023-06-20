
resource "awscc_iotevents_detector_model" "test" {
  detector_model_definition = {
    states = [{
      state_name = "state1"
      on_input = {
        events = [{
          event_name = "event1"
          condition  = "$input.sensorData.temperature > 25"
          nextState  = "state2"
        }]
      }
      }, {
      state_name = "state2"
      on_input = {
        events = [{
          event_name = "event2"
          condition  = "$input.sensorData.temperature < 10"
          nextState  = "state1"
        }]
      }
    }]
    initial_state_name = "state1"
  }
  detector_model_name        = "test"
  detector_model_description = "this is a test"
  role_arn                   = "arn:aws:iam::413812240765:role/service-role/Model"
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
              condition   = "$input.sensorData.temperature > 38"
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
              condition   = "$input.sensorData.temperature < 30"
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

