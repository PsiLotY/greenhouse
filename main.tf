terraform {
  backend "http"{
  }
  required_providers {
    tls = {
      source  = "hashicorp/tls"
      version = "4.0.4"
    }
    local = {
      source  = "hashicorp/local"
      version = "2.4.0"
    }
  }
}

# Root CA

resource "tls_private_key" "ca_keypair" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "tls_self_signed_cert" "ca_cert" {
  private_key_pem       = tls_private_key.ca_keypair.private_key_pem
  is_ca_certificate     = true
  allowed_uses          = ["cert_signing"]
  validity_period_hours = 8760
  subject {
    common_name = "iotauth"
  }
}

# Device-A certificate

resource "tls_private_key" "device_a_keypair" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "tls_cert_request" "device_a_cert_req" {
  private_key_pem = tls_private_key.device_a_keypair.private_key_pem
  subject {
    common_name = "a.iotauth"
  }
}

resource "tls_locally_signed_cert" "device_a_cert" {
  allowed_uses          = ["client_auth"]
  ca_cert_pem           = tls_self_signed_cert.ca_cert.cert_pem
  ca_private_key_pem    = tls_private_key.ca_keypair.private_key_pem
  cert_request_pem      = tls_cert_request.device_a_cert_req.cert_request_pem
  validity_period_hours = 8760
}

# Device-B certificate

resource "tls_private_key" "device_b_keypair" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "tls_cert_request" "device_b_cert_req" {
  private_key_pem = tls_private_key.device_b_keypair.private_key_pem
  subject {
    common_name = "b.iotauth"
  }
}

resource "tls_locally_signed_cert" "device_b_cert" {
  allowed_uses          = ["client_auth"]
  ca_cert_pem           = tls_self_signed_cert.ca_cert.cert_pem
  ca_private_key_pem    = tls_private_key.ca_keypair.private_key_pem
  cert_request_pem      = tls_cert_request.device_b_cert_req.cert_request_pem
  validity_period_hours = 8760
}

# Write certificates to local files

resource "local_file" "ca_cert_pem" {
  filename = "ca-cert.pem"
  content  = tls_self_signed_cert.ca_cert.cert_pem
}

resource "local_file" "device_a_cert_pem" {
  filename = "a-cert.pem"
  content  = tls_locally_signed_cert.device_a_cert.cert_pem
}

resource "local_file" "device_b_cert_pem" {
  filename = "b-cert.pem"
  content  = tls_locally_signed_cert.device_b_cert.cert_pem
}

resource "local_file" "device_a_key_pem" {
  filename = "a-key.pem"
  content  = tls_private_key.device_a_keypair.private_key_pem
}

resource "local_file" "device_b_key_pem" {
  filename = "b-key.pem"
  content  = tls_private_key.device_b_keypair.private_key_pem
}
