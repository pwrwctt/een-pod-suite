# Source policy

Use the following source hierarchy.

1. **Partnering Profile Quality Guidelines v1.2 — September 2024**: primary source for profile eligibility, profile type, mandatory content, drafting quality, partnership types and quality checks.
2. **Partner Webservices user guide (b2b) — 19 May 2026**: primary source for current documented Partner Web Service behaviour for Cooperation Profiles and Market/Technology reference data.
3. **Official public EEN partnering-opportunities website**: primary public source for exact public-profile lookup by POD Reference and public-page verification.
4. **Enterprise Europe Network Glossary 2024 v3**: source for EEN terminology and definitions.
5. **Managing Queries for Widgets and Ticker — 13 December 2024**: source for saved queries, Email vs Widget/Ticker queries and role permissions.
6. **Bundled EEN Community POD SDG / Market / Technology / NACE taxonomy workbook**: offline taxonomy snapshot.

## Version and freshness rule

Treat the bundled taxonomy workbook and 2024 UI instructions as snapshots, not automatically as current platform truth.

For current structured profile data, profile statuses and live Market/Technology labels, prefer the authenticated Partner Web Service when available and when the record is fully visible.

For exact public profile discovery by POD Reference, keep the official public EEN search as the preferred route because the 19 May 2026 Partner Web Service guide does not document a direct `reference` filter for `/profiles`.

For Market/Technology classification:
1. live Partner Web Service reference data;
2. bundled taxonomy snapshot if live API data is unavailable;
3. explicitly label fallback output as snapshot-based.

The 2026 Partner Web Service guide does not establish the reference-data endpoint as a source for NACE or SDG.

## Visibility rule

Partner Web Service items can be visibility-limited. A record containing only identifying/status information while substantive fields are `null` or `"N/A"` must not be treated as a poor-quality or incomplete profile.

Read `partner-webservice.md` and `api-quality-review.md` for the visibility gate.

## Security rule

Never expose or store an organisation API key. Use `EEN_API_KEY` at runtime only.

Read `api-security.md` before authenticated API use.

## Conflict rule

If a verified current authoritative source differs from a bundled snapshot, prefer the current source and explain the change.

Do not silently replace or "correct" an authoritative source with general knowledge.

## Excluded scope

The Partner Web Service **Events API is intentionally outside this POD Suite version**.
