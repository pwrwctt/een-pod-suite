# Changelog

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
