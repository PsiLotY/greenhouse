output "cert" {
  value = tls_self_signed_cert.self_signed.cert_pem
}

output "key" {
  value     = tls_private_key.my_private_key.private_key_pem
  sensitive = true
}

#gpt
output "thing_arn" {
  value = aws_iot_thing.my_thing.arn
}
