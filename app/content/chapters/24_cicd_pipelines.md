# 24. CI/CD Pipelines at Scale

Welcome to the advanced tier. Up to this point, you've run Terraform and Kubernetes manifests from your local laptop using `terraform apply` or `kubectl apply`. In a 2026 enterprise organization, **this is strictly forbidden.** 

To pass security audits, all infrastructure changes must flow through an automated pipeline. This chapter focuses on GitHub Actions, Shift-Left Security, and Workload Identity.

## What is Shift-Left Security?
In traditional DevOps models, code was written, deployed, and *then* the security team scanned the running infrastructure (Shift-Right). If a server was open to the internet, it might be exposed for weeks before detection.

**Shift-Left** means moving the security checks as far left in the development cycle as possible—right after the developer commits code, but *before* anything is applied to the cloud.

### Implementing Terraform Scanners
We use tools like `tfsec` or `Checkov` to scan raw HCL logic for vulnerabilities.

```yaml
# .github/workflows/deploy.yaml
name: "Terraform Infrastructure Pipeline"

on:
  push:
    branches:
      - main

jobs:
  terraform:
    name: "Terraform Plan & Apply"
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.9.0

      # SHIFT-LEFT: Fail the pipeline if the code is insecure!
      - name: Run Checkov Security Scan
        uses: bridgecrewio/checkov-action@master
        with:
          directory: ./terraform-configs
          framework: terraform
          soft_fail: false # 🚩 Hard fail the pipeline if a vulnerability is found.

      - name: Terraform Init
        run: terraform init

      - name: Terraform Plan
        run: terraform plan -out=tfplan
```

## The "God Mode" Auth: Keyless Identity

Historically, pipelines authenticated to Google Cloud (or AWS) using a long-lived JSON Service Account Key stored as a GitHub Secret. This is a massive vulnerability. If a developer dumps the `$SERVICE_ACCOUNT_KEY` to stdout, the entire cloud account is compromised.

The 2026 standard is **Workload Identity Federation (OIDC - OpenID Connect)**.

Instead of storing a password, you configure GCP to mathematically trust the GitHub Actions Identity Provider. When your pipeline runs, GitHub generates a short-lived, cryptographically signed JSON Web Token (JWT). GCP verifies the signature and issues a temporary 1-hour access token. **No keys are ever stored.**

### Implementing OIDC in GitHub Actions
To use Workload Identity, you must explicitly request an `id-token` in your workflow, and then exchange it:

```yaml
permissions:
  contents: read
  id-token: write # 🚩 CRITICAL: Allows actions to request an OIDC JWT.

steps:
  - id: 'auth'
    name: 'Authenticate to Google Cloud'
    uses: 'google-github-actions/auth@v1'
    with:
      workload_identity_provider: 'projects/12345/locations/global/workloadIdentityPools/my-pool/providers/my-provider'
      service_account: 'terraform-deployer@my-project.iam.gserviceaccount.com'

  - name: Terraform Apply
    run: terraform apply -auto-approve tfplan
```

## Key Takeaway
Pipeline automation eliminates the "it works on my machine" problem. By strictly enforcing Checkov scans and OIDC authentication within GitHub Actions, you achieve a zero-trust, shift-left deployment model that satisfies the strictest FinOps and InfoSec policies.
