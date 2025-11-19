# 3. Mastering State

The `terraform.tfstate` file is the "Brain" of Terraform. It maps your code to the real world.

## Local vs. Remote State

### Local State (Default)
Stored in a file named `terraform.tfstate` on your computer.
*   **Pros**: Simple, zero setup.
*   **Cons**: **Dangerous for teams**. If you lose this file, Terraform loses track of your infrastructure. It contains sensitive data in plain text.

### Remote State (The Professional Way)
Stored in a shared backend (S3, Azure Blob, Terraform Cloud).
*   **Pros**: Shared access, Locking, Encryption.

**Exercise: Inspecting State**
In your `terraform-learning` directory (from Chapter 1), run:

```bash
cat terraform.tfstate
```
You will see a JSON object. **NEVER EDIT THIS FILE MANUALLY.**

## State Commands
Sometimes, the real world and your state get out of sync.

### 1. terraform state list
Shows all resources currently tracked.
```bash
terraform state list
# Output: local_file.welcome
```

### 2. terraform state show
Shows details of a specific resource.
```bash
terraform state show local_file.welcome
```

### 3. terraform state mv (Move/Rename)
If you rename a resource in your code:
```hcl
# Changed from "welcome" to "hello"
resource "local_file" "hello" { ... }
```
Terraform will think you want to *delete* "welcome" and *create* "hello".
To tell Terraform it's the *same* resource, just renamed:

```bash
terraform state mv local_file.welcome local_file.hello
```

### 4. terraform state rm (Stop Tracking)
If you want to stop managing a resource but NOT delete it from the provider:
```bash
terraform state rm local_file.hello
```
Terraform forgets about it. The file stays on disk, but `terraform destroy` won't touch it.

## Troubleshooting State
**Scenario**: You deleted the `welcome.txt` file manually.
**Run**: `terraform plan`
**Result**: Terraform sees the file is missing (Drift) and plans to recreate it (`+`).
