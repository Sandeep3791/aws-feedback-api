resource "aws_dynamodb_table" "feedback" {
  name         = "feedback-table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Project = "aws-feedback-api"
  }
}