---
name: een-pod-suite
description: End-to-end Enterprise Europe Network Partnering Opportunities Database (POD) skill for EEN advisers. Use for eligibility, BO/BR/TO/TR/RDR classification, drafting, field/form readiness, Technology/Market/SDG taxonomy, public profile lookup, Partner Web Service profile retrieval, API-aware quality review, live Market/Technology reference-data lookup and synchronisation, profile status/openForEOI management, dissemination queries, and installed-suite version reporting. Excludes Event API integration.
---

# EEN POD Suite

**Installed suite version: v2.3.** For any version question, read `references/version.md` and report that value.

Use **Partnering Profile Quality Guidelines v1.2 (September 2024)** as the primary profile-quality source. Use the **Partner Webservices user guide (19 May 2026)** for documented Cooperation Profile and Market/Technology API behaviour, the **EEN Glossary 2024 v3** for terminology, the **Queries User Guide (13 December 2024)** for query workflows, and the supplied EEN taxonomy workbook as an offline 2024 snapshot.

Read `references/source-policy.md` whenever currency/version matters.

## Route the task

- For a POD Reference lookup, published-profile extraction or lookup-to-quality-review request: read `references/profile-lookup.md`; use `scripts/pod_reference.py` when helpful.
- For authenticated Partner Web Service profile retrieval, lifecycle/status data or portfolio synchronisation: read `references/partner-webservice.md` and `references/api-security.md`; use `scripts/een_b2b_api.py` when execution and credentials are available.
- For live Market/Technology labels or incremental taxonomy sync: read `references/taxonomy-api.md`; use the Partner Web Service first and bundled CSVs only as fallback.
- For quality review of API-originated profile data: read `references/api-quality-review.md` before the normal reviewer.
- For raw client notes, eligibility or profile-type uncertainty: read `references/intake-eligibility.md` and `references/profile-types.md`.
- For BO/BR/TO/TR operational field limits and field availability: read `references/form-schema.md`; use `scripts/form_readiness.py` when useful.
- For field requirements or a full draft: read `references/field-matrix.md`, `references/drafting-rules.md`, `references/partnership-types.md` and `references/output-template.md`.
- For Title or Short Summary: read `references/title-summary.md`.
- For Technology, Market, SDG or NACE classification: read `references/keywords-taxonomy.md`; prefer live Market/Technology API labels when available and use bundled CSVs as fallback.
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
8. Select SDG and relevant Technology/Market taxonomy entries; prefer verified live Partner Web Service labels when available and never invent codes.
9. If input originates from the Partner Web Service, classify API visibility as FULL / LIMITED / UNKNOWN before completeness review.
10. Run an independent pre-publication quality review.
11. Add dissemination/query guidance only when requested.

## Hard rules

- Do not invent client facts, metrics, IPR, certifications, partnerships, taxonomy codes, calls or deadlines.
- Do not turn a direct sales/customer-search request into a POD profile.
- Write public profile text in the third person; avoid `we`, `our`, `you`, `your`.
- Avoid marketing speak and unsupported superlatives.
- Preserve the user's anonymity decision; screen text and media metadata accordingly.
- Keep partnership type, partner role, Title, Summary and Description coherent.
- Treat the bundled 2024 UI/taxonomy files as snapshots. Verify current live data when currency matters.
- Never store or expose `EEN_API_KEY`; authenticated API access also requires IP whitelisting.
- Never treat `null` / `N/A` in an API visibility-limited record as a quality defect.
- Do not invent an undocumented `/profiles` reference filter; use exact public EEN lookup or exact matching within authorised API results.
- Keep `PUBLISHED` separate from `openForEOI`.
- Do not use the Partner Web Service Events API in this suite version.
- Use British English for profile text unless asked otherwise; explain in the user's language when helpful.

## Taxonomy helper

When code execution and authorised API access are available, `scripts/een_b2b_api.py` can retrieve Cooperation Profiles and live Market/Technology reference labels. Use `scripts/taxonomy_lookup.py` only for bundled snapshot fallback and NACE/SDG support. For live Market/Technology labels, UUID-based API identity takes precedence over bundled snapshot codes when verified.

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
