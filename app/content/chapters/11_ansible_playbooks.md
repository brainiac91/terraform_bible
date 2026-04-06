# 11. Ansible: Playbooks & Modules

If Ad-Hoc commands are the terminal commands of Ansible, then **Playbooks** are the bash scripts. Playbooks allow you to orchestrate complex operations, utilizing an idempotent workflow.

## What is a Playbook?

Playbooks are written in YAML. They contain a list of one or more "Plays." A Play maps a group of hosts to well-defined "Tasks." A Task represents a single step, utilizing an Ansible module.

```yaml
---
- name: Install and start Nginx
  hosts: webservers
  become: yes  # Run as root

  tasks:
    - name: Ensure Nginx is at the latest version
      apt:
        name: nginx
        state: latest
      
    - name: Copy the custom index.html
      copy:
        src: ./files/index.html
        dest: /var/www/html/index.html
        owner: www-data
        group: www-data
        mode: '0644'

    - name: Ensure Nginx is enabled and running
      service:
        name: nginx
        state: started
        enabled: yes
```

## Idempotency at Scale

Notice `state: started` or `state: latest`. Ansible does not just blindly run `apt-get install nginx`. First, it checks if it's already installed. If it is, it reports `ok`. If it isn't, it installs it and reports `changed`.

### Core Modules Every Devops Engineer Must Know
1. **File/Directory Management**: `file`, `copy`, `template`, `synchronize`
2. **Software Packages**: `apt`, `yum`, `dnf`, `pip`, `npm`
3. **Services**: `service`, `systemd`
4. **Commands execution**: `command`, `shell` (Avoid these if a dedicated module exists because raw shell commands are usually not idempotent by themselves!)

> [!WARNING]
> Only use `shell` or `command` modules if no dedicated Ansible module exists. If you *must* use them, combine them with `creates` or `removes` arguments to enforce idempotency manually.

## Execution

Run a playbook with:
```bash
ansible-playbook -i hosts.ini web_setup.yaml
```

To just do a "dry-run" to see what *would* change:
```bash
ansible-playbook -i hosts.ini web_setup.yaml --check
```
