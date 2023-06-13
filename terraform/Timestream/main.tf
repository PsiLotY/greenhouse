resource "aws_timestreamwrite_database" "my_database" {
  database_name = var.database_name

  tags = {
    Name = "value"
  }
}

resource "aws_timestreamwrite_table" "my_table" {
  database_name = aws_timestreamwrite_database.my_database.database_name
  table_name    = var.table_name

  retention_properties {
    magnetic_store_retention_period_in_days = 30
    memory_store_retention_period_in_hours  = 8
  }

  tags = {
    Name = "example-timestream-table"
  }
}