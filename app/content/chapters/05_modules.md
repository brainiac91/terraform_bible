# 5. Module Architecture

Modules are the Lego blocks of Terraform.

## The "Wrapper" Pattern
A common pattern is to wrap a public module to enforce company standards.

**Example**: Your company requires all S3 buckets to be encrypted and tagged.
Instead of asking devs to use `aws_s3_bucket` directly (and forget the tags), you create a module `modules/secure_bucket`.

**modules/secure_bucket/main.tf**:
```hcl
resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.this.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Enforce tags
resource "aws_s3_bucket_tagging" "this" {
  bucket = aws_s3_bucket.this.id
  tag_set = merge(var.tags, {
    ManagedBy = "Terraform"
    Security  = "High"
  })
}
```

Now devs just run:
```hcl
module "my_bucket" {
  source      = "./modules/secure_bucket"
  bucket_name = "my-data"
  tags        = { Owner = "Alin" }
}
```
They get security for free.

## Module Versioning
In production, **NEVER** point to a git branch (like `main`).
*   **Bad**: `source = "git::https://github.com/my/module.git"`
*   **Good**: `source = "git::https://github.com/my/module.git?ref=v1.2.0"`

This ensures that if you push a breaking change to the module repo, you don't break all the downstream apps that use it. They can upgrade at their own pace.

## The `terraform init` Gotcha
When you change code *inside* a module, `terraform apply` picks it up.
But if you change the `source` URL or version, you MUST run:
```bash
terraform init -upgrade
```
to download the new code.
