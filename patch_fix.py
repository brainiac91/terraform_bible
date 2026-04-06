import json

file_path = 'app/routers/bible.py'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Each chapter 01-20 needs exactly 1 more question to reach 10
q_bank = {
    "01_intro": {"q": "What is the critical difference between a `resource` and a `data` source in Terraform?", "options": ["Resources are read-only", "Data sources query existing infrastructure without managing it; resources create and manage infrastructure lifecycle", "There is no difference", "Data sources cost money"], "a": 1},
    "02_workflow": {"q": "What does `terraform workspace select staging` accomplish in a multi-environment setup?", "options": ["Deletes staging", "Switches the active state context so all subsequent plan/apply commands operate against the staging-specific state file", "Creates a new provider", "Renames the backend"], "a": 1},
    "03_state": {"q": "When using `terraform import aws_instance.web i-1234567`, what precisely happens?", "options": ["Terraform creates the EC2 instance", "Terraform adds the existing EC2 instance to the state file mapping. No HCL is generated — you must write the resource block yourself", "Terraform deletes the instance", "Terraform exports HCL automatically"], "a": 1},
    "04_variables_outputs": {"q": "What is the variable precedence order from lowest to highest in Terraform?", "options": ["CLI > env > file", "defaults < terraform.tfvars < *.auto.tfvars < -var-file < -var CLI < TF_VAR_ environment variables", "All are equal", "Environment always wins"], "a": 1},
    "05_modules": {"q": "What does a `terraform.lock.hcl` inside a module directory track?", "options": ["Module state", "Nothing; lock files only exist at the root module level tracking provider checksums", "Child module versions", "Backend configuration"], "a": 1},
    "06_advanced_hcl": {"q": "What does `flatten()` do when applied to a list of lists in Terraform?", "options": ["Sorts them", "Recursively merges all nested lists into a single flat list", "Removes duplicates", "Converts to a map"], "a": 1},
    "07_testing_validation": {"q": "What is the key difference between `precondition` and `postcondition` blocks in Terraform?", "options": ["They are identical", "Preconditions validate assumptions BEFORE a resource action; postconditions validate guarantees AFTER the action completes", "Preconditions run at destroy", "Postconditions run at init"], "a": 1},
    "08_production": {"q": "What is the architectural purpose of using Terraform workspaces in a CI/CD pipeline?", "options": ["To create backups", "To isolate state files per environment (dev/staging/prod) using a single codebase, preventing cross-environment state contamination", "To encrypt secrets", "To speed up applies"], "a": 1},
    "09_security": {"q": "Why should you never store provider credentials in `.tf` files committed to version control?", "options": ["It slows down git", "Credentials in VCS are permanently recoverable from git history even after deletion, creating an irreversible security breach", "Terraform ignores them", "It breaks the plan"], "a": 1},
    "10_ansible_intro": {"q": "What makes Ansible fundamentally different from Chef and Puppet in terms of node requirements?", "options": ["Ansible uses YAML", "Ansible is agentless — it requires zero software installation on managed nodes beyond Python and SSH", "Ansible is faster", "Ansible is free"], "a": 1},
    "11_ansible_playbooks": {"q": "What does `changed_when: false` do on an Ansible task?", "options": ["Skips the task", "Forces the task to always report 'ok' status regardless of actual changes, preventing false-positive change notifications in idempotency checks", "Deletes the output", "Runs it twice"], "a": 1},
    "12_ansible_roles_advanced": {"q": "What is the purpose of `ansible-galaxy collection install` versus `ansible-galaxy role install`?", "options": ["They are identical", "Collections bundle roles, modules, plugins, and playbooks into a single distributable namespace package; roles are single-purpose automation units", "Collections are deprecated", "Roles include collections"], "a": 1},
    "13_k8s_intro": {"q": "What is the fundamental difference between a Pod and a Container in Kubernetes?", "options": ["They are the same", "A Pod is the smallest deployable unit that can contain one or more tightly-coupled containers sharing the same network namespace and storage volumes", "A Container is larger", "Pods run on the control plane"], "a": 1},
    "14_k8s_manifests": {"q": "Why would you use a StatefulSet instead of a Deployment for a database workload?", "options": ["StatefulSets are faster", "StatefulSets provide stable, persistent network identities (ordinal naming) and ordered, graceful deployment/scaling, critical for databases requiring consistent storage bindings", "Deployments cannot use volumes", "StatefulSets use less RAM"], "a": 1},
    "15_k8s_architecture": {"q": "What happens to running Pods if the kube-apiserver goes down temporarily?", "options": ["All Pods crash immediately", "Existing Pods continue running because the kubelet manages local Pod lifecycle independently. However, no new scheduling, scaling, or API operations can occur until the apiserver recovers", "Nodes reboot", "etcd deletes everything"], "a": 1},
    "16_helm_intro": {"q": "What is the purpose of the `values.yaml` file in a Helm chart?", "options": ["It stores secrets", "It provides the default configuration values that feed into Go templates, allowing users to override any value at install time via --set or -f flags", "It defines the API version", "It is a lock file"], "a": 1},
    "17_helm_charts": {"q": "How do you create a reusable Helm library chart that other charts can depend on?", "options": ["Use `type: application`", "Set `type: library` in Chart.yaml. Library charts cannot be installed directly but provide shared templates and helpers via the `_helpers.tpl` convention", "Use `kind: Library`", "Library charts are deprecated"], "a": 1},
    "18_advanced_tf": {"q": "What is the primary benefit of using Terragrunt's `include` block in a multi-account AWS setup?", "options": ["It includes CSS", "It allows child modules to inherit and merge parent configurations (like backend and provider blocks) from a root `terragrunt.hcl`, eliminating massive DRY violations across hundreds of directories", "It includes Python", "It speeds up terraform init"], "a": 1},
    "19_advanced_ansible": {"q": "What is the primary advantage of Mitogen over standard Ansible SSH transport?", "options": ["It uses UDP", "Mitogen establishes a persistent in-memory Python interpreter on the remote node, eliminating the overhead of repeated SSH connections and temporary file transfers per task", "It uses gRPC", "It encrypts logs"], "a": 1},
    "20_advanced_k8s": {"q": "What problem does a Service Mesh like Istio or Linkerd solve that standard Kubernetes Services do not?", "options": ["DNS resolution", "Service Meshes provide transparent mTLS encryption, advanced traffic splitting, circuit breaking, and L7 observability between microservices without modifying application code", "Pod scheduling", "Storage provisioning"], "a": 1}
}

def inject():
    global text
    for ch_id, question in q_bank.items():
        idx = text.find(f'"id": "{ch_id}"')
        if idx == -1: continue
        quiz_end = text.find('        ],', idx)
        if quiz_end == -1: continue
        
        q_str = json.dumps(question)
        insert_str = f',\n            {q_str}\n'
        text = text[:quiz_end] + insert_str + text[quiz_end:]

inject()

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Fix patch executed successfully.")
