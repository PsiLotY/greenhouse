# resource "aws_lambda_function" "example" {
#   function_name    = "example-lambda"
#   filename         = "main.py"
#   source_code_hash = filebase64sha256("../functions2.zip") #path of the file are made from the main.tf where the module is called
#   handler          = "index.handler"
#   role             = "arn:aws:iam::413812240765:role/service-role/test-role-dmwgeyo6"
#   runtime          = "python3.7"
# }