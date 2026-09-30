---
name: een-pod-suite
description: End-to-end Enterprise Europe Network Partnering Opportunities Database (POD) skill for EEN advisers. Use for POD eligibility and groundwork, BO/BR/TO/TR/RDR classification, drafting or rewriting profiles, Title and 500-character Short Summary optimisation, partnership types, Technology/Market/SDG taxonomy, independent quality review, public profile lookup by exact POD Reference (for example BOCL20240903021), lookup-to-review requests such as 'verify profile quality', dissemination queries, profile management, and reporting the installed EEN POD Suite version when asked.
---

# EEN POD Suite

**Installed suite version: v2.2.** For any version question, read `references/version.md` and report that value.

Use the bundled **Partnering Profile Quality Guidelines v1.2 (September 2024)** as the primary operational profile-writing source, the **EEN Glossary 2024 v3** for terminology, the **Queries User Guide (13 December 2024)** for query workflows, and the supplied EEN taxonomy workbook as a 2024 taxonomy snapshot.

Read `references/source-policy.md` whenever currency/version matters.

## Route the task

- For a POD Reference lookup, published-profile extraction or lookup-to-quality-review request: read `references/profile-lookup.md`; use `scripts/pod_reference.py` when helpful.
- For raw client notes, eligibility or profile-type uncertainty: read `references/intake-eligibility.md` and `references/profile-types.md`.
- For BO/BR/TO/TR operational field limits and field availability: read `references/form-schema.md`; use `scripts/form_readiness.py` when useful.
- For field requirements or a full draft: read `references/field-matrix.md`, `references/drafting-rules.md`, `references/partnership-types.md` and `references/output-template.md`.
- For Title or Short Summary: read `references/title-summary.md`.
- For Technology, Market, SDG or NACE classification: read `references/keywords-taxonomy.md`; use the bundled CSV files.
- For final quality assurance: read `references/quality-review.md`.
- For dissemination queries: read `references/dissemination-queries.md`.
- For profile lifetime/renewal/EoI management: read `references/profile-management.md`.
- For EEN terminology: read `references/terminology.md`.

## Reference-first workflow

If the user supplies a POD Reference and asks to verify an existing published profile, perform **exact official EEN lookup → full-page POD Reference verification → public-field extraction → quality review**. Never draft a substitute profile before lookup.

## End-to-end workflow

1. Check client/profile eligibility and operational groundwork.
2. Classify BO / BR / TO / TR / RDR from the cooperation need.
3. Identify `MISSING INPUT`, `OPERATIONAL CHECK` and `CONFIDENTIALITY CHECK`.
4. Draft only fields supported by facts.
5. Explain WHY and HOW the selected cooperation type works.
6. Optimise Title and Short Summary; enforce the 500-character Summary limit.
7. Select partnership type(s), normally no more than 1–3.
8. Select SDG and relevant Technology/Market taxonomy entries; never invent codes.
9. Run an independent pre-publication quality review.
10. Add dissemination/query guidance only when requested.

## Hard rules

- Do not invent client facts, metrics, IPR, certifications, partnerships, taxonomy codes, calls or deadlines.
- Do not turn a direct sales/customer-search request into a POD profile.
- Write public profile text in the third person; avoid `we`, `our`, `you`, `your`.
- Avoid marketing speak and unsupported superlatives.
- Preserve the user's anonymity decision; screen text and media metadata accordingly.
- Keep partnership type, partner role, Title, Summary and Description coherent.
- Treat the bundled 2024 UI/taxonomy files as snapshots. Verify current live data when currency matters.
- Use British English for profile text unless asked otherwise; explain in the user's language when helpful.

## Taxonomy helper

When code execution is available, `scripts/taxonomy_lookup.py` can search the bundled Technology, Market, NACE and SDG references. The script is optional; the CSV files remain the source of truth for the bundled snapshot.

## Final gate

Do not call a profile submission-ready merely because the writing is polished. Require:
- an eligible profile purpose;
- correct profile type;
- clear cooperation objective;
- specific partner role;
- coherent partnership type;
- field-specific completeness;
- anonymity/IP safety;
- keyword discipline;
- no BLOCKER in the independent review.
