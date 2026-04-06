---
description: Automatically validates a user's local homework implementation against the expert agents' criteria.
---

# Validate Homework Workflow

1. Determine the relevant chapter ID and topics the user has been working on.
2. Use the `view_file` tool to inspect the user's generated code (Terraform `.tf` files, `cloudbuild.yaml`, Argo manifests, etc.) directly in their workspace.
3. Depending on the chapter, invoke the respective expert agents mentally and apply their principles to cross-examine the user's code:
    - **Chapter 15 (CI/CD)**: Check if shift-left tools (tfsec/checkov) and correct pipeline syntaxes are used. (Refer to `.agent/agents/cicd_expert.md`).
    - **Chapter 16 (GitOps)**: Check if deployments are pull-based and configurations match GitOps patterns. (Refer to `.agent/agents/gitops_expert.md`).
    - **Chapter 17 (SRE)**: Review their Dashboards or Prometheus configs for SLI/SLO and proper instrumentation. (Refer to `.agent/agents/sre_expert.md`).
    - **Chapter 18 (GCP)**: Validate against the `gcp_cloud_expert.md` principles (Workload Identity, Folder structure, no static keys).
4. If the code breaks any core logic defined by the specific agent or contains errors, reply to the user with actionable feedback and request them to fix the issues.
5. If the code is perfect, congratulate the user in terminal "God Mode" narrative style, explicitly simulating a successful production build or audit report.
