# 5. Module Architecture

As your infrastructure grows, a single `main.tf` becomes unmanageable. Modules allow you to package resources into reusable components.

## What is a Module?
Any directory with `.tf` files is a module.
*   **Root Module**: The directory where you run `terraform apply`.
*   **Child Module**: A module called by another module.

## Creating a Local Module
**Exercise**: Let's refactor our file creator into a module.

1.  Create a folder `modules/file_creator`.
2.  Inside it, create `main.tf`, `variables.tf`, and `outputs.tf`.

**modules/file_creator/variables.tf**:
```hcl
variable "path" { type = string }
variable "content" { type = string }
```

**modules/file_creator/main.tf**:
```hcl
resource "local_file" "file" {
  filename = var.path
  content  = var.content
}
```

**modules/file_creator/outputs.tf**:
```hcl
output "id" { value = local_file.file.id }
```

## Calling the Module
Go back to your root `main.tf` and replace the resource with:

```hcl
module "my_file" {
  source  = "./modules/file_creator"
  
  path    = "${path.module}/module_test.txt"
  content = "Created by a module!"
}
```

Run `terraform init` (required whenever you add a module) and `terraform apply`.

## The Terraform Registry
You don't have to write everything from scratch. The [Terraform Registry](https://registry.terraform.io/) has thousands of verified modules (e.g., AWS VPC, EKS).

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = "my-vpc"
  cidr = "10.0.0.0/16"
  # ...
}
```

**Best Practice**: Always pin the `version` to avoid breaking changes when the module author updates it.
