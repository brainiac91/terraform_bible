# 1. Introduction & Setup

Welcome to your journey to becoming a Terraform Expert. By the end of this course, you will be able to architect, deploy, and manage complex infrastructure at scale.

## What is Infrastructure as Code (IaC)?
IaC is the practice of managing and provisioning infrastructure through code instead of through manual processes.
*   **Manual**: Clicking buttons in the AWS Console. Error-prone, hard to replicate.
*   **Scripted**: Bash/Python scripts. Imperative ("Do this, then do that"). Hard to maintain.
*   **Declarative (Terraform)**: You define the *end state*, and the tool figures out how to get there.

## Prerequisites
You are running this on a Windows machine with WSL (Windows Subsystem for Linux). This is the industry standard for Windows-based DevOps.

### Step 1: Verify Your Environment
Open your **WSL Terminal** (Ubuntu) and run:

```bash
terraform version
```

**Troubleshooting**:
*   *Command not found*: Ensure you have installed Terraform in your WSL distribution.
    ```bash
    sudo apt-get update && sudo apt-get install -y gnupg software-properties-common
    wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
    sudo apt update && sudo apt install terraform
    ```

## Your First Terraform Project
We will use the `local` provider to create a file. This avoids the need for cloud credentials for now, allowing us to focus on the **Workflow**.

### Step 2: Create the Directory
In your terminal:
```bash
mkdir ~/terraform-learning
cd ~/terraform-learning
```

### Step 3: Write the Configuration
Create a file named `main.tf`:
```bash
nano main.tf
```

Paste the following **HCL** (HashiCorp Configuration Language) code:

```hcl
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

resource "local_file" "welcome" {
  filename = "${path.module}/welcome.txt"
  content  = "Hello, Future DevOps Expert!"
}
```

*   **terraform block**: Configures Terraform itself (required providers).
*   **resource block**: Defines a piece of infrastructure.
    *   `local_file`: The type of resource.
    *   `welcome`: The internal name (ID) of this resource in your code.

### Step 4: Initialize
Run:
```bash
terraform init
```
**Output**: `Terraform has been successfully initialized!`
This downloads the plugin for the `local` provider.

### Step 5: Apply
Run:
```bash
terraform apply
```
Type `yes` when prompted.

**Result**: Check your directory (`ls`). You will see `welcome.txt`. Cat it (`cat welcome.txt`) to see the content!

## Key Takeaway
You just defined infrastructure (a file) as code. If you delete the file manually, Terraform will know it's missing and recreate it next time. If you change the content in the code, Terraform will update the file.
