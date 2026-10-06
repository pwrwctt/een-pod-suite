---
name: een-pod-api
description: Enterprise Europe Network Partner Web Service integration for POD Cooperation Profiles and live Market/Technology reference data. Use when retrieving or synchronising authorised profile data, checking profile statuses/openForEOI/publicURL, classifying API visibility, extracting structured RDR fields, or refreshing Market/Technology taxonomy labels. Uses X-API-KEY via EEN_API_KEY and IP whitelisting. Excludes Event API integration.
---

# EEN POD API

For suite-version questions, read `references/version.md`.

Read:
- `references/partner-webservice.md` for documented Cooperation Profile API behaviour;
- `references/taxonomy-api.md` for Market/Technology reference-data behaviour;
- `references/api-security.md` before authenticated use;
- `references/api-quality-review.md` before handing API-originated data to the quality reviewer.

Use `scripts/een_b2b_api.py` when code execution and authorised credentials are available.

## Rules

- Never hard-code, print, log or commit `EEN_API_KEY`.
- Do not attempt to bypass IP whitelisting or authentication.
- Do not invent an undocumented `/profiles` reference filter.
- For exact public POD-reference lookup, prefer the public EEN search unless the exact record is already in authorised API results.
- Classify profile visibility as `FULL`, `LIMITED` or `UNKNOWN`.
- Never treat `null` / `N/A` in a `LIMITED` record as a quality defect.
- Prefer API `publicURL` when returned.
- Keep `PUBLISHED` separate from `openForEOI`.
- For Market/Technology labels use `uuid` / `parentUuid`, not legacy numeric `id` / `parentId`.
- Prefer active live labels; use bundled taxonomy only as fallback.
- Do not use Event API endpoints in this skill.
