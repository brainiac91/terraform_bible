---
description: Automatically run PM and QA checks after implementation
---

# Post-Implementation Review Workflow

This workflow MUST be executed at the end of every feature, fix, or implementation phase.

1. **Pause Finalization**: The primary developer agent completes initial code modifications and testing but must **NOT** conclude the task or yield control.
2. **QA Verification**: Trigger the QA Agent (by invoking its persona or passing context). The QA Agent must:
   - Verify that massive, unrequested refactors were avoided (Atomic Execution).
   - Ensure the code relies on existing config rather than overwriting or duplicating (Idempotency).
   - Verify frontend template files were written safely and end in proper HTML tags.
   - Review the robustness of any new Python API routes.
   - **Verify 2026 Standards**: Ensure Zero-Trust secrets management, shifted-left security rules, and eBPF-friendly component isolation.
3. **PM Verification**: Trigger the PM Agent. The PM Agent must:
   - Verify there is no placeholder text or partially functional UI.
   - Judge if the additions match the late-stage, release-ready "God Mode" posture.
   - **Confirm FinOps/GitOps Adherence**: Check if the architectural and educational features align with modern Pull-based GitOps and 2026 Cost-as-Code principles.
4. **Conclusion**: Only once both QA and PM profiles explicitly sign off on the exact changes can the developer agent generate the final `walkthrough.md` and yield back to the user.
