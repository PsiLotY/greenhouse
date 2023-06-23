data "archive_file" "lambda" {
    type        = "zip"
    source_file  = "../lambda_functions/TestLambda.py"
    output_path = "lambda_function_payload.zip"
 }

resource "aws_lambda_function" "example" {
    function_name    = "test_lambda"
    filename         = "lambda_function_payload.zip"
    handler          = "lambda_handler"
    role             = aws_iam_role.core_role.arn
    source_code_hash = data.archive_file.lambda.output_base64sha256
    runtime          = "python3.7"
}