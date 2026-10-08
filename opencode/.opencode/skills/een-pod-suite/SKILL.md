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

## Evidence and extended process

Read `references/process-extensions.md` and `references/source-provenance.md` for completeness, consistency, targeted interviews, version comparison, EoI drafts and partner-fit assessment. Explicit user instructions take priority over workflow preferences; never invent facts or verification. Record the actual second-review method and adviser confirmation.

For form/readiness tasks read `references/form-schema.md` and use `scripts/form_readiness.py` for populated BO/BR/TO/TR fields. Use `scripts/profile_checks.py` for completeness, exact taxonomy, country and RDR date checks. A length PASS does not establish submission readiness. Public nonvisibility requires a limited review, not an invented omission. For semantic taxonomy use `scripts/taxonomy_lookup.py` and inspect candidate reasons; for version comparison use `scripts/profile_diff.py`.
