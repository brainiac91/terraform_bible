import re

file_path = 'app/routers/bible.py'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

updates = {
    "06_advanced_hcl": '        "interview_prep": [\n            {"q": "Explain the difference between count and for_each. Why is for_each safer?", "a": "count uses lists/integers. If you remove an item from the middle, it shifts all resources, destroying them. for_each uses maps/keys, safely destroying only the removed key."}\n        ],\n        "flashcards": [',
    "07_testing_validation": '        "interview_prep": [\n            {"q": "How do you enforce Policy as Code in Terraform before apply?", "a": "You use OPA (Open Policy Agent) integrated in your CI/CD pipeline, or Checkov to scan the plan JSON and block the apply if policy fails."}\n        ],\n        "flashcards": [',
    "08_production": '        "interview_prep": [\n            {"q": "How do you prevent accidental deletion of a production database in HCL?", "a": "By using the lifecycle block with prevent_destroy = true. Applying a destroy will immediately fail until a PR removes that flag."}\n        ],\n        "flashcards": [',
    "09_security": '        "interview_prep": [\n            {"q": "How do you prevent secrets from leaking in Terraform state?", "a": "State is stored in plaintext. You must encrypt the S3 backend, restrict IAM access, and never hardcode secrets. Use data sources like AWS Secrets Manager to fetch them at runtime."}\n        ],\n        "flashcards": [',
    "10_ansible_intro": '        "interview_prep": [\n            {"q": "Ansible operates via Push, while puppet operates via Pull. What is the impact?", "a": "Push is agentless, meaning zero footprint on the target nodes. It simplifies security and scaling, though it requires persistent SSH access from the runner."}\n        ],\n        "flashcards": [',
    "11_ansible_playbooks": '        "interview_prep": [\n            {"q": "If a playbook fails midway, how do you resume without running everything again?", "a": "You can use the --start-at-task flag, or leverage retry files (.retry) from the failure point."}\n        ],\n        "flashcards": [',
    "12_ansible_roles_advanced": '        "interview_prep": [\n            {"q": "How do you handle secrets inside Ansible roles securely in a public repo?", "a": "Use Ansible Vault to encrypt variables or files. Only store the vault password on the highly secure CI/CD runner."}\n        ],\n        "flashcards": [',
    "13_k8s_intro": '        "interview_prep": [\n            {"q": "What happens if a Pod crashes continuously on startup?", "a": "K8s puts it into CrashLoopBackOff. You use kubectl logs --previous to view why the crash happened (e.g., missing env vars, OOMKilled)."}\n        ],\n        "flashcards": [',
    "14_k8s_manifests": '        "interview_prep": [\n            {"q": "Why use Deployments over bare Pods?", "a": "Deployments manage ReplicaSets, providing self-healing, rolling updates, and easy rollbacks if a deployment fails."}\n        ],\n        "flashcards": [',
    "15_k8s_architecture": '        "interview_prep": [\n            {"q": "What happens when you delete a pod?", "a": "The kube-apiserver updates etcd. The kubelet on the node sees the state change and sends a SIGTERM. The ReplicaSet controller notices the count is low and schedules a new pod."}\n        ],\n        "flashcards": [',
    "16_helm_intro": '        "interview_prep": [\n            {"q": "What is the primary advantage of Helm over raw YAML manifests?", "a": "Helm uses Go templates and values.yaml to provide DRY deployments across multiple environments. You write the YAML once and inject dynamic variables."}\n        ],\n        "flashcards": [',
    "17_helm_charts": '        "interview_prep": [\n            {"q": "How do you rollback a failed Helm deployment?", "a": "You run helm ls to find the revision history, and then helm rollback <release-name> <revision-number> to instantly restore the old stable state."}\n        ],\n        "flashcards": ['
}

for ch_id, repl in updates.items():
    pattern = r'("id": "' + ch_id + r'".*?)(        "flashcards": \[)'
    text = re.sub(pattern, r'\1' + repl, text, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Patcher executed successfully.")
