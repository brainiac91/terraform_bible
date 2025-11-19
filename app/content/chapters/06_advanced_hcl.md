# 6. Advanced HCL Patterns

This is where you separate the juniors from the seniors. HCL is a powerful language if you know how to use it.

## Loops: `count` vs `for_each`

### The `count` Meta-Argument
Creates N copies of a resource.
```hcl
resource "local_file" "copies" {
  count    = 3
  filename = "file_${count.index}.txt"
  content  = "I am number ${count.index}"
}
```
*   **Problem**: If you remove item 0, items 1 and 2 shift index, causing Terraform to recreate them.

### The `for_each` Meta-Argument (Preferred)
Iterates over a map or set. Stable keys mean no unnecessary recreation.

```hcl
variable "files" {
  type = map(string)
  default = {
    "config" = "Config data",
    "logs"   = "Log setup"
  }
}

resource "local_file" "loop" {
  for_each = var.files
  
  filename = "${each.key}.txt"
  content  = each.value
}
```

## Dynamic Blocks
Used to generate nested blocks (like `ingress` rules in a security group) dynamically.

```hcl
resource "aws_security_group" "example" {
  name = "example"

  dynamic "ingress" {
    for_each = [80, 443, 8080]
    content {
      from_port = ingress.value
      to_port   = ingress.value
      protocol  = "tcp"
    }
  }
}
```

## Terraform Functions
*   `try(local.foo, "fallback")`: Great for optional values.
*   `yamldecode(file("config.yaml"))`: Read config from YAML files.
*   `templatefile("script.sh.tftpl", { name = "Alin" })`: Generate scripts with variable substitution.

## Import Blocks (New in v1.5+)
If you have existing infrastructure created manually, you can bring it under Terraform control without complex CLI commands.

```hcl
import {
  to = aws_s3_bucket.legacy
  id = "my-existing-bucket-name"
}
```
Run `terraform plan`, and Terraform will generate the code for you!
