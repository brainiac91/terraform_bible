# 15. Kubernetes: Architecture & Advanced Concepts

To master Kubernetes, you must understand what happens under the hood when you run `kubectl apply`.

## The Control Plane (The Brain)

The Control Plane makes global decisions about the cluster (like scheduling), and detecting and responding to cluster events.

1. **kube-apiserver:** The front-end of the control plane. All components (and `kubectl`) communicate with it. It validates and configures data for resources.
2. **etcd:** Consistent and highly-available key-value store used as Kubernetes' backing store for all cluster data.
3. **kube-scheduler:** Watches for newly created Pods with no assigned node, and selects a node for them to run on.
4. **kube-controller-manager:** Runs controller processes (like Node Controller, Job Controller, EndpointSlice controller).

## The Worker Nodes (The Muscle)

These machines run the containerized applications.

1. **kubelet:** An agent that runs on each node in the cluster. It ensures that containers are running in a Pod according to the PodSpecs provided by the API server.
2. **kube-proxy:** A network proxy that runs on each node, maintaining network rules on nodes. These network rules allow network communication to your Pods from network sessions inside or outside of your cluster.
3. **Container Runtime:** The software that is responsible for running containers (containerd, CRI-O, Docker Engine).

## Advanced Networking: Ingress

While a **Service** exposes an application internally, an **Ingress** manages external access to the services in a cluster, typically HTTP. Ingress may provide load balancing, SSL termination, and name-based virtual hosting.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: minimal-ingress
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

> [!WARNING]
> An Ingress resource requires an **Ingress Controller** to be installed in the cluster (e.g., NGINX Ingress Controller, Traefik). It will not do anything on its own.
