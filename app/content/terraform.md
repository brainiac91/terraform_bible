# Terraform Fundamentals

Terraform is an Infrastructure as Code (IaC) tool that allows you to build, change, and version infrastructure safely and efficiently.

## Core Concepts

### 1. Resources
Resources are the most important element in the Terraform language. Each resource block describes one or more infrastructure objects.

```hcl
resource "local_file" "example" {
  filename = "${path.module}/example.txt"
  content  = "Hello, Terraform!"
}
```

### 2. Providers
Terraform relies on plugins called "providers" to interact with cloud providers, SaaS providers, and other APIs.

```hcl
provider "local" {
  # No config needed for local provider
}
```

### 3. State
Terraform must store state about your managed infrastructure and configuration. This state is used by Terraform to map real world resources to your configuration, keep track of metadata, and to improve performance for large infrastructures.

> **Tip:** Check out the "Terraform State" tab in the dashboard to see your live state!

## Workflow
1. **Write**: Define infrastructure in configuration files.
2. **Init**: Initialize the directory (`terraform init`).
3. **Plan**: Preview changes (`terraform plan`).
4. **Apply**: Provision infrastructure (`terraform apply`).
