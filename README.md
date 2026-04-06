# The Terraform Bible: Senior DevOps Edition

*(2026 Ready)* 

A comprehensive, gamified, and enterprise-grade learning platform designed to take engineers from Zero to Senior level. This platform teaches strictly modern, production-ready iterations of Terraform, Ansible, and Kubernetes—packing everything you need to crush technical DevOps and Cloud Native interviews.

![Platform Aesthetics](https://img.shields.io/badge/Aesthetics-Glassmorphism_v2-purple)
![Tech Stack](https://img.shields.io/badge/Stack-FastAPI_|_Tailwind_|_Node.js-blue)
![Role](https://img.shields.io/badge/Target_Role-Senior_DevOps-red)

##  Overview

The Terraform Bible is an immersive, web-based simulation environment that replaces boring textbook learning with a cyberpunk-inspired gamified dashboard. Beyond foundational configuration, the platform rigorously covers advanced concepts like **eBPF, Zero-Trust (SPIFFE), GitOps (ArgoCD), and FinOps (Infracost) constraints**.

##  Core Platform Features

- ** 2026 Premium UI/UX:** Complete visual overhaul featuring dark-mode native glassmorphism (`backdrop-blur-xl`), physics-based animations, and hyper-modern typography. 
- ** Progression & State:** All progress (XP, streaks, and completed chapters) is managed defensively via reactive client-side `localStorage`.
- ** Datacards:** Interactive 3D flip-cards embedded in every chapter for rapid memorization.
- ** "God Mode" Terminal:** A dedicated CRT-style hacking interface (`god_mode.html`) featuring animated gradient borders, scanlines, and telemetry layouts to validate your live coding solutions.
- ** Technical Interview Simulator:** An aggressive, high-pressure mode injected directly into **ALL 23 chapters**. It quizzes candidates on devastating failure scenarios (e.g., State Deadlocks, K8s CrashLoopBackOff, Quorum failures) using severe red aesthetics and redacted, interactively "blurred" expert answers.

##  Curriculum Breakdown

The platform consists of **23 rigorous chapters** broken into mastery paths:
1. **Terraform Fundamentals (Ch 1-5):** State locking, input prioritization, mutable vs immutable infrastructure.
2. **Advanced Terraform & Ops (Ch 6-9):** Dynamic HCL loops, Checkov SAST, `prevent_destroy` mechanics. 
3. **Ansible Masterclass (Ch 10-12, 19):** Agentless push theory, dynamic AWS inventory, Mitogen pipelining, and Execution Environments (EE).
4. **Kubernetes Architecture (Ch 13-17, 20):** Raft consensus algorithms, Operator logic, Helm templates, ArgoCD pull mechanics, and eBPF network planes.
5. **Interview prep series (Ch 21-23):** Concentrated technical whiteboarding simulators for all the above tools.

##  Architecture & Tech Stack

- **Backend:** `FastAPI` (Python 3.14-slim) processing highly optimized JSON datasets.
- **Frontend Engine:** Native HTML5, Javascript, and `TailwindCSS` injected via CDN configuration.
- **Build & Dependency:** Integrated `Node.js 24.x` image layer.
- **Execution:** Packaged entirely in Docker & Docker Compose for guaranteed idempotency across OS types.

##  Fast Installation & Setup

### Prerequisites
- Docker & Docker Compose
- Windows Subsystem for Linux (WSL) If operating on a Windows machine.
- PowerShell.

### Boot Sequence

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd terraform_bible-master
   ```

2. **Trigger the automated startup script:**
   *We provide a dedicated PowerShell script (`start.ps1`) that orchestrates Docker Compose and maps paths correctly between WSL distributions and the Windows networking layer.*
   ```powershell
   .\start.ps1
   ```
   
   If executing natively inside Linux/macOS without the script, fall back to:
   ```bash
   docker compose up --build -d
   ```

3. **Infiltrate the Platform:**
   Access the dashboard and begin your training at:
    **http://localhost:8000**

### Shutting Down
To maintain a clean environment and purge the mapped network layers when finished:
```bash
wsl docker compose down
```

## 🛡️ Best Practices & Guidelines
_Adhering to our 2026 Developer mandates:_
- **Idempotency:** The platform itself respects atomic execution.
- **State Safety:** Deleting standard frontend storage will revert your simulated XP back to Zero.
- **Customization:** Add chapters dynamically by inserting `[XX]_title.md` files into `/app/content/chapters` and registering the metadata directly in `app/routers/bible.py`.

##  License
This project is open-source and intended to democratize Senior-tier DevOps education. Available under the [MIT License](LICENSE).
