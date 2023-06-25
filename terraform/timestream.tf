resource "aws_timestreamwrite_database" "timestream_base" {
  database_name = "sensorDataDB"
}

resource "aws_timestreamwrite_table" "timestream_table" {
  database_name = aws_timestreamwrite_database.timestream_base.database_name
  table_name    = "sensorDataTable"

  retention_properties {
    magnetic_store_retention_period_in_days = 1
    memory_store_retention_period_in_hours  = 24
  }
}