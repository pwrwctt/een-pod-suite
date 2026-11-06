# Business Offer (BO) Quality Scoring Model
Operator-supplied transcription, reformatted without changing the numerical rules.
The original file's own version number is not specified. Database: Production.
Snapshot: 2026-09-29. Baseline: PPQG v1.2, September 2024.

## Purpose and formula
Rate published BO profiles consistently for ranking/filtering.
Eight positive criteria add +1 each; four penalties subtract 1 each.
Score = positives met minus penalties triggered; range -4 to +8.

## Positive criteria
- P1: At least one agreement type (commercial, outsourcing, supplier, investment) appears in the title AND at least one in the description.
- P2: Title 40–256 characters AND not ALL CAPS.
- P3: Summary 250–500 characters AND not copied from title or description opening.
- P4: Origin country name or demonym appears in summary AND description.
- P5: Description 800–4000 characters.
- P6: Advantages contain digits AND have at least 200 characters.
- P7: Expected role of partner has at least 300 characters.
- P8: Selected structured agreement type(s) are also mentioned in summary, description AND partner-sought text.

## Penalties
- N1: Profile text uses we, our, us, you, your; guidance requires third person.
- N2: Three or more generic terms, e.g. unique, innovative, best, high quality, reliable, cutting-edge, leading, state of the art.
- N3: Title entirely uppercase.
- N4: First 40 characters of summary identical to title.

## Bands
| Score | Band |
| --- | --- |
| 8 | Excellent |
| 6–7 | Good |
| 4–5 | Fair |
| 2–3 | Weak |
| -4–1 | Poor |

The Poor range restores the minus sign displaced in the supplied conversion.

## Scope
Only profiletype_code BO and profilestatus_name PUBLISHED. Exclude known test
profiles, e.g. all-field "123" entries. Drafts, expired and archived excluded.

## Deliberately excluded
Semantic product/service identification, unexplained abbreviations and typo
count were excluded as infeasible or unreliable in SQL/Athena. These may be
checked separately by NLP/LLM or a reviewer; they do not alter this formula.

## Known limitations
N1/N2 regex and word matching can produce false positives. P6 detects digits,
not meaningful quantification. P4 uses a country-name/demonym table of about
60 entries; unusual spelling can be missed. P8 checks keyword mentions, not
semantic coherence. Experts should manually inspect a sample in every band
before operational reliance.

The source SQL, complete marketing dictionary and country lookup table were
not supplied. Local implementation decisions are recorded in
`references/bo-scoring-model.json`; they are not asserted to be source rules.
