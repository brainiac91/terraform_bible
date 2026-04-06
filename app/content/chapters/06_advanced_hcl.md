# 6. Advanced HCL Patterns

HCL is not just configuration; it's a programming language.

## 1. Splat Expressions (`*`)
Extract a list of attributes from a list of objects.

```hcl
# Assume you created 3 servers with count = 3
output "all_ips" {
  value = aws_instance.web[*].public_ip
}
# Result: ["1.2.3.4", "5.6.7.8", "9.10.11.12"]
```

## 2. The `for` Expression
Transform lists and maps. Like Python list comprehensions.

```hcl
variable "names" {
  default = ["alice", "bob", "charlie"]
}

output "upper_names" {
  value = [for name in var.names : upper(name)]
}
# Result: ["ALICE", "BOB", "CHARLIE"]

# Filter a list
output "short_names" {
  value = [for name in var.names : name if length(name) < 4]
}
# Result: ["bob"]
```

## 3. Dynamic Blocks with Objects
The most powerful pattern for complex resources (like Load Balancers).

```hcl
variable "ingress_rules" {
  type = list(object({
    port        = number
    description = string
    cidr        = list(string)
  }))
  default = [
    { port = 80, description = "HTTP", cidr = ["0.0.0.0/0"] },
    { port = 22, description = "SSH",  cidr = ["10.0.0.0/8"] }
  ]
}

resource "aws_security_group" "main" {
  name = "dynamic-sg"

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = "tcp"
      description = ingress.value.description
      cidr_blocks = ingress.value.cidr
    }
  }
}
```
This creates a Security Group that adapts to however many rules you define in the variable.
