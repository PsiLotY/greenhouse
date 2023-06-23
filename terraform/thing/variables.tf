variable "region" {
  description = "AWS region"
  type        = string
}

variable "thing_name" {
  description = "Name of the IoT thing"
  type        = string
}

variable "thing_attributes" {
  description = "Attributes of the IoT thing"
  type        = map(any)
}
