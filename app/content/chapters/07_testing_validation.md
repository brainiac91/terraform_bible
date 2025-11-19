# 7. Testing & Validation

In 2025, we don't just "hope" our infrastructure works. We test it.

## 1. Preconditions & Postconditions
These are checks that run *during* the plan/apply phase.

**Example**: Ensure an AMI is valid before launching an instance.
```hcl
resource "aws_instance" "web" {
  ami = var.ami_id
  
  lifecycle {
    precondition {
      condition     = substr(var.ami_id, 0, 4) == "ami-"
      error_message = "The AMI ID must start with 'ami-'."
    }
  }
}
```

## 2. The `terraform test` Framework
Terraform now includes a native testing framework. You write tests in `.tftest.hcl` files.

**Exercise**:
Create a file `tests/validation.tftest.hcl`:

```hcl
# 1. Run a plan and check values
run "verify_filename" {
  command = plan

  assert {
    condition     = local_file.welcome.filename == "welcome.txt"
    error_message = "Filename is incorrect"
  }
}

# 2. Run an apply and check outputs
run "verify_content" {
  command = apply

  assert {
    condition     = local_file.welcome.content == "Hello, Future DevOps Expert!"
    error_message = "Content did not match"
  }
}
```

Run the test:
```bash
terraform test
```
Terraform will spin up ephemeral infrastructure, run the assertions, and tear it down.

## 3. Policy as Code (Sentinel / OPA)
For large organizations, you enforce rules like "No S3 buckets without encryption".
*   **Sentinel**: HashiCorp's proprietary policy engine (Terraform Cloud).
*   **OPA (Open Policy Agent)**: Open-source standard.
