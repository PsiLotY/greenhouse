resource "aws_timestreamwrite_database" "timestream_base" {
  database_name = var.database_name

  tags = {
    Name = "timestream database, created with terraform"
  }
}

resource "aws_timestreamwrite_table" "timestream_table" {
  database_name = aws_timestreamwrite_database.timestream_base.database_name
  table_name    = var.table_name

  retention_properties {
    magnetic_store_retention_period_in_days = 30
    memory_store_retention_period_in_hours  = 24
  }

  tags = {
    Name = "timestream table, created with terraform"
  }
}

