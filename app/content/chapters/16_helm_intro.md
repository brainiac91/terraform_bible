# 16. Helm: The Kubernetes Package Manager

Kubernetes manifests are powerful, but they are static. What if you need to deploy the same application to `dev`, `staging`, and `prod`, but with different replica counts and database passwords?

Duplicating YAML files is a violation of the **DRY (Don't Repeat Yourself)** principle. This is where **Helm** comes in.

## What is Helm?

Helm is the Package Manager for Kubernetes. Think of it like `apt`, `yum`, or `npm`, but for Kubernetes.

It uses a packaging format called **Charts**. A Chart is a collection of files that describe a related set of Kubernetes resources.

### Core Concepts:
1. **Chart:** A bundle of information necessary to create an instance of a Kubernetes application.
2. **Config:** Contains configuration information that can be merged into a packaged chart to create a releasable object.
3. **Release:** A running instance of a chart, combined with a specific config.

## Why Use Helm?

1. **Templating:** Helm uses Go templates inside Kubernetes manifests. You can use variables, if/else statements, and loops to generate dynamic YAML.
2. **Reusability:** You can install publicly available charts (e.g., WordPress, Redis, NGINX Ingress) written by experts.
3. **Rollbacks:** Helm tracks versions of your releases. If an upgrade fails, `helm rollback <release_name>` instantly reverts the cluster state to the previous version.

## Basic Commands

Add a public repository:
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

Install a chart (create a release):
```bash
helm install my-redis bitnami/redis
```

Upgrade a release with new values:
```bash
helm upgrade my-redis bitnami/redis --set replicaCount=3
```

List installed releases:
```bash
helm ls
```
