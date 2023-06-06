terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
  }
  
  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "eu-central-1"  # Update with your desired region
  access_key = "AKIAWAWJBWF65CWABPGM"
  secret_key = "nkMDWAVUsGBa1QKsU/GrrHxY+YqtukrBh8Oqzzx/"
}

resource "aws_iot_thing" "my_thing" {
  name = "terra_thing"
  attributes = {
    arn = "arn:aws:iam::aws:policy/service-role/AWSIoTThingsRegistration"
  }
}

resource "aws_iot_policy" "my_policy" {
  name   = "terra_policy"
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
    common_name         = "terra_thing"
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

output "cert" {
  value = tls_self_signed_cert.self_signed.cert_pem
}

output "key" {
  value     = tls_private_key.my_private_key.private_key_pem
  sensitive = true
}

