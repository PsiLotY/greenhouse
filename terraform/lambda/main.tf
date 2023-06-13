resource "aws_lambda_function" "example" {
  function_name    = "example-lambda"
  filename         = "test.py"
  source_code_hash = filebase64sha256("../functions/test.py")
  handler          = "index.handler"
  role             = "arn:aws:iam::413812240765:role/service-role/test-role-dmwgeyo6"
  runtime          = "python3.7"
}