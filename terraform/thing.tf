resource "aws_iot_thing" "my_thing" {
  name = "IoTGateway"
  attributes = {
    arn = aws_iam_role.core_role.arn
    }
}

resource "aws_iot_policy" "my_policy" {
  name   = "Gateway_policy"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["iot:Connect"],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": ["iot:Publish", "iot:Subscribe", "iot:Receive"],
      "Resource": "*"
    }
  ]
}
EOF
}

resource "tls_private_key" "my_private_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "tls_self_signed_cert" "self_signed" {
  private_key_pem       = tls_private_key.my_private_key.private_key_pem
  subject {
    common_name         = aws_iot_thing.my_thing.name
  }
  
  validity_period_hours = 8760  # 1 year
  allowed_uses          = ["key_encipherment", "digital_signature"]
}

resource "aws_iot_certificate" "my_certificate" {
  active           = true
  certificate_pem  = trimspace(tls_self_signed_cert.self_signed.cert_pem)
}

resource "aws_iot_policy_attachment" "my_policy_attachment" {
  policy     = aws_iot_policy.my_policy.name
  target     = aws_iot_certificate.my_certificate.arn
}

resource "aws_iot_thing_principal_attachment" "my_principal_attachment" {
  thing = aws_iot_thing.my_thing.name
  principal  = aws_iot_certificate.my_certificate.arn
}

