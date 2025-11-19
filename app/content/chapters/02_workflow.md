# 2. The Terraform Workflow

The Terraform workflow is a cycle: **Write -> Init -> Plan -> Apply**. Mastering this is crucial for avoiding production outages.

## The Core Cycle

### 1. Write
You modify your `.tf` files.
*   **Best Practice**: Keep files small and logical (`main.tf`, `variables.tf`, `outputs.tf`).

### 2. Format & Validate
Before you even try to run your code, clean it up.

**Exercise**:
Mess up the indentation in your `main.tf` from Chapter 1. Then run:
```bash
terraform fmt
```
Terraform will automatically fix the spacing to the canonical standard. **Always run this before committing to Git.**

Then run:
```bash
terraform validate
```
This checks for syntax errors (e.g., missing braces) without connecting to any cloud provider.

### 3. Plan (The Safety Net)
The `plan` command is your crystal ball. It tells you what *will* happen.

```bash
terraform plan
```

**Understanding the Output**:
*   `+` (Green): Resource will be created.
*   `-` (Red): Resource will be destroyed.
*   `~` (Yellow): Resource will be modified in place.
*   `-/+`: Resource will be destroyed and recreated (Dangerous!).

**Real World Tip**:
In automation (CI/CD), always save your plan:
```bash
terraform plan -out=tfplan
```
This guarantees that the `apply` step executes *exactly* what was shown in the plan, even if the infrastructure changed in the meantime.

### 4. Apply
Executes the changes.

```bash
terraform apply tfplan
```
(If you saved a plan file, you don't need to type `yes`).

## The "Destroy" Command
To tear everything down:
```bash
terraform destroy
```
**Warning**: This deletes EVERYTHING defined in your configuration. In production, you often want to prevent this. We'll cover "Lifecycle Rules" later to prevent accidental deletion.

## Troubleshooting Common Errors

### "Plugin not found"
*   **Cause**: You added a new provider but didn't run `init`.
*   **Fix**: Run `terraform init`.

### "Lock Error"
*   **Cause**: Another process (or you in another terminal) is running Terraform.
*   **Fix**: Wait for it to finish. If you are SURE it crashed, use `terraform force-unlock <LOCK_ID>`.
