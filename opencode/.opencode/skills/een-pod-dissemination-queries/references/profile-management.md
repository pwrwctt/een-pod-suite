# Publication, dissemination and profile management

Source basis: Partnering Profile Quality Guidelines v1.2, sections 3.2–3.5 and section 6.2.2.

## Dissemination

Once published, a profile may appear:
- in POD searches;
- on the public EEN website and partner websites;
- in automated profile queries;
- in partner mailing lists/newsletters/publications;
- via automated web publication and PDF downloads.

## Expressions of Interest

An EoI is sent by a Network partner when a potential cooperation partner matches a profile.
The EEN partnering process continues through matching and negotiations towards a partnership.

## Profile lifetime in v1.2

Non-RDR profiles:
- first publication validity: 365 days;
- maximum lifespan: 2 years;
- notification: two weeks before expiry;
- extension: once, up to 365 days;
- a published profile can be extended at earliest 30 days before expiry;
- expired profiles can be extended if expired less than a year;
- after 2 years the profile is automatically archived.

RDR lifespan is determined by the relevant call deadline.

## Active management

Keep contact with the client.
Archive/remove the profile when the client:
- is no longer interested;
- no longer responds; or
- no longer exists.

Treat these as v1.2 workflow rules; verify current platform behaviour when currency matters.


## Partner Web Service lifecycle/status data

When authenticated Partner Web Service data is available, use the documented profile status returned by `profileStatus.name`.

Documented statuses in the 19 May 2026 guide:
- DRAFT
- DRAFT_ACCEPTED
- DRAFT_REJECTED
- CLIENT_VALIDATION_PENDING
- ARCHIVED
- EXPIRED
- FLAGGED
- ON_HOLD
- REJECTED
- UNDER_REVIEW
- UNDER_VALIDATION
- PUBLISHED

Also capture when available:
- `created`
- `lastModified`
- `publicationDate`
- `expirationDate`
- `openForEOI`
- `publicURL`

Treat status as operational context. Do not invent the reason for `FLAGGED`, `ON_HOLD`, `REJECTED`, review or validation states.

Do not equate `PUBLISHED` with accepting expressions of interest. Report `openForEOI` separately.

### Incremental profile synchronisation

For portfolio/synchronisation tasks, prefer the documented filters:
- `ComparisonDate=LastModified`
- `FromDate=<last successful sync date>`
- `SortOrder=ASC`
- paginated retrieval with `PageSize` up to the documented maximum.

Do not invent an undocumented `reference` query parameter.
