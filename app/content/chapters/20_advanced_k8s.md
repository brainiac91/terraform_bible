# 20. Advanced Kubernetes: eBPF & SPIFFE/SPIRE

## The Death of the Sidecar

Legacy service meshes (like old Istio or Linkerd) relied on injecting proxy containers alongside every single Pod in your cluster. This doubled RAM consumption. 

In 2026, **eBPF (Extended Berkeley Packet Filter)** rules the control plane. Tools like **Cilium** attach directly to the Linux Kernel to observe, route, and secure traffic without ever breaking out into user-space proxies. 

### SPIFFE: Zero Trust Workload Identity
Stop using API keys! If a Pod needs to talk to a strictly locked-down vault, it shouldn't hold a static `secret.yaml`. 

**SPIFFE/SPIRE** issues short-lived cryptographic identity documents (SVIDs) directly to the Pod workload based on deep attestation checks (namespace, node, image hash). The JWT token rotates every few minutes.

```yaml
apiVersion: spiffeid.spiffe.io/v1beta1
kind: SpiffeID
metadata:
  name: payment-service
spec:
  spiffeId: spiffe://example.org/ns/finance/sa/payment
  podSelector:
    matchLabels:
      app: payment
```

### GitOps Sync

Imperative `kubectl apply` commands are banned in modern platforms. You check manifests into GitHub, and **ArgoCD** or **Flux** dynamically reaches out, sees the delta, and pulls the state into your cluster continuously.
