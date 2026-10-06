# Public POD profile lookup by POD Reference

Use this workflow when the user provides a POD Reference and asks to find, show, inspect, extract or quality-check the published profile.

Examples:
- `zweryfikuj jakość profilu BOCL20240903021`
- `znajdź profil TO...`
- `pokaż treść BR...`
- `sprawdź czy RDR... jest opublikowany`

## Scope and source

Use the official Enterprise Europe Network partnering opportunities site as the primary source:

`https://een.ec.europa.eu/partnering-opportunities`

Do not guess the profile page slug.

## 1. Recognise and normalise the reference

POD References normally begin with one of:
- `BO`
- `BR`
- `TO`
- `TR`
- `RDR`

Normalise the supplied reference to uppercase and remove surrounding whitespace.

A useful current pattern is:

`(?:BO|BR|TO|TR|RDR)[A-Z]{2}[0-9]{8,14}`

Treat the pattern as a recognition aid, not as an eternal platform specification. If the official site accepts a reference that does not match this pattern, trust the official site.

## 2. Build the exact filtered EEN search

Use the Keywords filter value:

`k:<POD_REFERENCE>`

The corresponding official URL is:

`https://een.ec.europa.eu/partnering-opportunities?f%5B0%5D=k%3A<POD_REFERENCE>`

Example:

`BOCL20240903021`

becomes:

`https://een.ec.europa.eu/partnering-opportunities?f%5B0%5D=k%3ABOCL20240903021`

When code execution is available, `scripts/pod_reference.py` can normalise a reference and generate this URL.

## 3. Find the exact result

Open/search the official filtered page.

Possible outcomes:
- `FOUND EXACT`
- `NOT FOUND`
- `AMBIGUOUS`
- `ACCESS BLOCKED`

Do not treat a similar reference, title or search-engine snippet as an exact match.

If the result list contains a candidate, follow the **actual href returned by the EEN site**. Never construct or guess the human-readable profile slug.

If the filtered page does not provide a usable result because of rendering/search limitations, use a web search restricted to the official domain with the exact reference, e.g. conceptually:

`site:een.ec.europa.eu/partnering-opportunities "<POD_REFERENCE>"`

Prefer an official EEN result. Do not silently substitute a third-party mirror.

## 4. Verify on the full profile page

Before extracting or reviewing the profile, confirm that the full page's displayed `POD Reference` exactly equals the requested reference.

If it does not, stop and report the mismatch.

## 5. Extract the public profile

Extract only fields actually visible on the official page. Preserve the wording faithfully enough for audit; do not invent missing fields.

Capture when available:
- POD Reference
- profile type
- title
- publication / validity dates
- short summary
- full description
- advantages / innovations
- technical specification / expertise sought
- stage of development
- IPR information
- SDG
- expected role / partner sought
- type and size of partner
- type(s) of partnership
- Technology keywords
- Market keywords
- target countries
- RDR programme/call information

Label fields not shown publicly as:

`NOT VISIBLE IN PUBLIC PROFILE`

Do **not** automatically conclude that an internal POD field is missing merely because the public page does not expose it.


## Partner Web Service integration

If authenticated Partner Web Service access is available, read `partner-webservice.md`.

Important:
- the 19 May 2026 guide does **not** document a direct `/profiles` filter by POD Reference;
- therefore keep the official public EEN search as the preferred exact-reference discovery route for a published profile;
- if the target profile is already present in an authorised API dataset or an intentional API scan is appropriate, match `item.reference` exactly;
- when an API record exposes `publicURL`, prefer that URL over constructing a slug;
- classify the API response as `FULL`, `LIMITED` or `UNKNOWN` before quality review;
- never convert `null` / `"N/A"` from a `LIMITED` record into missing-field blockers.

Use `scripts/een_b2b_api.py` for authenticated profile retrieval/scanning when code execution and `EEN_API_KEY` are available.

## 6. Handoff to quality review

If the user asks to `verify`, `review`, `audit`, `check quality`, `oceń`, `zweryfikuj jakość`, or equivalent:

1. complete the exact-reference lookup first;
2. extract the public profile;
3. state the quality standard used, normally the bundled Partnering Profile Quality Guidelines v1.2 unless a newer authoritative standard has been verified;
4. run `references/quality-review.md`;
5. distinguish:
   - **Observed public content**
   - **Quality finding**
   - **Suggested correction**
   - **Public-view limitation**, where applicable.

Never quality-review a different profile merely because its title looks similar.

## 7. Citation/source discipline

When browsing tools support citations, cite the official EEN result/profile page for extracted content.

For a published-profile audit, identify the exact POD Reference and the official page used.

## 8. Failure handling

### NOT FOUND
Say that no exact public profile was found through the official EEN lookup. Do not conclude that the record never existed; it may be expired, archived, unpublished, removed or not publicly indexed.

### ACCESS BLOCKED
Explain that the official page could not be retrieved in the current environment and do not fabricate the profile content.

### AMBIGUOUS
List the ambiguity and require exact verification of `POD Reference` before quality review.
