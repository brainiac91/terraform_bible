# 8. Production Best Practices

This is the "Senior DevOps Engineer" checklist.

## 1. The CI/CD Pipeline (GitHub Actions Example)
**Never** run `terraform apply` from your laptop.

```yaml
name: Terraform Prod
on:
  push:
    branches: [ "main" ]

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: hashicorp/setup-terraform@v2
      
      - name: Init
        run: terraform init
        
      - name: Format Check
        run: terraform fmt -check
        
      - name: Security Scan (Trivy)
        run: trivy config .
        
      - name: Plan
        run: terraform plan -out=tfplan
        
      - name: Apply
        run: terraform apply -auto-approve tfplan
```

## 2. Security Scanning (DevSecOps)
Tools like **Trivy**, **Checkov**, or **Terrascan** scan your code for vulnerabilities.
*   Open Security Groups (0.0.0.0/0).
*   Unencrypted Databases.
*   Public S3 Buckets.

**Run it locally**:
```bash
docker run --rm -v $PWD:/data aquasec/trivy config /data
```

## 3. Cost Estimation (FinOps)
Before you apply, know the cost.
**Infracost** is a tool that reads your `terraform plan` and generates a bill.

```bash
infracost breakdown --path .
```
**Output**:
> Overall Total: $1,240/month
> + aws_instance.web: $40/month
> + aws_db_instance.db: $1,200/month

## 4. Drift Detection
Set up a nightly cron job that runs `terraform plan -detailed-exitcode`.
*   Exit Code 0: No changes (Good).
*   Exit Code 2: Changes detected (Drift!). -> Send Slack Alert.

## Conclusion
You have completed **The Terraform Bible**.
You know how to:
1.  Write clean, modular HCL.
2.  Manage state safely.
3.  Test your code like software.
4.  Deploy securely via CI/CD.

**You are ready.**
