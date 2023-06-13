variable "tables" {
  default = [
    "Antti's Rasp",
    "Hannes' Rasp",
    "Anjo's Rasp",
    "Elisa's Rasp",
    "Isaac's Rasp",
    "Firaz's Rasp"
  ]
}

resource "aws_dynamodb_table" "iot_data" {
  count          = length(var.tables)
  name           = var.tables[count.index]
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "device_id"
  stream_enabled = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "device_id"
    type = "S"                        # Replace with your desired attribute type (e.g., "S" for string, "N" for number)
  }
  attribute {
    name = "timestamp"
    type = "S"
  }
  attribute {
    name = "temperature"
    type = "N"
  }
  attribute {
    name = "air_quality"
    type = "N"
  }
  attribute {
    name = "humidity"
    type = "N"
  }
  attribute {
    name = "light_exposure"
    type = "N"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  global_secondary_index {
    name               = "timestamp-index"
    hash_key           = "timestamp"
    projection_type    = "ALL"
    read_capacity      = 5
    write_capacity     = 5
    non_key_attributes = ["temperature", "air_quality", "pressure"]
  }

  # Add more attribute blocks as needed

  # Define global secondary indexes (if required)
  # Example:
  # global_secondary_index {
  #   name               = "example_gsi"
  #   hash_key           = "gsi_hash_key"
  #   range_key          = "gsi_range_key"
  #   read_capacity      = 5
  #   write_capacity     = 5
  #   projection_type    = "ALL"     # Set the projection type (e.g., "ALL", "INCLUDE", "KEYS_ONLY")
  # }
}