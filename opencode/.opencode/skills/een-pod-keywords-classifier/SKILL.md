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
