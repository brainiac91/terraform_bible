import re

file_path = 'app/routers/bible.py'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

quiz_updates = {
    "01_intro": """            ,{"q": "Boss Level: When utilizing Terraform Cloud for a remote backend, what happens if the local state file diverges dramatically while offline?", "options": ["Terraform overwrites the remote state instantly.", "Terraform forces an interactive resolution delta diff before unlocking.", "Terraform Cloud forces a hard fail, requiring workspace state manipulation.", "It automatically downloads the diff and deletes local drift."], "a": 2}""",
    "02_workflow": """            ,{"q": "Boss Level: A junior Dev ran `terraform plan -destroy` but closed the terminal. Will it destroy the resources?", "options": ["Yes, it runs in the background.", "No, `plan` only shows execution outlines; nothing is changed without an `apply`.", "Yes, unless you delete the local tfstate.", "Only if auto-approve was set in the environment variables."], "a": 1}""",
    "03_state": """            ,{"q": "Boss Level: What exact backend attribute is required to enforce DynamoDB State Locking on an S3 backend block natively?", "options": ["dynamodb_table_id = true", "dynamodb_lock = \\"active\\"", "dynamodb_table = \\"my-lock-table\\"", "lock_strategy = \\"dynamo\\""], "a": 2}""",
    "04_variables_outputs": """            ,{"q": "Boss Level: Given a variable of type `map(object({ name = string, age = number }))`, what is the precise HCL syntax to iterate and output a list of only ages?", "options": ["{ for k, v in var.obj : k => v.age }", "[ for k, v in var.obj : v.age ]", "var.obj[*].age", "map.obj(*).age"], "a": 1}""",
    "05_modules": """            ,{"q": "Boss Level: How do you pass a specific, non-default AWS provider alias configuration directly into a child module?", "options": ["modules={aws=aws.alternate}", "providers = { aws = aws.alternate }", "provider_aws = aws.alternate", "Using environment variables"], "a": 1}""",
    "06_advanced_hcl": """            ,{"q": "Boss Level: When building a `dynamic` block for AWS Security Group ingress rules, what is the implicit iterator variable named?", "options": ["item", "each.value", "The label of the dynamic block itself (e.g. `ingress.value`)", "block.key"], "a": 2}""",
    "07_testing_validation": """            ,{"q": "Boss Level: In Terraform 1.5+ config UI tests, what keyword is used to evaluate custom integration logic entirely inside native HCL?", "options": ["test_asserts", "run", "assert", "enforce"], "a": 1}""",
    "08_production": """            ,{"q": "Boss Level: When utilizing the `lifecycle` block inside a CI/CD pipeline, what does `create_before_destroy = true` effectively prevent?", "options": ["Cost overruns", "Micro-outages during resource replacement sweeps", "Secret leakage", "State file locking"], "a": 1}""",
    "09_security": """            ,{"q": "Boss Level: You are using HashiCorp Vault with the AppRole auth method in your Terraform Provider. What happens if the transient token expires mid-apply?", "options": ["Terraform creates a new token automatically.", "Terraform drops the lock and exits with a hard 403 Forbidden error.", "Terraform retries 5 times before failing.", "It skips the failed resources and applies the rest."], "a": 1}""",
    "10_ansible_intro": """            ,{"q": "Boss Level: Which Ansible command-line flag enables verbose connection diagnostics specifically targeted for SSH pipeline timeouts?", "options": ["-v", "-vvv", "--debug-ssh", "--trace-connection"], "a": 1}""",
    "11_ansible_playbooks": """            ,{"q": "Boss Level: If a playbook task handles highly sensitive credential output strings via the shell, how do you prevent it from being dumped into the Ansible logs?", "options": ["quiet: true", "no_log: true", "secret: true", "mask_output: true"], "a": 1}""",
    "12_ansible_roles_advanced": """            ,{"q": "Boss Level: When using Ansible Vault to store multiple environment secrets, how do you specify which vault identity password to use at runtime?", "options": ["--vault-password-file env.txt", "--vault-id prod@prompt", "--identity prod", "-v_pass prod"], "a": 1}""",
    "13_k8s_intro": """            ,{"q": "Boss Level: You encounter an `OOMKilled` Pod status. What component natively terminates the Pod, and why?", "options": ["The APIServer kills it to save bandwidth.", "The kernel's OOM Killer invoked via the kubelet cgroup limits.", "Docker runtime drops it randomly.", "The etcd database gets too full."], "a": 1}""",
    "14_k8s_manifests": """            ,{"q": "Boss Level: In a Deployment rolling update strategy, what does `maxSurge: 25%` and `maxUnavailable: 0` mean?", "options": ["It scales down to 0 first.", "It creates 25% extra pods before killing any old ones, ensuring zero downtime.", "It randomly deletes 25% of the pods.", "It blocks updates if more than 25% traffic hits the node."], "a": 1}""",
    "15_k8s_architecture": """            ,{"q": "Boss Level: What does etcd use the Raft Consensus mathematical threshold `(N/2)+1` to actively prevent across the Control Plane?", "options": ["CPU spiking", "Split-Brain scenarios during network partitions.", "IP overlap", "Memory leaks"], "a": 1}""",
    "16_helm_intro": """            ,{"q": "Boss Level: If a Helm deployment gets stuck in a `pending-upgrade` state due to a fatal interruption, how do you force a release clearance?", "options": ["helm reset", "helm rollback <release> 0", "helm delete --force", "helm upgrade --install"], "a": 1}""",
    "17_helm_charts": """            ,{"q": "Boss Level: In Go templating for Helm, what does the `-` character do inside `{{- .Values.variable -}}` tags?", "options": ["Subtracts numbers", "Decrypts the variable", "Chops whitespace, preventing YAML parsing layout errors.", "Ignores nil values"], "a": 2}""",
    "18_advanced_tf": """            ,{"q": "Boss Level: At an enterprise level, what specific state file locking technology is automatically mandated when integrating Terragrunt with AWS backends?", "options": ["Local .lock file", "S3 Bucket Versioning + DynamoDB", "Redis", "Consul Key/Value"], "a": 1}""",
    "19_advanced_ansible": """            ,{"q": "Boss Level: In Ansible Automation Platform (AWX), what happens if your `aws_ec2` plugin returns a newly instantiated ephemeral AWS inventory during a highly parallel execution?", "options": ["It crashes.", "Ansible dynamically routes jobs immediately to the newly resolved ephemeral IPs natively.", "It requires a manual Ansible reboot.", "It fails idempotency checks."], "a": 1}""",
    "20_advanced_k8s": """            ,{"q": "Boss Level: When utilizing eBPF (like Cilium) for advanced K8s networking instead of traditional iptables, where exactly does the data packet processing logic reside?", "options": ["Deep in the Pod user-space", "Directly hooked inside the OS Kernel socket layers", "In the external AWS router", "Inside the docker daemon"], "a": 1}"""
}

