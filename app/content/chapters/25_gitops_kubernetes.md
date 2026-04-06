# 25. GitOps & Advanced Orchestration

If CI/CD Pipelines are the standard for Terraform execution, **GitOps** is the 2026 standard for Kubernetes application delivery.

Before GitOps, a CI pipeline (like Jenkins) would run `docker build`, then literally execute `kubectl apply -f manifest.yaml` to *push* changes into a cluster. This is called the "Push Model."

## The Flaws of the Push Model
1. Your CI Server needs cluster admin credentials.
2. If a system admin runs `kubectl edit deployment my-app` directly on the cluster, they introduce "Configuration Drift". Your Git repository no longer reflects reality. If the cluster dies, you cannot rebuild it exactly as it was.

## The GitOps Paradigm (The Pull Model)

GitOps dictates that **Git is the absolute, single source of truth** for your system state.

We deploy an Operator—an intelligent software agent like **ArgoCD** or **FluxCD**—directly *inside* the Kubernetes cluster. This agent continuously reaches *out* (pulls) to your GitHub repository, reads the YAML or Helm charts, and compares them against the live cluster.

### Continuous Reconciliation
If the Git repository says "replicas: 3" and the cluster currently has "replicas: 3", ArgoCD reports `Synced` and `Healthy`.

If an intruder forcefully edits the cluster to "replicas: 10", ArgoCD's reconciliation loop detects the drift instantly. Because Git is the single source of truth, ArgoCD will forcefully and automatically revert the cluster back to "replicas: 3". **No human intervention. Total immutability.**

## Understanding ArgoCD Custom Resources

ArgoCD extends the Kubernetes API by introducing the `Application` Custom Resource Definition (CRD).

Instead of managing individual deployments, you manage an `Application` manifest that references a Git repo.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: billing-service
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/my-org/k8s-manifests.git'
    path: apps/billing/overlays/production
    targetRevision: HEAD # Automatically tracks the main branch
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: production
  syncPolicy:
    automated:
      prune: true     # If a file is deleted in Git, delete it in the cluster.
      selfHeal: true  # If cluster drift occurs, fix it automatically.
```

### The App of Apps Pattern
How do you deploy 500 microservices? You don't create 500 `Application` YAMLs manually.
You create a single "Root Application" in ArgoCD that points to a GitHub directory containing 500 `Application` YAMLs. ArgoCD syncs the root, discovers the 500 children, and recursively syncs the entire enterprise from one directory.

## Key Takeaway
GitOps bridges the gap between infrastructure declarations and running cluster reality. By embedding ArgoCD inside the network, you remove inbound firewall holes, strip CI/CD servers of cluster admin privileges, and guarantee that what is written in Git is exactly what exists in production.
