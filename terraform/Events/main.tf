
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
