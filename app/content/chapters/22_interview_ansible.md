# 22. Technical Interview: Ansible Scaling & Idempotency

## The Edge of Automated Configuration

Ansible behaves excellently on 50 servers. Once you hit 5,000 concurrent node executions, basic `.yaml` scripts grind to a complete halt. Interviewers will interrogate your knowledge of parallel execution and plugin logic.

### 1. Scaling Bottlenecks
Ansible relies on the SSH protocol by default. Doing a TCP handshake, authenticating, and copying a python script to `~/.ansible/tmp/` on 5,000 servers is slow.
To resolve this:
- **SSH Pipelining**: Disables the need to create multiple SSH connections per task. It pipes the python payloads standard-in over a single connection.
- **Forks**: The default Ansible process executes 5 nodes at a time. Update `ansible.cfg` to bump `forks = 50` or higher, provided the control node has sufficient memory.
- **Mitogen Strategy Plugin**: Bypasses traditional SSH execution logic entirely, holding a continuous persistent connection to execute python blobs natively in RAM, drastically accelerating playbooks.

### 2. Idempotency vs State
Senior engineers will fail your PRs if your code isn't **Idempotent** (safe to run 100 times in a row without making unintended mutations after the 1st run).

**Bad**:
```yaml
- name: Add a user
  command: useradd alineg
```
*Why?*: If run twice, the OS issues an error because the user exists. Ansible flags this as `FAILED` or `CHANGED`.

**Good**:
```yaml
- name: Add a user
  user:
    name: alineg
    state: present
```
*Why?*: Ansible reads the system state first. If the user exists, Ansible returns `OK` and skips execution.
