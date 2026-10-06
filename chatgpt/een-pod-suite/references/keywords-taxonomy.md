# Keywords, SDG and taxonomy use

Source basis:
- Partnering Profile Quality Guidelines v1.2, section 6.2.2;
- Partner Webservices user guide (b2b), 19 May 2026, for live Market/Technology labels;
- user-supplied EEN Community taxonomy workbook as an offline 2024 snapshot.

## Market keywords

Choose **maximum 5**.
Focus on the **market application** of the product/service/technology/know-how.

## Technology keywords

For TO/TR, choose **maximum 5** and focus on the **technology itself**, not its application market.
The RDR checklist also includes Technology keywords (max 5).
For BO/BR, Technology keywords may be used when they add value and are relevant.

## Specificity rule

The v1.2 Guidelines say:
- select **Level 3** keywords where available;
- where a branch has only two levels, select the **Level 2** keyword.

Search may be conducted using keywords alone, so prefer a small set of discriminating terms.

## Live taxonomy first

When authenticated Partner Web Service access is available, read `taxonomy-api.md` and prefer live `market_keyword` / `technology_keyword` labels from `/refdrupal/label`.

Use `uuid` as the label identifier and `parentUuid` for hierarchy. Ignore the legacy numeric `id` / `parentId` for persistent identity. Prefer active labels (`isActive == "True"`).

When live access is unavailable, fall back to the bundled taxonomy files.

## Bundled taxonomy files

Use:
- `taxonomy-technology-selectable.csv`
- `taxonomy-market-selectable.csv`
- `taxonomy-technology-full.csv`
- `taxonomy-market-full.csv`
- `taxonomy-nace-full.csv`
- `taxonomy-sdg.csv`

The selectable Technology/Market CSVs were derived from the user-supplied workbook using the v1.2 level rule.

## Ranking method

For each candidate:
1. identify exact evidence in the profile;
2. classify as Technology or Market;
3. search the corresponding selectable CSV;
4. prefer the most specific exact/semantic match;
5. rank as Primary or Secondary;
6. exclude broad, adjacent, speculative or duplicated entries;
7. keep within the maximum.

Never invent a code or label.

## NACE

The supplied workbook contains a NACE hierarchy. The searched text of Partnering Profile Quality Guidelines v1.2 does **not** establish NACE as a mandatory profile field.
Use NACE only when:
- the user asks for it; or
- the live POD form/workflow being used requires it.

Do not state that NACE is mandatory based only on the bundled workbook.

## SDG

SDG is mandatory under the v1.2 profile field guidance.
Use the bundled `taxonomy-sdg.csv`.
If none applies, use `Not relevant`.

## Version warning

The workbook metadata indicates a 2024-era snapshot. Do not let the bundled CSVs override verified live Partner Web Service labels.

The 19 May 2026 web-service guide documents Market and Technology reference labels only. Continue to treat NACE and SDG through their existing suite sources unless a newer authoritative source is verified.
