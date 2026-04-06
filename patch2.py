import re

file_path = 'app/routers/bible.py'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

updates = {
    "18_advanced_tf": '        "interview_prep": [\n            {"q": "How does Infracost shift-left Cloud FinOps?", "a": "Infracost reads the Terraform Plan output in the CI/CD pipeline and blocks the PR if the cost delta exceeds a defined budget, catching expensive mistakes before they are applied."}\n        ],\n        "flashcards": [',
    "19_advanced_ansible": '        "interview_prep": [\n            {"q": "What is the key advantage of an Ansible Execution Environment (EE)?", "a": "An EE is an OCI-compliant container image bundling ansible-core, collections, and python dependencies. It guarantees playbooks run identically on the developer laptop and in production AWX/Tower."}\n        ],\n        "flashcards": [',
    "20_advanced_k8s": '        "interview_prep": [\n            {"q": "Why is GitOps via ArgoCD considered superior to Jenkins push deployment for K8s?", "a": "Jenkins pushes manifests imperatively. ArgoCD sits INSIDE the K8s cluster and continuously pulls the Git state. If someone manually changes a deployment in production, ArgoCD immediately syncs it back to the Git state, preventing undocumented drift."}\n        ],\n        "flashcards": ['
}

for ch_id, repl in updates.items():
    pattern = r'("id": "' + ch_id + r'".*?)(        "flashcards": \[)'
    text = re.sub(pattern, r'\1' + repl, text, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Patcher 2 executed successfully.")
