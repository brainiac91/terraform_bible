[
    {
        id: 1,
        title: "The Public Bucket",
        desc: "A junior dev accidentally committed code that makes our customer data bucket public. Fix it immediately before the security bot flags it.",
        code: `resource "aws_s3_bucket" "customer_data" {
  bucket = "acme-customer-data"
  acl    = "public-read" # <--- DANGER
  
  tags = {
    Environment = "Production"
  }
}`,
        objectives: ["Change ACL to 'private'", "Ensure tags remain"],
        validator: (code) => code.includes('acl') && (code.includes('"private"') || code.includes("'private'")) && !code.includes('public-read')
    },
    {
        id: 2,
        title: "Hardcoded Secrets",
        desc: "We found a database password hardcoded in the main configuration. Replace it with a variable reference.",
        code: `resource "aws_db_instance" "default" {
  allocated_storage = 10
  engine            = "mysql"
  username          = "admin"
  password          = "SuperSecret123!" # <--- FIX THIS
}`,
        objectives: ["Remove the hardcoded string", "Use 'var.db_password'"],
        validator: (code) => !code.includes('SuperSecret123!') && code.includes('var.db_password')
    },
    {
        id: 3,
        title: "Missing Version Pin",
        desc: "The provider configuration is missing a version constraint. This caused a breaking change in production. Pin the AWS provider to version 5.0.",
        code: `terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      # Missing version
    }
  }
}`,
        objectives: ["Add 'version = \"~> 5.0\"'"],
        validator: (code) => code.includes('version') && code.includes('5.0')
    },
    {
        id: 4,
        title: "The Open Door",
        desc: "Security Alert! Someone opened SSH (port 22) to the entire world. Restrict it to the corporate VPN IP (10.0.0.0/8).",
        code: `resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow SSH inbound traffic"

  ingress {
    description = "SSH from VPC"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # <--- DANGER
  }
}`,
        objectives: ["Change cidr_blocks to '10.0.0.0/8'"],
        validator: (code) => code.includes('10.0.0.0/8') && !code.includes('0.0.0.0/0')
    },
    {
        id: 5,
        title: "Fat Finger Typo",
        desc: "Deployment failed. The developer typed 't2.microo' instead of 't2.micro'. Fix the instance type.",
        code: `resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.microo" # <--- OOPS
}`,
        objectives: ["Change type to 't2.micro'"],
        validator: (code) => code.includes('t2.micro') && !code.includes('t2.microo')
    },
    {
        id: 6,
        title: "Unencrypted Volume",
        desc: "Compliance Check Failed: All EBS volumes must be encrypted. Enable encryption for this volume.",
        code: `resource "aws_ebs_volume" "example" {
  availability_zone = "us-west-2a"
  size              = 40
  
  tags = {
    Name = "HelloWorld"
  }
}`,
        objectives: ["Add 'encrypted = true'"],
        validator: (code) => code.includes('encrypted') && (code.includes('true') || code.includes('= true'))
    },
    {
        id: 7,
        title: "Missing Tag",
        desc: "Cost allocation failed. Every resource must have a 'CostCenter' tag. Add 'CostCenter = \"IT-101\"' to the instance.",
        code: `resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  
  tags = {
    Name = "WebServer"
    # Missing CostCenter
  }
}`,
        objectives: ["Add 'CostCenter = \"IT-101\"'"],
        validator: (code) => code.includes('CostCenter') && code.includes('IT-101')
    },
    {
        id: 8,
        title: "Invalid CIDR",
        desc: "Network creation failed. The CIDR block '10.0.0.0/33' is invalid. Fix it to be a valid /24 subnet.",
        code: `resource "aws_subnet" "main" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.0.0/33" # <--- INVALID
}`,
        objectives: ["Change cidr_block to '10.0.0.0/24'"],
        validator: (code) => code.includes('10.0.0.0/24')
    },
    {
        id: 9,
        title: "IAM Wildcard",
        desc: "Security Audit: An IAM policy allows '*' action on all resources. Restrict it to 's3:ListBucket' only.",
        code: `resource "aws_iam_policy" "policy" {
  name        = "test_policy"
  description = "My test policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "*",
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}`,
        objectives: ["Change Action to 's3:ListBucket'"],
        validator: (code) => code.includes('s3:ListBucket') && !code.includes('"Action": "*"')
    },
    {
        id: 10,
        title: "Output Exposure",
        desc: "You are outputting a database password in plain text. Mark the output as sensitive.",
        code: `output "db_password" {
  value = aws_db_instance.default.password
  # Missing sensitive flag
}`,
        objectives: ["Add 'sensitive = true'"],
        validator: (code) => code.includes('sensitive') && code.includes('true')
    },
    {
        id: 11,
        title: "Deprecated Interpolation",
        desc: "Code Review: We are updating to HCL2. Remove the deprecated '${}' syntax for variable access.",
        code: `resource "aws_instance" "web" {
  ami = "\${var.ami_id}" # <--- OLD SYNTAX
}`,
        objectives: ["Change to 'var.ami_id'"],
        validator: (code) => code.includes('ami = var.ami_id') || code.includes('ami =var.ami_id')
    },
    {
        id: 12,
        title: "Wrong Resource Type",
        desc: "Syntax Error: You are trying to create an S3 bucket but used 'aws_s3_bucket_object'. Fix the resource type.",
        code: `resource "aws_s3_bucket_object" "my_bucket" {
  bucket = "my-new-bucket"
  acl    = "private"
}`,
        objectives: ["Change resource to 'aws_s3_bucket'"],
        validator: (code) => code.includes('resource "aws_s3_bucket"')
    },
    {
        id: 13,
        title: "Missing Backend",
        desc: "State Danger: This configuration is using local state. Configure an S3 backend with bucket 'my-tfstate'.",
        code: `terraform {
  # Missing backend configuration
}`,
        objectives: ["Add 'backend \"s3\"'", "Set bucket to 'my-tfstate'"],
        validator: (code) => code.includes('backend "s3"') && code.includes('my-tfstate')
    },
    {
        id: 14,
        title: "Circular Dependency",
        desc: "Logic Error: Security Group A references B, and B references A inline. Break the cycle by using 'aws_security_group_rule' for one of them.",
        code: `resource "aws_security_group" "sg_a" {
  ingress { security_groups = [aws_security_group.sg_b.id] }
}

resource "aws_security_group" "sg_b" {
  ingress { security_groups = [aws_security_group.sg_a.id] }
}`,
        objectives: ["Remove inline ingress from one SG", "Use standalone rule resource"],
        validator: (code) => code.includes('aws_security_group_rule')
    },
    {
        id: 15,
        title: "Hardcoded Region",
        desc: "Portability: The region is hardcoded to 'us-east-1'. Change it to use the 'var.aws_region' variable.",
        code: `provider "aws" {
  region = "us-east-1"
}`,
        objectives: ["Change region to 'var.aws_region'"],
        validator: (code) => code.includes('var.aws_region')
    },
    {
        id: 16,
        title: "Public RDS",
        desc: "Security: The RDS instance is publicly accessible. Set 'publicly_accessible' to false.",
        code: `resource "aws_db_instance" "default" {
  instance_class      = "db.t3.micro"
  publicly_accessible = true # <--- NO!
}`,
        objectives: ["Set publicly_accessible = false"],
        validator: (code) => code.includes('publicly_accessible') && code.includes('false')
    },
    {
        id: 17,
        title: "Missing Lifecycle",
        desc: "Safety: Prevent accidental deletion of this critical database. Add a lifecycle block with 'prevent_destroy = true'.",
        code: `resource "aws_db_instance" "critical" {
  instance_class = "db.t3.large"
  # Missing lifecycle
}`,
        objectives: ["Add lifecycle block", "Set prevent_destroy = true"],
        validator: (code) => code.includes('lifecycle') && code.includes('prevent_destroy') && code.includes('true')
    },
    {
        id: 18,
        title: "Incorrect Count",
        desc: "Logic: We need 3 instances, but the count is set to 1. Update the count.",
        code: `resource "aws_instance" "web" {
  count         = 1
  instance_type = "t2.micro"
}`,
        objectives: ["Set count = 3"],
        validator: (code) => code.includes('count') && (code.includes('3') || code.includes('= 3'))
    },
    {
        id: 19,
        title: "Wrong Attribute Reference",
        desc: "Syntax: You are trying to access the public IP of an instance using 'publicip'. The correct attribute is 'public_ip'.",
        code: `output "ip" {
  value = aws_instance.web.publicip
}`,
        objectives: ["Change to 'public_ip'"],
        validator: (code) => code.includes('public_ip')
    },
    {
        id: 20,
        title: "Provisioner Cleanup",
        desc: "Best Practice: 'local-exec' provisioners are brittle. Remove the provisioner block entirely.",
        code: `resource "aws_instance" "web" {
  instance_type = "t2.micro"
  
  provisioner "local-exec" {
    command = "echo ${aws_instance.web.private_ip} >> private_ips.txt"
  }
}`,
        objectives: ["Remove the provisioner block"],
        validator: (code) => !code.includes('provisioner') && !code.includes('local-exec')
    },
    {
        id: 21,
        title: "Unquoted String",
        desc: "Syntax: The AMI ID is a string and must be quoted.",
        code: `resource "aws_instance" "web" {
  ami = ami-12345678 # <--- Syntax Error
}`,
        objectives: ["Add quotes around the AMI ID"],
        validator: (code) => code.includes('"ami-12345678"')
    }
]
