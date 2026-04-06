# 18. Advanced Terraform: Terragrunt, CDK & FinOps

## Beyond the Monolith

By 2026, dropping raw `.tf` files into a single directory is considered legacy. Managing state at an enterprise scale requires decoupling environment configurations from the core modules.

### The Terragrunt Paradigm
[Terragrunt](https://terragrunt.gruntwork.io/) is a thin wrapper that provides extra tools for keeping your configurations DRY (Don't Repeat Yourself). Instead of copying the same backend definitions over and over across `dev`, `staging`, and `prod`, Terragrunt injects them perfectly using `terragrunt.hcl`.

```hcl
# terragrunt.hcl
remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite"
  }
  config = {
    bucket = "my-company-terraform-states"
    key    = "${path_relative_to_include()}/terraform.tfstate"
    region = "us-east-1"
  }
}
```

### Terraform CDK (Cloud Development Kit)
When conditional logic heavily strains HCL maps and `for_each` loops, developers turn to CDK. It allows you to synthesize Terraform JSON using Python, TypeScript, or Go.

### FinOps: Cost as Code
Blind deployments cause catastrophic billing. **Infracost** plugs directly into your GitHub Actions pipeline, blocking PRs if the cloud compute cost exceeds a budgeted threshold.

```yaml
- name: Run Infracost
  run: infracost breakdown --path . --format json > infracost-report.json
```
