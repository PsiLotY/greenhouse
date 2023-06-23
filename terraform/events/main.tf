resource "awscc_iotevents_input" "device_input" {
  input_definition = {
    attributes = [{
      json_path = "messageId"
      }, {
      json_path = "humidity"
      }, {
      json_path = "temperature"
      }, {
      json_path = "light"
    }]
  }
  input_name = "device_input"
}

resource "awscc_iotevents_detector_model" "window" {
  detector_model_name        = "window_events"
  detector_model_description = "monitors and changes the state of the windows"
  evaluation_method          = "SERIAL"
  role_arn                   = "arn:aws:iam::413812240765:role/service-role/IoTCoreRole"

  detector_model_definition = {
    states = [
      {
        state_name = "windows_closed"
        on_input = {
          events = []
          transition_events = [
            {
              event_name = "open_windows"
              condition  = "$input.device_input.temperature > 38"
              actions    = []
              next_state = "windows_open"
            }
          ]
        }
        on_enter = {
          events = [{
            event_name = "enter_windows_closed_state",
            condition = "true",
            actions = [
              {
                iot_topic_publish = {
                  mqtt_topic = "iot/actor_data"
                }
              }
            ]
          }]
        }
        on_exit = {
          events = []
        }
      },
      {
        state_name = "windows_open"
        on_input = {
          events = []
          transition_events = [
            {
              event_name = "close_windows"
              condition  = "$input.device_input.temperature < 30"
              actions    = []
              next_state = "windows_closed"
            }
          ]
        }
        on_enter = {
          events = [{
            event_name = "enter_windows_open_state",
            condition = "true",
            actions = [
              {
                iot_topic_publish = {
                  mqtt_topic = "iot/actor_data"
                }
              }
            ]
          }]
        }
        on_exit = {
          events = []
        }
      }
    ]
    initial_state_name = "windows_closed"
  }
}


resource "awscc_iotevents_detector_model" "sprinkler" {
  detector_model_name        = "sprinkler_events"
  detector_model_description = "Starts and stops the sprinklers based on humidity"
  evaluation_method          = "SERIAL"
  role_arn                   = "arn:aws:iam::413812240765:role/service-role/IoTCoreRole"

  detector_model_definition = {
    states = [
      {
        state_name = "sprinklers_off"
        on_input = {
          events = []
          transition_events = [
            {
              event_name = "start_sprinklers"
              condition  = "$input.device_input.humidity < 20"
              actions    = []
              next_state = "sprinklers_on"
            }
          ]
        }
        on_enter = {
          events = [{
            event_name = "enter_sprinklers_off_state",
            condition = "true",
            actions = [
              {
                iot_topic_publish = {
                  mqtt_topic = "iot/actor_data"
                }
              }
            ]
          }]
        }
        on_exit = {
          events = []
        }
      },
      {
        state_name = "sprinklers_on"
        on_input = {
          events = []
          transition_events = [
            {
              event_name = "stop_sprinklers"
              condition  = "$input.device_input.humidity >= 20"
              actions    = []
              next_state = "sprinklers_off"
            }
          ]
        }
        on_enter = {
          events = [{
            event_name = "enter_sprinklers_on_state",
            condition = "true",
            actions = [
              {
                iot_topic_publish = {
                  mqtt_topic = "iot/actor_data"
                }
              }
            ]
          }]
        }
        on_exit = {
          events = []
        }
      }
    ]
    initial_state_name = "sprinklers_off"
  }
}
