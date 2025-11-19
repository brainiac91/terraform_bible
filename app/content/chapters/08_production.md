# 8. Production Best Practices

This is the knowledge that gets you the €10,000/mo salary.

## 1. Multi-Environment Strategy
**Do NOT** use Terraform Workspaces for environments (Dev/Prod). Use directory separation.

**Recommended Structure**:
```
├── modules/           # Shared modules (versioned)
├── environments/
│   ├── dev/
│   │   ├── main.tf    # Calls modules with dev variables
│   │   └── backend.tf # State: s3://my-state/dev
│   └── prod/
│       ├── main.tf    # Calls modules with prod variables
│       └── backend.tf # State: s3://my-state/prod
```
This ensures complete isolation. If you break Dev state, Prod is untouched.

## 2. CI/CD Integration
**Never run `terraform apply` locally for production.**
Use GitHub Actions, GitLab CI, or Terraform Cloud.

**The Golden Workflow**:
1.  **Pull Request**: CI runs `terraform fmt`, `validate`, and `plan`.
2.  **Code Review**: Team reviews the `plan` output attached to the PR.
3.  **Merge**: CI runs `terraform apply` on the `main` branch.

## 3. Drift Detection
Infrastructure Drift happens when someone manually changes a resource (e.g., changes a Security Group rule in the AWS Console) bypassing Terraform.
*   **Solution**: Run a scheduled `terraform plan` every night. If it shows changes, alert the team.

## 4. Security
*   **State File**: Encrypt it! (S3 Bucket Encryption + DynamoDB).
*   **Secrets**: Use a secrets manager (AWS Secrets Manager, HashiCorp Vault). Pass them to Terraform as data sources, not variables.

```hcl
data "aws_secretsmanager_secret_version" "db_pass" {
  secret_id = "production/db/password"
}

resource "aws_db_instance" "default" {
  password = data.aws_secretsmanager_secret_version.db_pass.secret_string
}
```

## Conclusion
You have completed **The Terraform Bible**. You now possess the knowledge of the entire lifecycle, from writing your first resource to managing complex, tested, and automated production environments.

**Go forth and build!**
