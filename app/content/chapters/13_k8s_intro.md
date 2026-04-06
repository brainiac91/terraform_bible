# 13. Kubernetes: Introduction to Container Orchestration

Containers changed how we package applications, but managing hundreds of containers across dozens of servers is chaotic. **Kubernetes (K8s)** is the orchestrator that solves this problem.

## What is Kubernetes?

Kubernetes is an open-source system for automating deployment, scaling, and management of containerized applications.

If Docker is the engine of a single car, Kubernetes is the city's traffic management system. It decides where cars go, when bridges open, and handles accidents automatically.

### Key Features
- **Service Discovery & Load Balancing:** K8s can expose a container using a DNS name or its own IP address.
- **Storage Orchestration:** Automatically mount local storage, public cloud providers, and more.
- **Automated Rollouts/Rollbacks:** Describe the desired state, and K8s changes the actual state to the desired state at a controlled rate.
- **Self-Healing:** Restarts containers that fail, replaces containers, kills containers that don't respond to health checks.

## The Shift to Declarative Models

Just like Terraform, Kubernetes uses a declarative model via YAML. You don't tell Kubernetes *how* to deploy a container; you tell it what the end result must look like.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx
    image: nginx:1.14.2
    ports:
    - containerPort: 80
```

> [!TIP]
> The atom of Kubernetes is not a Container, it is a **Pod**. A Pod is a wrapper around one or more containers that share the same network, IP, and storage namespace.
