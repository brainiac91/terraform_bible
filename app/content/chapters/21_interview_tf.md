# 21. Technical Interview: Terraform Architecture

## Preparing for the Technical Screen

In Senior DevOps operations, writing basic HCL modules is assumed. Interviewers will drill down into **Failure Domains, State File Recoveries, and Internal Workings**. This chapter focuses on edge cases.

### State Corruptions & Locks
When a deployment pipeline crashes mid-execution (e.g., due to an AWS service outtage or OOM kill on the runner), the `terraform.tfstate` lock located in DynamoDB or S3 will not be released. 

If this happens, subsequent pipelines will fail. You must identify the lock via the state registry and execute:
```bash
terraform force-unlock <LOCK_ID>
```
*Warning*: Do not do this if another pipeline is definitively still applying. After unlocking, use `terraform state pull` to verify you aren't looking at garbage data.

### Circular Dependencies
Sometimes architectures demand circular routing. Security Group "Private" must allow traffic from Security Group "Public", but "Public" requires "Private"'s ID for its outbound routing limit. 

Terraform will detect the cycle and instantly fail mapping the DAG (Directed Acyclic Graph). You break this by standing up the "empty" security groups first, and abstracting the rules to `aws_security_group_rule`:

```hcl
resource "aws_security_group_rule" "link" {
  type                     = "ingress"
  from_port                = 80
  to_port                  = 80
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.public.id
  security_group_id        = aws_security_group.private.id
}
```
