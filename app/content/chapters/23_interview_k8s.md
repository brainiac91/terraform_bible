# 23. Technical Interview: K8s SysDesign & Operators

## The Kubernetes Data Plane

Interviews for K8s Administrators go far deeper than deploying a `replicaSet`. They dissect the Control Plane's limitations, the networking mesh overhead, and Custom Operator architectures.

### 1. Etcd and the Raft Consensus
`etcd` is the brain. It is inherently distributed. So what happens if 2 nodes crash in a 5-node cluster?
Using the **Raft Consensus Algorithm**, `etcd` requires a mathematical majority (`Quorum = (N/2)+1`) to accept write operations. 
In a 5 node cluster, Quorum is 3. The 3 remaining nodes continue operating normally.
If 3 nodes crash, Quorum is lost. The remaining 2 nodes will enter a Read-Only state to prevent Split-Brain corruption. K8s will continue to route existing traffic, but you cannot schedule any new Pods.

### 2. Operators & Custom Resource Definitions (CRD)
Kubernetes doesn't know what a 'PostgresCluster' is natively. To make it understand:
1. You deploy a **CRD** defining the YAML schema (e.g., `replicas`, `storageSize`, `version`).
2. You write a continuous monitoring script (in Go, Rust, or Python) called an **Operator Controller**. This loop constantly reads your custom `PostgresCluster` yaml object, talks to the AWS/GCP API, and spins up standard Pods and PVCs to fulfill your customized request.

### 3. Hyper-Scaling and Limits 
At 5,000 nodes, the default `kube-proxy` mapping thousands of `iptables` NAT rules sequentially causes CPU deadlock. Traffic latency halts. To fix this at an enterprise scale, architectures rip out `kube-proxy` entirely, substituting the network plugin with **Cilium (eBPF)**, which injects high-speed C-rules directly into the Linux Kernel networking stack, bypassing iptables traversal.