empty_quiz_updates = {
    "21_interview_tf": """            {"q": "Boss Level: During a state recovery, if you `terraform state rm aws_instance.web`, what happens to the physical ec2 server?", "options": ["It is destroyed via API.", "Nothing physical happens; it is merely forgotten by the tracking file.", "It is stopped.", "It is marked for recreation."], "a": 1}""",
    "22_interview_ansible": """            {"q": "Boss Level: What is the defining trait of an Ansible `fact` cache in high performance large-scale deployments?", "options": ["It bypasses the gathering phase completely by recalling saved node realities.", "It deletes old variables.", "It uses a MySQL database.", "It encrypts logs."], "a": 0}""",
    "23_interview_k8s": """            {"q": "Boss Level: When designing an Operator via CRDs, what exact component continuously loops to observe, diff, and act upon state?", "options": ["The Kubelet", "The Custom Controller Reconciler", "The Ingress rule", "etcd storage"], "a": 1}"""
}

for ch_id, q_string in quiz_updates.items():
    # Regex to match the block up to the very last closing bracket element before ],
    # We use a positive lookahead to assert we are right before the closing bracket of the quiz array
    pattern = re.compile(r'("id": "' + ch_id + r'".*?"quiz": \[[^\]]*?)(?=\n        \],)', re.DOTALL)
    text = pattern.sub(r'\1\n' + q_string, text)

for ch_id, q_string in empty_quiz_updates.items():
    pattern = re.compile(r'("id": "' + ch_id + r'".*?"quiz": )\[\]', re.DOTALL)
    text = pattern.sub(r'\1[\n' + q_string + r'\n        ]', text)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Boss Level Quizzes patched successfully.")
