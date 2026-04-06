import json

file_path = 'app/routers/bible.py'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

homework = {
    "01_intro": {
        "title": "GCP Project Bootstrap with Terraform",
        "objective": "Provision a brand new GCP project from scratch using Terraform, enable essential APIs, and configure a Service Account with least-privilege IAM bindings.",
        "platform": "Google Cloud Platform",
        "difficulty": "Beginner",
        "scenario": "Your company just signed a GCP contract. The Cloud team needs a reproducible, auditable way to spin up new GCP projects for each product team. No ClickOps allowed.",
        "steps": [
            "Install the Google Cloud SDK and authenticate via `gcloud auth application-default login`.",
            "Create a `main.tf` with the `google` provider pointing to your billing account and org ID.",
            "Use `google_project` to create a new project with a unique `project_id`.",
            "Use `google_project_service` to enable: compute.googleapis.com, container.googleapis.com, cloudbuild.googleapis.com.",
            "Create a `google_service_account` named 'terraform-sa' with the roles/editor binding.",
            "Output the project ID and service account email using `output` blocks.",
            "Run `terraform init`, `terraform plan`, review the plan, then `terraform apply`.",
            "Verify in the GCP Console that the project, APIs, and service account exist."
        ],
        "deliverables": ["Working `main.tf` with project, APIs, and IAM", "Clean `terraform plan` output with no errors", "Screenshot of the GCP Console showing the created project"],
        "solution_hint": "Use `google_project` with `auto_create_network = false` to avoid default VPC. Chain `google_project_service` resources with `depends_on` on the project. For IAM, use `google_project_iam_member` instead of `google_project_iam_policy` to avoid overwriting existing bindings.",
        "real_world_context": "This is the 'Project Factory' pattern used by every enterprise GCP customer. Google's own Cloud Foundation Toolkit provides Terraform modules for this exact workflow."
    },
    "02_workflow": {
        "title": "GCE Instance Lifecycle Management",
        "objective": "Practice the full Terraform workflow (init → plan → apply → modify → destroy) by provisioning a Compute Engine VM with a startup script that installs Nginx.",
        "platform": "Google Cloud Platform",
        "difficulty": "Beginner",
        "scenario": "A developer needs a quick staging server running Nginx. You must provision it reproducibly, demonstrate the plan diff when modifying it, and cleanly tear it down afterwards.",
        "steps": [
            "Create a `main.tf` with a `google_compute_instance` resource using `e2-micro` machine type.",
            "Add a `metadata_startup_script` that installs and starts Nginx: `apt-get update && apt-get install -y nginx`.",
            "Create a `google_compute_firewall` rule allowing HTTP (port 80) traffic from `0.0.0.0/0`.",
            "Run `terraform plan` and review every resource that will be created.",
            "Run `terraform apply` and verify Nginx is running by opening the external IP in a browser.",
            "Modify the machine type to `e2-small` and run `terraform plan` — observe the 'replace' action.",
            "Apply the change and verify the instance was recreated (new external IP).",
            "Run `terraform destroy` and confirm all resources are cleaned up."
        ],
        "deliverables": ["Complete plan/apply/modify/destroy cycle logs", "Screenshot of Nginx welcome page from the VM's external IP", "Understanding of when Terraform replaces vs. updates in-place"],
        "solution_hint": "Machine type changes force replacement. Use `lifecycle { create_before_destroy = true }` to minimize downtime. Use `google_compute_address` for a static IP that survives replacements.",
        "real_world_context": "Understanding the plan → apply → destroy lifecycle is fundamental. In production, you'd use Managed Instance Groups instead of standalone VMs, but the workflow is identical."
    },
    "03_state": {
        "title": "Remote State Backend on GCS with Locking",
        "objective": "Migrate Terraform state from local to a GCS bucket with versioning, encryption, and state locking to prevent team conflicts.",
        "platform": "Google Cloud Platform",
        "difficulty": "Intermediate",
        "scenario": "Your team of 5 engineers just started sharing Terraform code via Git. Two engineers ran `terraform apply` simultaneously and corrupted the state file. Implement a remote backend to prevent this.",
        "steps": [
            "Create a GCS bucket manually via `gsutil mb -l us-central1 gs://your-tf-state-bucket`.",
            "Enable versioning: `gsutil versioning set on gs://your-tf-state-bucket`.",
            "Add a `backend \"gcs\"` block in your `terraform` configuration pointing to the bucket.",
            "Run `terraform init -migrate-state` to move local state to GCS.",
            "Verify the state file exists in the bucket: `gsutil ls gs://your-tf-state-bucket/`.",
            "Open two terminals and run `terraform plan` simultaneously — observe the lock mechanism.",
            "Enable Customer-Managed Encryption Keys (CMEK) on the bucket for state-at-rest encryption.",
            "Test state recovery by reverting to a previous version using `gsutil` object versioning."
        ],
        "deliverables": ["GCS bucket with versioning and encryption enabled", "Working `backend.tf` configuration", "Proof of state locking preventing concurrent access"],
        "solution_hint": "GCS backend has native locking built-in (no DynamoDB needed like AWS). Use `prefix` in the backend config to namespace state files per environment. Never store the backend bucket's own Terraform state in itself — bootstrap it manually.",
        "real_world_context": "Every production Terraform deployment uses remote state. GCS is Google's equivalent of S3 for state storage. The locking mechanism prevents the exact corruption scenario described."
    },
    "04_variables_outputs": {
        "title": "Parameterized Multi-Region VPC Network",
        "objective": "Build a fully parameterized VPC network using variables for CIDR ranges, regions, and subnet configuration, with outputs exposing network metadata.",
        "platform": "Google Cloud Platform",
        "difficulty": "Intermediate",
        "scenario": "The network team needs a VPC template that can deploy to any GCP region with custom CIDR ranges. The solution must be reusable across dev/staging/prod by only changing variable values.",
        "steps": [
            "Define input variables: `project_id`, `region`, `vpc_name`, `subnets` (list of objects with name, cidr, region).",
            "Use `variable` blocks with proper types, descriptions, and validation rules.",
            "Create a `google_compute_network` with `auto_create_subnetworks = false`.",
            "Use `for_each` with `google_compute_subnetwork` to create subnets from the variable.",
            "Add a `google_compute_router` and `google_compute_router_nat` for outbound internet access.",
            "Create `outputs.tf` exposing the VPC self_link, subnet IDs, and NAT IP.",
            "Create separate `dev.tfvars` and `prod.tfvars` files with different CIDR ranges.",
            "Deploy both environments: `terraform apply -var-file=dev.tfvars` and verify isolation."
        ],
        "deliverables": ["Modular VPC code with variables/outputs", "Separate .tfvars for dev and prod", "Proof of two isolated VPCs deployed in different regions"],
        "solution_hint": "Use `object` type constraints in variables for complex subnet definitions. Cloud NAT eliminates the need for public IPs on internal VMs. Use `google_compute_global_address` for deterministic NAT IPs.",
        "real_world_context": "This is the foundation of every GCP landing zone. Google's Cloud Foundation Toolkit VPC module follows this exact parameterized pattern."
    },
    "05_modules": {
        "title": "Reusable GKE Cluster Module",
        "objective": "Write a production-quality Terraform module that provisions a GKE cluster with configurable node pools, networking, and security settings.",
        "platform": "Google Cloud Platform",
        "difficulty": "Advanced",
        "scenario": "Platform Engineering wants a single, reusable GKE module that any product team can call with minimal inputs. It must enforce private clusters, Workload Identity, and autoscaling by default.",
        "steps": [
            "Create `modules/gke/` with `main.tf`, `variables.tf`, `outputs.tf`, and `versions.tf`.",
            "Define the `google_container_cluster` with `private_cluster_config` and `workload_identity_config`.",
            "Use `google_container_node_pool` with autoscaling min/max and `oauth_scopes`.",
            "Expose outputs: cluster_endpoint, cluster_ca_certificate, cluster_name.",
            "Create a root module that calls your GKE module: `module \"gke\" { source = \"./modules/gke\" }`.",
            "Add input validation: node count must be >= 1, machine type must match `e2-*` pattern.",
            "Deploy the cluster and verify with `gcloud container clusters get-credentials`.",
            "Run `kubectl get nodes` to confirm the cluster is operational."
        ],
        "deliverables": ["Complete module under `modules/gke/` with README", "Root module calling the GKE module with different configs", "Running GKE cluster accessible via kubectl"],
        "solution_hint": "Enable `enable_private_nodes = true` and `enable_private_endpoint = false` for private nodes with public control plane access. Use `release_channel` for automatic GKE version management.",
        "real_world_context": "Google's terraform-google-modules/terraform-google-kubernetes-engine is the industry-standard GKE module used by thousands of companies. Your module follows the same architecture."
    },
    "06_advanced_hcl": {
        "title": "Dynamic Firewall Rules with Advanced HCL",
        "objective": "Use dynamic blocks, for_each, locals, and complex expressions to manage hundreds of GCP firewall rules from a single, DRY YAML configuration.",
        "platform": "Google Cloud Platform",
        "difficulty": "Advanced",
        "scenario": "The security team provides a YAML file with 50+ firewall rules. You must consume this file and generate all rules dynamically without writing individual resource blocks.",
        "steps": [
            "Create a `firewall_rules.yaml` file defining rules: name, direction, protocol, ports, source_ranges.",
            "Use `yamldecode(file(\"firewall_rules.yaml\"))` to load the rules into a Terraform local.",
            "Use `for_each` on `google_compute_firewall` to dynamically create all rules.",
            "Inside each resource, use a `dynamic \"allow\"` block to iterate over protocols/ports.",
            "Add `log_config` to enable VPC Flow Logs for audit compliance.",
            "Use `merge()` and `lookup()` to apply default values where YAML entries are incomplete.",
            "Validate with `terraform plan` that all 50+ rules appear correctly.",
            "Demonstrate adding a new rule by only editing the YAML file (zero HCL changes)."
        ],
        "deliverables": ["YAML-driven firewall management system", "Dynamic blocks generating correct resources", "Proof that adding YAML entries creates new rules without HCL edits"],
        "solution_hint": "Use `locals` to transform the YAML into a normalized map. `flatten()` helps when rules have multiple protocol/port combinations. Consider using `try()` for optional YAML fields.",
        "real_world_context": "Palo Alto's pan-os-terraform module uses this exact pattern. Security teams manage policies via YAML/CSV, and Terraform dynamically enforces them in GCP."
    },
    "07_testing_validation": {
        "title": "Terraform CI/CD Pipeline with Cloud Build",
        "objective": "Build an automated CI/CD pipeline using Google Cloud Build that runs fmt, validate, tfsec, plan, and apply on every Git push.",
        "platform": "Google Cloud Platform",
        "difficulty": "Advanced",
        "scenario": "The VP of Engineering mandates that no Terraform code reaches production without automated security scanning and approval gates. Build the pipeline.",
        "steps": [
            "Create a `cloudbuild.yaml` with sequential steps: fmt-check, validate, tfsec scan, plan, apply.",
            "Configure the Cloud Build trigger to fire on pushes to the `main` branch.",
            "Use the `hashicorp/terraform` Docker image for Terraform steps.",
            "Add a `tfsec/tfsec` step that fails the build if HIGH severity issues are found.",
            "Implement manual approval for the apply step using Cloud Build approval gates.",
            "Store the plan output as an artifact in a GCS bucket for audit trail.",
            "Add Infracost integration to estimate cost impact in the PR comment.",
            "Test the pipeline by pushing a misconfigured resource and verifying the scan catches it."
        ],
        "deliverables": ["Working `cloudbuild.yaml` with security scanning", "Cloud Build trigger connected to your repository", "Proof of a failed build due to tfsec finding a security issue"],
        "solution_hint": "Use `--run-all` with tfsec for comprehensive scanning. Cloud Build substitution variables (`$_ENVIRONMENT`) enable multi-environment pipelines. Store plan files using `terraform plan -out=tfplan`.",
        "real_world_context": "This mirrors the exact CI/CD pipeline used by Google Cloud's own infrastructure team. Shift-left security scanning is a 2026 non-negotiable requirement."
    },
    "08_production": {
        "title": "Multi-Environment GCP Landing Zone",
        "objective": "Deploy a complete multi-environment architecture (dev/staging/prod) using Terraform workspaces with shared modules and environment-specific configurations.",
        "platform": "Google Cloud Platform",
        "difficulty": "Advanced",
        "scenario": "CTO requires a standardized landing zone: each environment gets its own VPC, GKE cluster, Cloud SQL instance, and IAM boundaries. Everything must be DRY and reproducible.",
        "steps": [
            "Structure your code: `modules/` (vpc, gke, cloudsql), `environments/` (dev, staging, prod).",
            "Each environment directory contains only `main.tf` (calling modules) and `terraform.tfvars`.",
            "Deploy VPC with private subnets and Cloud NAT per environment.",
            "Deploy a GKE Autopilot cluster in each environment's VPC.",
            "Deploy Cloud SQL (PostgreSQL) with private IP only, accessible only from the VPC.",
            "Use `terraform workspace` to manage state separation.",
            "Implement a promotion workflow: deploy to dev → validate → promote to staging → prod.",
            "Add resource labels for cost allocation: `environment`, `team`, `managed-by`."
        ],
        "deliverables": ["Three isolated environments with identical architecture", "Shared modules called with different variables", "Cost labels visible in GCP Billing reports"],
        "solution_hint": "Use `terraform.workspace` interpolation in resource names for uniqueness. Cloud SQL private IP requires `google_service_networking_connection`. GKE Autopilot eliminates node management overhead.",
        "real_world_context": "Google's Enterprise Foundation Blueprint follows this exact pattern. The 'Project Factory' + 'Landing Zone' combo is how Fortune 500 companies onboard to GCP."
    },
    "09_security": {
        "title": "Zero-Trust IAM with Workload Identity Federation",
        "objective": "Eliminate all long-lived service account keys by implementing Workload Identity Federation for GitHub Actions and Workload Identity for GKE pods.",
        "platform": "Google Cloud Platform",
        "difficulty": "Expert",
        "scenario": "Security audit found 47 service account keys in the codebase. CISO demands zero static credentials within 30 days. Implement keyless authentication everywhere.",
        "steps": [
            "Create a Workload Identity Pool: `google_iam_workload_identity_pool`.",
            "Create a GitHub OIDC Provider: `google_iam_workload_identity_pool_provider`.",
            "Bind the provider to a service account: `google_service_account_iam_binding` with `principalSet`.",
            "Update GitHub Actions to use `google-github-actions/auth@v2` with WIF (no keys).",
            "For GKE: Enable Workload Identity on the cluster.",
            "Create a Kubernetes Service Account annotated with `iam.gke.io/gcp-service-account`.",
            "Bind the KSA to a GSA: `google_service_account_iam_binding` with `serviceAccount:PROJECT.svc.id.goog[NAMESPACE/KSA]`.",
            "Verify: Deploy a pod that accesses Cloud Storage without any mounted keys."
        ],
        "deliverables": ["Working WIF for GitHub Actions (zero keys)", "Working Workload Identity for GKE pods (zero keys)", "Proof that `gcloud auth list` inside a pod shows the GSA identity"],
        "solution_hint": "The WIF attribute mapping must use `assertion.repository` for GitHub. For GKE, the node pool must have `workload_metadata_config { mode = GKE_METADATA }`. Test with `curl -H 'Metadata-Flavor: Google' metadata.google.internal/computeMetadata/v1/instance/service-accounts/`.",
        "real_world_context": "Workload Identity Federation is Google's answer to AWS OIDC roles. Every SOC2/ISO27001 compliant company must eliminate static credentials by 2026."
    },
    "10_ansible_intro": {
        "title": "GCE Fleet Configuration with Dynamic Inventory",
        "objective": "Use Ansible with the GCP dynamic inventory plugin to automatically discover and configure a fleet of Compute Engine VMs.",
        "platform": "Google Cloud Platform",
        "difficulty": "Beginner",
        "scenario": "You have 10 Compute Engine VMs that need identical security hardening. Manually SSHing into each is unacceptable. Use Ansible to configure them all at once.",
        "steps": [
            "Install the `google.cloud` Ansible collection: `ansible-galaxy collection install google.cloud`.",
            "Create a `gcp_compute.yml` inventory file using the `google.cloud.gcp_compute` plugin.",
            "Configure the inventory with project, zones, and service account authentication.",
            "Run `ansible-inventory -i gcp_compute.yml --list` to verify VM discovery.",
            "Create a playbook `harden.yml` that: disables root SSH, installs fail2ban, enables UFW.",
            "Execute: `ansible-playbook -i gcp_compute.yml harden.yml`.",
            "Verify by SSHing into a VM and confirming fail2ban is running.",
            "Add `keyed_groups` to the inventory to auto-group VMs by labels (e.g., `env: prod`)."
        ],
        "deliverables": ["Working GCP dynamic inventory file", "Security hardening playbook", "Proof of fail2ban running on all VMs"],
        "solution_hint": "Use `auth_kind: application` for Application Default Credentials. Filter VMs with `filters: [\"status = RUNNING\"]`. Group by labels using `keyed_groups: [{key: labels.env, prefix: env}]`.",
        "real_world_context": "Dynamic inventory is how Netflix and Spotify manage their fleets. Static inventory files become unmaintainable beyond 20 servers."
    },
    "11_ansible_playbooks": {
        "title": "Full Stack Application Deployment on GCE",
        "objective": "Deploy a complete LEMP stack (Linux, Nginx, MySQL, PHP) on GCE instances using structured Ansible playbooks with handlers, templates, and variables.",
        "platform": "Google Cloud Platform",
        "difficulty": "Intermediate",
        "scenario": "The development team needs a staging environment mirroring production. Deploy a WordPress site with Nginx reverse proxy, MySQL backend, and automated SSL certificate provisioning.",
        "steps": [
            "Provision 2 GCE VMs via Terraform: one for web (Nginx+PHP), one for database (MySQL).",
            "Create Ansible roles: `nginx`, `php-fpm`, `mysql`, `wordpress`.",
            "Use Jinja2 templates for nginx.conf with upstream PHP-FPM configuration.",
            "Use handlers to restart Nginx only when configuration changes.",
            "Template the MySQL root password using Ansible Vault encryption.",
            "Create the WordPress database and user with the `mysql_db` and `mysql_user` modules.",
            "Deploy WordPress files and configure `wp-config.php` via template.",
            "Run the playbook and verify WordPress is accessible via the web server's external IP."
        ],
        "deliverables": ["Structured roles under `roles/` directory", "Vault-encrypted secrets file", "Running WordPress site accessible via browser"],
        "solution_hint": "Use `ansible-vault create secrets.yml` for MySQL passwords. Nginx upstream config: `upstream php { server unix:/var/run/php/php-fpm.sock; }`. Enable gzip compression in the Nginx template.",
        "real_world_context": "This is the classic Ansible use case. While Kubernetes is replacing this pattern, millions of production WordPress sites still run on VMs with Ansible-managed configurations."
    },
    "12_ansible_roles_advanced": {
        "title": "Ansible + GCP Secret Manager + OS Patch Management",
        "objective": "Build an advanced automation pipeline that pulls secrets from GCP Secret Manager, applies OS patches with rollback capability, and generates compliance reports.",
        "platform": "Google Cloud Platform",
        "difficulty": "Advanced",
        "scenario": "The compliance team requires monthly OS patching with full audit trails. Secrets must come from GCP Secret Manager, never from local files. Build the automation.",
        "steps": [
            "Install the GCP Secret Manager lookup plugin: `google.cloud.gcp_secret_manager`.",
            "Store database credentials in GCP Secret Manager via `gcloud secrets create`.",
            "Write a playbook that fetches secrets at runtime: `lookup('google.cloud.gcp_secret_manager', 'db-password')`.",
            "Create a patching role that: snapshots the VM disk, applies updates, verifies services, rolls back if health checks fail.",
            "Use `block/rescue/always` for the rollback pattern.",
            "Generate a compliance report using `ansible.builtin.template` outputting patched packages.",
            "Store the report in a GCS bucket using the `google.cloud.gcp_storage_object` module.",
            "Schedule the playbook via Cloud Scheduler → Cloud Functions → Ansible Tower/AWX API."
        ],
        "deliverables": ["Playbook fetching secrets from GCP Secret Manager", "Patching role with automatic rollback", "Compliance report uploaded to GCS bucket"],
        "solution_hint": "For disk snapshots, use `gcloud compute disks snapshot` in a shell task before patching. The rescue block should restore from snapshot if `systemctl is-active nginx` fails. Use `csv` callback plugin for compliance reports.",
        "real_world_context": "This exact pipeline is used by healthcare and financial companies for HIPAA/PCI compliance. The snapshot-before-patch pattern prevents catastrophic outages."
    },
    "13_k8s_intro": {
        "title": "First GKE Deployment — Containerized Web App",
        "objective": "Deploy a containerized web application to GKE, expose it via a LoadBalancer Service, and practice basic kubectl operations.",
        "platform": "Google Cloud Platform",
        "difficulty": "Beginner",
        "scenario": "The development team just containerized their Node.js API. Deploy it to GKE and make it publicly accessible. This is your first Kubernetes production deployment.",
        "steps": [
            "Create a GKE Autopilot cluster: `gcloud container clusters create-auto my-cluster --region us-central1`.",
            "Get credentials: `gcloud container clusters get-credentials my-cluster`.",
            "Create a `deployment.yaml` with 3 replicas of `nginx:alpine`.",
            "Apply: `kubectl apply -f deployment.yaml`.",
            "Create a `service.yaml` with `type: LoadBalancer` exposing port 80.",
            "Apply and wait for external IP: `kubectl get svc -w`.",
            "Scale the deployment: `kubectl scale deployment nginx --replicas=5`.",
            "View logs: `kubectl logs -l app=nginx --tail=50`.",
            "Clean up: `kubectl delete -f .` and then `gcloud container clusters delete my-cluster`."
        ],
        "deliverables": ["Running GKE cluster with Nginx deployment", "External IP serving Nginx", "Proof of scaling from 3 to 5 replicas"],
        "solution_hint": "GKE Autopilot manages nodes automatically — no node pool configuration needed. Use `kubectl describe svc` to debug pending LoadBalancer IPs. Add `readinessProbe` and `livenessProbe` for production readiness.",
        "real_world_context": "This is day-1 of every Kubernetes engineer's journey. GKE Autopilot is Google's recommended mode for most workloads since 2024."
    },
    "14_k8s_manifests": {
        "title": "Three-Tier Application on GKE with Cloud SQL",
        "objective": "Deploy a production-grade three-tier architecture: React frontend, Python API backend, and Cloud SQL PostgreSQL — all communicating securely within GKE.",
        "platform": "Google Cloud Platform",
        "difficulty": "Intermediate",
        "scenario": "The product team needs a scalable architecture: frontend serves static assets, API handles business logic, database stores persistent data. Deploy it on GKE with proper networking.",
        "steps": [
            "Provision Cloud SQL (PostgreSQL) with private IP via Terraform.",
            "Deploy the Cloud SQL Auth Proxy as a sidecar container in your API deployment.",
            "Create Kubernetes Secrets for database credentials using `kubectl create secret`.",
            "Write the API Deployment manifest with env vars from Secrets and the SQL proxy sidecar.",
            "Write the Frontend Deployment with Nginx serving the React build.",
            "Create ClusterIP Services for internal communication (API) and LoadBalancer for frontend.",
            "Add NetworkPolicies to restrict: frontend → API only, API → SQL only.",
            "Verify end-to-end: frontend calls API, API reads from Cloud SQL."
        ],
        "deliverables": ["Three deployments (frontend, api, db-proxy) running on GKE", "Cloud SQL accessible only via private IP and auth proxy", "NetworkPolicies restricting traffic flow"],
        "solution_hint": "Cloud SQL Auth Proxy runs at `127.0.0.1:5432` as a sidecar. Use `google_sql_database_instance` with `ipv4_enabled = false` for private-only access. NetworkPolicies require a CNI that supports them (GKE Dataplane V2).",
        "real_world_context": "This is the bread-and-butter architecture of 80% of production GKE workloads. The sidecar proxy pattern is Google's recommended way to connect to Cloud SQL."
    },
    "15_k8s_architecture": {
        "title": "GKE Autoscaling & High Availability Architecture",
        "objective": "Configure Horizontal Pod Autoscaling, Cluster Autoscaler, Pod Disruption Budgets, and multi-zone node pools for a resilient production workload.",
        "platform": "Google Cloud Platform",
        "difficulty": "Advanced",
        "scenario": "Black Friday is in 2 weeks. The e-commerce platform must handle 10x normal traffic. Configure autoscaling and HA to survive the surge without manual intervention.",
        "steps": [
            "Create a GKE cluster with a multi-zone node pool spanning 3 zones.",
            "Deploy a sample API with CPU resource requests: `requests: {cpu: 100m, memory: 128Mi}`.",
            "Create an HPA targeting 50% CPU utilization with min=2, max=20 replicas.",
            "Apply: `kubectl autoscale deployment api --cpu-percent=50 --min=2 --max=20`.",
            "Create a PodDisruptionBudget allowing at most 1 pod unavailable during maintenance.",
            "Generate load using `kubectl run loadgen --image=busybox -- /bin/sh -c 'while true; do wget -q -O- http://api; done'`.",
            "Monitor HPA scaling: `kubectl get hpa -w`.",
            "Observe Cluster Autoscaler adding nodes: `kubectl get nodes -w`.",
            "Verify PDB prevents aggressive evictions: `kubectl get pdb`."
        ],
        "deliverables": ["HPA scaling pods based on CPU", "Cluster Autoscaler adding/removing nodes", "PDB protecting minimum availability"],
        "solution_hint": "Resource requests are REQUIRED for HPA to work. Use `topologySpreadConstraints` to ensure pods spread across zones. The Cluster Autoscaler respects PDBs — it won't evict pods that would violate the budget.",
        "real_world_context": "This is exactly how Shopify and Mercado Libre prepare for Black Friday. The HPA + CA + PDB trio is the industry-standard resilience pattern."
    },
    "16_helm_intro": {
        "title": "Deploy a Monitoring Stack via Helm on GKE",
        "objective": "Install and configure Prometheus + Grafana on GKE using official Helm charts, customize values, and set up dashboards for cluster monitoring.",
        "platform": "Google Cloud Platform",
        "difficulty": "Intermediate",
        "scenario": "The SRE team needs observability for the GKE cluster. Deploy a full monitoring stack using Helm charts instead of writing raw manifests.",
        "steps": [
            "Add the Prometheus community Helm repo: `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`.",
            "Create a `monitoring-values.yaml` with custom Grafana admin password and persistence enabled.",
            "Install: `helm install monitoring prometheus-community/kube-prometheus-stack -f monitoring-values.yaml -n monitoring --create-namespace`.",
            "Verify all pods are running: `kubectl get pods -n monitoring`.",
            "Port-forward Grafana: `kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring`.",
            "Log into Grafana and import dashboard #315 (Kubernetes Cluster Monitoring).",
            "Configure GKE node-level metrics by enabling `kubelet-serving-ca-configmap`.",
            "Upgrade the release to enable alerting: `helm upgrade monitoring ... --set alertmanager.enabled=true`."
        ],
        "deliverables": ["Prometheus + Grafana running on GKE", "Grafana accessible with Kubernetes dashboards", "AlertManager configured for cluster alerts"],
        "solution_hint": "Use `--set grafana.adminPassword=yourpass` or better, a Kubernetes Secret. For GKE, you may need to disable the default `kube-proxy` metrics since GKE uses Dataplane V2. Persistent volumes require a StorageClass.",
        "real_world_context": "The kube-prometheus-stack Helm chart is the #1 most installed chart globally. Every production Kubernetes cluster runs some form of Prometheus monitoring."
    },
    "17_helm_charts": {
        "title": "Build and Publish a Custom Helm Chart to Artifact Registry",
        "objective": "Create a custom Helm chart for a microservice, package it, and publish it to Google Artifact Registry as an OCI-compliant Helm repository.",
        "platform": "Google Cloud Platform",
        "difficulty": "Advanced",
        "scenario": "The platform team wants every microservice deployed via standardized Helm charts stored in a private company registry. Build the chart and publishing pipeline.",
        "steps": [
            "Scaffold a new chart: `helm create my-service`.",
            "Customize `templates/deployment.yaml` with health probes, resource limits, and pod anti-affinity.",
            "Add configurable values: `replicaCount`, `image.repository`, `image.tag`, `resources`.",
            "Create a `templates/hpa.yaml` that's conditionally rendered based on `autoscaling.enabled`.",
            "Lint the chart: `helm lint my-service/`.",
            "Package: `helm package my-service/`.",
            "Create an Artifact Registry Helm repo: `gcloud artifacts repositories create helm-repo --repository-format=docker --location=us-central1`.",
            "Push the chart: `helm push my-service-0.1.0.tgz oci://us-central1-docker.pkg.dev/PROJECT/helm-repo`.",
            "Install from the registry: `helm install my-svc oci://us-central1-docker.pkg.dev/PROJECT/helm-repo/my-service --version 0.1.0`."
        ],
        "deliverables": ["Custom Helm chart with conditional templates", "Chart published to Artifact Registry", "Successful installation from the remote registry"],
        "solution_hint": "Use `{{ if .Values.autoscaling.enabled }}` for conditional HPA rendering. Artifact Registry supports OCI format natively — no `helm repo add` needed. Use `helm template` to test rendering locally before pushing.",
        "real_world_context": "Artifact Registry replaced Container Registry as Google's recommended image/chart store. OCI-based Helm repositories are the 2026 standard, replacing ChartMuseum."
    },
    "18_advanced_tf": {
        "title": "Terragrunt Multi-Project GCP Organization",
        "objective": "Use Terragrunt to manage a multi-project GCP organization with DRY configurations, cascading variables, and cross-project dependencies.",
        "platform": "Google Cloud Platform",
        "difficulty": "Expert",
        "scenario": "Your company has 12 GCP projects across 3 environments. Managing them with vanilla Terraform is a maintenance nightmare. Migrate to Terragrunt for DRY infrastructure management.",
        "steps": [
            "Structure: `terragrunt.hcl` (root) → `dev/staging/prod/` → `networking/compute/gke/` subdirectories.",
            "Root `terragrunt.hcl`: Define the GCS remote backend with dynamic project/env pathing.",
            "Use `include` blocks so child configs inherit the backend and provider settings.",
            "Define `inputs` in each environment's `env.hcl` (region, project_id, labels).",
            "Use `dependency` blocks to pass VPC output to GKE: `dependency \"vpc\" { config_path = \"../networking\" }`.",
            "Add `generate` blocks to write standardized provider configs in every directory.",
            "Run `terragrunt run-all plan` from the environment root to see all changes at once.",
            "Implement CI/CD with `terragrunt run-all apply --terragrunt-non-interactive` in Cloud Build."
        ],
        "deliverables": ["Full Terragrunt directory structure for 3 environments", "Cross-project dependencies working via `dependency` blocks", "Single `run-all plan` showing unified change preview"],
        "solution_hint": "Use `path_relative_to_include()` for dynamic backend key pathing. `dependency` blocks create an implicit DAG — Terragrunt handles the apply order automatically. Use `mock_outputs` for plan-only runs without existing state.",
        "real_world_context": "Gruntwork (Terragrunt's creator) manages infrastructure for hundreds of enterprises. This exact directory structure is their 'Reference Architecture' used by companies like Duolingo."
    },
    "19_advanced_ansible": {
        "title": "Execution Environment + GCP-Native Automation Pipeline",
        "objective": "Build a custom Ansible Execution Environment container, integrate it with GCP APIs for infrastructure automation, and deploy via Cloud Run.",
        "platform": "Google Cloud Platform",
        "difficulty": "Expert",
        "scenario": "Your Ansible control node has 47 conflicting Python dependencies. Build an Execution Environment that packages everything cleanly and run it serverlessly on Cloud Run.",
        "steps": [
            "Install `ansible-builder`: `pip install ansible-builder`.",
            "Create `execution-environment.yml` specifying: base image, Galaxy collections (google.cloud), Python deps (google-auth).",
            "Build: `ansible-builder build -t my-ee:latest -f execution-environment.yml`.",
            "Push to Artifact Registry: `docker push us-central1-docker.pkg.dev/PROJECT/images/my-ee:latest`.",
            "Create a playbook that uses `google.cloud.gcp_compute_instance` to provision VMs.",
            "Write a Cloud Run service that executes `ansible-playbook` inside the EE container on HTTP trigger.",
            "Configure Workload Identity for the Cloud Run service so it authenticates to GCP APIs keylessly.",
            "Trigger the automation: `curl -X POST https://your-cloud-run-url/run -d '{\"playbook\": \"provision.yml\"}'`."
        ],
        "deliverables": ["Custom Execution Environment published to Artifact Registry", "Cloud Run service executing Ansible playbooks", "Keyless GCP API authentication via Workload Identity"],
        "solution_hint": "The EE base image should be `quay.io/ansible/ansible-runner:latest`. Cloud Run has a 60-minute timeout max — sufficient for most playbooks. Use `ansible-runner` Python API for programmatic execution.",
        "real_world_context": "Red Hat's Ansible Automation Platform uses Execution Environments as the standard deployment unit. Running them on Cloud Run creates a serverless automation platform."
    },
    "20_advanced_k8s": {
        "title": "GitOps with ArgoCD on GKE + Cilium Service Mesh",
        "objective": "Deploy ArgoCD for GitOps-driven continuous delivery on GKE with Cilium as the CNI providing eBPF-based service mesh capabilities.",
        "platform": "Google Cloud Platform",
        "difficulty": "Expert",
        "scenario": "The CTO mandates: no more kubectl apply in production. All deployments must flow through Git. Implement GitOps with ArgoCD and eBPF-native networking with Cilium.",
        "steps": [
            "Create a GKE cluster with Dataplane V2 (Cilium-based): `--enable-dataplane-v2`.",
            "Install ArgoCD: `kubectl create namespace argocd && kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml`.",
            "Expose ArgoCD UI: `kubectl port-forward svc/argocd-server -n argocd 8080:443`.",
            "Connect ArgoCD to your Git repository containing Kubernetes manifests.",
            "Create an ArgoCD Application pointing to `apps/production/` in the repo.",
            "Push a manifest change to Git and watch ArgoCD auto-sync the deployment.",
            "Install Hubble for network flow visualization: `cilium hubble enable`.",
            "Create a CiliumNetworkPolicy that restricts egress to only approved external domains.",
            "Verify with Hubble UI: `cilium hubble ui` and observe L7 traffic flows."
        ],
        "deliverables": ["ArgoCD managing all GKE deployments via Git", "Automatic sync on Git push", "Cilium network policies with Hubble observability"],
        "solution_hint": "ArgoCD initial password: `kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d`. GKE Dataplane V2 IS Cilium — no separate installation needed. Use `CiliumNetworkPolicy` for L7-aware policies.",
        "real_world_context": "ArgoCD + Cilium is the 2026 Cloud Native standard. ArgoCD has 18k+ GitHub stars and is used by Intuit, Tesla, and Red Hat. Cilium powers GKE's networking layer."
    },
    "21_interview_tf": {
        "title": "Interview Lab: End-to-End GCP Infrastructure Deployment",
        "objective": "Under interview conditions (45 minutes), design and deploy a complete GCP infrastructure stack: networking, compute, database, and CI/CD — demonstrating senior-level Terraform mastery.",
        "platform": "Google Cloud Platform",
        "difficulty": "Expert",
        "scenario": "INTERVIEW PROMPT: 'You have 45 minutes. Deploy a production-ready GCP environment for a web application. Show me your architecture, explain your decisions, and handle the follow-up questions.'",
        "steps": [
            "MINUTE 0-5: Sketch the architecture on a whiteboard — VPC, subnets, GKE, Cloud SQL, Load Balancer.",
            "MINUTE 5-15: Write the VPC module with private subnets, Cloud NAT, and firewall rules.",
            "MINUTE 15-25: Write the GKE module with private nodes, Workload Identity, and autoscaling.",
            "MINUTE 25-35: Write Cloud SQL with private IP, automated backups, and read replicas.",
            "MINUTE 35-40: Wire everything together with proper IAM and output the connection strings.",
            "MINUTE 40-45: Run `terraform plan` and explain every resource to the interviewer.",
            "FOLLOW-UP: Be prepared to explain state locking, import strategy, and disaster recovery.",
            "FOLLOW-UP: Explain how you'd implement blue-green deployments with this infrastructure."
        ],
        "deliverables": ["Complete infrastructure deployed in <45 minutes", "Clear verbal explanation of every architectural decision", "Answers to follow-up questions demonstrating deep understanding"],
        "solution_hint": "Start with the VPC — everything depends on it. Use `google_compute_global_address` + `google_service_networking_connection` for Cloud SQL private IP. Keep modules simple during interviews — avoid over-engineering.",
        "real_world_context": "This simulates a real Staff/Principal DevOps interview at Google, Meta, or Stripe. The key is demonstrating architectural reasoning, not just code syntax."
    },
    "22_interview_ansible": {
        "title": "Interview Lab: Zero-Downtime Configuration Management Pipeline",
        "objective": "Under interview conditions (45 minutes), design and implement an Ansible pipeline that performs rolling configuration updates across a GCE fleet with zero downtime.",
        "platform": "Google Cloud Platform",
        "difficulty": "Expert",
        "scenario": "INTERVIEW PROMPT: 'We have 50 production VMs running a critical API. Show me how you'd update the Nginx configuration across all of them with zero downtime, automatic rollback, and an audit trail.'",
        "steps": [
            "MINUTE 0-5: Explain the rolling update strategy — serial: 5 (10% at a time).",
            "MINUTE 5-15: Write the GCP dynamic inventory with label-based grouping.",
            "MINUTE 15-25: Write the rolling update playbook with `serial`, `max_fail_percentage`, and health checks.",
            "MINUTE 25-35: Implement block/rescue for automatic rollback on health check failure.",
            "MINUTE 35-40: Add the audit trail — log every change to a GCS bucket with timestamps.",
            "MINUTE 40-45: Demonstrate the pipeline and explain the failure scenarios.",
            "FOLLOW-UP: How would you handle a scenario where rollback also fails?",
            "FOLLOW-UP: How does this scale to 5,000 servers across 3 regions?"
        ],
        "deliverables": ["Rolling update playbook with serial batching", "Automatic rollback mechanism", "Audit trail uploaded to GCS"],
        "solution_hint": "Use `serial: '10%'` for percentage-based batching. Health checks: `wait_for: port=80 timeout=30`. Rollback: keep a backup of the previous config and restore it in the `rescue` block. Scale: use `strategy: free` + `forks: 50` for parallelism.",
        "real_world_context": "This is the canonical Ansible interview question for Senior positions. LinkedIn, Uber, and Datadog all ask variations of this in their SRE interviews."
    },
    "23_interview_k8s": {
        "title": "Interview Lab: Production GKE Platform with Full Observability",
        "objective": "Under interview conditions (60 minutes), design and deploy a production-grade GKE platform with auto-scaling, service mesh, observability, and disaster recovery.",
        "platform": "Google Cloud Platform",
        "difficulty": "Expert",
        "scenario": "INTERVIEW PROMPT: 'Design a GKE platform that can handle 10,000 RPS with 99.99% uptime. Show me the architecture, deploy the core components, and explain your scaling and DR strategy.'",
        "steps": [
            "MINUTE 0-10: Architecture — Regional GKE, multi-zone node pools, Ingress via Gateway API.",
            "MINUTE 10-20: Deploy the GKE cluster with Dataplane V2, Workload Identity, and VPA.",
            "MINUTE 20-30: Deploy a sample API with HPA, PDB, and topology spread constraints.",
            "MINUTE 30-40: Install the observability stack — Prometheus, Grafana, and Hubble.",
            "MINUTE 40-50: Configure alerting rules for error rate, latency P99, and pod restarts.",
            "MINUTE 50-55: Implement DR — explain Multi-Cluster Services and Backup for GKE.",
            "MINUTE 55-60: Present the architecture and handle follow-up questions.",
            "FOLLOW-UP: What's your strategy for zero-downtime GKE version upgrades across 200 microservices?"
        ],
        "deliverables": ["Regional GKE cluster with full autoscaling stack", "Observability stack with alerting", "Verbal DR strategy with RPO/RTO targets"],
        "solution_hint": "Use `google_container_cluster` with `location = region` (not zone) for regional HA. Gateway API replaces Ingress in 2026. For DR: GKE Backup for etcd snapshots, Multi-Cluster Services for cross-region failover. Target RPO=5min, RTO=15min.",
        "real_world_context": "This is the ultimate Kubernetes interview question. Companies like Google, Amazon, and Cloudflare ask this to evaluate Staff+ engineering candidates."
    }
}

# Inject homework into each chapter
for ch_id, hw in homework.items():
    marker = f'"id": "{ch_id}"'
    idx = text.find(marker)
    if idx == -1:
        print(f"WARNING: Chapter {ch_id} not found!")
        continue

    # Find the closing of the chapter dict - search for the flashcards key
    fc_idx = text.find('"flashcards"', idx)
    if fc_idx == -1:
        fc_idx = text.find('"challenge"', idx)
    if fc_idx == -1:
        print(f"WARNING: No insertion point found for {ch_id}")
        continue

    hw_json = json.dumps(hw, indent=12)
    # Remove outer braces and re-indent
    insert = f'        "homework": {hw_json},\n        '
    text = text[:fc_idx] + insert + text[fc_idx:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Homework injection completed for all 23 chapters.")
