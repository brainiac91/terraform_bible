# 7. Testing & Validation

In 2025, Infrastructure testing is mandatory.

## 1. The `terraform test` Framework (Deep Dive)
Introduced in v1.6, this allows you to spin up real infrastructure, assert conditions, and destroy it.

### Mocking (New in v1.7+)
You don't always want to create real expensive resources just to test logic. You can **Mock** providers.

**tests/main.tftest.hcl**:
```hcl
mock_provider "aws" {}

run "verify_instance_name" {
  command = plan

  assert {
    condition     = aws_instance.web.tags.Name == "Production-Web"
    error_message = "Tagging standard not met"
  }
}
```
This runs the plan *as if* AWS were there, but without making API calls. It's instant and free.

## 2. Policy as Code (OPA/Conftest)
Terraform validates *syntax*. Policy validates *compliance*.

**Example Policy (Rego)**: "All S3 buckets must have a 'CostCenter' tag."

You run this in your CI pipeline:
```bash
terraform plan -out=tfplan
terraform show -json tfplan > tfplan.json
conftest test tfplan.json
```

If the policy fails, the pipeline fails. This prevents non-compliant infrastructure from ever being created.

## 3. Preconditions (Defensive Coding)
Stop errors before they happen.

```hcl
resource "aws_instance" "db" {
  instance_type = var.size

  lifecycle {
    precondition {
      condition     = var.size != "t2.micro"
      error_message = "Databases cannot be t2.micro for performance reasons."
    }
  }
}
```
This gives the user a clear error message immediately, instead of a vague cloud provider error 5 minutes later.
