resource "awscc_iotevents_input" "device_input" {
  input_definition = {
    attributes = [{
      json_path = "messageId"
      }, {
      json_path = "timestamp"
      }, {
      json_path = "humidity"
      }, {
      json_path = "temperature"
      }, {
      json_path = "light"
      }, {
      json_path = "need_light"
    }]
  }
  input_name = "device_input"
}

resource "awscc_iotevents_input" "device_input2" {
  input_definition = {
    attributes = [{
      json_path = "messageId"
      }, {
      json_path = "timestamp"
      }, {
      json_path = "humidity"
      }, {
      json_path = "temperature"
      }, {
      json_path = "light"
      }, {
      json_path = "need_light"
    }]
  }
  input_name = "device_input2"
}

resource "awscc_iotevents_input" "device_input3" {
  input_definition = {
    attributes = [{
      json_path = "messageId"
      }, {
      json_path = "timestamp"
      }, {
      json_path = "humidity"
      }, {
      json_path = "temperature"
      }, {
      json_path = "light"
      }, {
      json_path = "need_light"
    }]
  }
  input_name = "device_input3"
}

resource "awscc_iotevents_detector_model" "window" {
  detector_model_name        = "window_events"
  detector_model_description = "monitors and changes the state of the windows"
  evaluation_method          = "SERIAL"
  role_arn                   = var.arn

  detector_model_definition = {
    states = [
      {
        state_name = "windows_closed"
        on_input = {
          events = []
          transition_events = [
            {
              event_name = "open_windows"
              condition  = "$input.device_input2.temperature > 25"
              actions    = []
              next_state = "windows_open"
            }
          ]
        }
        on_enter = {
          events = [{
            event_name = "enter_windows_closed_state",
            condition  = "true",
            actions = [
              {
                iot_topic_publish = {
                  mqtt_topic = "iot/actor_data"
                  payload = {
                    content_expression = "\"{\\\"state\\\": \\\"windows_closed\\\"}\"",
                    type               = "JSON"
                  }
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
              condition  = "$input.device_input2.temperature <= 25"
              actions    = []
              next_state = "windows_closed"
            }
          ]
        }
        on_enter = {
          events = [{
            event_name = "enter_windows_open_state",
            condition  = "true",
            actions = [
              {
                iot_topic_publish = {
                  mqtt_topic = "iot/actor_data"
                  payload = {
                    content_expression = "\"{\\\"state\\\": \\\"windows_open\\\"}\"",
                    type               = "JSON"
                  }
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
  role_arn                   = var.arn

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
            event_name = "enter_sprinklers_off_state"
            condition  = "true"
            actions = [
              {
                iot_topic_publish = {
                  mqtt_topic = "iot/actor_data"
                  payload = {
                    content_expression = "\"{\\\"state\\\": \\\"sprinklers_off\\\"}\"",
                    type               = "JSON"
                  }
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
            condition  = "true",
            actions = [
              {
                iot_topic_publish = {
                  mqtt_topic = "iot/actor_data"
                  payload = {
                    content_expression = "\"{\\\"state\\\": \\\"sprinklers_on\\\"}\"",
                    type               = "JSON"
                  }
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

resource "awscc_iotevents_detector_model" "light" {
  detector_model_name        = "light_Detector"
  detector_model_description = "determines if lights need to be on or off"
  evaluation_method          = "SERIAL"
  role_arn                   = var.arn

  detector_model_definition = {
    states = [
      {
        state_name = "lights_off",
        on_input = {
          events = [
            {
              event_name = "input_light_off_state",
              condition  = "$input.device_input3.light < 60",
              actions = [
                {
                  lambda = {
                    function_arn = var.arn
                  }
                }
              ]
            }
          ],
          transition_events = [
            {
              event_name = "turn_on",
              condition  = "$input.device_input3.need_need_light == true",
              actions    = [],
              next_state = "lights_on"
            }
          ]
        },
        on_enter = {
          events = [
            {
              event_name = "enter_lights_off_state",
              condition  = "true",
              actions = [
                {
                  iot_topic_publish = {
                    mqtt_topic = "iot/actor_data",
                    payload = {
                      content_expression = "\"{\\\"state\\\": \\\"light_turned_off\\\"}\"",
                      type               = "JSON"
                    }
                  }
                }
              ]
            }
          ]
        },
        on_exit = {
          events = []
        }
      },
      {
        state_name = "lights_on",
        on_input = {
          events = [
            {
              event_name = "input_light_on_state",
              condition  = "$input.device_input3.light < 60",
              actions = [
                {
                  lambda = {
                    function_arn = var.arn
                  }
                }
              ]
            }
          ],
          transition_events = [
            {
              event_name = "turn_off",
              condition  = "$input.device_input3.need_need_light == false",
              actions    = [],
              next_state = "lights_off"
            }
          ]
        },
        on_enter = {
          events = [
            {
              event_name = "enter_lights_off_state",
              condition  = "true",
              actions = [
                {
                  iot_topic_publish = {
                    mqtt_topic = "iot/actor_data",
                    payload = {
                      content_expression = "\"{\\\"state\\\": \\\"light_turned_on\\\"}\"",
                      type               = "JSON"
                    }
                  }
                }
              ]
            }
          ]
        },
        on_exit = {
          events = []
        }
      }
    ],
    initial_state_name = "lights_off"
  }

}
