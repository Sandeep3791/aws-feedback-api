resource "aws_lambda_function" "feedback_lambda" {
  function_name = "feedback-lambda"
  role          = aws_iam_role.lambda_role.arn
  handler       = "app.lambda_handler"
  runtime       = "python3.11"

  filename         = "../lambda/function.zip"
  source_code_hash = filebase64sha256("../lambda/function.zip")

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.feedback.name
    }
  }

  tags = {
    Project = "aws-feedback-api"
  }
}