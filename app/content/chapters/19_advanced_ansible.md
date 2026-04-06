# 19. Advanced Ansible: Dynamic Scale & Zero-Trust

## Execution Environments

Running Ansible from a developer's Macbook is fraught with "it works on my machine" python path errors. Ansible 2026 relies purely on **Execution Environments (EEs)** via `Ansible Builder`. These are pre-packaged podman/docker containers that securely encapsulate the exact `ansible-core` version, python dependencies, and galaxy collections required.

### Molecule Testing (Shift-Left)
To prevent bad configurations from taking down fleets, we use **Molecule**.

```yaml
# molecule/default/molecule.yml
---
dependency:
  name: galaxy
driver:
  name: docker
platforms:
  - name: instance
    image: "geerlingguy/docker-ubuntu2404-ansible:latest"
    command: ""
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:rw
    cgroupns_mode: host
```
By running `molecule test`, Ansible will spin up ephemeral Docker containers, run your role, verify idempotency (run it again to ensure 0 changes), and then destroy the container.

### Dynamic Inventory Plugin
Static `hosts.ini` files fail in ephemeral clouds.

```yaml
# aws_ec2.yml
plugin: aws_ec2
regions:
  - us-west-2
filters:
  tag:role:
    - webserver
compose:
  ansible_host: public_ip_address
```
This dynamically requests instances tagged `role=webserver` directly from the AWS API.
