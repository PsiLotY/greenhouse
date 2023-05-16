# Define your AWS provider configuration
provider "aws" {
  region = "eu-central-1"  # Replace with your desired region
}

# Create an AWS IoT thing
resource "aws_iot_thing" "my_thing" {
  name = "my-thing"
}

# Create an AWS IoT policy
resource "aws_iot_policy" "my_policy" {
  name = "my-policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iot:*",
      "Resource": "*"
    }
  ]
}
EOF
}

# Create an AWS IoT certificate
resource "aws_iot_certificate" "my_certificate" {
  active = true
}

# Attach the certificate to the thing
resource "aws_iot_certificate_to_thing" "my_attachment" {
  certificate_id = aws_iot_certificate.my_certificate.id
  thing_name    = aws_iot_thing.my_thing.name
}

# Output the certificate ARN
output "certificate_arn" {
  value = aws_iot_certificate.my_certificate.arn
}
