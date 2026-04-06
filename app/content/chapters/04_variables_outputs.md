# 4. Variables & Outputs

Hardcoding values is an anti-pattern. Use Input Variables to make your code reusable.

## Complex Types
Strings are boring. Let's use Objects.

```hcl
variable "server_config" {
  type = object({
    name      = string
    instances = number
    tags      = map(string)
  })
  
  default = {
    name      = "web"
    instances = 2
    tags      = { Environment = "Dev" }
  }
}
```

## Validation with Regex
You can enforce strict rules.

```hcl
variable "image_id" {
  type        = string
  description = "The ID of the machine image (AMI)"

  validation {
    condition     = can(regex("^ami-[a-z0-9]{8,17}$", var.image_id))
    error_message = "The image_id must start with 'ami-', followed by alphanumeric characters."
  }
}
```

## The `tfvars` Ecosystem
How do you set variables in production?

1.  **terraform.tfvars**: Automatically loaded. Good for default values.
2.  **prod.tfvars**: Explicitly loaded.
    ```bash
    terraform apply -var-file="prod.tfvars"
    ```
3.  **Environment Variables**: Good for secrets (CI/CD).
    ```bash
    export TF_VAR_db_password="correct-horse-battery-staple"
    ```

## Outputs & `terraform_remote_state`
Outputs are the "API" of your module.

**Scenario**: Your Network team creates a VPC. Your App team needs the VPC ID.
1.  **Network Team**:
    ```hcl
    output "vpc_id" { value = aws_vpc.main.id }
    ```
2.  **App Team**:
    ```hcl
    data "terraform_remote_state" "network" {
      backend = "s3"
      config = {
        bucket = "network-state"
        key    = "terraform.tfstate"
      }
    }
    
    resource "aws_instance" "web" {
      subnet_id = data.terraform_remote_state.network.outputs.vpc_id
    }
    ```
This decouples your teams while keeping them connected.
