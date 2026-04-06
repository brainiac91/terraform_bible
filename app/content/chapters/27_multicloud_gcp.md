# 27. GCP & Multi-Cloud Landing Zones

If you deploy a single VM or a single GKE cluster, you just open the GCP Console and click "Create." 

When an enterprise holding petabytes of data migrates 500 microservices to the cloud, you cannot dump them all into a single "Project." The blast radius of a security breach or an expensive billing error would be catastrophic. 

This requires a **Landing Zone**.

## What is a Landing Zone?
A Landing Zone is a pre-configured, secure cloud environment ready to host enterprise workloads. It defines the foundational network topology, identity constraints, billing rules, and security boundaries through IaC.

The Google Cloud Foundation Toolkit is the industry standard for deploying these heavily governed environments using Terraform.

## The GCP Resource Hierarchy
GCP differs heavily from AWS when it comes to organizational structuring. It utilizes a strict hierarchy descending from a root Organization Node.

```text
[Org Node: acme.com]
 ├── [Folder: Production]
 │    ├── [Project: Prod-Frontend]
 │    └── [Project: Prod-Database]
 └── [Folder: Development]
      ├── [Project: Dev-Frontend]
      └── [Project: Dev-Sandbox]
```

### 1. Folders
Folders act as policy isolation boundaries. If you apply an IAM role or an Organization Policy (like "Restrict deployments strictly to the `europe-west4` region") at the Production Folder, it trickles down and explicitly restricts everything underneath it via inheritance.

### 2. Projects
Projects are fundamentally isolation boundaries for billing, quotas, and APIs. A compromised Dev project physically cannot access a Prod project by default.

## The Hub-and-Spoke Shared VPC
Instead of creating a new VPC network in every single project (resulting in fragmented IP address spaces and complex VPN peering routing), Enterprise GCP uses **Shared VPCs**.

A central "Host Project" owns the actual Networking resources (Subnets, Routes, Cloud NAT). It then "shares" those subnets seamlessly with "Service Projects" (where the compute/GKE clusters live).

This allows the Network Security Team to govern firewalls strictly in one central Host Project, while App Developers maintain Admin rights over their applications inside their isolated Service Projects.

## Aggregate Logging Sinks
In highly regulated sectors, you must construct a central, immutable audit trail.
Using Terraform, we deploy an **Organization Sink**. This intercepts *every single* Cloud Audit Log generated across the entire Organization Node (every cluster, every query, every VM login) and forcefully routes it to a centralized, locked-down BigQuery dataset.

```hcl
resource "google_logging_organization_sink" "audit_logs" {
  name             = "org-global-audit-sink"
  org_id           = var.org_id
  destination      = "bigquery.googleapis.com/projects/security-project/datasets/audit_logs"
  include_children = true
}
```

## Key Takeaway
A Landing Zone built with Terraform is the prerequisite for enterprise cloud adoption. By strictly compartmentalizing applications into inherited Folders and Shared VPC structures, you guarantee zero-trust alignment, precise cost tracking, and immense scalability.
