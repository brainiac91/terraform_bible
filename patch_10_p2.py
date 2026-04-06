import json
import re

file_path = 'app/routers/bible.py'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

q_bank = {
    "09_security": [
        {"q": "What is the primary danger of using `provisioner \"local-exec\"` with embedded AWS access keys?", "options": ["The keys are saved permanently in the `.terraform.lock.hcl` file", "The block's entire resolved string evaluation, including secrets, is written in plaintext to the `terraform.tfstate` file", "AWS revokes them immediately", "Provisioners fail constantly"], "a": 1},
        {"q": "How does Terraform Enterprise/Cloud implement RBAC for workspace runs compared to open source Terraform?", "options": ["It doesn't, it uses regular IAM", "It abstracts API execution behind Team and Workspace permissions, preventing developers from downloading the root AWS credentials directly", "It forces Python syntax", "It encrypts the console"], "a": 1},
        {"q": "If you must perform dynamic policy checks against the physical cloud state instead of the Terraform plan JSON, what tool do you use?", "options": ["Checkov", "OPA (evaluating tfplan)", "AWS Config or Cloud Custodian", "tfsec"], "a": 2},
        {"q": "What attribute natively ensures that a resource parameter (like a generated RDS password) is concealed from the local CLI output during an apply?", "options": ["secret = true", "hidden = true", "sensitive = true", "encrypt = true"], "a": 2},
        {"q": "If you expose a `sensitive = true` output, does it prevent the secret from entering the `terraform.tfstate`?", "options": ["Yes", "No. State files always contain sensitive values in plaintext. The flag ONLY masks CLI output.", "Only in Terraform Cloud", "Yes, it encrypts it"], "a": 1},
        {"q": "To strictly enforce that developers cannot provision high-cost instances like `p3.16xlarge`, you write an OPA Rego policy. Which phase of the pipeline does OPA evaluate?", "options": ["`terraform init`", "The output JSON of `terraform plan` BEFORE allowing `terraform apply` to run", "After the instances are created", "During state refresh"], "a": 1}
    ],
    "10_ansible_intro": [
        {"q": "What is the implicit transport layer default Ansible relies upon for Linux targets?", "options": ["SNMP", "WinRM", "OpenSSH", "gRPC"], "a": 2},
        {"q": "How does Ansible handle parallel execution across nodes by default?", "options": ["Iterates linearly one by one", "Forks 5 processes simultaneously and batches the execution across the inventory", "Spawns infinite threads", "Delegates to Docker"], "a": 1},
        {"q": "What command structure would execute a raw shell command exclusively against nodes belonging to BOTH 'web' and 'db' groups?", "options": ["ansible 'web,db' -m shell -a 'uptime'", "ansible 'web:&db' -m shell -a 'uptime'", "ansible 'web!db' -m shell -a 'uptime'", "ansible all -m shell -a 'uptime'"], "a": 1},
        {"q": "Where does the Ansible control node natively store gathered device facts automatically without configuring a persistent cache?", "options": ["In memory during the playbook run", "In a local SQLite database", "In `/etc/ansible/facts`", "In an S3 bucket"], "a": 0},
        {"q": "What mechanism allows you to bypass the SSH paradigm to configure API endpoints (like an F5 Load Balancer)?", "options": ["You can't", "Using `connection: local` on the control node combined with the relevant API module", "Installing bash on the F5", "Using `connection: telnet`"], "a": 1},
        {"q": "If you run `ansible all -m setup`, what precisely are you doing?", "options": ["Installing Python on all nodes", "Gathering and printing the sprawling dictionary of System Facts for all inventory nodes", "Testing ping latency", "Formatting the inventory"], "a": 1}
    ],
    "11_ansible_playbooks": [
        {"q": "During a playbook failure, what does the resulting `.retry` file contain?", "options": ["The error logs", "The specific list of hostnames that failed, allowing you to re-run the playbook exclusively targeted at them", "A backup of the previous configuration", "Instructions on how to fix it"], "a": 1},
        {"q": "In an Ansible task, what is the hierarchical relationship between `block`, `rescue`, and `always`?", "options": ["Rescue runs first", "Block executes; if it errors, Rescue executes to recover; Always executes regardless of Block/Rescue success, similar to try/catch/finally", "They run in parallel", "Always runs first"], "a": 1},
        {"q": "If you set `serial: 20%` inside a playbook targeting 100 webservers, what deployment pattern is established?", "options": ["A rolling update. It updates 20 servers at a time, moving to the next 20 only if the previous batch succeeds.", "It randomly skips 20% of servers", "It throttles bandwidth by 20%", "It fails immediately"], "a": 0},
        {"q": "To prevent an asynchronous, long-running job (like a massive DB schema update) from blocking the SSH connection indefinitely, which directives do you use?", "options": ["detach: true", "async: <seconds> and poll: 0 (or a set interval)", "background: true", "nohup: true"], "a": 1},
        {"q": "What is the primary difference between the `command` and `shell` modules?", "options": ["command requires root", "shell passes the command through `/bin/sh`, allowing pipes (|) and redirects (>), whereas command executes the executable directly without shell mechanics", "shell is deprecated", "no difference"], "a": 1},
        {"q": "How do you enforce idempotency on a `shell` module task that compiles a binary?", "options": ["Add `ignore_errors: true`", "Add the `creates: /path/to/binary` parameter. Ansible will gracefully skip the shell task if that file already exists.", "Run it twice", "You cannot"], "a": 1}
    ],
    "12_ansible_roles_advanced": [
        {"q": "In a Galaxy Role structure, what is the functional difference between `vars/main.yml` and `defaults/main.yml`?", "options": ["There is no difference", "`defaults/main.yml` provides baseline values with the absolute LOWEST precedence, easily overridden by any external variable. `vars/main.yml` provides internal role variables with HIGH precedence.", "vars is for passwords", "defaults is deprecated"], "a": 1},
        {"q": "When writing an Ansible Role, what directory inherently houses custom embedded Python modules packaged with the role?", "options": ["/python", "/library", "/modules", "/plugins"], "a": 1},
        {"q": "How does `ansible-pull` reverse the standard execution architecture?", "options": ["It uses FTP", "Instead of a central server pushing SSH commands, cronjobs on the target nodes periodically pull a Git repo and execute the playbook locally against `localhost`", "It pulls data from AWS", "It deletes servers"], "a": 1},
        {"q": "When configuring large dynamic inventories (e.g., thousands of EC2 endpoints), what severely bottlenecks the start time of the playbook, and how is it fixed?", "options": ["Bandwidth; use 5G", "Fact gathering; disable implicit gathering via `gather_facts: no` and rely on a centralized Redis/Memcached Fact Cache", "Python parsing; use Go", "YAML syntax"], "a": 1},
        {"q": "What specific file inside an Ansible Role dictates its dependencies upon other Galaxy roles?", "options": ["requirements.txt", "package.json", "meta/main.yml", "dependencies.yaml"], "a": 2},
        {"q": "If you encrypt a specific variable string inside a YAML file rather than encrypting the whole file, what feature are you using?", "options": ["GPG Inline", "Vault IDs", "Ansible Vault Inline String Encryption (`!vault |`)", "Base64"], "a": 2}
    ],
    "13_k8s_intro": [
        {"q": "What is the underlying Linux container primitive that heavily isolates a Pod's memory space?", "options": ["Chroot", "Linux Namespaces and Cgroups", "Hypervisors", "systemd"], "a": 1},
        {"q": "What exactly does a Kubernetes `Service` of type `ClusterIP` rely upon within the node operating system to route traffic?", "options": ["NGINX", "iptables or IPVS (managed by kube-proxy) programming local DNAT rules", "A physical hardware router", "DNS exclusively"], "a": 1},
        {"q": "When writing a Pod manifest, what `restartPolicy` guarantees a Batch Job will NOT restart endlessly after it successfully completes?", "options": ["Always", "Never or OnFailure", "Timeout", "Exit0"], "a": 1},
        {"q": "What component is directly responsible for mounting volumes into the underlying container runtime?", "options": ["kube-apiserver", "The Kubelet", "etcd", "kube-scheduler"], "a": 1},
        {"q": "If a Pod requires a dedicated GPU, how does the control plane know which node to place it on?", "options": ["It guesses", "The kube-scheduler analyzes the Pod's `resources.requests` and node labels/taints, then binds the Pod to a node with sufficient unallocated GPU capacity", "The user types the IP", "etcd routes it randomly"], "a": 1},
        {"q": "Why is running a container as `privileged: true` considered a massive security violation in K8s?", "options": ["It costs too much", "It completely bypasses cgroup isolation, granting the container near-root capabilities over the underlying host Kernel and Node hardware", "It exposes port 80", "It disables logging"], "a": 1}
    ],
    "14_k8s_manifests": [
        {"q": "In a DaemonSet architecture, what determines if a Pod spins up on a newly joined cluster Node?", "options": ["A manual command", "A deployment trigger", "The DaemonSet Controller automatically evaluates the new Node. If it matches the nodeSelector/affinity, it instantly schedules exactly one Pod onto it", "Nothing"], "a": 2},
        {"q": "What happens to the previously established Pods when you delete a ReplicaSet but pass the `--cascade=orphan` (formerly `--cascade=false`) flag?", "options": ["They are corrupted", "The ReplicaSet API object is deleted, but the Pods are intentionally left running unmanaged in the cluster", "They instantly crash", "They freeze"], "a": 1},
        {"q": "Regarding Probes, what defines a situation where a Pod is running, but is NOT ready to receive HTTP traffic from a Service?", "options": ["Liveness Probe failed", "Readiness Probe failed", "Startup Probe failed", "Network crash"], "a": 1},
        {"q": "If an autoscaler defines `targetCPUUtilizationPercentage: 80`, what specifically does the HorizontalPodAutoscaler (HPA) algorithm do when traffic spikes?", "options": ["Kills the master node", "Queries the Metrics Server, dynamically calculates desired replicas based on CPU load, and updates the targeted Deployment/ReplicaSet scale count", "Requests more RAM", "Limits traffic"], "a": 1},
        {"q": "When a PersistentVolumeClaim (PVC) has `accessModes: ReadWriteOnce`, what physical limitation exists?", "options": ["It cannot be read", "The underlying storage volume can be firmly mounted as read-write by exactly ONE generic cluster Node at a time", "It cannot be written to", "Only one user can see it"], "a": 1},
        {"q": "What is an InitContainer, and what happens if it constantly fails?", "options": ["A fast container. The main pod runs anyway.", "A prep container that runs to completion before the main app starts. If it fails, K8s continually restarts the Pod, preventing the main application from ever starting.", "A logging daemon.", "A proxy."], "a": 1}
    ],
    "15_k8s_architecture": [
        {"q": "When the kube-scheduler binds a Pod to Node A, how does Node A actually receive the instruction to pull the image and start the Docker/containerd process?", "options": ["The scheduler SSHs into Node A", "The Kubelet on Node A continuously long-polls/watches the API Server. It notices a Pod bound to 'Node A' and initiates the runtime execution locally", "etcd sends an email", "A webhook is fired"], "a": 1},
        {"q": "What is the extreme consequence of etcd compaction failing and the database hitting its 2GB hard quota?", "options": ["Kubernetes runs faster", "etcd enters a read-only state. The entire Control Plane locks up, and you can no longer apply, delete, or update any resources until it is defragmented", "Pods crash", "Nodes restart"], "a": 1},
        {"q": "What mechanism does the Kube-APIServer use to authenticate incoming external webhook traffic BEFORE it processes authorization (RBAC)?", "options": ["Basic Auth", "Passwords", "X.509 Client Certificates, OIDC tokens, or Service Account Bearer Tokens", "IP whitelisting"], "a": 2},
        {"q": "Explain the architectural difference between a MutatingAdmissionWebhook and a ValidatingAdmissionWebhook.", "options": ["They are the same", "Mutating Webhooks intercept an API request (e.g. creating a Pod) and physically alter the JSON payload (like injecting a proxy sidecar). Validating Webhooks run AFTER mutation to strictly approve or reject the final object.", "Mutating destroys pods", "Validating writes code"], "a": 1},
        {"q": "What is the primary architectural bottleneck of the `kube-proxy` iptables mode when a cluster reaches 5,000+ services?", "options": ["Disk space", "iptables processes rules sequentially. 5,000 services mean massive sequential evaluations for every packet, causing exponential latency degradation. Migration to IPVS or eBPF becomes mandatory", "RAM usage", "Bandwidth caps"], "a": 1},
        {"q": "In a highly available (HA) multi-master K8s control plane, how is the `kube-controller-manager` prevented from running duplicate overlapping reconciliation loops?", "options": ["They talk over TCP", "Only one controller is active at a time via Lead Election mechanisms locked using native Kubernetes Leases/Endpoints, while the others remain on hot standby", "etcd balances them", "They all run together"], "a": 1}
    ],
    "16_helm_intro": [
        {"q": "When running `helm install`, where does Helm v3 natively store the exact binary release state information documenting the installation?", "options": ["In a Tiller pod", "As a Kubernetes Secret or ConfigMap directly inside the target namespace", "In an S3 bucket", "In local laptop metadata"], "a": 1},
        {"q": "How does Helm guarantee atomic deployments across multi-resource charts (e.g., ensuring the DB and the Web App both succeed, or both rollback)?", "options": ["It doesn't", "By using the `--atomic` flag. Helm waits for all resources to reach a Ready state. If they timeout, Helm automatically purges the release entirely.", "Using Terraform", "By pausing the cluster"], "a": 1},
        {"q": "Why did Helm v3 completely remove the `Tiller` server-side component?", "options": ["It was too slow", "Tiller required excessive root-level RBAC cluster permissions, creating a massive centralized security vulnerability footprint. Helm v3 now relies purely on your local kubeconfig RBAC context.", "It used too much RAM", "Google requested it"], "a": 1},
        {"q": "If you wish to pass an array of lists dynamically into a Helm chart without touching `values.yaml`, how do you format the CLI command?", "options": ["You cannot", "Use `helm install --set list\\[0\\]=a,list\\[1\\]=b`", "Use JSON strings", "Use basic comma strings"], "a": 1},
        {"q": "What happens during a `helm upgrade` if you have manually used `kubectl edit` to dramatically alter a deployment managed by Helm?", "options": ["Helm crashes", "Helm v3 uses an advanced 3-way strategic merge patch. It compares the old chart, the new chart, and the *current live cluster state*, ensuring manual additions aren't blindly destroyed unless they conflict directly.", "Helm deletes the deployment", "Helm ignores the upgrade"], "a": 1},
        {"q": "What does `helm template` specifically output during execution?", "options": ["The cluster URL", "The fully rendered raw YAML exactly as it would be sent to the API Server, allowing you to bypass Helm execution and apply via separate GitOps pipelines.", "An active release ID", "A zip file"], "a": 1}
    ]
}

def inject():
    global text
    for ch_id, questions in q_bank.items():
        idx = text.find(f'"id": "{ch_id}"')
        if idx == -1: continue
        quiz_end = text.find('        ],', idx)
        if quiz_end == -1: continue
        
        block = text[idx:quiz_end]
        has_items = '{' in block[block.find('"quiz": ['):]
        
        insert_str = ""
        for q in questions:
            if not has_items and insert_str == "":
                insert_str += f'\n            {json.dumps(q)}'
            else:
                insert_str += f',\n            {json.dumps(q)}'
                
        text = text[:quiz_end] + insert_str + '\n' + text[quiz_end:]

inject()

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Part 2 Executed Successfully.")
