# 1. Introduction & Setup

Welcome to **The Terraform Bible**. This guide is designed to take you from absolute beginner to a highly paid Infrastructure as Code (IaC) expert. We focus on the latest version of Terraform (v1.9+) and best practices relevant in late 2025.

## What is Infrastructure as Code (IaC)?
IaC is the practice of managing and provisioning infrastructure through code instead of through manual processes.

### The "Immutable" Paradigm
Terraform is an **Immutable Infrastructure** tool.
*   **Mutable (Ansible/Chef)**: You have a server. You run a script to update software. If it fails halfway, your server is in a "broken" state.
*   **Immutable (Terraform)**: You don't update the server. You destroy the old one and create a new one with the new configuration. This guarantees consistency.

## Prerequisites
You are running this on a Windows machine with WSL (Windows Subsystem for Linux). This is the industry standard for Windows-based DevOps.

### Step 1: Verify Your Environment
Open your **WSL Terminal** (Ubuntu) and run:

```bash
terraform version
```

## Your First Project: The "Provider" Concept
Terraform doesn't know how to talk to AWS or Azure natively. It uses **Providers**—plugins that translate HCL code into API calls.

### Step 2: Create the Directory
```bash
mkdir ~/terraform-learning
cd ~/terraform-learning
```

### Step 3: Multi-Provider Configuration
We will use two providers: `local` (files) and `random` (generating random strings). This simulates a real-world scenario where you might use AWS (infrastructure) and Vault (secrets) together.

Create `main.tf`:

```hcl
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

# 1. Generate a random pet name
resource "random_pet" "server_name" {
  length    = 2
  separator = "-"
}

# 2. Create a file using that name
resource "local_file" "server_config" {
  filename = "${path.module}/${random_pet.server_name.id}.conf"
  content  = "Server Name: ${random_pet.server_name.id}\nStatus: Active"
}
```

### Step 4: Initialize
Run:
```bash
terraform init
```
**What happens?**
1.  Terraform reads the `required_providers` block.
2.  It downloads the `local` and `random` binaries from the HashiCorp Registry.
3.  It creates a `.terraform.lock.hcl` file (We'll cover this in Chapter 2).

### Step 5: Apply
Run:
```bash
terraform apply
```
Type `yes`.

**Interactive Check**:
Run `ls` in your terminal. You should see a file with a funny name like `hip-duck.conf`.
Run `cat hip-duck.conf` to see the content.

## Key Takeaway
You defined a **dependency**. The file *depended* on the random name. Terraform figured out the order:
1.  Create `random_pet`.
2.  Read its ID.
3.  Create `local_file`.

You didn't have to tell it "Wait for the name". That is the power of the **Dependency Graph**.
