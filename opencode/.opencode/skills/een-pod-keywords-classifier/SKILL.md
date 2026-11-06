---
name: een-pod-keywords-classifier
description: Classify and audit EEN POD Technology keywords, Market keywords, SDGs and optional NACE entries using the bundled 2024 EEN Community taxonomy snapshot. Use for exact code-label lookup, Level-3/Level-2 selection, max-five limits, Technology-vs-Market separation, keyword stuffing checks and current-taxonomy caveats.
---

For suite-version questions, read `references/version.md`.

# EEN POD keywords classifier

Read `references/keywords-taxonomy.md` and `references/source-policy.md`.

Use the bundled selectable CSVs for exact Technology/Market code-label pairs.
Never invent codes.
Prefer Level 3; use Level 2 only where the branch has no Level 3 entries, following v1.2.
Keep Market keywords focused on application and Technology keywords on the technology itself.
Use NACE only when requested or required by the live workflow; do not call it mandatory from v1.2 alone.
Use `scripts/taxonomy_lookup.py` when convenient.

Return exact verified bundled-snapshot codes/labels and explicitly state that the snapshot is 2024 unless current live data has been checked.

## Evidence and extended process

Read `references/process-extensions.md` and `references/source-provenance.md` for completeness, consistency, targeted interviews, version comparison, EoI drafts and partner-fit assessment. Explicit user instructions take priority over workflow preferences; never invent facts or verification. Record the actual second-review method and adviser confirmation.

For form/readiness tasks read `references/form-schema.md` and use `scripts/form_readiness.py` for populated BO/BR/TO/TR fields. Use `scripts/profile_checks.py` for completeness, exact taxonomy, country and RDR date checks. A length PASS does not establish submission readiness. Public nonvisibility requires a limited review, not an invented omission. For semantic taxonomy use `scripts/taxonomy_lookup.py` and inspect candidate reasons; for version comparison use `scripts/profile_diff.py`.

## BO quality pilot

Read `references/bo-quality-scoring.md` for BO points, bounds, remediation drafts and two-month comparison. Use `scripts/bo_quality_score.py` when executable or connected score_business_offer / compare_bo_scores tools. Missing data is UNKNOWN, not empty. Keep pilot bands distinct from PPQG findings and readiness; no automatic flagging, sending or reminder creation. Do not apply BO points to other types/Achievements.

Include the separate pilot-derived score by default for full identified published-BO audits; retain partial evidence limitations without suppressing supported PPQG findings.
