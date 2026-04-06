# 2. The Terraform Workflow

The Terraform workflow is a cycle: **Write -> Init -> Plan -> Apply**. But expert engineers know the hidden steps in between.

## 1. Write & Format
Code readability is not optional.

### The Canonical Format
Terraform includes a built-in style guide.
```bash
terraform fmt -recursive
```
**Pro Tip**: Add this to your CI/CD pipeline. If code isn't formatted, fail the build.

### Validation
```bash
terraform validate
```
Checks for syntax errors and attribute correctness (e.g., using a string where a number is required). It does **not** check if your AWS credentials are valid.

## 2. Init & The Lock File
When you run `terraform init`, a file named `.terraform.lock.hcl` is created.

**Why is this critical?**
It records the *exact* SHA256 hash of the provider plugins you used.
*   **Scenario**: You use `aws` provider v5.0. It works.
*   **Tomorrow**: AWS releases v5.1 with a breaking bug.
*   **Result**: Without the lock file, your colleague might download v5.1 and break production. With the lock file, they are forced to use v5.0 until you explicitly upgrade.

**Command**: `terraform init -upgrade` (To update the lock file).

## 3. Plan: The Crystal Ball
```bash
terraform plan -out=tfplan
```

### Understanding "Drift"
Drift occurs when the real world changes without Terraform knowing.
*   **Example**: You created a file. Someone deleted it manually.
*   **Terraform's Reaction**:
    1.  `plan` refreshes state (checks the real world).
    2.  It sees the file is gone.
    3.  It plans to recreate it (`+`).

### Refresh-Only Mode
Sometimes you *want* to accept the manual changes (e.g., someone manually added a tag you want to keep).
```bash
terraform plan -refresh-only
```
This updates your state file to match reality, without changing any infrastructure.

## 4. Apply
```bash
terraform apply tfplan
```

## 5. Destroy (and how to prevent it)
```bash
terraform destroy
```

### Lifecycle Rules
You can prevent accidental deletion of critical resources (like Databases).

```hcl
resource "local_file" "critical" {
  filename = "database.db"
  content  = "DATA"

  lifecycle {
    prevent_destroy = true
  }
}
```
**Exercise**:
1.  Add the `lifecycle` block to your file from Chapter 1.
2.  Run `terraform apply`.
3.  Try `terraform destroy`.
4.  **Result**: Terraform will error and refuse to destroy it. This is a safety mechanism.
