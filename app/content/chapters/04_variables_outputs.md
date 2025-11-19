# 4. Variables & Outputs

Hardcoding values (like IPs, names, counts) makes your code brittle. Use Variables to make it dynamic.

## Input Variables
Define them in a `variables.tf` file.

### Basic Syntax
```hcl
variable "filename" {
  type        = string
  description = "The name of the file to create"
  default     = "default.txt"
}
```

### Type Constraints
Always use types!
*   `string`, `number`, `bool`
*   `list(string)`, `map(string)`, `object({ name=string, age=number })`

### Validation (Best Practice)
You can enforce rules on your variables.

```hcl
variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "prod"], var.environment)
    error_message = "Environment must be 'dev' or 'prod'."
  }
}
```

## Setting Variables
Order of precedence (Last one wins):
1.  `default` value in config.
2.  `TF_VAR_filename` environment variable.
3.  `terraform.tfvars` file.
4.  `-var="filename=foo.txt"` command line argument.

**Exercise**:
1.  Create `variables.tf` with the content above.
2.  Update `main.tf` to use it:
    ```hcl
    resource "local_file" "welcome" {
      filename = var.filename
      content  = "Content for ${var.environment}"
    }
    ```
3.  Create a `terraform.tfvars` file:
    ```hcl
    filename    = "production.txt"
    environment = "prod"
    ```
4.  Run `terraform apply`.

## Outputs
Outputs are like return values for your infrastructure.

```hcl
output "file_id" {
  value = local_file.welcome.id
}
```

Run `terraform output` to see them.

### Sensitive Data
If you output a password, mark it sensitive!
```hcl
output "db_password" {
  value     = "supersecret"
  sensitive = true
}
```
Terraform will redact this in the CLI ("<sensitive>"), but it is **still visible in the state file**.
