---
name: een-pod-suite
description: Orchestrate complete EEN Partnering Opportunities Database workflows across eligibility, drafting, Title/Summary, keywords, quality review, auditing operator-supplied profile URLs, Partner Web Service profile/taxonomy access, dissemination and profile management. Use for BO/BR/TO/TR/RDR tasks spanning multiple modules, live Market/Technology reference data, API-aware review, profile status/openForEOI handling and suite-version reporting. Excludes Event API integration.
---

For suite-version questions, read `references/version.md`.

# EEN POD Suite orchestrator

Use the smallest specialised chain that fits the task.

Specialised skills:
- `een-pod-api`
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

## Existing published profile by reference

For requests such as `zweryfikuj jakość profilu BOCL20240903021`, route:
Operator-supplied exact detail URL → `een-pod-profile-lookup` → displayed-reference verification/extraction → `een-pod-profile-quality-reviewer`.
