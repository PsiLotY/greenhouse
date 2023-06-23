resource "aws_iam_role" "test_role" {
  name = "test_role"
  assume_role_policy = file("${path.module}/assume_role_policy.json")
  tags = {
    tag-key = "tag-value"
  }
}

resource "aws_iam_role_policy" "test_policy" {
  name = "test_policy"
  role = aws_iam_role.test_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
    {
      Effect = "Allow"
      actions = ["lambda:*"]
      resources = ["*"]
    },
    {
        Effect = "Allow"
        actions = ["timestream:*"]
        resources = ["*"]
    },
    {
        Effect = "Allow"
        actions = ["iot:*"]
        resources = ["*"]
    },
    {
        Effect = "Allow"
        actions = ["iotevents:*"]
        resources = ["*"]
    }
  ]
  })
}