---
name: een-pod-suite
description: "Prepare and audit EEN partnering profiles: eligibility, drafting, taxonomy, field limits and quality review. Audit only an operator-supplied exact profile URL or supplied text."
---

# EEN POD Suite

**Installed suite version: v2.7.** For any version question, read `references/version.md` and report that value.

Read `references/source-policy.md` whenever currency/version matters.

For the read-only Reader & Audit Agent, read `references/reader-agent.md`. Connected MCP tools retrieve data; the skill supplies audit rules. Installation alone does not establish a working MCP connection.


## Claude execution

Use this skill in Claude when preparing or reviewing EEN partnering profiles.
Resolve references and scripts relative to this installed skill directory.
Use available browsing, code execution or explicitly connected read-only MCP tools
to read only the operator-supplied official detail URL. Run the bundled Python
helpers only when code execution is available. Network access depends on the
Claude environment; installing this skill does not enable browsing or connect MCP.
If reading is unavailable or fails, request the same profile's text/HTML export
and state which content could not be verified. Never substitute another profile.

## Route the task

- For evidence-led audits, completeness, consistency, client interviews, version comparison, partner-fit assessment or EoI drafts: read `references/process-extensions.md` and `references/source-provenance.md`. Use `scripts/profile_checks.py` and `scripts/profile_diff.py` when applicable.
- For taxonomy queries, use `scripts/taxonomy_lookup.py` in semantic mode for curated English/Polish concept expansion; inspect reasons and verify codes.

- For auditing an existing profile: require the operator's exact official detail URL and read `references/profile-lookup.md`; use `scripts/profile_url.py` for direct retrieval when available.
- For raw client notes, eligibility or profile-type uncertainty: read `references/intake-eligibility.md` and `references/profile-types.md`.
- For BO/BR/TO/TR operational field limits and field availability: read `references/form-schema.md`; use `scripts/form_readiness.py` when useful.
- For field requirements or a full draft: read `references/field-matrix.md`, `references/drafting-rules.md`, `references/partnership-types.md` and `references/output-template.md`.
- For Title or Short Summary: read `references/title-summary.md`.
- For Technology, Market, SDG or NACE classification: read `references/keywords-taxonomy.md` and use the bundled CSVs, identified as a 2024 snapshot.
- For final quality assurance: read `references/quality-review.md`.
- For dissemination queries: read `references/dissemination-queries.md`.
- For profile lifetime/renewal/EoI management: read `references/profile-management.md`.
- For EEN terminology: read `references/terminology.md`.

## Operator-supplied URL workflow

Require the exact official detail URL supplied by the operator or supplied profile text. Read that page, verify its displayed POD Reference, extract visible fields and review. If only a number/name is supplied, request the exact URL. If reading fails, request a text/HTML export of the same profile and report the limitation.

## End-to-end workflow

1. Check client/profile eligibility and operational groundwork.
2. Classify BO / BR / TO / TR / RDR from the cooperation need.
3. Identify `MISSING INPUT`, `OPERATIONAL CHECK` and `CONFIDENTIALITY CHECK`.
4. Draft only fields supported by facts.
5. Explain WHY and HOW the selected cooperation type works.
6. Optimise Title and Short Summary; enforce the 500-character Summary limit.
7. Select partnership type(s), normally no more than 1–3.
8. Select applicable keywords from the bundled 2024 taxonomy; never invent codes.
9. Run a separate pre-publication review, record its actual method and apply the verdict gates in `references/process-extensions.md`. Same-context self-review does not establish independence; approval remains with the adviser.
10. Add dissemination/query guidance only when requested.

## Hard rules

- Do not invent client facts, metrics, IPR, certifications, partnerships, taxonomy codes, calls or deadlines.
- Do not turn a direct sales/customer-search request into a POD profile.
- Write public profile text in the third person; avoid `we`, `our`, `you`, `your`.
- Avoid marketing speak and unsupported superlatives.
- Preserve the user's anonymity decision; screen text and media metadata accordingly.
- Keep partnership type, partner role, Title, Summary and Description coherent.
- Treat the bundled 2024 UI/taxonomy files as snapshots. Verify current live data when currency matters.
- Do not discover profiles by reference or name. Audit only the operator-supplied exact detail URL or supplied profile content.
- Use British English for profile text unless asked otherwise; explain in the user's language when helpful.

## Taxonomy helper

Use `scripts/taxonomy_lookup.py` to search bundled Technology, Market, NACE and SDG CSVs when execution is available. These are 2024 snapshots, not an automatic current-data source.

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
- no BLOCKER or unresolved MAJOR; only MINOR permits READY AFTER MINOR EDITS;
- sufficient evidence, confirmed form limits/operational work and actual review method.

Explicit user instructions take priority over workflow preferences; never invent facts or source verification. Exclude the client’s own country from restricted target lists. Preserve uncertainty about provisional form limits and incomplete public evidence.
