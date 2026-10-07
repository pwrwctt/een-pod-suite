---
name: een-pod-suite
description: Coordinate EEN profile eligibility, drafting, optimisation, bundled taxonomy, supplied-URL extraction and independent quality review.
---

For suite-version questions, read `references/version.md`.

# EEN POD Suite orchestrator

Use the smallest specialised chain that fits the task.

Specialised skills:
- `een-pod-profile-lookup`
- `een-pod-intake`
- `een-pod-profile-drafter`
- `een-pod-title-summary-optimizer`
- `een-pod-keywords-classifier`
- `een-pod-profile-quality-reviewer`
- `een-pod-dissemination-queries`

For a complete new profile:
1. intake
2. drafter
3. title-summary optimiser
4. keywords classifier
5. quality reviewer

Add dissemination/query guidance only when requested.

Read `references/source-policy.md`, `references/workflow.md` and `references/output-template.md`.

Preserve `MISSING INPUT`, `OPERATIONAL CHECK`, `CONFIDENTIALITY CHECK` and `CURRENT-VERSION CHECK` between stages.
Do not let a later stage invent facts to resolve an earlier gap.

## Existing published profile by supplied URL

Require the operator's exact official profile detail URL, then route:
Operator-supplied exact detail URL → `een-pod-profile-lookup` → displayed-reference verification/extraction → `een-pod-profile-quality-reviewer`.
