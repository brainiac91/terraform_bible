# 14. Kubernetes: Manifests & Core Resources

Kubernetes manages everything as **Resources**. We define these resources in YAML files (Manifests) and send them to the API server.

## Core Workload Resources

### 1. The Pod
The smallest deployable unit. Usually runs a single container, but can run multiple (e.g., an app container and a sidecar proxy).
*Rule of thumb: Never deploy a naked Pod in production. They do not self-heal well if the node dies.*

### 2. The Deployment
A Deployment manages a ReplicaSet, which in turn manages Pods. Deployments provide declarative updates.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
```

### 3. The Service
Pods are mortal. They are born, they die, and they get new IP addresses. A **Service** provides a stable IP address and DNS name to abstract away the fluid Pod IP addresses. It load-balances traffic to any Pod matching its selector.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

## Running Manifests

You use `kubectl`, the command-line tool for Kubernetes, to apply these manifests.

```bash
# Apply a file
kubectl apply -f deployment.yaml

# See the running pods
kubectl get pods

# See the services
kubectl get svc
```

> [!IMPORTANT]
> Because Kubernetes is declarative, `kubectl apply` is idempotent out of the box, similar to `terraform apply` or `ansible-playbook`.
