terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = ">= 2.0.0"
    }
  }
}

resource "local_file" "devops_config" {
  filename = "${path.module}/config.txt"
  content  = "environment = ${var.environment_name}"
}

resource "local_file" "welcome_message" {
  filename = "${path.module}/welcome.txt"
  content  = "Welcome to the DevOps Learning Platform! This file was created by Terraform."
}
