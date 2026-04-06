# 12. Ansible: Roles, Vault & Dynamic Inventory

Writing everything in a single massive playbook (`site.yaml`) quickly becomes unmaintainable. Ansible offers **Roles** as a mechanism to organize variables, tasks, files, templates, and handlers into a known file structure.

## Ansible Roles

A role is simply a directory with subdirectories like `tasks`, `handlers`, `defaults`, `vars`, `files`, and `templates`.

When you include a role in a playbook, Ansible automatically looks inside these folders.

```yaml
---
- hosts: webservers
  roles:
    - common
    - nginx
    - app_deploy
```

You can initialize a new role structure using Ansible Galaxy:
```bash
ansible-galaxy init my_custom_role
```

## Ansible Vault

You must never commit secrets (passwords, tokens, private keys) in plain text. **Ansible Vault** encrypts variables and files so you can safely store them in version control.

Encrypt an existing file:
```bash
ansible-vault encrypt secret.yaml
```

Edit an encrypted file:
```bash
ansible-vault edit secret.yaml
```

Run a playbook that uses a vault:
```bash
ansible-playbook -i hosts database.yaml --ask-vault-pass
```

## Dynamic Inventories

Static inventories (`hosts.ini`) are useless in an elastic cloud where VMs scale up and down dynamically.
Dynamic Inventories are scripts (or plugins) that Ansible runs to fetch the current list of hosts from AWS, GCP, Azure, or Kubernetes.

For example, using the AWS EC2 plugin:
```yaml
plugin: aws_ec2
regions:
  - us-east-1
filters:
  tag:Environment: Production
```

Running against specific tags:
```bash
ansible-playbook -i aws_ec2.yaml playbook.yaml --limit tag_Environment_Production
```

> [!IMPORTANT]
> The principle of SOLID applies directly to Ansible Roles. An NGINX role should ONLY install and configure NGINX (Single Responsibility Principle). It shouldn't configure the database simply because the app requires a database.
