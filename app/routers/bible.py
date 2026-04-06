from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import markdown
import os

router = APIRouter(
    prefix="/bible",
    tags=["bible"]
)

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"))
CHAPTERS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content", "chapters")

CHAPTERS = [
    {
        "id": "01_intro",
        "title": "1. Introduction & Setup",
        "quiz": [
            {"q": "What is the key difference between Mutable and Immutable infrastructure?", "options": ["Mutable is faster", "Immutable replaces servers instead of updating them", "Mutable uses Python", "Immutable never changes"], "a": 1},
            {"q": "Which command initializes the working directory?", "options": ["terraform start", "terraform run", "terraform init", "terraform create"], "a": 2},
            {"q": "What is a Terraform Provider?", "options": ["A cloud server", "A plugin that talks to APIs", "A database", "A variable"], "a": 1}
,
            {"q": "How does Terraform calculate the checksums placed in `.terraform.lock.hcl`?", "options": ["SHA256 of the zip file", "SHA256 of the extracted binary and zip using h1/zh tags", "MD5 of the provider binary", "A random hash from Hashicorp"], "a": 1},
            {"q": "What happens if a resource is modified outside Terraform AND someone modifies the HCL code to a third conflicting state before running an apply?", "options": ["Terraform crashes", "Terraform forces a manual merge", "Terraform refreshes state to the raw reality, diffs against the HCL, and applies the HCL desired state", "Terraform ignores the HCL"], "a": 2},
            {"q": "Can you use dynamic logic (like counts) to instantiate `provider` blocks?", "options": ["Yes, using for_each", "Yes, using count", "No, provider configurations must be static", "Yes, using nested modules"], "a": 2},
            {"q": "When writing to the local backend, how does Terraform ensure acid compliance on the state file?", "options": ["fsync and atomic file renames", "SQLite transactions", "AWS DynamoDB", "It doesn't"], "a": 0},
            {"q": "What is the primary technical drawback of the `depends_on` meta-argument?", "options": ["It causes circular dependencies", "It disables Terraform's concurrent graph execution for those nodes, heavily slowing down apply times", "It costs money", "It breaks state locks"], "a": 1},
            {"q": "If you misspell a resource type, at what specific phase does Terraform catch the error?", "options": ["terraform init", "terraform plan", "terraform validate or plan parsing phase", "terraform apply"], "a": 2}
,
            {"q": "What is the critical difference between a `resource` and a `data` source in Terraform?", "options": ["Resources are read-only", "Data sources query existing infrastructure without managing it; resources create and manage infrastructure lifecycle", "There is no difference", "Data sources cost money"], "a": 1}
        ],
        "interview_prep": [
            {"q": "Technical Screen: Explain Mutable vs Immutable infrastructure in the context of drift.", "a": "Mutable infrastructure allows in-place updates (e.g., SSH in, run apt-get update). Immutable infrastructure mandates replacing the server entirely with a new image. Terraform enforces immutable deployment, which minimizes 'configuration drift' because servers are never manually altered after provisioning."}
        ],
                "homework": {
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
            "deliverables": [
                        "Working `main.tf` with project, APIs, and IAM",
                        "Clean `terraform plan` output with no errors",
                        "Screenshot of the GCP Console showing the created project"
            ],
            "solution_hint": "Use `google_project` with `auto_create_network = false` to avoid default VPC. Chain `google_project_service` resources with `depends_on` on the project. For IAM, use `google_project_iam_member` instead of `google_project_iam_policy` to avoid overwriting existing bindings.",
            "real_world_context": "This is the 'Project Factory' pattern used by every enterprise GCP customer. Google's own Cloud Foundation Toolkit provides Terraform modules for this exact workflow."
},
        "flashcards": [
            {"front": "Immutable Infrastructure", "back": "The practice of replacing infrastructure rather than updating it in-place."},
            {"front": "terraform init", "back": "Initializes the directory, downloads providers, and creates the lock file."},
            {"front": "HCL", "back": "HashiCorp Configuration Language - the syntax used by Terraform."}
        ],
        "challenge": {
            "title": "The Multi-Cloud Simulator",
            "description": "Create a main.tf that uses the 'random' provider to generate a pet name, and then uses the 'local' provider to create a file named after that pet. The file content must contain the pet name in uppercase.",
            "hints": ["Use resource 'random_pet'", "Use resource 'local_file'", "Use the upper() function"],
            "solution": "resource 'random_pet' 'p' {}\nresource 'local_file' 'f' {\n  filename = '${random_pet.p.id}.txt'\n  content = upper(random_pet.p.id)\n}"
        }
    },
    {
        "id": "02_workflow",
        "title": "2. The Terraform Workflow",
        "quiz": [
            {"q": "What does 'terraform plan' do?", "options": ["Creates resources", "Deletes resources", "Previews changes", "Downloads plugins"], "a": 2},
            {"q": "Why is .terraform.lock.hcl important?", "options": ["It encrypts your state", "It pins provider versions for consistency", "It speeds up downloads", "It is not important"], "a": 1},
            {"q": "How do you fix Drift without changing infrastructure?", "options": ["terraform apply", "terraform plan -refresh-only", "terraform destroy", "terraform import"], "a": 1}
,
            {"q": "What does `terraform apply -replace=aws_instance.web` do?", "options": ["Renames it", "Taints the resource, forcing destruction and recreation in the current plan execution", "Upgrades the AMI", "Ignores the resource"], "a": 1},
            {"q": "When a `terraform plan` outputs `~ update in-place`, what determines if it can be done in-place or if it forces replacement?", "options": ["The cloud provider's API capabilities mapping to the resource schema fields (ForceNew attribute)", "The user's IAM permissions", "Terraform's local state file", "The version of Terraform"], "a": 0},
            {"q": "If you delete the `.terraform` folder, do you lose your infrastructure?", "options": ["Yes", "No, it only contains downloaded plugins and backend cache, which can be restored via init", "Only if it is a remote backend", "Only if using workspaces"], "a": 1},
            {"q": "What is the exact JSON structure generated by `terraform plan -out=plan.binary`?", "options": ["It is plaintext JSON", "It is heavily compressed zip archive", "It is a proprietary binary zip containing the state, config, and diff. It must be read with `terraform show -json`", "It is a Go Lang object"], "a": 2},
            {"q": "How does `terraform console` evaluate expressions without internet access?", "options": ["It parses the `.tf` files and uses the local cached state variables", "It uses an embedded V8 engine", "It guesses", "It actually requires internet access"], "a": 0},
            {"q": "What does a non-zero exit code (exactly 2) mean when running `terraform plan -detailed-exitcode`?", "options": ["Syntax error", "Success with NO changes", "Success WITH changes present (drift detected)", "Provider crash"], "a": 2}
,
            {"q": "What does `terraform workspace select staging` accomplish in a multi-environment setup?", "options": ["Deletes staging", "Switches the active state context so all subsequent plan/apply commands operate against the staging-specific state file", "Creates a new provider", "Renames the backend"], "a": 1}
        ],
        "interview_prep": [
            {"q": "Scenario: You deployed an AWS instance using Terraform. A Junior DevOps engineer manually deletes it from the AWS Console. What happens when you run 'terraform plan', and how does Terraform know?", "a": "When you run 'terraform plan', Terraform first performs an implicit 'refresh' by querying the AWS API. It compares the real-world state to the local `terraform.tfstate`. It will notice the instance is missing and the plan will declare that it must CREATE the instance to restore the desired state."}
        ],
                "homework": {
            "title": "GCE Instance Lifecycle Management",
            "objective": "Practice the full Terraform workflow (init \u2192 plan \u2192 apply \u2192 modify \u2192 destroy) by provisioning a Compute Engine VM with a startup script that installs Nginx.",
            "platform": "Google Cloud Platform",
            "difficulty": "Beginner",
            "scenario": "A developer needs a quick staging server running Nginx. You must provision it reproducibly, demonstrate the plan diff when modifying it, and cleanly tear it down afterwards.",
            "steps": [
                        "Create a `main.tf` with a `google_compute_instance` resource using `e2-micro` machine type.",
                        "Add a `metadata_startup_script` that installs and starts Nginx: `apt-get update && apt-get install -y nginx`.",
                        "Create a `google_compute_firewall` rule allowing HTTP (port 80) traffic from `0.0.0.0/0`.",
                        "Run `terraform plan` and review every resource that will be created.",
                        "Run `terraform apply` and verify Nginx is running by opening the external IP in a browser.",
                        "Modify the machine type to `e2-small` and run `terraform plan` \u2014 observe the 'replace' action.",
                        "Apply the change and verify the instance was recreated (new external IP).",
                        "Run `terraform destroy` and confirm all resources are cleaned up."
            ],
            "deliverables": [
                        "Complete plan/apply/modify/destroy cycle logs",
                        "Screenshot of Nginx welcome page from the VM's external IP",
                        "Understanding of when Terraform replaces vs. updates in-place"
            ],
            "solution_hint": "Machine type changes force replacement. Use `lifecycle { create_before_destroy = true }` to minimize downtime. Use `google_compute_address` for a static IP that survives replacements.",
            "real_world_context": "Understanding the plan \u2192 apply \u2192 destroy lifecycle is fundamental. In production, you'd use Managed Instance Groups instead of standalone VMs, but the workflow is identical."
},
        "flashcards": [
            {"front": "Drift", "back": "When the real-world infrastructure differs from the Terraform state."},
            {"front": "terraform fmt", "back": "Automatically formats your HCL code to the canonical standard."},
            {"front": "terraform validate", "back": "Checks code for syntax errors and internal consistency."}
        ],
        "challenge": {
            "title": "The Drift Detective",
            "description": "1. Create a file with Terraform. 2. Manually delete the file in your terminal. 3. Run a command to update the state to match reality (so Terraform knows it's gone) without running 'apply'.",
            "hints": ["You need to refresh the state", "Look at 'terraform plan' flags"],
            "solution": "terraform plan -refresh-only\n(Then accept the plan)"
        }
    },
    {
        "id": "03_state",
        "title": "3. Mastering State",
        "quiz": [
            {"q": "Where is the default state stored?", "options": ["S3", "terraform.tfstate", "In memory", "On HashiCorp servers"], "a": 1},
            {"q": "What command moves a resource in state?", "options": ["terraform move", "terraform state mv", "terraform rename", "terraform mv"], "a": 1},
            {"q": "Why should you use State Locking?", "options": ["To encrypt data", "To prevent concurrent updates corrupting state", "To speed up apply", "To hide secrets"], "a": 1}
,
            {"q": "In a remote S3 backend, what precisely does the DynamoDB table store?", "options": ["The actual JSON state", "A lock item with a Digest and LockID session", "The provider config", "The history of applies"], "a": 1},
            {"q": "If someone accidentally deletes the `terraform.tfstate` from S3 and you have NO versioning, how do you recover?", "options": ["Run apply immediately", "You cannot. You must recreate empty state and manually `terraform import` every single ID back into the graph", "HashiCorp can restore it", "Run `terraform init -refresh`"], "a": 1},
            {"q": "What command allows you to rename the identity of a module inside the state file without destroying its resources?", "options": ["terraform rename", "terraform module mv", "terraform state mv module.old module.new", "terraform state replace"], "a": 2},
            {"q": "Why is manipulating the state file manually (e.g. `vim terraform.tfstate`) extremely dangerous beyond just typos?", "options": ["It breaks formatting", "It corrupts the `serial` lineage, causing remote backends to hard-reject the push", "It encrypts the file", "It locks the file permanently"], "a": 1},
            {"q": "What does `terraform force-unlock` do under the hood?", "options": ["Deletes the lock entry directly from DynamoDB/Consul", "Kills the running terraform process on another machine", "Bypasses AWS IAM", "None of the above"], "a": 0},
            {"q": "When is the `terraform state pull` command useful?", "options": ["To update providers", "To safely grab a localized JSON copy of the remote state for inspection without locking the backend", "To pull git repos", "To import resources"], "a": 1}
,
            {"q": "When using `terraform import aws_instance.web i-1234567`, what precisely happens?", "options": ["Terraform creates the EC2 instance", "Terraform adds the existing EC2 instance to the state file mapping. No HCL is generated \u2014 you must write the resource block yourself", "Terraform deletes the instance", "Terraform exports HCL automatically"], "a": 1}
        ],
        "interview_prep": [
            {"q": "Technical Screen: Why is 'terraform import' considered dangerous or tedious, and when is it absolutely necessary?", "a": "Importing handles state mapping, but it does NOT generate configuration (.tf files). It is tedious because you must manually write the HCL code to match the imported state exactly. It is necessary when inheriting legacy infrastructure (e.g., 'ClickOps' AWS setups) that need to be brought under Terraform's strict lifecycle management without destroying them."}
        ],
                "homework": {
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
                        "Open two terminals and run `terraform plan` simultaneously \u2014 observe the lock mechanism.",
                        "Enable Customer-Managed Encryption Keys (CMEK) on the bucket for state-at-rest encryption.",
                        "Test state recovery by reverting to a previous version using `gsutil` object versioning."
            ],
            "deliverables": [
                        "GCS bucket with versioning and encryption enabled",
                        "Working `backend.tf` configuration",
                        "Proof of state locking preventing concurrent access"
            ],
            "solution_hint": "GCS backend has native locking built-in (no DynamoDB needed like AWS). Use `prefix` in the backend config to namespace state files per environment. Never store the backend bucket's own Terraform state in itself \u2014 bootstrap it manually.",
            "real_world_context": "Every production Terraform deployment uses remote state. GCS is Google's equivalent of S3 for state storage. The locking mechanism prevents the exact corruption scenario described."
},
        "flashcards": [
            {"front": "terraform state list", "back": "Lists all resources currently tracked in the state file."},
            {"front": "State Locking", "back": "Prevents two people from modifying state at the same time."},
            {"front": "terraform import", "back": "Brings existing, unmanaged infrastructure into Terraform state."}
        ],
        "challenge": {
            "title": "The Refactor",
            "description": "You have a resource 'local_file.A'. Rename it in your code to 'local_file.B'. Make Terraform recognize this as a RENAME, not a destroy/create.",
            "hints": ["If you just change the code, Terraform sees a destroy/create", "You need to tell the state about the move"],
            "solution": "terraform state mv local_file.A local_file.B"
        }
    },
    {
        "id": "04_variables_outputs",
        "title": "4. Variables & Outputs",
        "quiz": [
            {"q": "How do you define a default value for a variable?", "options": ["value = ...", "default = ...", "set = ...", "input = ..."], "a": 1},
            {"q": "Which file is automatically loaded to set variables?", "options": ["vars.txt", "terraform.tfvars", "variables.tf", "input.tf"], "a": 1},
            {"q": "How do you mark an output as sensitive?", "options": ["hidden = true", "private = true", "sensitive = true", "secret = true"], "a": 2}
,
            {"q": "What is the maximum allowed size of a sensitive variable output when processed by the command line?", "options": ["64kb", "There is no theoretical limit, but it will be redacted. RAM is the limit.", "1MB", "2KB"], "a": 1},
            {"q": "Can you use variables inside the `backend \"s3\" {}` block?", "options": ["Yes", "No, backend blocks are initialized before variables are parsed (interpolation is forbidden)", "Only string variables", "Only with TF Cloud"], "a": 1},
            {"q": "If you dynamically generate a variable value using `locals` and it fails validation, when does Terraform error out?", "options": ["At Apply phase", "During the syntax/parsing phase of `terraform plan` or `validate`", "During Init", "It never errors"], "a": 1},
            {"q": "Which data structure is correctly defined by this type constraint: `list(object({ name = string, tags = map(string) }))`?", "options": ["A map of strings", "An array containing dictionaries, each with a string name and an internal dictionary of strings for tags", "A string encoded as JSON", "An AWS Tag array"], "a": 1},
            {"q": "What happens if a `sensitive = true` output is referenced by a non-sensitive output?", "options": ["Terraform decrypts it", "Terraform throws a hard error indicating sensitive boundaries were breached unless you explicitly mark the recipient output as sensitive too", "It is printed in plaintext", "It is ignored"], "a": 1},
            {"q": "How can you validate an input variable to ensure it is a valid IPv4 address?", "options": ["Use the `regex()` function inside a `validation {}` block", "Use `ipv4 = true`", "Ask AWS", "Format as a number"], "a": 0}
,
            {"q": "What is the variable precedence order from lowest to highest in Terraform?", "options": ["CLI > env > file", "defaults < terraform.tfvars < *.auto.tfvars < -var-file < -var CLI < TF_VAR_ environment variables", "All are equal", "Environment always wins"], "a": 1}
        ],
        "interview_prep": [
            {"q": "Technical Screen: Explain variable precedence in Terraform. If I set a variable in `terraform.tfvars`, export an environment variable `TF_VAR_env`, and pass `-var 'env=prod'`, which one wins?", "a": "The `-var` command-line flag has the highest precedence and wins. The precedence order (lowest to highest) is: Environment Variables -> terraform.tfvars -> terraform.tfvars.json -> *.auto.tfvars -> -var or -var-file flags."}
        ],
                "homework": {
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
            "deliverables": [
                        "Modular VPC code with variables/outputs",
                        "Separate .tfvars for dev and prod",
                        "Proof of two isolated VPCs deployed in different regions"
            ],
            "solution_hint": "Use `object` type constraints in variables for complex subnet definitions. Cloud NAT eliminates the need for public IPs on internal VMs. Use `google_compute_global_address` for deterministic NAT IPs.",
            "real_world_context": "This is the foundation of every GCP landing zone. Google's Cloud Foundation Toolkit VPC module follows this exact parameterized pattern."
},
        "flashcards": [
            {"front": "Input Variable", "back": "Parameters to customize a module (like function arguments)."},
            {"front": "Output Value", "back": "Return values from a module (like function return values)."},
            {"front": "terraform.tfvars", "back": "The default file for assigning values to variables."}
        ],
        "challenge": {
            "title": "The Validator",
            "description": "Create a variable 'environment' that only accepts 'dev', 'staging', or 'prod'. If the user tries 'test', it must fail with a custom error message.",
            "hints": ["Use the 'validation' block", "Use the 'contains' function"],
            "solution": "variable 'environment' {\n  validation {\n    condition = contains(['dev', 'staging', 'prod'], var.environment)\n    error_message = 'Must be dev, staging, or prod'\n  }\n}"
        }
    },
    {
        "id": "05_modules",
        "title": "5. Module Architecture",
        "quiz": [
            {"q": "What is a Terraform Module?", "options": ["A plugin", "A container for multiple resources", "A database", "A variable file"], "a": 1},
            {"q": "How do you reference a module in the same directory?", "options": ["source = './module'", "source = 'local'", "import module", "include module"], "a": 0},
            {"q": "Why pin module versions?", "options": ["To save space", "To prevent breaking changes", "To speed up init", "It is required"], "a": 1}
,
            {"q": "When calling a child module, how does the child pass data BACK up to the root module?", "options": ["Environment variables", "It exports the data via `output` blocks, which the root module references via `module.<name>.<output_name>`", "Shared state files", "Local files"], "a": 1},
            {"q": "Can a Terraform module call another Terraform module (Nested Modules)?", "options": ["Yes, up to infinite theoretical depth", "No", "Only once", "Only in Terraform Enterprise"], "a": 0},
            {"q": "What happens to the `.terraform` directory when you run `terraform get`?", "options": ["It deletes variables", "It forces a re-download/update of module source code referenced in the root without reinitializing providers", "It downloads cloud resources", "It gets state data"], "a": 1},
            {"q": "If you use `source = \"git::https://example.com/vpc.git?ref=v1.2.0\"`, what is Terraform doing?", "options": ["Using the public registry", "Cloning a specific git tag/branch specifically via the go-getter library to ensure exact versioning", "Downloading a zip", "Nothing"], "a": 1},
            {"q": "How do you completely remove a module and all its resources from your infrastructure?", "options": ["Just delete the file", "Remove the `module` block from HCL and run `terraform apply`, allowing Terraform to destroy the unreferenced resources", "terraform remove module", "rm -rf .terraform"], "a": 1},
            {"q": "If a module does not expose an input variable for an attribute you need to change, what must you do?", "options": ["Change it in AWS console", "Fork the module, add the variable to the module's `variables.tf` and pass it down, then update the module source", "Use a remote-exec", "Override the state"], "a": 1}
,
            {"q": "What does a `terraform.lock.hcl` inside a module directory track?", "options": ["Module state", "Nothing; lock files only exist at the root module level tracking provider checksums", "Child module versions", "Backend configuration"], "a": 1}
        ],
        "interview_prep": [
            {"q": "Scenario: You want to deploy a VPC module from the public HashiCorp Registry, but your security team mandates that external code cannot change without approval. How do you implement this?", "a": "You must implement strict version pinning in the `source` block. For example: `version = \"~> 3.0.0\"`. This prevents Terraform from automatically downloading a major `4.x` patch containing breaking changes or unverified malicious code during `terraform init`."}
        ],
                "homework": {
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
            "deliverables": [
                        "Complete module under `modules/gke/` with README",
                        "Root module calling the GKE module with different configs",
                        "Running GKE cluster accessible via kubectl"
            ],
            "solution_hint": "Enable `enable_private_nodes = true` and `enable_private_endpoint = false` for private nodes with public control plane access. Use `release_channel` for automatic GKE version management.",
            "real_world_context": "Google's terraform-google-modules/terraform-google-kubernetes-engine is the industry-standard GKE module used by thousands of companies. Your module follows the same architecture."
},
        "flashcards": [
            {"front": "Root Module", "back": "The main directory where you run terraform commands."},
            {"front": "Child Module", "back": "A module called by another module."},
            {"front": "Module Source", "back": "The location of the module code (local path, git URL, registry)."}
        ],
        "challenge": {
            "title": "The Wrapper",
            "description": "Create a local module 'my_file' that wraps 'local_file'. It should take 'content' as input, but ALWAYS force the filename to be 'secure.txt'.",
            "hints": ["Create a folder 'modules/my_file'", "Hardcode the filename in the resource inside the module"],
            "solution": "# modules/my_file/main.tf\nresource 'local_file' 'this' {\n  filename = 'secure.txt'\n  content  = var.content\n}"
        }
    },
    {
        "id": "06_advanced_hcl",
        "title": "6. Advanced HCL Patterns",
        "quiz": [
            {"q": "What does the splat operator [*] do?", "options": ["Multiplies numbers", "Extracts a list of attributes", "Comments out code", "Deletes resources"], "a": 1},
            {"q": "Which construct creates multiple resources based on a map?", "options": ["count", "for_each", "loop", "repeat"], "a": 1},
            {"q": "What is a dynamic block used for?", "options": ["Creating dynamic resources", "Creating nested blocks (like ingress rules)", "Dynamic variables", "Dynamic outputs"], "a": 1}
,
            {"q": "In a `for_each` loop, what do `each.key` and `each.value` represent when iterating over a `set(string)`?", "options": ["Key is index, Value is string", "Both `each.key` and `each.value` are the exact same string from the set", "Key is random, Value is string", "Sets cannot be iterated"], "a": 1},
            {"q": "What does the `try()` function do in Terraform?", "options": ["It tries to run an apply 3 times", "It evaluates multiple expressions and returns the result of the first one that does NOT produce an error", "It tests AWS API connectivity", "It catches bash script errors"], "a": 1},
            {"q": "If you want to filter a list inside a `for` expression, which keyword do you append?", "options": ["where", "filter", "if", "select"], "a": 2},
            {"q": "What is a major limitation of `count` compared to `for_each` regarding index shifting?", "options": ["Count is faster", "If you remove the middle item in a list passed to `count`, all subsequent resources shift index, causing mass destruction/recreation.", "Count uses more RAM", "None"], "a": 1},
            {"q": "When writing a `dynamic` block, what argument controls the mapping collection?", "options": ["collection", "dynamic_set", "for_each", "iterator elements"], "a": 2},
            {"q": "What is the `coalesce()` function primarily used for?", "options": ["Combining lists", "Returning the first non-null argument from a given list of arguments to establish defaults", "Encrypting strings", "Hashing passwords"], "a": 1}
,
            {"q": "What does `flatten()` do when applied to a list of lists in Terraform?", "options": ["Sorts them", "Recursively merges all nested lists into a single flat list", "Removes duplicates", "Converts to a map"], "a": 1}
        ],
        "interview_prep": [
            {"q": "Explain the difference between count and for_each. Why is for_each safer?", "a": "count uses lists/integers. If you remove an item from the middle, it shifts all resources, destroying them. for_each uses maps/keys, safely destroying only the removed key."}
        ],
                "homework": {
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
            "deliverables": [
                        "YAML-driven firewall management system",
                        "Dynamic blocks generating correct resources",
                        "Proof that adding YAML entries creates new rules without HCL edits"
            ],
            "solution_hint": "Use `locals` to transform the YAML into a normalized map. `flatten()` helps when rules have multiple protocol/port combinations. Consider using `try()` for optional YAML fields.",
            "real_world_context": "Palo Alto's pan-os-terraform module uses this exact pattern. Security teams manage policies via YAML/CSV, and Terraform dynamically enforces them in GCP."
},
        "flashcards": [
            {"front": "for_each", "back": "Iterates over a map/set to create multiple resource instances."},
            {"front": "count", "back": "Iterates over a number (0, 1, 2...) to create multiple instances."},
            {"front": "Splat [*]", "back": "Short for 'for' loop to get a list of attributes (e.g., all IP addresses)."}
        ],
        "challenge": {
            "title": "The Loop Master",
            "description": "Given a list of names ['a', 'b', 'c'], use a 'for' expression to output a list where every name is capitalized.",
            "hints": ["Use [for n in var.names : ...]", "Use the upper() function"],
            "solution": "output 'caps' {\n  value = [for n in var.names : upper(n)]\n}"
        }
    },
    {
        "id": "07_testing_validation",
        "title": "7. Testing & Validation",
        "quiz": [
            {"q": "What is the purpose of 'terraform test'?", "options": ["To test python code", "To validate infrastructure logic", "To check spelling", "To test network speed"], "a": 1},
            {"q": "What is OPA?", "options": ["Open Policy Agent", "Only Private Access", "Official Provider API", "Object Property Access"], "a": 0},
            {"q": "What does a precondition do?", "options": ["Runs before init", "Checks a condition before applying a resource", "Installs providers", "Validates variables"], "a": 1}
,
            {"q": "With Terraform 1.5's native `test` framework, where do you place the test files?", "options": ["In `/tests` with `.tftest.hcl` extensions", "In a python script", "In a bash script", "In Jenkins"], "a": 0},
            {"q": "What is a `postcondition` block used for?", "options": ["Checking state after apply", "Validating the outputs of a resource *after* it is created, halting execution if the cloud provider returned invalid configurations", "Posting to slack", "Applying updates"], "a": 1},
            {"q": "If Policy as Code (OPA) returns a 'Deny' on a terraform plan JSON, what phase of the pipeline is halted?", "options": ["It blocks the Plan generation", "It halts prior to the Apply phase since the plan JSON violates security bounds", "It destroys the resources", "It sends an email but applies anyway"], "a": 1},
            {"q": "How does Terratest differ from native `terraform test`?", "options": ["Terratest uses Go and actively deploys real infrastructure to AWS, runs API checks, and then tears it down. Native testing can sometimes mock or assert without full destruction loops.", "Terratest is for Python", "They are identical", "Terratest is deprecated"], "a": 0},
            {"q": "Can you use Checkov to scan custom modules before they are invoked by the root module?", "options": ["No", "Yes, it evaluates static HCL code regardless of state", "Only with API keys", "Only in production"], "a": 1},
            {"q": "What happens if a `precondition` fails during a `terraform plan`?", "options": ["The plan is generated but throws a warning", "The plan immediately aborts and fails with a non-zero exit code", "Terraform deletes the resource", "Terraform ignores it"], "a": 1}
,
            {"q": "What is the key difference between `precondition` and `postcondition` blocks in Terraform?", "options": ["They are identical", "Preconditions validate assumptions BEFORE a resource action; postconditions validate guarantees AFTER the action completes", "Preconditions run at destroy", "Postconditions run at init"], "a": 1}
        ],
        "interview_prep": [
            {"q": "How do you enforce Policy as Code in Terraform before apply?", "a": "You use OPA (Open Policy Agent) integrated in your CI/CD pipeline, or Checkov to scan the plan JSON and block the apply if policy fails."}
        ],
                "homework": {
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
            "deliverables": [
                        "Working `cloudbuild.yaml` with security scanning",
                        "Cloud Build trigger connected to your repository",
                        "Proof of a failed build due to tfsec finding a security issue"
            ],
            "solution_hint": "Use `--run-all` with tfsec for comprehensive scanning. Cloud Build substitution variables (`$_ENVIRONMENT`) enable multi-environment pipelines. Store plan files using `terraform plan -out=tfplan`.",
            "real_world_context": "This mirrors the exact CI/CD pipeline used by Google Cloud's own infrastructure team. Shift-left security scanning is a 2026 non-negotiable requirement."
},
        "flashcards": [
            {"front": "Policy as Code", "back": "Defining security/compliance rules as code (e.g., OPA, Sentinel)."},
            {"front": "Precondition", "back": "A lifecycle block to validate assumptions about resources."},
            {"front": "Mock Provider", "back": "Simulates a provider for testing without real API calls."}
        ],
        "challenge": {
            "title": "The Gatekeeper",
            "description": "Add a precondition to a 'local_file' resource. It should only allow the creation of the file if the content is exactly 'APPROVED'.",
            "hints": ["lifecycle { precondition { ... } }", "condition = self.content == ..."],
            "solution": "lifecycle {\n  precondition {\n    condition = self.content == 'APPROVED'\n    error_message = 'Content must be APPROVED'\n  }\n}"
        }
    },
    {
        "id": "08_production",
        "title": "8. Production Best Practices",
        "quiz": [
            {"q": "Why should you NOT run apply locally in production?", "options": ["It's slow", "Lack of audit trail and consistency", "It costs money", "It requires admin rights"], "a": 1},
            {"q": "What tool estimates Terraform costs?", "options": ["TerraCost", "Infracost", "CostExplorer", "MoneyForm"], "a": 1},
            {"q": "What is Trivy used for?", "options": ["Formatting", "Security Scanning", "Cost estimation", "State management"], "a": 1}
,
            {"q": "What is the absolute safest method to run Terraform in a highly-regulated enterprise production environment?", "options": ["From a developer laptop", "Terraform Cloud or a locked-down CI/CD runner (e.g. GitHub Actions) with ephemeral assumed IAM roles (OIDC) and branch-protection required reviews.", "From an EC2 bastion host", "Using hardcoded root credentials"], "a": 1},
            {"q": "How do you handle drift detection passively in production?", "options": ["Do nothing", "Set up a CRON job/Pipeline to run `terraform plan -detailed-exitcode` daily and send Slack alerts if the exit code is 2.", "Run terraform destroy every night", "Manually check AWS"], "a": 1},
            {"q": "Why is separating state files by environment and logical component (e.g. `prod/network/state`, `prod/app/state`) vital?", "options": ["To keep files small", "To isolate failure domains (Blast Radius). An error in the 'app' state won't accidentally destroy the mission-critical 'network' VPC.", "Because AWS requires it", "To save costs"], "a": 1},
            {"q": "When doing blue/green deployments with Terraform, what resource attribute is typically mapped to shift traffic?", "options": ["EC2 Instance type", "Route53 Weights or Target Group bindings", "Security Groups", "VPC ID"], "a": 1},
            {"q": "What is the primary role of the `.terraform.lock.hcl` file in a team environment?", "options": ["It locks the DynamoDB table", "It ensures that every developer and the CI/CD runner download the EXACT same provider hashes, preventing malicious updates or version drift.", "It encrypts the secrets", "It stops applies"], "a": 1},
            {"q": "Which of these is a valid architectural pattern for injecting secrets at scale without hardcoding `.tfvars`?", "options": ["Use `data \"aws_secretsmanager_secret_version\"` blocks to fetch them directly inside Terraform memory at execution time.", "Write them to a public wiki", "Put them in state", "Use default arguments"], "a": 0}
,
            {"q": "What is the architectural purpose of using Terraform workspaces in a CI/CD pipeline?", "options": ["To create backups", "To isolate state files per environment (dev/staging/prod) using a single codebase, preventing cross-environment state contamination", "To encrypt secrets", "To speed up applies"], "a": 1}
        ],
        "interview_prep": [
            {"q": "Scenario: You need to prevent a database from accidentally being destroyed by 'terraform destroy' or an accidental code deletion in production. How do you enforce this natively in HCL?", "a": "You use the `lifecycle` block and set `prevent_destroy = true`. Terraform will then hard-fail any plan that attempts to destroy the resource. To delete it, you would first have to merge a PR setting the value back to false."}
        ],
        "interview_prep": [
            {"q": "How do you prevent accidental deletion of a production database in HCL?", "a": "By using the lifecycle block with prevent_destroy = true. Applying a destroy will immediately fail until a PR removes that flag."}
        ],
                "homework": {
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
                        "Implement a promotion workflow: deploy to dev \u2192 validate \u2192 promote to staging \u2192 prod.",
                        "Add resource labels for cost allocation: `environment`, `team`, `managed-by`."
            ],
            "deliverables": [
                        "Three isolated environments with identical architecture",
                        "Shared modules called with different variables",
                        "Cost labels visible in GCP Billing reports"
            ],
            "solution_hint": "Use `terraform.workspace` interpolation in resource names for uniqueness. Cloud SQL private IP requires `google_service_networking_connection`. GKE Autopilot eliminates node management overhead.",
            "real_world_context": "Google's Enterprise Foundation Blueprint follows this exact pattern. The 'Project Factory' + 'Landing Zone' combo is how Fortune 500 companies onboard to GCP."
},
        "flashcards": [
            {"front": "CI/CD", "back": "Continuous Integration/Deployment - Automating the apply process."},
            {"front": "Infracost", "back": "A tool to estimate cloud costs from Terraform plans."},
            {"front": "Drift Detection", "back": "Scheduled checks to ensure reality matches state."}
        ],
        "challenge": {
            "title": "The Auditor",
            "description": "Write a GitHub Actions step (pseudo-code) that runs 'terraform plan' and FAILS if there are any changes (drift detection mode).",
            "hints": ["terraform plan -detailed-exitcode", "Check the exit code"],
            "solution": "run: terraform plan -detailed-exitcode\n# If exit code is 2, there is drift -> Fail build"
        }
    },
    {
        "id": "09_security",
        "title": "9. Advanced Security & Compliance",
        "quiz": [
            {"q": "What is the best way to handle database passwords in Terraform?", "options": ["Hardcode them", "Use environment variables or a secrets manager", "Put them in a text file", "Use default values"], "a": 1},
            {"q": "What does Checkov do?", "options": ["Formats code", "Scans for security misconfigurations", "Destroys resources", "Generates documentation"], "a": 1},
            {"q": "Which tool allows you to write Policy as Code?", "options": ["OPA", "Git", "Docker", "Bash"], "a": 0}
,
            {"q": "What is the primary danger of using `provisioner \"local-exec\"` with embedded AWS access keys?", "options": ["The keys are saved permanently in the `.terraform.lock.hcl` file", "The block's entire resolved string evaluation, including secrets, is written in plaintext to the `terraform.tfstate` file", "AWS revokes them immediately", "Provisioners fail constantly"], "a": 1},
            {"q": "How does Terraform Enterprise/Cloud implement RBAC for workspace runs compared to open source Terraform?", "options": ["It doesn't, it uses regular IAM", "It abstracts API execution behind Team and Workspace permissions, preventing developers from downloading the root AWS credentials directly", "It forces Python syntax", "It encrypts the console"], "a": 1},
            {"q": "If you must perform dynamic policy checks against the physical cloud state instead of the Terraform plan JSON, what tool do you use?", "options": ["Checkov", "OPA (evaluating tfplan)", "AWS Config or Cloud Custodian", "tfsec"], "a": 2},
            {"q": "What attribute natively ensures that a resource parameter (like a generated RDS password) is concealed from the local CLI output during an apply?", "options": ["secret = true", "hidden = true", "sensitive = true", "encrypt = true"], "a": 2},
            {"q": "If you expose a `sensitive = true` output, does it prevent the secret from entering the `terraform.tfstate`?", "options": ["Yes", "No. State files always contain sensitive values in plaintext. The flag ONLY masks CLI output.", "Only in Terraform Cloud", "Yes, it encrypts it"], "a": 1},
            {"q": "To strictly enforce that developers cannot provision high-cost instances like `p3.16xlarge`, you write an OPA Rego policy. Which phase of the pipeline does OPA evaluate?", "options": ["`terraform init`", "The output JSON of `terraform plan` BEFORE allowing `terraform apply` to run", "After the instances are created", "During state refresh"], "a": 1}
,
            {"q": "Why should you never store provider credentials in `.tf` files committed to version control?", "options": ["It slows down git", "Credentials in VCS are permanently recoverable from git history even after deletion, creating an irreversible security breach", "Terraform ignores them", "It breaks the plan"], "a": 1}
        ],
        "interview_prep": [
            {"q": "Technical Screen: Your team uses a mono-repo. Running 'terraform plan' locally takes 20 minutes because it processes 10,000 resources. How do you architect this to be faster and safer?", "a": "You must decouple the state. Monolithic states are anti-patterns. You should break the infrastructure into multiple independent directories (e.g., `network/`, `database/`, `app/`) using Terragrunt or Terraform Cloud Workspaces, and link them using `terraform_remote_state` data sources. This shrinks the graph size and limits the blast radius."}
        ],
        "interview_prep": [
            {"q": "How do you prevent secrets from leaking in Terraform state?", "a": "State is stored in plaintext. You must encrypt the S3 backend, restrict IAM access, and never hardcode secrets. Use data sources like AWS Secrets Manager to fetch them at runtime."}
        ],
                "homework": {
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
            "deliverables": [
                        "Working WIF for GitHub Actions (zero keys)",
                        "Working Workload Identity for GKE pods (zero keys)",
                        "Proof that `gcloud auth list` inside a pod shows the GSA identity"
            ],
            "solution_hint": "The WIF attribute mapping must use `assertion.repository` for GitHub. For GKE, the node pool must have `workload_metadata_config { mode = GKE_METADATA }`. Test with `curl -H 'Metadata-Flavor: Google' metadata.google.internal/computeMetadata/v1/instance/service-accounts/`.",
            "real_world_context": "Workload Identity Federation is Google's answer to AWS OIDC roles. Every SOC2/ISO27001 compliant company must eliminate static credentials by 2026."
},
        "flashcards": [
            {"front": "Secrets Management", "back": "The practice of securely storing and accessing sensitive data (e.g., Vault, AWS Secrets Manager)."},
            {"front": "Static Analysis (SAST)", "back": "Analyzing code for security flaws without executing it (e.g., Checkov, TFSec)."},
            {"front": "Policy as Code", "back": "Defining and enforcing rules using code (e.g., OPA Rego)."}
        ],
        "challenge": {
            "title": "The Security Auditor",
            "description": "You found a resource 'aws_s3_bucket' 'data' with 'acl = \"public-read\"'. Write a Checkov-style rule (conceptually) or simply fix the Terraform code to make it private.",
            "hints": ["Change the ACL", "Public buckets are bad"],
            "solution": "resource \"aws_s3_bucket\" \"data\" {\n  bucket = \"...\"\n  acl    = \"private\"\n}"
        }
    },
    {
        "id": "10_ansible_intro",
        "title": "10. Ansible: Introduction & Setup",
        "quiz": [
            {"q": "What is the key difference between Ansible and Terraform?", "options": ["Ansible is for provisioning, Terraform for config", "Ansible is agent-based", "Ansible is typically for Configuration Management", "Terraform uses YAML"], "a": 2},
            {"q": "Does Ansible require an agent on managed nodes?", "options": ["Yes, always", "Only on Windows", "No, it is agentless", "Yes, the master agent"], "a": 2},
            {"q": "Which file defines the servers Ansible manages?", "options": ["ansible.cfg", "main.tf", "hosts.ini (Inventory)", "playbook.yaml"], "a": 2}
,
            {"q": "What is the implicit transport layer default Ansible relies upon for Linux targets?", "options": ["SNMP", "WinRM", "OpenSSH", "gRPC"], "a": 2},
            {"q": "How does Ansible handle parallel execution across nodes by default?", "options": ["Iterates linearly one by one", "Forks 5 processes simultaneously and batches the execution across the inventory", "Spawns infinite threads", "Delegates to Docker"], "a": 1},
            {"q": "What command structure would execute a raw shell command exclusively against nodes belonging to BOTH 'web' and 'db' groups?", "options": ["ansible 'web,db' -m shell -a 'uptime'", "ansible 'web:&db' -m shell -a 'uptime'", "ansible 'web!db' -m shell -a 'uptime'", "ansible all -m shell -a 'uptime'"], "a": 1},
            {"q": "Where does the Ansible control node natively store gathered device facts automatically without configuring a persistent cache?", "options": ["In memory during the playbook run", "In a local SQLite database", "In `/etc/ansible/facts`", "In an S3 bucket"], "a": 0},
            {"q": "What mechanism allows you to bypass the SSH paradigm to configure API endpoints (like an F5 Load Balancer)?", "options": ["You can't", "Using `connection: local` on the control node combined with the relevant API module", "Installing bash on the F5", "Using `connection: telnet`"], "a": 1},
            {"q": "If you run `ansible all -m setup`, what precisely are you doing?", "options": ["Installing Python on all nodes", "Gathering and printing the sprawling dictionary of System Facts for all inventory nodes", "Testing ping latency", "Formatting the inventory"], "a": 1}
,
            {"q": "What makes Ansible fundamentally different from Chef and Puppet in terms of node requirements?", "options": ["Ansible uses YAML", "Ansible is agentless \u2014 it requires zero software installation on managed nodes beyond Python and SSH", "Ansible is faster", "Ansible is free"], "a": 1}
        ],
        "interview_prep": [
            {"q": "Scenario: You must pass an API token to a terraform provider, but you cannot hardcode it in `.tfvars` due to security mandates. How do you inject it into Terraform securely?", "a": "You can export it as an environment variable in the CI/CD pipeline (e.g., `export TF_VAR_api_token=xyz`). Alternatively, use a secrets manager provider (like AWS Secrets Manager or HashiCorp Vault) to fetch the credential dynamically at runtime during the `terraform apply` phase."}
        ],
        "interview_prep": [
            {"q": "Ansible operates via Push, while puppet operates via Pull. What is the impact?", "a": "Push is agentless, meaning zero footprint on the target nodes. It simplifies security and scaling, though it requires persistent SSH access from the runner."}
        ],
                "homework": {
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
            "deliverables": [
                        "Working GCP dynamic inventory file",
                        "Security hardening playbook",
                        "Proof of fail2ban running on all VMs"
            ],
            "solution_hint": "Use `auth_kind: application` for Application Default Credentials. Filter VMs with `filters: [\"status = RUNNING\"]`. Group by labels using `keyed_groups: [{key: labels.env, prefix: env}]`.",
            "real_world_context": "Dynamic inventory is how Netflix and Spotify manage their fleets. Static inventory files become unmaintainable beyond 20 servers."
},
        "flashcards": [
            {"front": "Agentless", "back": "Ansible communicates over standard SSH or WinRM without installing endpoint software."},
            {"front": "Ad-hoc command", "back": "A quick, one-line Ansible command executed without a playbook."},
            {"front": "Inventory", "back": "A file or script defining the hosts and groups Ansible can manage."}
        ],
        "challenge": {
            "title": "The Ad-Hoc Ping",
            "description": "Write a command to ping all servers in the 'webservers' group using an inventory file named 'hosts.ini'.",
            "hints": ["ansible <group> -m <module> -i <inventory>"],
            "solution": "ansible webservers -m ping -i hosts.ini"
        }
    },
    {
        "id": "11_ansible_playbooks",
        "title": "11. Ansible: Playbooks & Modules",
        "quiz": [
            {"q": "What format are Ansible Playbooks written in?", "options": ["JSON", "XML", "HCL", "YAML"], "a": 3},
            {"q": "Why is the 'shell' module discouraged?", "options": ["It is too slow", "It is usually not idempotent", "It requires root", "It cannot be encrypted"], "a": 1},
            {"q": "How do you do a dry-run of a playbook?", "options": ["--dry", "--test", "--check", "--plan"], "a": 2}
,
            {"q": "During a playbook failure, what does the resulting `.retry` file contain?", "options": ["The error logs", "The specific list of hostnames that failed, allowing you to re-run the playbook exclusively targeted at them", "A backup of the previous configuration", "Instructions on how to fix it"], "a": 1},
            {"q": "In an Ansible task, what is the hierarchical relationship between `block`, `rescue`, and `always`?", "options": ["Rescue runs first", "Block executes; if it errors, Rescue executes to recover; Always executes regardless of Block/Rescue success, similar to try/catch/finally", "They run in parallel", "Always runs first"], "a": 1},
            {"q": "If you set `serial: 20%` inside a playbook targeting 100 webservers, what deployment pattern is established?", "options": ["A rolling update. It updates 20 servers at a time, moving to the next 20 only if the previous batch succeeds.", "It randomly skips 20% of servers", "It throttles bandwidth by 20%", "It fails immediately"], "a": 0},
            {"q": "To prevent an asynchronous, long-running job (like a massive DB schema update) from blocking the SSH connection indefinitely, which directives do you use?", "options": ["detach: true", "async: <seconds> and poll: 0 (or a set interval)", "background: true", "nohup: true"], "a": 1},
            {"q": "What is the primary difference between the `command` and `shell` modules?", "options": ["command requires root", "shell passes the command through `/bin/sh`, allowing pipes (|) and redirects (>), whereas command executes the executable directly without shell mechanics", "shell is deprecated", "no difference"], "a": 1},
            {"q": "How do you enforce idempotency on a `shell` module task that compiles a binary?", "options": ["Add `ignore_errors: true`", "Add the `creates: /path/to/binary` parameter. Ansible will gracefully skip the shell task if that file already exists.", "Run it twice", "You cannot"], "a": 1}
,
            {"q": "What does `changed_when: false` do on an Ansible task?", "options": ["Skips the task", "Forces the task to always report 'ok' status regardless of actual changes, preventing false-positive change notifications in idempotency checks", "Deletes the output", "Runs it twice"], "a": 1}
        ],
        "interview_prep": [
            {"q": "If a playbook fails midway, how do you resume without running everything again?", "a": "You can use the --start-at-task flag, or leverage retry files (.retry) from the failure point."}
        ],
                "homework": {
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
            "deliverables": [
                        "Structured roles under `roles/` directory",
                        "Vault-encrypted secrets file",
                        "Running WordPress site accessible via browser"
            ],
            "solution_hint": "Use `ansible-vault create secrets.yml` for MySQL passwords. Nginx upstream config: `upstream php { server unix:/var/run/php/php-fpm.sock; }`. Enable gzip compression in the Nginx template.",
            "real_world_context": "This is the classic Ansible use case. While Kubernetes is replacing this pattern, millions of production WordPress sites still run on VMs with Ansible-managed configurations."
},
        "flashcards": [
            {"front": "Playbook", "back": "A YAML file containing a list of plays to execute against an inventory."},
            {"front": "Module", "back": "The unit of code Ansible executes (e.g., apt, copy, service)."},
            {"front": "--check", "back": "The dry-run flag for ansible-playbook that simulates changes."}
        ],
        "challenge": {
            "title": "The Idempotent Installer",
            "description": "Write a single task (YAML syntax) using the 'apt' module to ensure 'nginx' is installed and at the latest version.",
            "hints": ["module is apt", "name: nginx", "state: latest"],
            "solution": "- name: Install Nginx\n  apt:\n    name: nginx\n    state: latest"
        }
    },
    {
        "id": "12_ansible_roles_advanced",
        "title": "12. Ansible: Roles, Vault & Dynamic Inventory",
        "quiz": [
            {"q": "What is an Ansible Role?", "options": ["A security permission", "A predefined directory structure for reuse", "An AWS IAM role", "A type of module"], "a": 1},
            {"q": "How do you encrypt a file with Ansible?", "options": ["ansible-encrypt", "ansible-vault encrypt", "gpg --encrypt", "terraform lock"], "a": 1},
            {"q": "What solves the problem of IP addresses changing constantly in AWS?", "options": ["Static IP configs", "DNS caching", "Dynamic Inventories", "Docker"], "a": 2}
,
            {"q": "In a Galaxy Role structure, what is the functional difference between `vars/main.yml` and `defaults/main.yml`?", "options": ["There is no difference", "`defaults/main.yml` provides baseline values with the absolute LOWEST precedence, easily overridden by any external variable. `vars/main.yml` provides internal role variables with HIGH precedence.", "vars is for passwords", "defaults is deprecated"], "a": 1},
            {"q": "When writing an Ansible Role, what directory inherently houses custom embedded Python modules packaged with the role?", "options": ["/python", "/library", "/modules", "/plugins"], "a": 1},
            {"q": "How does `ansible-pull` reverse the standard execution architecture?", "options": ["It uses FTP", "Instead of a central server pushing SSH commands, cronjobs on the target nodes periodically pull a Git repo and execute the playbook locally against `localhost`", "It pulls data from AWS", "It deletes servers"], "a": 1},
            {"q": "When configuring large dynamic inventories (e.g., thousands of EC2 endpoints), what severely bottlenecks the start time of the playbook, and how is it fixed?", "options": ["Bandwidth; use 5G", "Fact gathering; disable implicit gathering via `gather_facts: no` and rely on a centralized Redis/Memcached Fact Cache", "Python parsing; use Go", "YAML syntax"], "a": 1},
            {"q": "What specific file inside an Ansible Role dictates its dependencies upon other Galaxy roles?", "options": ["requirements.txt", "package.json", "meta/main.yml", "dependencies.yaml"], "a": 2},
            {"q": "If you encrypt a specific variable string inside a YAML file rather than encrypting the whole file, what feature are you using?", "options": ["GPG Inline", "Vault IDs", "Ansible Vault Inline String Encryption (`!vault |`)", "Base64"], "a": 2}
,
            {"q": "What is the purpose of `ansible-galaxy collection install` versus `ansible-galaxy role install`?", "options": ["They are identical", "Collections bundle roles, modules, plugins, and playbooks into a single distributable namespace package; roles are single-purpose automation units", "Collections are deprecated", "Roles include collections"], "a": 1}
        ],
        "interview_prep": [
            {"q": "How do you handle secrets inside Ansible roles securely in a public repo?", "a": "Use Ansible Vault to encrypt variables or files. Only store the vault password on the highly secure CI/CD runner."}
        ],
                "homework": {
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
                        "Schedule the playbook via Cloud Scheduler \u2192 Cloud Functions \u2192 Ansible Tower/AWX API."
            ],
            "deliverables": [
                        "Playbook fetching secrets from GCP Secret Manager",
                        "Patching role with automatic rollback",
                        "Compliance report uploaded to GCS bucket"
            ],
            "solution_hint": "For disk snapshots, use `gcloud compute disks snapshot` in a shell task before patching. The rescue block should restore from snapshot if `systemctl is-active nginx` fails. Use `csv` callback plugin for compliance reports.",
            "real_world_context": "This exact pipeline is used by healthcare and financial companies for HIPAA/PCI compliance. The snapshot-before-patch pattern prevents catastrophic outages."
},
        "flashcards": [
            {"front": "Ansible Galaxy", "back": "A repository of pre-packaged Ansible roles."},
            {"front": "Ansible Vault", "back": "A tool to encrypt passwords and secrets in your playbooks."},
            {"front": "Dynamic Inventory", "back": "A script/plugin that queries cloud providers to build the inventory on the fly."}
        ],
        "challenge": {
            "title": "The Vault Keeper",
            "description": "Write the command to execute 'secure.yaml' assuming it references an encrypted variable. You need Ansible to ask for the password.",
            "hints": ["--ask-vault-pass"],
            "solution": "ansible-playbook secure.yaml --ask-vault-pass"
        }
    },
    {
        "id": "13_k8s_intro",
        "title": "13. Kubernetes: Introduction",
        "quiz": [
            {"q": "What is the primary function of Kubernetes?", "options": ["Building docker images", "Container orchestration", "Virtual machine management", "Source code versioning"], "a": 1},
            {"q": "What is the smallest deployable unit in K8s?", "options": ["Container", "Pod", "Node", "Service"], "a": 1},
            {"q": "How does Kubernetes approach deployments?", "options": ["Imperatively", "Procedurally", "Declaratively", "Manually"], "a": 2}
,
            {"q": "What is the underlying Linux container primitive that heavily isolates a Pod's memory space?", "options": ["Chroot", "Linux Namespaces and Cgroups", "Hypervisors", "systemd"], "a": 1},
            {"q": "What exactly does a Kubernetes `Service` of type `ClusterIP` rely upon within the node operating system to route traffic?", "options": ["NGINX", "iptables or IPVS (managed by kube-proxy) programming local DNAT rules", "A physical hardware router", "DNS exclusively"], "a": 1},
            {"q": "When writing a Pod manifest, what `restartPolicy` guarantees a Batch Job will NOT restart endlessly after it successfully completes?", "options": ["Always", "Never or OnFailure", "Timeout", "Exit0"], "a": 1},
            {"q": "What component is directly responsible for mounting volumes into the underlying container runtime?", "options": ["kube-apiserver", "The Kubelet", "etcd", "kube-scheduler"], "a": 1},
            {"q": "If a Pod requires a dedicated GPU, how does the control plane know which node to place it on?", "options": ["It guesses", "The kube-scheduler analyzes the Pod's `resources.requests` and node labels/taints, then binds the Pod to a node with sufficient unallocated GPU capacity", "The user types the IP", "etcd routes it randomly"], "a": 1},
            {"q": "Why is running a container as `privileged: true` considered a massive security violation in K8s?", "options": ["It costs too much", "It completely bypasses cgroup isolation, granting the container near-root capabilities over the underlying host Kernel and Node hardware", "It exposes port 80", "It disables logging"], "a": 1}
,
            {"q": "What is the fundamental difference between a Pod and a Container in Kubernetes?", "options": ["They are the same", "A Pod is the smallest deployable unit that can contain one or more tightly-coupled containers sharing the same network namespace and storage volumes", "A Container is larger", "Pods run on the control plane"], "a": 1}
        ],
        "interview_prep": [
            {"q": "What happens if a Pod crashes continuously on startup?", "a": "K8s puts it into CrashLoopBackOff. You use kubectl logs --previous to view why the crash happened (e.g., missing env vars, OOMKilled)."}
        ],
                "homework": {
            "title": "First GKE Deployment \u2014 Containerized Web App",
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
            "deliverables": [
                        "Running GKE cluster with Nginx deployment",
                        "External IP serving Nginx",
                        "Proof of scaling from 3 to 5 replicas"
            ],
            "solution_hint": "GKE Autopilot manages nodes automatically \u2014 no node pool configuration needed. Use `kubectl describe svc` to debug pending LoadBalancer IPs. Add `readinessProbe` and `livenessProbe` for production readiness.",
            "real_world_context": "This is day-1 of every Kubernetes engineer's journey. GKE Autopilot is Google's recommended mode for most workloads since 2024."
},
        "flashcards": [
            {"front": "Pod", "back": "The smallest deployable computing unit you can create and manage in K8s, containing one or more containers."},
            {"front": "Declarative Model", "back": "You declare the desired state, and K8s makes the actual state match it."},
            {"front": "Self-Healing", "back": "K8s automatically restarts containers that fail health checks."}
        ],
        "challenge": {
            "title": "The Pod Definition",
            "description": "Write the bare minimum top-level YAML keys required for a Pod manifest (Hint: there are 4 main ones).",
            "hints": ["apiVersion, kind, metadata, spec"],
            "solution": "apiVersion: v1\nkind: Pod\nmetadata:\n  name: my-pod\nspec:\n  containers:\n  - name: dummy\n    image: dummy"
        }
    },
    {
        "id": "14_k8s_manifests",
        "title": "14. Kubernetes: Manifests & Core Resources",
        "quiz": [
            {"q": "Which K8s resource provides a stable IP address for ephemeral Pods?", "options": ["Deployment", "Service", "ReplicaSet", "Ingress"], "a": 1},
            {"q": "Why should you avoid deploying naked Pods?", "options": ["They are too large", "They don't self-heal if the Node dies", "They cost extra", "They bypass the firewall"], "a": 1},
            {"q": "Which tool sends YAML manifests to the K8s API?", "options": ["docker run", "kubectl", "helm", "kube-proxy"], "a": 1}
,
            {"q": "In a DaemonSet architecture, what determines if a Pod spins up on a newly joined cluster Node?", "options": ["A manual command", "A deployment trigger", "The DaemonSet Controller automatically evaluates the new Node. If it matches the nodeSelector/affinity, it instantly schedules exactly one Pod onto it", "Nothing"], "a": 2},
            {"q": "What happens to the previously established Pods when you delete a ReplicaSet but pass the `--cascade=orphan` (formerly `--cascade=false`) flag?", "options": ["They are corrupted", "The ReplicaSet API object is deleted, but the Pods are intentionally left running unmanaged in the cluster", "They instantly crash", "They freeze"], "a": 1},
            {"q": "Regarding Probes, what defines a situation where a Pod is running, but is NOT ready to receive HTTP traffic from a Service?", "options": ["Liveness Probe failed", "Readiness Probe failed", "Startup Probe failed", "Network crash"], "a": 1},
            {"q": "If an autoscaler defines `targetCPUUtilizationPercentage: 80`, what specifically does the HorizontalPodAutoscaler (HPA) algorithm do when traffic spikes?", "options": ["Kills the master node", "Queries the Metrics Server, dynamically calculates desired replicas based on CPU load, and updates the targeted Deployment/ReplicaSet scale count", "Requests more RAM", "Limits traffic"], "a": 1},
            {"q": "When a PersistentVolumeClaim (PVC) has `accessModes: ReadWriteOnce`, what physical limitation exists?", "options": ["It cannot be read", "The underlying storage volume can be firmly mounted as read-write by exactly ONE generic cluster Node at a time", "It cannot be written to", "Only one user can see it"], "a": 1},
            {"q": "What is an InitContainer, and what happens if it constantly fails?", "options": ["A fast container. The main pod runs anyway.", "A prep container that runs to completion before the main app starts. If it fails, K8s continually restarts the Pod, preventing the main application from ever starting.", "A logging daemon.", "A proxy."], "a": 1}
,
            {"q": "Why would you use a StatefulSet instead of a Deployment for a database workload?", "options": ["StatefulSets are faster", "StatefulSets provide stable, persistent network identities (ordinal naming) and ordered, graceful deployment/scaling, critical for databases requiring consistent storage bindings", "Deployments cannot use volumes", "StatefulSets use less RAM"], "a": 1}
        ],
        "interview_prep": [
            {"q": "Why use Deployments over bare Pods?", "a": "Deployments manage ReplicaSets, providing self-healing, rolling updates, and easy rollbacks if a deployment fails."}
        ],
                "homework": {
            "title": "Three-Tier Application on GKE with Cloud SQL",
            "objective": "Deploy a production-grade three-tier architecture: React frontend, Python API backend, and Cloud SQL PostgreSQL \u2014 all communicating securely within GKE.",
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
                        "Add NetworkPolicies to restrict: frontend \u2192 API only, API \u2192 SQL only.",
                        "Verify end-to-end: frontend calls API, API reads from Cloud SQL."
            ],
            "deliverables": [
                        "Three deployments (frontend, api, db-proxy) running on GKE",
                        "Cloud SQL accessible only via private IP and auth proxy",
                        "NetworkPolicies restricting traffic flow"
            ],
            "solution_hint": "Cloud SQL Auth Proxy runs at `127.0.0.1:5432` as a sidecar. Use `google_sql_database_instance` with `ipv4_enabled = false` for private-only access. NetworkPolicies require a CNI that supports them (GKE Dataplane V2).",
            "real_world_context": "This is the bread-and-butter architecture of 80% of production GKE workloads. The sidecar proxy pattern is Google's recommended way to connect to Cloud SQL."
},
        "flashcards": [
            {"front": "Deployment", "back": "Manages ReplicaSets and provides declarative updates to Pods."},
            {"front": "Service", "back": "An abstraction defining a logical set of Pods and a policy to access them."},
            {"front": "kubectl apply", "back": "The command declarative way to create or update resources from a file."}
        ],
        "challenge": {
            "title": "The Applicator",
            "description": "Write the command to apply a manifest named 'deployment.yaml' to your cluster.",
            "hints": ["use kubectl apply"],
            "solution": "kubectl apply -f deployment.yaml"
        }
    },
    {
        "id": "15_k8s_architecture",
        "title": "15. Kubernetes: Architecture",
        "quiz": [
            {"q": "Which component is the database of the K8s cluster?", "options": ["kube-apiserver", "etcd", "kubelet", "PostgreSQL"], "a": 1},
            {"q": "Which agent runs on every Worker Node?", "options": ["kubelet", "kube-scheduler", "kube-apiserver", "etcd"], "a": 0},
            {"q": "What exposes HTTP/HTTPS routes from outside the cluster to services within?", "options": ["NodePort", "Ingress", "ClusterIP", "kube-proxy"], "a": 1}
,
            {"q": "When the kube-scheduler binds a Pod to Node A, how does Node A actually receive the instruction to pull the image and start the Docker/containerd process?", "options": ["The scheduler SSHs into Node A", "The Kubelet on Node A continuously long-polls/watches the API Server. It notices a Pod bound to 'Node A' and initiates the runtime execution locally", "etcd sends an email", "A webhook is fired"], "a": 1},
            {"q": "What is the extreme consequence of etcd compaction failing and the database hitting its 2GB hard quota?", "options": ["Kubernetes runs faster", "etcd enters a read-only state. The entire Control Plane locks up, and you can no longer apply, delete, or update any resources until it is defragmented", "Pods crash", "Nodes restart"], "a": 1},
            {"q": "What mechanism does the Kube-APIServer use to authenticate incoming external webhook traffic BEFORE it processes authorization (RBAC)?", "options": ["Basic Auth", "Passwords", "X.509 Client Certificates, OIDC tokens, or Service Account Bearer Tokens", "IP whitelisting"], "a": 2},
            {"q": "Explain the architectural difference between a MutatingAdmissionWebhook and a ValidatingAdmissionWebhook.", "options": ["They are the same", "Mutating Webhooks intercept an API request (e.g. creating a Pod) and physically alter the JSON payload (like injecting a proxy sidecar). Validating Webhooks run AFTER mutation to strictly approve or reject the final object.", "Mutating destroys pods", "Validating writes code"], "a": 1},
            {"q": "What is the primary architectural bottleneck of the `kube-proxy` iptables mode when a cluster reaches 5,000+ services?", "options": ["Disk space", "iptables processes rules sequentially. 5,000 services mean massive sequential evaluations for every packet, causing exponential latency degradation. Migration to IPVS or eBPF becomes mandatory", "RAM usage", "Bandwidth caps"], "a": 1},
            {"q": "In a highly available (HA) multi-master K8s control plane, how is the `kube-controller-manager` prevented from running duplicate overlapping reconciliation loops?", "options": ["They talk over TCP", "Only one controller is active at a time via Lead Election mechanisms locked using native Kubernetes Leases/Endpoints, while the others remain on hot standby", "etcd balances them", "They all run together"], "a": 1}
,
            {"q": "What happens to running Pods if the kube-apiserver goes down temporarily?", "options": ["All Pods crash immediately", "Existing Pods continue running because the kubelet manages local Pod lifecycle independently. However, no new scheduling, scaling, or API operations can occur until the apiserver recovers", "Nodes reboot", "etcd deletes everything"], "a": 1}
        ],
        "interview_prep": [
            {"q": "What happens when you delete a pod?", "a": "The kube-apiserver updates etcd. The kubelet on the node sees the state change and sends a SIGTERM. The ReplicaSet controller notices the count is low and schedules a new pod."}
        ],
                "homework": {
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
            "deliverables": [
                        "HPA scaling pods based on CPU",
                        "Cluster Autoscaler adding/removing nodes",
                        "PDB protecting minimum availability"
            ],
            "solution_hint": "Resource requests are REQUIRED for HPA to work. Use `topologySpreadConstraints` to ensure pods spread across zones. The Cluster Autoscaler respects PDBs \u2014 it won't evict pods that would violate the budget.",
            "real_world_context": "This is exactly how Shopify and Mercado Libre prepare for Black Friday. The HPA + CA + PDB trio is the industry-standard resilience pattern."
},
        "flashcards": [
            {"front": "etcd", "back": "The highly-available key-value store acting as K8s' database."},
            {"front": "kubelet", "back": "The primary 'node agent' that ensures containers are running in a Pod."},
            {"front": "Ingress", "back": "An API object that manages external access to the services, usually HTTP."}
        ],
        "challenge": {
            "title": "Control Plane Anatomy",
            "description": "Name at least two core components of the Kubernetes Control Plane.",
            "hints": ["It manages API calls and scheduling", "kube-apiserver, etcd, etc"],
            "solution": "kube-apiserver and etcd"
        }
    },
    {
        "id": "16_helm_intro",
        "title": "16. Helm: The Kubernetes Package Manager",
        "quiz": [
            {"q": "What is Helm?", "options": ["A container runtime", "A package manager for K8s", "A service mesh", "A CI/CD tool"], "a": 1},
            {"q": "What is the Helm equivalent of a 'package'?", "options": ["Image", "Chart", "Manifest", "Tarball"], "a": 1},
            {"q": "How does Helm implement DRY?", "options": ["By deleting duplicate pods", "By using Go templates to make YAML dynamic", "By compressing images", "It relies on Terraform"], "a": 1}
,
            {"q": "When running `helm install`, where does Helm v3 natively store the exact binary release state information documenting the installation?", "options": ["In a Tiller pod", "As a Kubernetes Secret or ConfigMap directly inside the target namespace", "In an S3 bucket", "In local laptop metadata"], "a": 1},
            {"q": "How does Helm guarantee atomic deployments across multi-resource charts (e.g., ensuring the DB and the Web App both succeed, or both rollback)?", "options": ["It doesn't", "By using the `--atomic` flag. Helm waits for all resources to reach a Ready state. If they timeout, Helm automatically purges the release entirely.", "Using Terraform", "By pausing the cluster"], "a": 1},
            {"q": "Why did Helm v3 completely remove the `Tiller` server-side component?", "options": ["It was too slow", "Tiller required excessive root-level RBAC cluster permissions, creating a massive centralized security vulnerability footprint. Helm v3 now relies purely on your local kubeconfig RBAC context.", "It used too much RAM", "Google requested it"], "a": 1},
            {"q": "If you wish to pass an array of lists dynamically into a Helm chart without touching `values.yaml`, how do you format the CLI command?", "options": ["You cannot", "Use `helm install --set list\\[0\\]=a,list\\[1\\]=b`", "Use JSON strings", "Use basic comma strings"], "a": 1},
            {"q": "What happens during a `helm upgrade` if you have manually used `kubectl edit` to dramatically alter a deployment managed by Helm?", "options": ["Helm crashes", "Helm v3 uses an advanced 3-way strategic merge patch. It compares the old chart, the new chart, and the *current live cluster state*, ensuring manual additions aren't blindly destroyed unless they conflict directly.", "Helm deletes the deployment", "Helm ignores the upgrade"], "a": 1},
            {"q": "What does `helm template` specifically output during execution?", "options": ["The cluster URL", "The fully rendered raw YAML exactly as it would be sent to the API Server, allowing you to bypass Helm execution and apply via separate GitOps pipelines.", "An active release ID", "A zip file"], "a": 1}
,
            {"q": "What is the purpose of the `values.yaml` file in a Helm chart?", "options": ["It stores secrets", "It provides the default configuration values that feed into Go templates, allowing users to override any value at install time via --set or -f flags", "It defines the API version", "It is a lock file"], "a": 1}
        ],
        "interview_prep": [
            {"q": "What is the primary advantage of Helm over raw YAML manifests?", "a": "Helm uses Go templates and values.yaml to provide DRY deployments across multiple environments. You write the YAML once and inject dynamic variables."}
        ],
                "homework": {
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
            "deliverables": [
                        "Prometheus + Grafana running on GKE",
                        "Grafana accessible with Kubernetes dashboards",
                        "AlertManager configured for cluster alerts"
            ],
            "solution_hint": "Use `--set grafana.adminPassword=yourpass` or better, a Kubernetes Secret. For GKE, you may need to disable the default `kube-proxy` metrics since GKE uses Dataplane V2. Persistent volumes require a StorageClass.",
            "real_world_context": "The kube-prometheus-stack Helm chart is the #1 most installed chart globally. Every production Kubernetes cluster runs some form of Prometheus monitoring."
},
        "flashcards": [
            {"front": "Helm Chart", "back": "A bundle of information necessary to create an instance of a Kubernetes application."},
            {"front": "Helm Release", "back": "A running instance of a chart within a K8s cluster."},
            {"front": "Go Templates", "back": "The templating language Helm uses to dynamically inject values into YAML."}
        ],
        "challenge": {
            "title": "The Installer",
            "description": "Write the command to install a Helm chart named 'bitnami/nginx' and name the release 'my-web'.",
            "hints": ["helm install <release_name> <chart>"],
            "solution": "helm install my-web bitnami/nginx"
        }
    },
    {
        "id": "17_helm_charts",
        "title": "17. Helm: Creating Charts & Templating",
        "quiz": [
            {"q": "Which file holds the default configuration values for a Chart?", "options": ["Chart.yaml", "templates.yaml", "values.yaml", "config.json"], "a": 2},
            {"q": "How do you reference a value from values.yaml in a template?", "options": ["$value", "{{ .Values.myValue }}", "<myValue>", "${myValue}"], "a": 1},
            {"q": "What command generates a skeleton for a new chart?", "options": ["helm init", "helm create <name>", "helm new", "helm generate"], "a": 1}
,
            {"q": "What happens if a Helm release includes a `pre-upgrade` hook that strictly produces a non-zero exit code on failure, and it fails?", "options": ["Helm retries infinitely", "Helm aborts the deployment and leaves the release in a 'failed' state while preserving the previous deployment objects", "Helm rolls back automatically", "Helm ignores it"], "a": 1},
            {"q": "Inside a Helm template, what is the precise purpose of the `required` function syntax (e.g. `{{ required \"Password is required!\" .Values.dbPass }}`)?", "options": ["To encrypt the password", "To fail the template rendering explicitly during compilation if the user did not supply the mandatory Value in `values.yaml` or `--set`", "To pull data from K8s secrets", "To generate a random password"], "a": 1},
            {"q": "If you add `helm.sh/hook-delete-policy: hook-succeeded` to a Job manifest, what happens?", "options": ["The job runs forever", "The K8s garbage collector deletes the Job object ONLY after it completes successfully, preventing clutter from temporary migration pods", "It deletes the pod if it crashes", "It deletes the Helm chart"], "a": 1},
            {"q": "How does Helm v3 natively differ from Kustomize when handling YAML variants?", "options": ["Helm uses explicit text templating (Go templates), whereas Kustomize uses a base-and-overlay patching strategy without touching the original YAML lines", "Helm is for Ansible", "Kustomize uses Python", "They are identical"], "a": 0},
            {"q": "What specific file inside a Chart controls dependencies dynamically fetched from other remote Helm repositories?", "options": ["dependencies.yaml", "values.yaml", "requirements.txt", "Chart.yaml"], "a": 3},
            {"q": "What command strictly verifies the internal structural integrity and templating validity of your local `.tgz` Helm package without contacting a cluster?", "options": ["helm install", "helm test", "helm lint", "helm diff"], "a": 2}
,
            {"q": "How do you create a reusable Helm library chart that other charts can depend on?", "options": ["Use `type: application`", "Set `type: library` in Chart.yaml. Library charts cannot be installed directly but provide shared templates and helpers via the `_helpers.tpl` convention", "Use `kind: Library`", "Library charts are deprecated"], "a": 1}
        ],
        "interview_prep": [
            {"q": "How do you rollback a failed Helm deployment?", "a": "You run helm ls to find the revision history, and then helm rollback <release-name> <revision-number> to instantly restore the old stable state."}
        ],
                "homework": {
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
            "deliverables": [
                        "Custom Helm chart with conditional templates",
                        "Chart published to Artifact Registry",
                        "Successful installation from the remote registry"
            ],
            "solution_hint": "Use `{{ if .Values.autoscaling.enabled }}` for conditional HPA rendering. Artifact Registry supports OCI format natively \u2014 no `helm repo add` needed. Use `helm template` to test rendering locally before pushing.",
            "real_world_context": "Artifact Registry replaced Container Registry as Google's recommended image/chart store. OCI-based Helm repositories are the 2026 standard, replacing ChartMuseum."
},
        "flashcards": [
            {"front": "values.yaml", "back": "The file containing default values that templates will use."},
            {"front": "helm create", "back": "Bootstraps a new Helm chart directory structure."},
            {"front": "helm template", "back": "Renders chart templates locally and displays the output YAML."}
        ],
        "challenge": {
            "title": "The Dry Run",
            "description": "Write a command to test an installation of a local directory './my-chart' as the release 'test-app' without actually applying it to the cluster.",
            "hints": ["--dry-run", "--debug"],
            "solution": "helm install test-app ./my-chart --dry-run --debug"
        }
    },
    {
        "id": "18_advanced_tf",
        "title": "18. Advanced Terraform & FinOps",
        "quiz": [
            {"q": "What problem does Terragrunt primarily solve?", "options": ["It acts as a Terraform GUI", "It keeps configs DRY over multiple environments", "It scans for security issues", "It writes Python code"], "a": 1},
            {"q": "What tool calculates the cost of a Terraform plan?", "options": ["Checkov", "tfsec", "Infracost", "Terraform Cloud"], "a": 2},
            {"q": "Which tool generates Terraform JSON using languages like Python/TypeScript?", "options": ["Terraform CDK", "Terragrunt", "Ansible", "Kubernetes"], "a": 0}
,
            {"q": "When deploying Terragrunt at scale across hundreds of AWS Accounts, what is the safest way to orchestrate role assumption?", "options": ["Hardcode root keys", "Utilize OIDC authentication from the CI/CD pipeline pointing directly to the target Account's IAM Cross-Account roles via native backend trust policies", "Store keys in GitHub", "Use an EC2 instance profile on a bastion host"], "a": 1},
            {"q": "If someone accidentally breaks the `.terragrunt-cache` directory locally, what is the immediate resolution?", "options": ["Run apply", "Format the drive", "You simply delete the cache directory entirely and run `terragrunt init` again to re-download the remote modules", "It cannot be fixed"], "a": 2},
            {"q": "What mechanism does Infracost use to map specific Terraform resources to real-world cloud billing prices dynamically?", "options": ["Regex matching", "Infracost parses the proprietary TF execution plan JSON, matches the schema IDs against its Cloud Pricing API graph, and calculates hourly metrics", "It scrapes the AWS Console", "It uses Cost Explorer"], "a": 1},
            {"q": "How does the `tflint` engine differ from the native `terraform validate`?", "options": ["`terraform validate` just checks HCL syntax and internal references. `tflint` dynamically queries cloud provider APIs to ensure validity against reality (e.g., verifying if an EC2 instance class actually exists built-in).", "They are the exact same", "`tflint` costs money", "Validation is deprecated"], "a": 0},
            {"q": "Why is utilizing Terraform CDK over raw HCL sometimes viewed as risky in strict highly-regulated enterprises?", "options": ["CDK is slower", "Generative Python/TS CDK code creates an abstraction layer. Debugging complex state failures often forces engineers to reverse-engineer thousands of lines of auto-synthesized HCL JSON instead of directly reading readable config files.", "It does not support AWS", "It uses Docker"], "a": 1},
            {"q": "What is the primary architectural function of Terragrunt's `generate` block?", "options": ["To make code", "To dynamically write `.tf` files (like standardized provider block definitions or backend configs) into child directories before Terraform is executed, enforcing DRY configuration", "To generate passwords", "To deploy pods"], "a": 1}
,
            {"q": "What is the primary benefit of using Terragrunt's `include` block in a multi-account AWS setup?", "options": ["It includes CSS", "It allows child modules to inherit and merge parent configurations (like backend and provider blocks) from a root `terragrunt.hcl`, eliminating massive DRY violations across hundreds of directories", "It includes Python", "It speeds up terraform init"], "a": 1}
        ],
        "interview_prep": [
            {"q": "How does Infracost shift-left Cloud FinOps?", "a": "Infracost reads the Terraform Plan output in the CI/CD pipeline and blocks the PR if the cost delta exceeds a defined budget, catching expensive mistakes before they are applied."}
        ],
                "homework": {
            "title": "Terragrunt Multi-Project GCP Organization",
            "objective": "Use Terragrunt to manage a multi-project GCP organization with DRY configurations, cascading variables, and cross-project dependencies.",
            "platform": "Google Cloud Platform",
            "difficulty": "Expert",
            "scenario": "Your company has 12 GCP projects across 3 environments. Managing them with vanilla Terraform is a maintenance nightmare. Migrate to Terragrunt for DRY infrastructure management.",
            "steps": [
                        "Structure: `terragrunt.hcl` (root) \u2192 `dev/staging/prod/` \u2192 `networking/compute/gke/` subdirectories.",
                        "Root `terragrunt.hcl`: Define the GCS remote backend with dynamic project/env pathing.",
                        "Use `include` blocks so child configs inherit the backend and provider settings.",
                        "Define `inputs` in each environment's `env.hcl` (region, project_id, labels).",
                        "Use `dependency` blocks to pass VPC output to GKE: `dependency \"vpc\" { config_path = \"../networking\" }`.",
                        "Add `generate` blocks to write standardized provider configs in every directory.",
                        "Run `terragrunt run-all plan` from the environment root to see all changes at once.",
                        "Implement CI/CD with `terragrunt run-all apply --terragrunt-non-interactive` in Cloud Build."
            ],
            "deliverables": [
                        "Full Terragrunt directory structure for 3 environments",
                        "Cross-project dependencies working via `dependency` blocks",
                        "Single `run-all plan` showing unified change preview"
            ],
            "solution_hint": "Use `path_relative_to_include()` for dynamic backend key pathing. `dependency` blocks create an implicit DAG \u2014 Terragrunt handles the apply order automatically. Use `mock_outputs` for plan-only runs without existing state.",
            "real_world_context": "Gruntwork (Terragrunt's creator) manages infrastructure for hundreds of enterprises. This exact directory structure is their 'Reference Architecture' used by companies like Duolingo."
},
        "flashcards": [
            {"front": "Terragrunt", "back": "A thin wrapper that provides extra tools and keeps HCL configurations DRY."},
            {"front": "Infracost", "back": "A CI/CD tool that generates cost estimates directly from terraform plan data."},
            {"front": "Terraform CDK", "back": "Cloud Development Kit - Defines infrastructure using familiar programming languages."}
        ],
        "challenge": {
            "title": "The FinOps Enforcer",
            "description": "Write the command to execute Infracost on the current directory, generating a breakdown in JSON format, and save it to 'report.json'.",
            "hints": ["infracost breakdown", "--format json", "> report.json"],
            "solution": "infracost breakdown --path . --format json > report.json"
        }
    },
    {
        "id": "19_advanced_ansible",
        "title": "19. Advanced Ansible & CI/CD",
        "quiz": [
            {"q": "What is Ansible Molecule used for?", "options": ["Writing playbooks", "Testing Ansible roles iteratively", "Encrypting secrets", "Deploying to production"], "a": 1},
            {"q": "What is an Execution Environment (EE)?", "options": ["A virtual machine", "A container image with ansible-core and dependencies pre-installed", "A python script", "A cloud server"], "a": 1},
            {"q": "Instead of a static hosts.ini, how do you scale dynamic AWS instances?", "options": ["AWS CLI", "Dynamic Inventory Plugin (aws_ec2)", "Terraform Import", "Manual entry"], "a": 1}
,
            {"q": "If you define an `ansible.builtin.assert` block inside a CI pipeline and it fails, what happens to the pipeline execution?", "options": ["The pipeline is ignored", "Ansible throws a fatal error and produces a non-zero exit code, physically halting the Jenkins/GitLab pipeline execution step", "It emails the admin", "It skips the host"], "a": 1},
            {"q": "Inside an Execution Environment (EE), what is `ansible-builder` specifically used for?", "options": ["Editing YAML", "Parsing Dockerfiles incrementally to dynamically construct the container image encapsulating `ansible-core`, Python libraries, and mapped Collections", "Running the playbook", "Configuring passwords"], "a": 1},
            {"q": "When configuring AWS inventory generation via `aws_ec2.yml`, what is the precise parameter that stops Ansible from caching the inventory indefinitely?", "options": ["refresh: true", "flush_cache: true", "cache_timeout: <seconds>", "cache: false"], "a": 2},
            {"q": "In massive horizontal scaling (e.g. 5,000 servers), why does SSH multiplexing (ControlMaster) substantially drop playbook execution latency?", "options": ["It compresses the payload", "It reuses an existing, persistent TCP/SSH connection socket for multiple consecutive module executions, bypassing the heavy cryptographic SSH handshake overhead for every single task", "It removes encryption", "It runs Python locally"], "a": 1},
            {"q": "If you are targeting a Windows endpoint, what implicit transport layer protocol natively guarantees encrypted configuration logic delivery?", "options": ["SSHv2", "WinRM functioning over HTTPS port 5986", "SNMP", "TCP Port 80"], "a": 1},
            {"q": "What specifically separates Ansible Automation Platform (AAP/Tower) from generic cron-based Ansible executions?", "options": ["AAP uses Go", "AAP introduces Role-Based Access Control (RBAC), credential masking, execution environment isolation per team, and granular REST API scheduling.", "AAP is free", "AAP destroys faster"], "a": 1}
,
            {"q": "What is the primary advantage of Mitogen over standard Ansible SSH transport?", "options": ["It uses UDP", "Mitogen establishes a persistent in-memory Python interpreter on the remote node, eliminating the overhead of repeated SSH connections and temporary file transfers per task", "It uses gRPC", "It encrypts logs"], "a": 1}
        ],
        "interview_prep": [
            {"q": "What is the key advantage of an Ansible Execution Environment (EE)?", "a": "An EE is an OCI-compliant container image bundling ansible-core, collections, and python dependencies. It guarantees playbooks run identically on the developer laptop and in production AWX/Tower."}
        ],
                "homework": {
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
            "deliverables": [
                        "Custom Execution Environment published to Artifact Registry",
                        "Cloud Run service executing Ansible playbooks",
                        "Keyless GCP API authentication via Workload Identity"
            ],
            "solution_hint": "The EE base image should be `quay.io/ansible/ansible-runner:latest`. Cloud Run has a 60-minute timeout max \u2014 sufficient for most playbooks. Use `ansible-runner` Python API for programmatic execution.",
            "real_world_context": "Red Hat's Ansible Automation Platform uses Execution Environments as the standard deployment unit. Running them on Cloud Run creates a serverless automation platform."
},
        "flashcards": [
            {"front": "Molecule", "back": "A testing framework for Ansible roles using ephemeral infrastructure like Docker."},
            {"front": "Execution Environment", "back": "A standardized container image encapsulating Ansible so it runs consistently anywhere."},
            {"front": "Dynamic Inventory", "back": "A script or plugin that queries cloud providers directly to target ephemeral nodes."}
        ],
        "challenge": {
            "title": "Molecule Dry Run",
            "description": "Write the command to execute the default Molecule testing sequence on your role without destroying the test infrastructure afterward.",
            "hints": ["molecule test", "--destroy never"],
            "solution": "molecule test --destroy never"
        }
    },
    {
        "id": "20_advanced_k8s",
        "title": "20. Advanced K8s: eBPF & Zero-Trust",
        "quiz": [
            {"q": "What does eBPF replace in modern Kubernetes clusters?", "options": ["etcd", "Heavy user-space sidecar proxies", "kube-apiserver", "Deployments"], "a": 1},
            {"q": "Which tool issues short-lived SVID tokens to K8s Pods for Zero-Trust authentication?", "options": ["Cilium", "Helm", "SPIFFE/SPIRE", "ArgoCD"], "a": 2},
            {"q": "What model does ArgoCD use to synchronize clusters?", "options": ["Imperative push", "Manual apply", "Pull-based GitOps", "SSH scripting"], "a": 2}
,
            {"q": "When implementing ArgoCD inside an On-Premise bare-metal cluster, what fundamentally prevents external firewalls from blocking deployments?", "options": ["ArgoCD uses Ping", "ArgoCD utilizes a highly secure Pull Model: it initiates outbound TCP/443 requests from the internal cluster out to Github, effectively bypassing inbound NAT/Firewall blocks", "We use VPNs", "ArgoCD opens Port 22"], "a": 1},
            {"q": "If Cilium is acting as the CNI and entirely replacing kube-proxy, how does it process `ClusterIP` network routing without IPTables?", "options": ["DNS spoofing", "It dynamically compiles socket-layer BPF programs inserted directly into the Linux kernel networking stack algorithms, natively translating DNAT operations via high-performance maps", "It routes traffic through a physical switch", "It relies on Docker"], "a": 1},
            {"q": "Under the SPIFFE/SPIRE architecture in Kubernetes, what cryptographic object is generated to prove a Pod's Identity (SVID)?", "options": ["A Basic Auth password", "An ephemeral, strictly-scoped X.509 Certificate or JWT token automatically rotated by the SPIRE agent on the node", "An AWS IAM Key", "An SSL cert valid for 10 years"], "a": 1},
            {"q": "How does Karpenter fundamentally differ from the standard Cluster Autoscaler (CAS)?", "options": ["Karpenter is slower", "Karpenter dynamically calculates pod constraints and requests JUST-IN-TIME bare-metal/EC2 instances that exclusively fit those dimensions without mimicking traditional Node Groups or ASGs", "Karpenter uses Python", "They are identical"], "a": 1},
            {"q": "In an eBPF observability stack, what does Hubble natively provide over traditional Prometheus scraping?", "options": ["It stores logs forever", "It provides highly-granular L3/L4/L7 flow visibility directly from the kernel dataplane without modifying application code or deploying heavy sidecar proxies", "It formats YAML", "It sends cheaper metrics"], "a": 1},
            {"q": "If an ArgoCD application object reads an `OutOfSync` condition, what precisely does it mean?", "options": ["The cluster is down", "The actual deployed objects inside Kubernetes differ systematically from the declarative YAML stored in the monitored Git repository", "The Github repo is offline", "Docker is full"], "a": 1}
,
            {"q": "What problem does a Service Mesh like Istio or Linkerd solve that standard Kubernetes Services do not?", "options": ["DNS resolution", "Service Meshes provide transparent mTLS encryption, advanced traffic splitting, circuit breaking, and L7 observability between microservices without modifying application code", "Pod scheduling", "Storage provisioning"], "a": 1}
        ],
        "interview_prep": [
            {"q": "Why is GitOps via ArgoCD considered superior to Jenkins push deployment for K8s?", "a": "Jenkins pushes manifests imperatively. ArgoCD sits INSIDE the K8s cluster and continuously pulls the Git state. If someone manually changes a deployment in production, ArgoCD immediately syncs it back to the Git state, preventing undocumented drift."}
        ],
                "homework": {
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
            "deliverables": [
                        "ArgoCD managing all GKE deployments via Git",
                        "Automatic sync on Git push",
                        "Cilium network policies with Hubble observability"
            ],
            "solution_hint": "ArgoCD initial password: `kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d`. GKE Dataplane V2 IS Cilium \u2014 no separate installation needed. Use `CiliumNetworkPolicy` for L7-aware policies.",
            "real_world_context": "ArgoCD + Cilium is the 2026 Cloud Native standard. ArgoCD has 18k+ GitHub stars and is used by Intuit, Tesla, and Red Hat. Cilium powers GKE's networking layer."
},
        "flashcards": [
            {"front": "eBPF", "back": "Extended Berkeley Packet Filter - Runs sandboxed programs in the OS kernel for high-perf observability."},
            {"front": "SPIFFE", "back": "Secure Production Identity Framework for Everyone - standards for securing identities between workloads."},
            {"front": "ArgoCD", "back": "A declarative, GitOps continuous delivery tool for Kubernetes."}
        ],
        "challenge": {
            "title": "The GitOps Sync",
            "description": "Imagine you are using ArgoCD CLI. Write the command to trigger an immediate synchronization (sync) for an application named 'core-api'.",
            "hints": ["argocd app sync <appname>"],
            "solution": "argocd app sync core-api"
        }
    },
    {
        "id": "21_interview_tf",
        "title": "21. Interview: Terraform Architecture",
        "quiz": [
            {"q": "Boss Level: During a state recovery, if you `terraform state rm aws_instance.web`, what happens to the physical ec2 server?", "options": ["It is destroyed via API.", "Nothing physical happens; it is merely forgotten by the tracking file.", "It is stopped.", "It is marked for recreation."], "a": 1}
,
            {"q": "If a provider changes their API violently and a Terraform resource becomes permanently corrupted in your state (`terraform apply` constantly crashes on deserialization), how do you forcefully evict it?", "options": ["terraform delete", "terraform force-unlock", "Delete the .tf file", "terraform state rm <resource_identifier>"], "a": 3},
            {"q": "What happens if two Jenkins pipelines execute `terraform apply` simultaneously using the SAME local state file location (no backend)?", "options": ["Terraform creates a lock.", "Data corruption. The processes will aggressively overwrite the local JSON file simultaneously, causing massive graph serialization faults.", "Wait, then apply.", "It merges the files."], "a": 1},
            {"q": "Explain how to circumvent the 'Provider Configuration Invalid' error when the provider logic fundamentally requires values that are dynamically created during the same apply.", "options": ["Use external scripts", "Terraform architecture inherently restricts this. You must use decoupled deployments (e.g. Terragrunt layers), deploying the dependencies first, writing to state, and pulling them as purely static inputs in the lower-tier module.", "Write a bash script", "Use the `-refresh` flag"], "a": 1},
            {"q": "When writing reusable code, why do Senior Engineers favor `optional(string)` arguments inside object variable constraint types?", "options": ["It looks cleaner", "It drastically reduces configuration footprint for module consumers by establishing deep native default schemas inside heavily nested dictionaries.", "It saves AWS costs", "It hides secrets"], "a": 1},
            {"q": "In a scenario involving thousands of security rules, what Terraform primitive minimizes JSON payload sizes to AWS?", "options": ["Multiple Security Group modules", "A single dynamic block wrapped in an aggregate rule API payload, compressing massive independent HCL logic into one serialized JSON API push.", "Count arrays", "It doesn't matter."], "a": 1},
            {"q": "How do you forcefully intercept state migrations when upgrading from Terraform version 0.12 to 1.5 across breaking changes?", "options": ["Use `terraform init -upgrade` iteratively through middle versions (e.g. 0.13, 0.14) because state file formats shifted strictly between generations.", "You don't, you just use 1.5.", "Change the text in state.", "Re-apply everything."], "a": 0},
            {"q": "What occurs when the `create_before_destroy` lifecycle parameter triggers an AWS IP collision?", "options": ["Terraform aborts.", "The plan evaluates cleanly, but the apply forces a destructive hard-crash midway during the CREATE phase, stranding the environment gracefully.", "AWS modifies the quota.", "It overwrites the IP."], "a": 1},
            {"q": "What is the structural risk of using `data` sources aggressively for dynamic dependencies like VPC IDs across thousands of nodes?", "options": ["It doesn't matter", "They trigger API rate-limiting issues implicitly during the `terraform plan` phase because Terraform pulls the data synchronously before establishing the graph execution.", "It deletes nodes.", "It bypasses IAM."], "a": 1},
            {"q": "How do you correctly handle external third-party Terraform providers not found in the HashiCorp registry inside a strict Air-Gapped enterprise?", "options": ["Download manually.", "Configure a filesystem mirror using `provider_installation` block mapping in `.terraformrc`, pointing to a local directory loaded with the pre-compiled checksummed binaries.", "Contact HashiCorp.", "You cannot."], "a": 1}
        ],
        "interview_prep": [
            {"q": "Scenario: A developer ran 'terraform apply' and crashed midway. The remote state is now completely locked and the deployment is half-baked. How do you recover?", "a": "First, manually force-unlock the state using `terraform force-unlock <LOCK_ID>`. Then, carefully assess the actual infrastructure delta. You may need to run `terraform refresh` or use `terraform import` / `terraform state rm` to manually align the HCL state file with reality before attempting another apply."},
            {"q": "What is the tradeoff between Terraform Workspaces and Terragrunt for Multi-environment scaling?", "a": "Workspaces use the same backend and code, which is dangerous if someone runs 'destroy' in the wrong workspace. They are better suited for ephemeral PR environments. Terragrunt is preferred for strict Production scaling because it maps separate directories (dev/staging/prod) to physically isolated remote backend states, ensuring failure domains remain completely independent."},
            {"q": "How would you handle a circular dependency deadlock (Resource A needs Resource B, Resource B needs Resource A)?", "a": "You must decouple the resources. In Terraform, this usually means separating the components. For example, if two Security Groups must allow traffic to each other, you create BOTH Security Groups first with no inbound rules. Then, you use standalone `aws_security_group_rule` resources to inject the references asynchronously."}
        ],
                "homework": {
            "title": "Interview Lab: End-to-End GCP Infrastructure Deployment",
            "objective": "Under interview conditions (45 minutes), design and deploy a complete GCP infrastructure stack: networking, compute, database, and CI/CD \u2014 demonstrating senior-level Terraform mastery.",
            "platform": "Google Cloud Platform",
            "difficulty": "Expert",
            "scenario": "INTERVIEW PROMPT: 'You have 45 minutes. Deploy a production-ready GCP environment for a web application. Show me your architecture, explain your decisions, and handle the follow-up questions.'",
            "steps": [
                        "MINUTE 0-5: Sketch the architecture on a whiteboard \u2014 VPC, subnets, GKE, Cloud SQL, Load Balancer.",
                        "MINUTE 5-15: Write the VPC module with private subnets, Cloud NAT, and firewall rules.",
                        "MINUTE 15-25: Write the GKE module with private nodes, Workload Identity, and autoscaling.",
                        "MINUTE 25-35: Write Cloud SQL with private IP, automated backups, and read replicas.",
                        "MINUTE 35-40: Wire everything together with proper IAM and output the connection strings.",
                        "MINUTE 40-45: Run `terraform plan` and explain every resource to the interviewer.",
                        "FOLLOW-UP: Be prepared to explain state locking, import strategy, and disaster recovery.",
                        "FOLLOW-UP: Explain how you'd implement blue-green deployments with this infrastructure."
            ],
            "deliverables": [
                        "Complete infrastructure deployed in <45 minutes",
                        "Clear verbal explanation of every architectural decision",
                        "Answers to follow-up questions demonstrating deep understanding"
            ],
            "solution_hint": "Start with the VPC \u2014 everything depends on it. Use `google_compute_global_address` + `google_service_networking_connection` for Cloud SQL private IP. Keep modules simple during interviews \u2014 avoid over-engineering.",
            "real_world_context": "This simulates a real Staff/Principal DevOps interview at Google, Meta, or Stripe. The key is demonstrating architectural reasoning, not just code syntax."
},
        "flashcards": [
            {"front": "force-unlock", "back": "A dangerous command used to break a backend lock on a crashed terraform operation."},
            {"front": "Failure Domain Isolation", "back": "The primary reason why separate directories/Terragrunt are preferred over Workspaces for production isolation."},
            {"front": "aws_security_group_rule", "back": "A standalone linking resource used to break SG circular dependencies."}
        ],
        "challenge": {
            "title": "The Deadlock Decoupler",
            "description": "Examine this deadlock: SG 'a' ingress points to SG 'b'. Assuming both are created, write the standalone ingress rule code for SG 'a' allowing port 443 from SG 'b'.",
            "hints": ["resource \"aws_security_group_rule\" ..."],
            "solution": "resource \"aws_security_group_rule\" \"a_allow_b\" {\n  type = \"ingress\"\n  from_port = 443\n  to_port = 443\n  protocol = \"tcp\"\n  security_group_id = aws_security_group.a.id\n  source_security_group_id = aws_security_group.b.id\n}"
        }
    },
    {
        "id": "22_interview_ansible",
        "title": "22. Interview: Ansible Operations",
        "quiz": [
            {"q": "Boss Level: What is the defining trait of an Ansible `fact` cache in high performance large-scale deployments?", "options": ["It bypasses the gathering phase completely by recalling saved node realities.", "It deletes old variables.", "It uses a MySQL database.", "It encrypts logs."], "a": 0}
,
            {"q": "If you deploy an Ansible Playbook heavily relying on `ansible_env` facts, what happens if the target machine utilizes a restricted `/bin/sh` shell environment?", "options": ["It works normally.", "The facts return blank.", "The playbook fundamentally fails execution errors due to native Python parsing breaking over missing baseline variables injected natively by full POSIX shells (like bash).", "It changes permissions."], "a": 2},
            {"q": "Explain how to circumvent standard SSH latency constraints natively within the Ansible `ansible.cfg` when processing 200,000 files.", "options": ["Use the `strategy: free` to bypass linear host sequencing, immediately paired with `pipelining = True` to halt multi-stage directory pushes.", "Buy faster servers.", "Use an agent.", "Compress the files manually."], "a": 0},
            {"q": "What is the architectural impact of changing the execution strategy from `linear` to `free` in a rolling deployment?", "options": ["It doesn't change anything.", "The playbook abandons synchronization. Hosts race to the end individually without waiting for other nodes to complete the current horizontal task layer, destroying rolling consistency.", "It crashes Jenkins.", "It costs more CPU."], "a": 1},
            {"q": "If a Vault password is provided via a python script (`--vault-password-file script.py`), what exact security requirement exists on the script file?", "options": ["None.", "It must be executable by the user invoking Ansible, and output the raw plaintext password exclusively to stdout upon invocation.", "It must be encrypted.", "It must use Docker."], "a": 1},
            {"q": "What occurs when multiple developers push distinct Ansible `roles` utilizing conflicting internal variable structures without using role prefixes?", "options": ["Syntax error.", "Global Variable Namespace Collisions. Because variables scope globally in playbooks, the last-loaded role violently overwrites the previous variables, causing silent logic shifts without failing.", "It skips the roles.", "Docker isolates them."], "a": 1},
            {"q": "When writing custom Python modules for Ansible, what native method allows seamless JSON payload streaming back to the controller?", "options": ["print()", "sys.exit()", "The built-in `AnsibleModule.exit_json()` library call seamlessly translates the dictionary into standardized stdout structures.", "Writing to a file."], "a": 2},
            {"q": "In high-security networks utilizing Bastion Hosts, how is Ansible architected to dynamically traverse the proxy natively?", "options": ["It uses VPNs.", "Configuring `ProxyJump` proxy commands implicitly within the `ansible_ssh_common_args` parameter within the dynamic inventory definition.", "It cannot bypass proxies.", "It installs an agent on the bastion."], "a": 1},
            {"q": "What is the consequence of utilizing the `template` module aggressively inside a high-frequency `for_each` loop spanning 5,000 strings?", "options": ["It finishes quickly.", "It destroys the control node.", "Catastrophic CPU saturation on the Automation controller, as the Jinja2 rendering engine evaluates the templating tree syntactically *before* the SSH distribution phase.", "It formats YAML automatically."], "a": 2},
            {"q": "How does AAP (Tower) implicitly guarantee playbook consistency if the underlying Linux OS libraries of the execution node routinely change?", "options": ["It ignores changes.", "Through Execution Environments. Playbooks operate strictly inside deterministic OCI-compliant Podman containers loaded securely via immutable registries.", "It installs packages locally.", "It uses Terraform."], "a": 1}
        ],
        "interview_prep": [
            {"q": "Performance Scenario: Your playbook takes 45 minutes to run across 1,000 nodes. How do you drastically reduce this execution time?", "a": "1) Increase the `forks` count in ansible.cfg to run more parallel SSH connections. 2) Enable SSH pipelining to reduce the number of SSH handshakes per module. 3) Replace the standard SSH connection plugin with `mitogen` for persistent, optimized node communication. 4) Use async polling for long-running blocking tasks."},
            {"q": "You wrote a playbook using the `shell` module to restart a service. During a PR review, a Senior Engineer rejects it due to 'Idempotency failure'. What does this mean?", "a": "The `shell` module runs blindly every single time, meaning the system state changes regardless of its initial condition (it always registers as 'changed'). To fix this, you must use a declarative module like `systemd` or `service` which checks the state first, or at minimum, append a `creates` or `removes` conditional parameter to the shell module."},
            {"q": "How does Ansible handle dynamic ephemeral scaling in AWS, where IP addresses change instantly?", "a": "We abandon static `hosts.ini` files. We use the `aws_ec2` dynamic inventory plugin. Ansible reaches out directly to the AWS API authenticating via IAM roles, filters instances by tags (e.g. `role: webserver`), and maps their current dynamic public/private IPs at runtime."}
        ],
                "homework": {
            "title": "Interview Lab: Zero-Downtime Configuration Management Pipeline",
            "objective": "Under interview conditions (45 minutes), design and implement an Ansible pipeline that performs rolling configuration updates across a GCE fleet with zero downtime.",
            "platform": "Google Cloud Platform",
            "difficulty": "Expert",
            "scenario": "INTERVIEW PROMPT: 'We have 50 production VMs running a critical API. Show me how you'd update the Nginx configuration across all of them with zero downtime, automatic rollback, and an audit trail.'",
            "steps": [
                        "MINUTE 0-5: Explain the rolling update strategy \u2014 serial: 5 (10% at a time).",
                        "MINUTE 5-15: Write the GCP dynamic inventory with label-based grouping.",
                        "MINUTE 15-25: Write the rolling update playbook with `serial`, `max_fail_percentage`, and health checks.",
                        "MINUTE 25-35: Implement block/rescue for automatic rollback on health check failure.",
                        "MINUTE 35-40: Add the audit trail \u2014 log every change to a GCS bucket with timestamps.",
                        "MINUTE 40-45: Demonstrate the pipeline and explain the failure scenarios.",
                        "FOLLOW-UP: How would you handle a scenario where rollback also fails?",
                        "FOLLOW-UP: How does this scale to 5,000 servers across 3 regions?"
            ],
            "deliverables": [
                        "Rolling update playbook with serial batching",
                        "Automatic rollback mechanism",
                        "Audit trail uploaded to GCS"
            ],
            "solution_hint": "Use `serial: '10%'` for percentage-based batching. Health checks: `wait_for: port=80 timeout=30`. Rollback: keep a backup of the previous config and restore it in the `rescue` block. Scale: use `strategy: free` + `forks: 50` for parallelism.",
            "real_world_context": "This is the canonical Ansible interview question for Senior positions. LinkedIn, Uber, and Datadog all ask variations of this in their SRE interviews."
},
        "flashcards": [
            {"front": "Mitogen", "back": "An alternative connection execution plugin for Ansible that drastically speeds up multi-node operations."},
            {"front": "SSH Pipelining", "back": "A parameter that reduces the number of SSH connections required to execute a module, boosting performance."},
            {"front": "Idempotency", "back": "The property that running an operation once produces the exact same outcome as running it 1,000 times."}
        ],
        "challenge": {
            "title": "The Fork Bomb",
            "description": "Write the exact line you add to `ansible.cfg` to increase the parallel execution workers from the default to 50.",
            "hints": ["forks = ..."],
            "solution": "forks = 50"
        }
    },
    {
        "id": "23_interview_k8s",
        "title": "23. Interview: K8s System Design",
        "quiz": [
            {"q": "Boss Level: When designing an Operator via CRDs, what exact component continuously loops to observe, diff, and act upon state?", "options": ["The Kubelet", "The Custom Controller Reconciler", "The Ingress rule", "etcd storage"], "a": 1}
,
            {"q": "When a worker node suffers a kernel panic, what specific K8s component is responsible for permanently marking the node as Dead, and how long is the generic default timeout?", "options": ["The Kubelet, 5 seconds.", "The Node Controller (running within kube-controller-manager), defaulting around 40 seconds before initiating eviction sequences.", "Docker, 5 minutes.", "The APIServer, instantly."], "a": 1},
            {"q": "Explain the architectural consequence inside etcd when you violently hit the default 2MB transaction limit boundary during a massive API injection.", "options": ["It crashes.", "etcd throws the `etcdserver: request is too large` exception. The operation halts deterministically across the Raft quorum to prevent unpredictable database state bloat.", "It parses the data perfectly.", "It writes to the disk."], "a": 1},
            {"q": "What occurs if an Operator's custom controller possesses an unoptimized reconciliation loop that lacks jitter bounds?", "options": ["It scales infinitely.", "It triggers a widespread 'Thundering Herd' DDoSing the Kube-APIServer aggressively during cluster restarts as thousands of objects continuously demand synchronization polling.", "It ignores the queue.", "It deletes nodes."], "a": 1},
            {"q": "How does `cert-manager` dynamically circumvent DNS propagation latency issues when executing ACME DNS-01 challenges heavily across massive domains?", "options": ["It doesn't.", "Using AWS Route53.", "It actively modifies its logic to query the Authoritative Nameservers directly mimicking split-horizon detection to ensure rapid token availability before validating.", "It uses HTTP verification."], "a": 2},
            {"q": "When utilizing native Kubernetes Headless Services (`clusterIP: None`), what is fundamentally altered at the DNS translation layer?", "options": ["It acts identically.", "It removes the proxy abstraction completely, forcing CoreDNS to return the explicit raw IP addresses of all underlying Ready Pods back directly to the client endpoint for client-side load balancing.", "It denies traffic.", "It uses NodePort."], "a": 1},
            {"q": "Describe the core consequence of implementing highly complex OPA Gatekeeper logic evaluating strictly at the ValidatingAdmissionWebhook phase across 5,000 pods.", "options": ["It works fine.", "If the underlying policy logic requires external API lookups outside the cluster boundary, you instantly incur severe latency, bottlenecking all cluster scaling execution and creating massive timeouts.", "It crashes Docker.", "It logs to Slack."], "a": 1},
            {"q": "If a StatefulSet requires an immediate, forceful rollback crossing an immutable volume constraint, what is the required operational pattern?", "options": ["Apply `terraform destroy`.", "Manually unbinding and backing up the underlying PV constraints, completely deleting the active StatefulSet via `cascade=orphan`, patching PVCs, and recreating matching labels.", "Applying `helm refresh`.", "Waiting for etcd."], "a": 1},
            {"q": "In high-performance analytical environments, what limits the capability of standard kube-proxy IPVS load balancing logic?", "options": ["It lacks UDP.", "The inherent lack of DSR (Direct Server Return) architectures seamlessly integrated. Processing massive multi-gigabit traffic strictly within conventional translation pipelines bogs down node network namespaces severely.", "It relies strictly on Terraform.", "It runs entirely on Python."], "a": 1},
            {"q": "What specific consequence emerges functionally when integrating Kustomize multi-layer patching aggressively against conflicting Helm Chart hooks defined by third vendors?", "options": ["Helm wins out.", "Kustomize entirely strips or violently alters annotations blindly before execution, frequently crippling Helm's intrinsic pre/post rendering verification states.", "It merges cleanly.", "Kustomize ignores Helm."], "a": 1}
        ],
        "interview_prep": [
            {"q": "System Design Scenario: Describe how etcd handles data consistency across Control Plane nodes during a network partition.", "a": "etcd uses the Raft consensus algorithm. It requires a strict quorum (majority) to commit writes (e.g., in a 5-node cluster, 3 must agree). If a network partition isolates 2 nodes, those nodes lose quorum, cannot elect a leader, and will reject all write operations, ensuring split-brain corruption cannot occur."},
            {"q": "How do you extend Kubernetes to manage custom business logic, such as a specialized MySQL cluster?", "a": "You use the Operator Pattern. First, you define the desired schema using a Custom Resource Definition (CRD). Then, you write a custom controller (often in Go or Python via Kopf) that continuously watches the API for that CRD and runs loop logic to reconcile the physical MySQL state to match the user's YAML spec."},
            {"q": "What happens when a Kubernetes cluster starts hitting hard scaling limits (e.g., past 5,000 nodes or 150,000 pods)?", "a": "The primary bottleneck becomes the kube-apiserver's connection to etcd and kube-proxy's iptables rules on the nodes. To resolve this: 1) Migrate from iptables to IPVS or an eBPF dataplane like Cilium. 2) Horizontally scale the api-server and optimize etcd IOPS. 3) Partition the architecture using Cluster Federation or tools like Karpenter for hyper-scale node provisioning."}
        ],
                "homework": {
            "title": "Interview Lab: Production GKE Platform with Full Observability",
            "objective": "Under interview conditions (60 minutes), design and deploy a production-grade GKE platform with auto-scaling, service mesh, observability, and disaster recovery.",
            "platform": "Google Cloud Platform",
            "difficulty": "Expert",
            "scenario": "INTERVIEW PROMPT: 'Design a GKE platform that can handle 10,000 RPS with 99.99% uptime. Show me the architecture, deploy the core components, and explain your scaling and DR strategy.'",
            "steps": [
                        "MINUTE 0-10: Architecture \u2014 Regional GKE, multi-zone node pools, Ingress via Gateway API.",
                        "MINUTE 10-20: Deploy the GKE cluster with Dataplane V2, Workload Identity, and VPA.",
                        "MINUTE 20-30: Deploy a sample API with HPA, PDB, and topology spread constraints.",
                        "MINUTE 30-40: Install the observability stack \u2014 Prometheus, Grafana, and Hubble.",
                        "MINUTE 40-50: Configure alerting rules for error rate, latency P99, and pod restarts.",
                        "MINUTE 50-55: Implement DR \u2014 explain Multi-Cluster Services and Backup for GKE.",
                        "MINUTE 55-60: Present the architecture and handle follow-up questions.",
                        "FOLLOW-UP: What's your strategy for zero-downtime GKE version upgrades across 200 microservices?"
            ],
            "deliverables": [
                        "Regional GKE cluster with full autoscaling stack",
                        "Observability stack with alerting",
                        "Verbal DR strategy with RPO/RTO targets"
            ],
            "solution_hint": "Use `google_container_cluster` with `location = region` (not zone) for regional HA. Gateway API replaces Ingress in 2026. For DR: GKE Backup for etcd snapshots, Multi-Cluster Services for cross-region failover. Target RPO=5min, RTO=15min.",
            "real_world_context": "This is the ultimate Kubernetes interview question. Companies like Google, Amazon, and Cloudflare ask this to evaluate Staff+ engineering candidates."
},
        "flashcards": [
            {"front": "Raft", "back": "The consensus algorithm utilized by etcd to guarantee data consistency and leader election."},
            {"front": "Operator Pattern", "back": "A method of packaging, deploying, and managing a Kubernetes application linking a CRD to a custom controller."},
            {"front": "IPVS / eBPF", "back": "Alternatives to standard kube-proxy iptables used to handle massive network routing scale."}
        ],
        "challenge": {
            "title": "Control Plane Architecture",
            "description": "What is the formula to calculate quorum in a Raft cluster where N is the total number of nodes?",
            "hints": ["(N / 2) + ..."],
            "solution": "(N / 2) + 1"
        }
    },
    {
        "id": "24_cicd_pipelines",
        "title": "24. CI/CD Pipelines at Scale",
        "quiz": [
            {"q": "What is the primary benefit of Shift-Left Security in pipelines?", "options": ["Faster deployments", "Catching vulnerabilities like plaintext secrets or misconfigurations before code is deployed", "It uses less RAM", "It bypasses tests"], "a": 1},
            {"q": "Which tool is commonly used to scan infrastructure as code in the pipeline?", "options": ["Checkov", "Ansible", "Kubernetes", "Prometheus"], "a": 0},
            {"q": "How does Workload Identity Federation eliminate the need for static Service Account keys in GitHub Actions?", "options": ["It uses basic auth", "It uses an OIDC trust relationship where GitHub signs a short-lived JWT, and GCP verifies it to issue temporary access tokens", "It stores keys in Vault", "It disables IAM entirely"], "a": 1},
            {"q": "What is the purpose of the `soft_fail` flag in a Checkov GitHub Action?", "options": ["It deletes resources", "It forces the Action to return a 0 exit code even if vulnerabilities are found, allowing the pipeline to continue (useful for baseline audits)", "It makes the scan run faster", "It ignores all errors"], "a": 1},
            {"q": "In a strict production Terraform CI/CD pipeline, when should `terraform apply` execute?", "options": ["On every commit to a feature branch", "Automatically on merge to the main/master branch after reviewers have explicitly approved the `terraform plan` output", "Manually via the AWS console", "Never"], "a": 1}
        ],
        "interview_prep": [
            {"q": "How do you securely pass cloud credentials to a CI/CD pipeline (e.g., GitHub Actions)?", "a": "You should never pass long-lived static credentials. Implement Workload Identity Federation (OIDC) so the pipeline runner can assume a short-lived IAM role dynamically based on its verified identity."},
            {"q": "During a pipeline run, tfsec flags an S3 bucket for missing encryption, but the engineering team claims this specific bucket must remain unencrypted for legacy public access. How do you resolve this?", "a": "Instead of removing tfsec or soft-failing the entire pipeline, I would use an inline code annotation (e.g., `#tfsec:ignore:aws-s3-enable-bucket-encryption`) directly above the Terraform resource to uniquely whitelist that specific failure with a documented justification."},
            {"q": "If multiple developers merge PRs simultaneously to main, causing three GitHub Actions to run `terraform apply` at the exact same moment, how does Terraform prevent catastrophic state corruption?", "a": "Terraform relies on State Locking via the remote backend (e.g., DynamoDB for AWS or Cloud Storage native locking for GCP). The first pipeline to acquire the lock proceeds; the subsequent pipelines will inherently fail with a 'State Locked' error, preventing race conditions."}
        ],
        "homework": {
            "title": "Build a Secure Terraform CI/CD Pipeline via GitHub Actions",
            "objective": "Establish an automated pipeline that checks code formatting, scans for security flaws, and applies Terraform infrastructure via GitHub Actions using Workload Identity Federation.",
            "platform": "Google Cloud Platform / Cloud Agnostic",
            "difficulty": "Advanced",
            "scenario": "Your security team mandates shift-left deployment policies. Push code to GitHub, trigger a pipeline that runs tfsec/Checkov, and deploy using Workload Identity (no service account keys).",
            "steps": [
                "Configure Workload Identity Federation in GCP linked to your GitHub repo's OIDC issuer.",
                "Create a `.github/workflows/deploy.yaml`.",
                "Add checkout and OIDC token auth steps (e.g., `google-github-actions/auth@v1`).",
                "Add `terraform fmt -check` and `terraform validate` steps.",
                "Integrate a `Checkov` or `tfsec` scan step configured to hard-fail on critical vulnerabilities.",
                "Add `terraform plan` and `terraform apply -auto-approve` scoped only to trigger on merge to the main branch."
            ],
            "deliverables": [
                "A working GitHub Actions YAML pipeline definition.",
                "A successful run log demonstrating keyless OIDC authentication and successful Terraform execution."
            ],
            "solution_hint": "In GitHub Actions, use `permissions: id-token: write` at the job level. Without this explicit permission, GitHub will not generate the OIDC JWT necessary to authenticate with GCP.",
            "real_world_context": "Shift-left CI/CD with OIDC auth is the absolute minimum baseline requirement in modern DevOps. Major enterprises will fail compliance audits if static cloud keys are discovered anywhere within GitHub Secrets."
        },
        "flashcards": [
            {"front": "Shift-Left", "back": "Integrating security and testing early in the software development lifecycle, rather than post-deployment."},
            {"front": "OIDC (OpenID Connect)", "back": "An identity layer on top of OAuth 2.0 used for secure Workload Identity Federation to eliminate static cloud keys."},
            {"front": "tfsec / Checkov", "back": "Static Application Security Testing (SAST) tools specifically designed to scan Infrastructure as Code for misconfigurations."}
        ],
        "challenge": {
            "title": "The Security Scanner",
            "description": "Write a pipeline command to forcefully run a Checkov scan against the local Terraform directory and output findings to the terminal.",
            "hints": ["checkov -d <directory>"],
            "solution": "checkov -d ."
        }
    },
    {
        "id": "25_gitops_kubernetes",
        "title": "25. GitOps & Advanced Orchestration",
        "quiz": [
            {"q": "What fundamentally differentiates GitOps from traditional CI/CD Push models?", "options": ["GitOps relies on pull-based operators living inside the cluster to synchronize state from Git", "GitOps is push-based only", "GitOps uses FTP", "GitOps requires Terraform"], "a": 0},
            {"q": "Which tool is standard for declarative GitOps delivery in Kubernetes?", "options": ["Jenkins", "Argo CD", "Chef", "Ansible"], "a": 1},
            {"q": "If a GitOps application object reads an `OutOfSync` condition, what precisely does it mean?", "options": ["The cluster is down", "The actual deployed objects inside Kubernetes differ systematically from the declarative YAML stored in the monitored Git repository", "The Github repo is offline", "Docker is full"], "a": 1},
            {"q": "What happens if a rogue developer runs `kubectl scale deployment web --replicas=100` against a deployment strictly managed by ArgoCD with self-healing enabled?", "options": ["ArgoCD crashes", "ArgoCD instantly detects the manual drift, flags it, and forcefully scales the deployment back to the replica count defined in the Git repository.", "The cluster scales to 100 pods.", "It asks for confirmation."], "a": 1},
            {"q": "What is the 'App of Apps' pattern in ArgoCD architecture?", "options": ["A mobile application framework", "Deploying a single Root ArgoCD Application that points to a Git directory containing 50 other ArgoCD Application YAMLs, allowing mass cluster bootstrapping.", "A Python script.", "A way to compile Docker images."], "a": 1}
        ],
        "interview_prep": [
            {"q": "What happen if an engineer manually edits a deployment using 'kubectl edit' in a GitOps environment?", "a": "The GitOps operator (like ArgoCD) will immediately detect the drift (Difference between Git and Cluster) and automatically revert the manual change to match the source of truth in Git if Self-Heal is enabled."},
            {"q": "Why is a Pull-Based GitOps architecture inherently more secure than a Push-Based Jenkins architecture for Kubernetes?", "a": "In a Push model, Jenkins sits entirely outside the cluster and requires powerful Inbound firewall rules and highly-privileged Cluster Admin API keys to push changes. In a Pull model, ArgoCD lives inside the cluster. It only needs outbound internet access to pull from GitHub, vastly narrowing the attack surface and centralizing RBAC."},
            {"q": "Explain how you handle Kubernetes Secrets in a strict declarative GitOps environment without exposing passwords in plain text in Github.", "a": "You cannot store raw k8s Secret YAMLs in Git. You must integrate a tool like External Secrets Operator (which pulls dynamically from AWS Secrets Manager/HashiCorp Vault at runtime) or use Bitnami Sealed Secrets (which encrypts the secret payload using a public key so it can be safely committed to Git, to be decrypted by the cluster controller)."}
        ],
        "homework": {
            "title": "Deploy Argo CD on GKE with Multi-Environment GitOps",
            "objective": "Install Argo CD, connect a Git repository, and deploy an application across Dev and Prod environments using declarative synchronization.",
            "platform": "Google Cloud Platform",
            "difficulty": "Advanced",
            "scenario": "Your CTO mandates absolute immutability. No one is allowed to use `kubectl apply`. Configure ArgoCD to automatically deploy and self-heal your helm charts whenever you merge a PR.",
            "steps": [
                "Install Argo CD in the `argocd` namespace on GKE using the official stable install manifest.",
                "Port-forward the Argo CD UI (`kubectl port-forward svc/argocd-server -n argocd 8080:443`) and log in using the initial admin secret.",
                "Create a public Git repository containing standard Kubernetes deployment and service manifests for a sample Nginx app.",
                "Create an Argo CD `Application` custom resource targeting your repository's path.",
                "Enable Automated Sync and Self-Heal within the ArgoCD Application parameters.",
                "Intentionally cause drift by manually deleting the Nginx pod via CLI, and observe ArgoCD effortlessly spawn a replacement."
            ],
            "deliverables": [
                "A screenshot of the Argo CD dashboard showing the target application as 'Healthy' and 'Synced'.",
                "The Argo CD Application YAML definition used to bootstrap the deployment."
            ],
            "solution_hint": "To retrieve the initial ArgoCD admin password natively, run: `kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d`.",
            "real_world_context": "The GitOps workflow powered by ArgoCD is adopted by massive enterprises (like Red Hat, Intuit, and Tesla) to guarantee that what is specified in Git perfectly matches the production cluster reality without fail."
        },
        "flashcards": [
            {"front": "GitOps", "back": "A paradigm where Git is treated as the single absolute source of truth for declarative infrastructure and applications."},
            {"front": "Argo CD", "back": "A declarative, pull-based continuous delivery and GitOps tool specifically engineered for Kubernetes."},
            {"front": "Self-Heal", "back": "An ArgoCD automated sync policy parameter that forcefully reverts manual cluster changes back to the Git state."}
        ],
        "challenge": {
            "title": "Sync Immediacy",
            "description": "Imagine you are using the ArgoCD CLI. Write the command to trigger an immediate manual synchronization (sync) for an application named 'core-api'.",
            "hints": ["argocd app sync <appname>"],
            "solution": "argocd app sync core-api"
        }
    },
    {
        "id": "26_sre_observability",
        "title": "26. SRE & Observability Practices",
        "quiz": [
            {"q": "What are the three pillars of observability?", "options": ["Logs, Metrics, Traces", "CPU, RAM, Disk", "Terraform, Ansible, K8s", "Git, CI, CD"], "a": 0},
            {"q": "Which component is widely used for scraping and storing metrics in Cloud Native environments?", "options": ["Prometheus", "Fluentd", "Jenkins", "Helm"], "a": 0},
            {"q": "How does Prometheus fundamentally collect telemetric data from massive K8s workloads?", "options": ["It uses push agents", "It utilizes an iterative Pull Model, reaching out to exposed `/metrics` HTTP endpoints on configured target intervals to scrape data", "It reads log files", "It connects to the database"], "a": 1},
            {"q": "In SRE principles, what specifically triggers an engineer via PagerDuty under 'Symptom-Based Alerting' rules?", "options": ["A CPU spike", "When the explicit user experience degrades beyond defined thresholds (e.g., HTTP 500 error rates exceed 5% over 10 minutes)", "A pod restart", "A cron job failure"], "a": 1},
            {"q": "What happens when an engineering team totally depletes their Error Budget (drops below their SLO)?", "options": ["The engineers get fired", "A strict freeze is placed on rolling out new features; engineering velocity is halted to focus exclusively on reliability improvements until the mathematical budget recovers", "They ignore it", "Cloud provider increases capacity"], "a": 1}
        ],
        "interview_prep": [
            {"q": "What is the difference between an SLI and an SLO?", "a": "An SLI (Service Level Indicator) is the direct measurement (e.g., 99.5% of completed requests returned HTTP 200). An SLO (Service Level Objective) is the negotiated target threshold agreed upon by the business (e.g., We aim for a 99.9% success rate). If the factual SLI falls below the objective SLO, the error budget is depleted."},
            {"q": "To prevent 'Alert Fatigue' in a 24/7 on-call rotation, how would you design the Prometheus alerting pipeline?", "a": "I would strictly enforce Symptom-Based Alerting rules in Prometheus so an engineer is only woken up if the customer is directly impacted (e.g., high latency, rapid 5xx generation). Additionally, I would use AlertManager's grouping and inhibition features to deduplicate massive cascading failure alerts into a single cohesive incident notification."},
            {"q": "Briefly differentiate Metrics, Logs, and Traces in a microservice environment.", "a": "Metrics are highly compressible numeric aggregates over time indicating system health (CPU%). Logs are immutable timestamped events detailing specific occurrences (Application errors). Traces stitch together the end-to-end journey of a single user request as it traverses across multiple discrete microservice boundaries."}
        ],
        "homework": {
            "title": "Deploy Prometheus & Grafana for Cluster Telemetry",
            "objective": "Install a full SRE observability stack via the kube-prometheus-stack Helm chart to monitor GKE workloads, and define a proactive alerting rule.",
            "platform": "Google Cloud Platform",
            "difficulty": "Intermediate",
            "scenario": "You are flying blind in production. Deploy Prometheus for metrics scraping, Grafana for visual dashboards, and AlertManager for PageDuty integration to secure system observation.",
            "steps": [
                "Add the Prometheus-Community helm repository (`helm repo add prometheus-community`).",
                "Install the `kube-prometheus-stack` chart using Helm against an active Kubernetes cluster.",
                "Use `kubectl port-forward` to access the Grafana UI locally.",
                "Explore the pre-configured Kubernetes API and Node resource dashboards dynamically generated by the Operator.",
                "Write a custom Prometheus rule (`PrometheusRule` CRD) that fires a warning when Deployment replicas crash.",
                "Bonus: Deliberately scale down a core `kube-system` metric deployment to trigger and validate your alert."
            ],
            "deliverables": [
                "Running Prometheus, Grafana, and AlertManager StatefulSets/Deployments.",
                "Screenshot of the Grafana dashboard showing live node CPU and namespace metrics."
            ],
            "solution_hint": "The Prometheus Operator pattern makes tracking configuration states robust by automatically discovering and applying `ServiceMonitor` and `PrometheusRule` objects without restarting the Prometheus daemon manually.",
            "real_world_context": "Monitoring is the bedrock foundation of Site Reliability Engineering. You simply cannot fix what you cannot measure, making Prometheus and Grafana non-negotiable deployments universally."
        },
        "flashcards": [
            {"front": "Observability", "back": "The ability to measure the internal state of a complex system based purely on its external outputs (Metrics, Logs, Traces)."},
            {"front": "SLO", "back": "Service Level Objective; a reliable, quantifiable target metric agreed upon by the engineering team and product stakeholders."},
            {"front": "PromQL", "back": "The massively powerful functional query language designed explicitly to extract data from Prometheus Time-Series Databases."}
        ],
        "challenge": {
            "title": "The PromQL Query",
            "description": "Write a basic PromQL query to calculate the per-second rate of HTTP server requests over a rolling 5 minute window.",
            "hints": ["rate(...)"],
            "solution": "rate(http_requests_total[5m])"
        }
    },
    {
        "id": "27_multicloud_gcp",
        "title": "27. GCP & Multi-Cloud Landing Zones",
        "quiz": [
            {"q": "What is a Landing Zone in cloud architecture?", "options": ["A pre-configured environment with established network, identity, and security guardrails", "A specific server instance", "A CI/CD artifact", "A load balancer"], "a": 0},
            {"q": "Which native GCP feature securely connects an external identity provider to authenticate pipelines without local service account keys?", "options": ["Workload Identity Federation", "Identity Aware Proxy", "Cloud IAM", "Cloud Identity"], "a": 0},
            {"q": "In the structured Google Cloud Resource Hierarchy, what acts as the foundational root node?", "options": ["The Project", "The Folder", "The Organization Node", "The Billing Account"], "a": 2},
            {"q": "What is the inherent architectural benefit of utilizing a GCP Shared VPC?", "options": ["It increases internet speed", "It centralizes IP subnet management and Firewall rules in a Host Project while seamlessly attaching isolated Service Projects containing workloads", "It makes servers cheaper", "It deploys VPNs"], "a": 1},
            {"q": "When enforcing regulatory compliance (like HIPAA), how do you guarantee every single Cloud Audit transaction across the enterprise is securely captured?", "options": ["Write a python script", "Deploy an Organization-Level Logging Sink directing all recursive telemetry to a locked-down BigQuery analytics dataset", "Copy logs to a flash drive", "Use Cloud Storage"], "a": 1}
        ],
        "interview_prep": [
            {"q": "Why use the Google Cloud Foundation Toolkit instead of writing custom foundational Terraform from scratch?", "a": "It provides vetted, compliant, and highly optimized best-practice modules built and maintained by Google's own engineers for Landing Zones (including complex Hub-and-Spoke networks, IAM hierarchies, and logging sinks), heavily reducing technical debt and deployment time."},
            {"q": "Explain the architectural difference between a GCP Folder and a GCP Project in a Landing Zone.", "a": "A Folder is an organizational boundary utilized to apply hierarchical IAM policies and organizational constraints that trickle down globally (e.g. 'Production Folder'). A Project is the absolute trust boundary and deployment unit where actual API billing, quotas, and physical compute resources exist."},
            {"q": "If a rogue developer deployed a public Load Balancer inside a secure Service Project, how does the Shared VPC model prevent an immediate breach?", "a": "In a true Shared VPC network separation, the developers only possess 'Compute Admin' within their Service Project to launch instances. They completely lack the 'Compute Network Admin' rights required to manipulate routing, firewalls, or expose public interfaces, which are tightly restricted to the Host Project administered strictly by the Network Security team."}
        ],
        "homework": {
            "title": "Construct an Enterprise GCP Landing Zone",
            "objective": "Design and build a multi-environment foundational architecture utilizing GCP Organizations, Folders, Shared VPCs, and IAM bindings executed via Terraform.",
            "platform": "Google Cloud Platform",
            "difficulty": "Expert",
            "scenario": "You are leading a massive enterprise migration to GCP. Formulate a secure Foundation equipped with absolute network segregation (Dev vs Prod), automated central logging, and hierarchical project isolation.",
            "steps": [
                "Utilize official Google Cloud Foundation Toolkit modules (or write customized `terragrunt` structures).",
                "Create Top-Level Folders segregating Development resources from Production capabilities.",
                "Initialize specific GCP Projects dynamically nested underneath those folders.",
                "Structure a Shared VPC architecture where a centralized Host Project distributes subnets down to attached Service Projects.",
                "Imprint Cloud NAT and Private Google Access requirements directly onto the regional subnets.",
                "Configure an Organization-level aggregate sink utilizing `google_logging_organization_sink` to forcefully export all compliance audit logs to a central BigQuery repository."
            ],
            "deliverables": [
                "A hierarchical Terraform/Terragrunt repository housing the Landing Zone modules.",
                "A successfully initialized GCP Org/Folder structure integrating Shared VPC boundaries."
            ],
            "solution_hint": "Creating folders and orchestrating projects programmatically often strictly requires extreme privileges like Domain Administrator or Folder Admin roles positioned directly at the GCP Organization Level.",
            "real_world_context": "Implementing rigorous Landing Zones prevents catastrophic 'spaghetti cloud' deployments, guaranteeing centralized billing, strict network governance, and ironclad security posturing massively favored by Fortune 500 integrations."
        },
        "flashcards": [
            {"front": "Landing Zone", "back": "A deeply governed, highly scalable multi-project cloud foundation deployed consistently using infrastructure as code."},
            {"front": "Shared VPC", "back": "A native GCP networking construct enabling a centralized Host Project to securely distribute subnets to multiple peripheral Service Projects."},
            {"front": "Organization Node", "back": "The root parameter of the Google Cloud hierarchy, acting as the absolute foundational origin for all Folders, Projects, and cascading IAM policies."}
        ],
        "challenge": {
            "title": "The Logging Sink",
            "description": "What primary Terraform resource is utilized to programmatically route vast project-level logs out to a secure destination like BigQuery or PubSub?",
            "hints": ["google_logging_project_sink"],
            "solution": "google_logging_project_sink"
        }
    }
]

