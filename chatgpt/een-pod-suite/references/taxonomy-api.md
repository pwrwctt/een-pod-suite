# Live Market and Technology taxonomy via Partner Web Service

Source basis: **Partner Webservices user guide (b2b), 19 May 2026**.

Use this workflow only for Market and Technology keywords. The guide does not establish this endpoint as a source for NACE or SDG.

## Endpoint

`GET /refdrupal/label`

The endpoint returns reference-data labels for:
- `market_keyword`
- `technology_keyword`

Use query parameter `Filter.Descriptor`. Filter and parameter names are case-sensitive.

Useful descriptor conditions:
- `dataTypeId^equals^market_keyword`
- `dataTypeId^equals^technology_keyword`
- `FromDate^equals^DD-MM-YYYY`
- `ToDate^equals^DD-MM-YYYY`

Conditions may be concatenated with `^`.

## Pagination

This endpoint uses:
- `page` — **0-based**;
- `page_size`.

This differs from the Profiles endpoint. Do not reuse Profiles pagination assumptions.

## Identity

Treat these fields as authoritative identity/hierarchy data:
- `uuid` — persistent label identifier;
- `parentUuid` — parent label identifier;
- `name`
- `acronym`
- `isActive`
- `dataTypeId`
- `dataTypeName`

Do **not** use:
- `id` for persistent label identity;
- `parentId` for persistent parent identity.

A root label has:

`parentUuid = 00000000-0000-0000-0000-000000000000`

## Active-label rule

Prefer labels with `isActive == "True"`.

If an existing profile contains an inactive label, preserve it as historical profile data but do not recommend it for a new classification without confirming current live availability.

## Hierarchy

Build the hierarchy from `uuid` and `parentUuid`.

Continue applying the PPQG keyword-selection rule. When using API hierarchy, derive parent/child relationships from UUIDs and do not invent hierarchy levels solely from code length.

## Freshness priority

For Market/Technology keyword selection:

1. live authenticated Partner Web Service reference data;
2. if unavailable, bundled EEN taxonomy snapshot;
3. clearly label fallback output as snapshot-based.

The bundled snapshot remains useful offline but must not override verified live labels.

## Incremental sync

Use `FromDate` and optionally `ToDate` to retrieve labels changed during a period.

For a robust merge:
- add/update by `uuid`;
- preserve parent relationship via `parentUuid`;
- update `name`, `acronym`, `isActive`, `dataTypeId`;
- never overwrite a live item solely because its legacy numeric `id` changed.
