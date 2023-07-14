data "archive_file" "light_lambda_file" {
  type        = "zip"
  source_file = "../lambda_functions/light_lambda.py"
  output_path = "lambda_function_payload.zip"
}

resource "aws_lambda_function" "light_lambda" {
  function_name    = "light_lambda"
  filename         = "lambda_function_payload.zip"
  handler          = "lambda_handler"
  role             = aws_iam_role.core_role.arn
  source_code_hash = data.archive_file.light_lambda_file.output_base64sha256
  runtime          = "python3.7"
}