import logging
import traceback

# Configure logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

@router.get("/debug")
async def debug_paths():
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        content_dir = os.path.join(base_dir, "content")
        chapters_dir = os.path.join(content_dir, "chapters")
        
        return {
            "base_dir": base_dir,
            "content_dir": content_dir,
            "chapters_dir": chapters_dir,
            "chapters_exists": os.path.exists(chapters_dir),
            "files": os.listdir(chapters_dir) if os.path.exists(chapters_dir) else [],
            "templates_dir": templates.env.loader.searchpath
        }
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}

@router.get("/{chapter_id}", response_class=HTMLResponse)
async def get_chapter(request: Request, chapter_id: str):
    try:
        logging.info(f"Requesting chapter: {chapter_id}")
        
        # Find current chapter index
        try:
            current_index = next(i for i, c in enumerate(CHAPTERS) if c["id"] == chapter_id)
        except StopIteration:
            logging.error(f"Chapter {chapter_id} not found in list")
            raise HTTPException(status_code=404, detail="Chapter not found")
    
        # Navigation logic
        prev_chapter = CHAPTERS[current_index - 1] if current_index > 0 else None
        next_chapter = CHAPTERS[current_index + 1] if current_index < len(CHAPTERS) - 1 else None
    
        # Load content
        file_path = os.path.join(CHAPTERS_DIR, f"{chapter_id}.md")
        logging.info(f"Looking for file at: {file_path}")
        
        if not os.path.exists(file_path):
            logging.warning(f"File not found: {file_path}")
            content = "# Content Coming Soon"
        else:
            with open(file_path, 'r') as f:
                content = f.read()
            logging.info(f"File read successfully. Length: {len(content)}")
    
        # Convert Markdown
        try:
            html_content = markdown.markdown(content, extensions=['fenced_code', 'tables'])
            logging.info("Markdown conversion successful")
        except Exception as e:
            logging.error(f"Markdown error: {e}")
            raise
    
        return templates.TemplateResponse("chapter.html", {
            "request": request,
            "content": html_content,
            "chapters": CHAPTERS,
            "current_chapter": CHAPTERS[current_index],
            "prev_chapter": prev_chapter,
            "next_chapter": next_chapter
        })
    except Exception as e:
        logging.error(f"Unhandled error: {e}")
        logging.error(traceback.format_exc())
        return HTMLResponse(content=f"<h1>Internal Server Error</h1><pre>{traceback.format_exc()}</pre>", status_code=500)
