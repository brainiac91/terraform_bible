---
id: "09_security"
title: "9. Advanced Security & Compliance"
description: "Secure your infrastructure with industry-standard tools and practices."
prev_chapter: "08_production"
next_chapter: null
---

# Advanced Security & Compliance

Security is not an afterthought; it's a fundamental part of the infrastructure lifecycle. In this chapter, we'll explore how to secure your Terraform code and enforce compliance policies.

## 1. Secrets Management

**Never** commit secrets to version control.

### Bad Practice ❌
```hcl
resource "aws_db_instance" "default" {
  username = "admin"
  password = "mysecretpassword123" # 😱 DANGER!
}
```

### Best Practice: Environment Variables ✅
```hcl
variable "db_password" {
  type      = string
  sensitive = true
}

resource "aws_db_instance" "default" {
  username = "admin"
  password = var.db_password
}
```
Run with: `export TF_VAR_db_password="securepassword"`

### Best Practice: HashiCorp Vault / AWS Secrets Manager ✅
Retrieve secrets dynamically at runtime.

```hcl
data "aws_secretsmanager_secret_version" "db_creds" {
  secret_id = "production/db/creds"
}

locals {
  db_creds = jsondecode(data.aws_secretsmanager_secret_version.db_creds.secret_string)
}

resource "aws_db_instance" "default" {
  username = local.db_creds.username
  password = local.db_creds.password
}
```

## 2. Static Analysis (SAST)

Catch misconfigurations *before* you deploy.

### Checkov
Checkov is a popular tool for scanning IaC for security and compliance misconfigurations.

**Installation:**
```bash
pip install checkov
```

**Usage:**
```bash
checkov -d .
```

**Example Output:**
```text
Failed checks:
Check: CKV_AWS_20: "Ensure S3 bucket has encryption enabled"
    FAILED for resource: aws_s3_bucket.data
    File: /main.tf:10-15
```

### TFSec
Another powerful scanner specifically for Terraform.

```bash
tfsec .
```

## 3. Policy as Code (PaC)

Enforce rules on *what* can be deployed.

### Open Policy Agent (OPA)
OPA allows you to write policies in Rego language to validate your Terraform plans.

**Example Policy (deny public S3 buckets):**
```rego
package terraform

deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket"
  resource.change.after.acl == "public-read"
  msg = sprintf("Public S3 bucket found: %v", [resource.address])
}
```

## 4. State Security

Your state file contains everything (including secrets). **Protect it.**

1.  **Encryption at Rest**: Enable S3 bucket encryption.
2.  **Access Control**: Restrict access to the state bucket using IAM policies.
3.  **Versioning**: Enable versioning to recover from accidental corruption.

```hcl
resource "aws_s3_bucket" "terraform_state" {
  bucket = "my-company-tfstate"
  
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  versioning {
    enabled = true
  }
}
```
