# 10. Ansible: Introduction & Setup

Welcome to the **Ansible** chapter! While Terraform excels at provisioning infrastructure (creating servers, VPCs, clusters), Ansible shines at **Configuration Management** (installing software, managing files, configuring servers).

## What is Ansible?

Ansible is an open-source IT automation engine. It automates:
*   **Provisioning:** Setting up the basic infrastructure (though Terraform is often preferred).
*   **Configuration Management:** Ensuring packages are installed, files exist, and services are running.
*   **Application Deployment:** Deploying code to your servers from CI/CD.

### Key Characteristics:
1.  **Agentless:** You don't need to install any agent on the target nodes. It uses standard SSH (Linux) or WinRM (Windows).
2.  **Idempotent:** Like Terraform, running an Ansible script multiple times will yield the same result. It checks the state before making changes.
3.  **YAML based:** Human-readable automation language.

## Architecture

Ansible relies on the following core components:
1.  **Control Node:** The machine where Ansible is installed.
2.  **Managed Nodes:** The servers you are managing.
3.  **Inventory:** A list of managed nodes (IPs or hostnames) grouped logically.
4.  **Modules:** The tools Ansible uses to do the actual work (e.g., `apt`, `yum`, `copy`, `service`).

## First Steps: The Inventory

The inventory file (`hosts.ini`) tells Ansible what machines it can talk to.

```ini
[webservers]
192.168.1.10
192.168.1.11

[dbservers]
192.168.1.20
```

## First Command: Ad-Hoc Commands

Ad-hoc commands are quick, one-off commands you can run without writing an entire script.

Ping all servers in the `webservers` group:
```bash
ansible webservers -m ping -i hosts.ini
```

The `-m ping` uses the `ping` module to verify the connection is successful.

> [!TIP]
> Use ad-hoc commands for quick checks or immediate remediation. Use Playbooks for repeatable automation.
