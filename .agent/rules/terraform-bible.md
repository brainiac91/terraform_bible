---
trigger: always_on
---

# Project Rules: The Terraform Bible

These rules are established to ensure stability, efficiency, and code integrity based on the specific constraints and technologies of this project.

## 1. UI & Frontend Integrity
- **Overwrite vs. Patch**: When modifying complex template files (e.g., `app/templates/index.html`, `god_mode.html`), **ALWAYS** prefer using `write_to_file` to overwrite the entire file content rather than `replace_file_content`. The risk of stripping closing tags (`</script>`, `</div>`, `</body>`) or breaking the HTML/JS structure with partial replacements is too high.
- **Verification**: After any frontend edit, explicitly verify that the file ends with `</body>` and `</html>`.
- **State Safety**: All client-side logic must handle `localStorage` state defensively. Always provide default values for `userState` properties (streak, xp, progress) to prevent "undefined" errors for existing users.

## 2. Backend & Runtime
- **Restart Protocol**: Changes to Python files (`app/*.py`) are **NOT** hot-reloaded reliably in this environment. **ALWAYS** instruct the user to restart the server/container after modifying backend logic.
- **Naming Conventions**: Chapter content files must follow the `XX_title.md` format. Immediately update `app/routers/bible.py` to register new chapters with IDs matching their filenames.

## 3. Environment Limitations
- **No Shell File Ops**: Do **NOT** use `run_command` for file management (e.g., `rm`, `mv`, `del`) as it fails with WSL/shell incompatibilities. Use `write_to_file` to create/overwrite, and ask the user to manually delete unused files.
- **Path Handling**: Always use absolute paths for file operations.

## 4. Development Philosophy
- **"God Mode" First**: When adding interactive features, prioritize the "God Mode" gamification style—immersive, terminal-like interfaces that validate user input strictly.
- **Content-First**: The value is in the learning. Ensure all markdown content is rendered correctly and accessible via the `CHAPTERS` registry.

## 5. Architectural & Code Quality Principles
- **SOLID, DRY, KISS**: Write readable and maintainable code. Optimize only where needed.
- **Idempotency & Context**: Agents MUST read target configuration files before acting. Do not duplicate keys, restate existing settings with conflicting values, or inject overlapping configuration blocks.
- **Cross-Platform API Contracts**: Ensure all endpoints and WebSocket abstractions are platform-agnostic.
- **Atomic Execution**: Fix exactly the requested issue. No opportunistic refactoring or expansive cleanup unless asked explicitly.
- **Error Handling & Logging**: Use robust route error handling. Use low-cardinality structured logging and reliable, stable message strings.
- **Late-Stage Product Posture**: Ensure clarity, compliance hardening, and release-readiness. No placeholder UX, no fake flows, and no partially wired surfaces in shipped builds.

## 6. Agent Post-Implementation Review
- **Automatic Checking Workflow**: After *every* implementation (feature addition, code fix, etc.), the Developer Agent MUST trigger the `post_implementation_review.md` workflow. This invokes the PM and QA agents to verify idempotency, robustness, and release-readiness before the system yields control to the user.

## 7. 2026 DevOps & Coding Standards
- **Zero-Trust Identity**: Prefer Workload Identity (OIDC, SPIFFE/SPIRE) over long-lived keys or passwords.
- **eBPF & Modern Observability**: Structure deployments to favor eBPF kernel-level profiling rather than legacy heavyweight sidecars.
- **GitOps Default**: Assume Pull-based GitOps (e.g., ArgoCD, Flux) is the standard for continuous deployment operations over Push-based CI/CD scripts.
- **Shift-Left Security & FinOps**: Security scanning (SAST/DAST) and cost estimation (Infracost) are non-negotiable prerequisites before infrastructure merges.
