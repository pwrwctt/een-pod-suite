# API-aware POD quality review

Apply this layer before the normal profile-quality checklist when input originates from the Partner Web Service.

## Record provenance

Report:
- Data source: `Partner Web Service` / `Public EEN website` / `Bundled snapshot` / `User input`
- POD Reference
- Profile type
- API visibility: `FULL` / `LIMITED` / `UNKNOWN`
- Profile status, when available
- Last modified, when available
- Open for EOI, when available
- Public URL, when available

## Visibility gate

### FULL
Proceed with normal PPQG and form-readiness review.

### LIMITED
Do not convert `null` or `"N/A"` fields into blockers or "missing mandatory field" findings.

If the profile is published or has a usable public URL, use the public page for public-content QA. Otherwise report:

`QUALITY REVIEW LIMITED — authorised API response does not expose the substantive profile content.`

### UNKNOWN
Review only fields actually visible and label uncertainty.

## Status-aware observations

Treat status as operational context, not automatic quality scoring.

Examples:
- `DRAFT` — review may be pre-publication.
- `PUBLISHED` — assess current public content.
- `EXPIRED` / `ARCHIVED` — do not present as an active opportunity.
- `ON_HOLD`, `UNDER_REVIEW`, `UNDER_VALIDATION`, `CLIENT_VALIDATION_PENDING` — flag workflow status without inventing the reason.

Do not infer status meaning beyond documented labels.

## Open for EOI

Report `openForEOI` separately from publication status.

Do not say an opportunity is open for expressions of interest solely because it is `PUBLISHED`.

## Structured field mapping

Map API fields directly to the normal reviewer:
- `title`
- `shortSummary`
- `description`
- `advantagesAndInnovation`
- `technicalSpecificationOrExpertiseSought`
- `stageOfDevelopment`
- `iprStatus`
- `iprNotes`
- `expectedRoleOfThePartner`
- `marketKeywords`
- `technologyKeywords`
- `sdgKeywords`
- `typesOfPartnership`
- `typesAndSizes`
- `targetedCountries`

For RDR additionally map the documented structured call/project fields.

## Media QA

Review attachment/video metadata only when useful:
- anonymity leakage;
- organisation/brand exposure inconsistent with anonymity choice;
- misleading or irrelevant title;
- obviously mismatched profile association.

Do not mark absence of media as a blocker unless another authoritative rule requires it.
