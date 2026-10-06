# Partner Web Service — POD integration

Source basis: **Partner Webservices user guide (b2b), last updated 19 May 2026**.

Use this reference for the Partner Web Service integration for **Cooperation Profiles and Market/Technology reference data only**. Do not use the Events endpoint in this suite.

## Access and security

The service requires:
- the caller's IP to be whitelisted;
- an organisation-specific API key sent in the `X-API-KEY` request header.

Never store or expose the API key in `SKILL.md`, reference files, prompts, logs, Git or generated reports.

Use environment variable `EEN_API_KEY`. The helper script also supports `EEN_B2B_BASE_URL` for testing; default base URL:

`https://b2b.een.ec.europa.eu/v1`

If access fails with HTTP 401/403, report an authentication/whitelisting problem. Do not attempt to bypass it.

## Profiles endpoint

Endpoint:

`GET /profiles`

It returns:
- full details of Cooperation Profiles owned by the organisation initiating the call;
- full details of currently published Cooperation Profiles;
- only limited data for non-published profiles not owned by the initiating organisation.

### Supported profile filters

Use only documented parameters:

- `PageIndex`
- `PageSize`
- `ProfileTypes`
- `ProfileStatuses`
- `Countries`
- `ComparisonDate`
- `SortOrder`
- `FromDate`
- `ToDate`

Profile types:
- `BO`
- `BR`
- `TO`
- `TR`
- `RDR`

Documented profile statuses:
- `DRAFT`
- `DRAFT_ACCEPTED`
- `DRAFT_REJECTED`
- `CLIENT_VALIDATION_PENDING`
- `ARCHIVED`
- `EXPIRED`
- `FLAGGED`
- `ON_HOLD`
- `REJECTED`
- `UNDER_REVIEW`
- `UNDER_VALIDATION`
- `PUBLISHED`

Documented comparison-date values:
- `Created`
- `LastModified`
- `PublicationDate`

Documented sort order:
- `ASC`
- `DESC`

Use `PageSize=200` for bulk synchronisation unless there is a reason to use a smaller page.

Do not invent an undocumented `reference` query parameter.

## Exact-reference strategy

For a user request such as `zweryfikuj jakość profilu BOCL20240903021`, the public EEN partnering-opportunities search remains the preferred exact-reference discovery route because the 19 May 2026 guide does not document a `reference` filter for `/profiles`.

If an authenticated API workflow already has the target record or intentionally scans the authorised profile dataset, compare `item.reference` exactly.

When an API item has a usable `publicURL`, prefer that URL instead of constructing or guessing a slug.

## Profile response fields

When visible, the profile response can provide structured fields including:

- `id`
- `reference`
- `created`
- `lastModified`
- `title`
- `profileType`
- `partnerOrganisationCountry`
- `shortSummary`
- `description`
- `advantagesAndInnovation`
- `technicalSpecificationOrExpertiseSought`
- `stageOfDevelopment`
- `iprStatus`
- `iprNotes`
- `frameworkProgram`
- `callTitleAndIdentifier`
- `submissionAndEvaluationScheme`
- `anticipatedProjectBudget`
- `coordinatorRequired`
- `deadlineForEoI`
- `deadlineOfTheCall`
- `projectDurationInWeeks`
- `webLinkToTheCall`
- `projectTitleAndAcronym`
- `expectedRoleOfThePartner`
- `profileStatus`
- `publicationDate`
- `expirationDate`
- `marketKeywords`
- `technologyKeywords`
- `sdgKeywords`
- `typesOfPartnership`
- `typesAndSizes`
- `sectorGroupsInvolved`
- `targetedCountries`
- `openForEOI`
- `publicURL`
- `attachments`
- `videoPitch`

Use only fields actually returned. Do not infer missing values.

## Visibility classification

Classify an API profile record as:

- `FULL` — substantive profile fields are visible;
- `LIMITED` — the API intentionally exposes only identifying/status information and the remaining content is `null` or `"N/A"`;
- `UNKNOWN` — visibility cannot be established safely.

The guide states that non-eligible items may be returned with limited information so partner organisations can identify them and update their own databases.

**Never treat `null` or `"N/A"` in a LIMITED record as a quality defect or missing mandatory field.**

If quality review is requested:
- `FULL` → review the visible content;
- `LIMITED` → do not issue field-completeness blockers; try the public site if the profile is public, otherwise report the visibility limitation;
- `UNKNOWN` → distinguish uncertainty from a confirmed defect.

## Pagination

The Profiles endpoint uses `PageIndex` and `PageSize`. Follow returned paging metadata and `hasNext`; do not assume one page contains all results.

For bulk/incremental sync use:
- `ComparisonDate=LastModified`;
- `FromDate=<last successful sync date>`;
- `SortOrder=ASC`.

## Profile lifecycle data

Use `profileStatus.name` as returned status.

Also capture:
- `created`
- `lastModified`
- `publicationDate`
- `expirationDate`
- `openForEOI`

Do not equate `PUBLISHED` with `openForEOI=true`.

## Attachments and Video Pitch

API profile data may include attachments with:
- `id`
- `url`
- `title`
- `orderNumber`
- `size`

and a Video Pitch with metadata such as:
- `url`
- `title`
- `cooperationProfileId`
- `created`
- `lastModified`
- `id`

Use media metadata as an optional QA signal:
- anonymity/identity leakage;
- misleading attachment title;
- wrong profile association;
- missing/invalid URL if checked.

Do not make media mandatory merely because fields exist.

## RDR structured fields

For RDR reviews use API fields when available:
- `frameworkProgram`
- `callTitleAndIdentifier`
- `submissionAndEvaluationScheme`
- `anticipatedProjectBudget`
- `coordinatorRequired`
- `deadlineForEoI`
- `deadlineOfTheCall`
- `projectDurationInWeeks`
- `webLinkToTheCall`
- `projectTitleAndAcronym`

Apply PPQG v1.2 mandatory/quality rules to the structured values.
