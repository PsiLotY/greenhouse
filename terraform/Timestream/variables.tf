variable "database_name" {
  description = "Name of the Timestream database"
  type        = string
}

variable "table_name" {
  description = "Name of the Timestream table"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
}
