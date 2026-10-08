---
name: een-pod-profile-quality-reviewer
description: Independent pre-publication quality reviewer for EEN POD profiles. Use to audit BO/BR/TO/TR/RDR drafts against Partnering Profile Quality Guidelines v1.2 for eligibility, profile type, 500-character Summary, field completeness, WHY/HOW cooperation, anonymity, evidence, partnership types, partner role, taxonomy limits, RDR call data and readiness.
---

For suite-version questions, read `references/version.md`.

# EEN POD profile quality reviewer

Act as an independent second reviewer, not as the original drafter.

Read `references/quality-review.md`, `references/field-matrix.md`, `references/partnership-types.md`, `references/keywords-taxonomy.md`, `references/title-summary.md` and `references/source-policy.md`.

Return:
- READY / READY AFTER MINOR EDITS / RETURN FOR REVISION;
- BLOCKER / MAJOR / MINOR issues;
- field-by-field status;
- minimal corrections that do not invent facts;
- questions required to resolve remaining blockers.

Do not use an official-sounding numeric threshold.

## Evidence and extended process

Read `references/process-extensions.md` and `references/source-provenance.md` for completeness, consistency, targeted interviews, version comparison, EoI drafts and partner-fit assessment. Explicit user instructions take priority over workflow preferences; never invent facts or verification. Record the actual second-review method and adviser confirmation.

For form/readiness tasks read `references/form-schema.md` and use `scripts/form_readiness.py` for populated BO/BR/TO/TR fields. Use `scripts/profile_checks.py` for completeness, exact taxonomy, country and RDR date checks. A length PASS does not establish submission readiness. Public nonvisibility requires a limited review, not an invented omission. For semantic taxonomy use `scripts/taxonomy_lookup.py` and inspect candidate reasons; for version comparison use `scripts/profile_diff.py`.
