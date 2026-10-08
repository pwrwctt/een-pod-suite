# Changelog

## v2.7 — 2026-10-08

- Fixed Claude YAML generation and added real YAML, nested-reference and common-content release validation.
- Fixed retrieval error flags; added conservative labelled fields, identity/content separation, visibility and timestamps.
- Added field completeness, partnership/country/date/taxonomy checks and evidence-based review gates.
- Added interviews, version comparison, EoI drafting and partner-fit support.
- Added offline bilingual concept-based semantic taxonomy ranking and exact-code lookup, exposed through read-only MCP tools.
- Completed missing PPQG guidance and recorded unavailable template sources explicitly.
- Synchronised ChatGPT, Claude and all eight OpenCode modules; added five-type fixtures and platform evaluation scenarios.

## v2.6 — 2026-10-07

- Added a Claude unified skill and installation guidance for Claude and Claude Code.
- Released ChatGPT, OpenCode and Claude together at v2.6.
- Added deterministic Claude generation, stale-content checks and cross-platform version regressions.
- Recorded the mandatory three-platform release policy in AGENTS.md and repository documentation.

## v2.5 — 2026-10-07

- Removed Partner Web Service integration, code, references, credentials guidance and live taxonomy retrieval.
- Removed the dedicated OpenCode API module and narrowed the reader tools to public URL reading and local form checks.
- Audits use the operator-supplied exact public profile URL or supplied text; taxonomy uses the bundled 2024 snapshot.

## v2.4 — 2026-10-06

- Removed profile discovery and retrieval by POD Reference or profile name, including API identifier scanning.
- Individual profile audits now require the exact official profile detail URL supplied by the operator.
- Replaced the discovery helper with a URL-only reader and narrowed the MCP tool schema.

## v2.3 maintenance — exact EEN search-card parsing

- Follow the detail anchor inside `div.ecl-content-block__title` using both ECL anchor classes.
- Verify the reference on the full detail page without requiring it on the search card.
- Preserve profile-name queries and report ambiguous name results without selecting the first profile.
- Add regressions for nested title markup, class ordering, navigation exclusion and name lookup.

## v2.3 maintenance — Reader & Audit Agent

- Added the read-only EEN POD Reader & Audit Agent contract and OpenCode agent definition.
- Added a standard-library MCP server with public profile, authorised API, live label and form-limit tools.
- Added local stdio and authenticated stateless HTTP transports, plus connection instructions.
- Added transport and tool regression tests; hosting and live EEN access require separate configuration.

## v2.3 maintenance — public profile retrieval

- Added public HTML retrieval and exact displayed-reference verification to the lookup helper.
- Added direct official URL support to avoid dependence on search indexing.
- Preserve supplied reference/URL on access failures and ignore unrelated search results.
- Distinguish HTTP access, network and unresolved lookup failures from profile absence.
- Added regression coverage for the BOAL20261006010 lookup scenario using synthetic fixtures; live profile retrieval remains environment-dependent.

## v2.3 — 2026-10-06

## Added
- Partner Web Service integration for Cooperation Profiles.
- Live Market/Technology reference-data retrieval.
- Incremental taxonomy/profile synchronisation guidance.
- FULL / LIMITED / UNKNOWN API visibility gate.
- Profile status, `openForEOI`, `publicURL`, attachment and Video Pitch metadata handling.
- API-aware RDR structured-field review.
- `een-pod-api` OpenCode module.
- Secure `EEN_API_KEY` runtime handling and IP-whitelisting error handling.

## Changed
- Live Market/Technology reference data now has priority over the bundled 2024 taxonomy snapshot.
- Public EEN search remains the preferred exact-reference discovery route because the 19 May 2026 guide does not document a `/profiles` reference filter.
- API `null` / `N/A` values are not treated as missing-field defects when visibility is LIMITED.

- Classify incomplete or blank API records conservatively as UNKNOWN.
- Build release archives without a machine-specific packaging tool.

## Excluded
- Event API integration.

## v2.2 — 2026-09-30
- Added BO/BR/TO/TR operational form limits.
- Added deterministic field-length and keyword-count checks.
- Distinguished optional form controls from mandatory PPQG requirements.

## v2.1
- Added exact public profile lookup by POD Reference.
- Added version self-reporting.

## v2.0
- Added PPQG v1.2, glossary, taxonomy snapshot and dissemination-query guidance.
