output "api_url" {
  value = aws_apigatewayv2_api.feedback_api.api_endpoint
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.feedback.name
}

output "lambda_function_name" {
  value = aws_lambda_function.feedback_lambda.function_name
}