# BO pilot scoring and remediation
Read `references/source-BO_Quality_Scoring_Model_2026-09-29.md`,
`references/bo-scoring-model.json` and `references/quality-review.md`.
The 2026 pilot supplements the 2024 baseline; the old statement about no central
pre-publication review does not imply that no published-profile pilot now exists.

## Separate assessment layers
1. Pilot-derived BO points (-4 to 8; Poor/Weak/Fair/Good/Excellent).
2. Evidence-based PPQG findings (BLOCKER/MAJOR/MINOR), including semantic checks
   excluded from SQL: actual product/offer, genuine cooperation, eligibility,
   WHY/HOW, real quantified benefits, coherence, acronyms and language errors.
3. Submission readiness and missing-evidence/operational/adviser gates.

Do not equate Excellent with READY, Poor with BLOCKER, or a lost point with
a proven rule violation. Scoring minima (40/250/800/200/300 characters) earn
points; do not recast them as mandatory PPQG field minima. The pilot's 256/4000
values define scoring ranges; they do not independently verify current form UI.

## Inputs and execution
Use `scripts/bo_quality_score.py` or the connected read-only
score_business_offer tool. Input: profile_type BO, profile_status PUBLISHED,
reference and/or exact supplied URL, country code/name, fields (title, summary,
description, advantages, partner_role, partnership_types).
Use original field strings for lengths. Normalised HTML may require operator
confirmation; a partial extraction is not a complete database record.

Missing, null or not_visible fields mean UNKNOWN; an explicitly observed empty
string/list is empty. Do not turn public nonvisibility into an empty value.
Country names/demonyms require identified origin; do not infer origin from a
passing country mention. The local dictionary is not the pilot SQL dictionary.
Unknown country terms or structured agreement labels leave the criterion unknown.

The default scope is published BO only. Missing publication status is SCOPE
UNVERIFIED. Draft assessment is available only through explicit simulation mode,
clearly labelled SIMULATION, with no operational flag/notification recommendation.
Known tests and all-visible-123 patterns are excluded. No identifier/name search.

Report all twelve criteria with counts, matched terms, source rule and local
interpretation. If data is incomplete show minimum/maximum score and possible
bands; even a unique possible band is provisional until evidence is complete.
State that this is a local implementation of the supplied pilot model, not an
official EISMEA tool result. Original SQL equivalence is unverified.

## Declared interpretations
Lengths use original Unicode code points. P3 compares casefolded, whitespace-
collapsed summary with title and entire summary against description opening.
N4 compares raw, case-sensitive first 40 characters of BOTH fields, each at
least 40 characters. N2 counts distinct terms in the illustrative eight-term
list, with spacing/hyphen aliases, not repeated occurrences. N1 scans the five
public narrative fields case-insensitively; US and quoted text can be false
positives. P1 allows a different agreement in each field; P8 separately checks
every selected agreement in all three fields. ALL CAPS ignores uncased digits
and punctuation. These decisions must be replaced/versioned if source SQL
clarifies them; never silently claim exact parity.

## Operational recommendations from coordinator message
- Poor: adviser-verified Guidelines Compliance flag with concrete non-compliance
  quotation/rule/correction; invitation to POD Quality Clinic.
- Weak: owner improvement notification and clinic invitation.
- Fair/Good: owner improvement notification.
- Excellent: no specific remedial action prescribed; semantic audit still applies.
- Repeat review after two calendar months from the agreed baseline evaluation,
  not from email receipt. Date calculations clamp to month end where necessary.

Prepare drafts only. No tool flags POD, contacts an owner, sends invitations,
publishes records or schedules an automatic reminder. A Poor proxy score alone
is insufficient evidence for a non-compliance allegation. Populate templates
only from observed issues, keeping local score and proven PPQG non-compliance
separate. Drafts contain placeholders until the adviser confirms facts.

## Saved runs and follow-up
Save score output as JSON; it contains the relevant input snapshot, identity,
evaluation/recheck dates, model ID/implementation and model/dictionary hashes.
Use `scripts/bo_quality_score.py` compare or compare_bo_scores on two runs.
Require the same explicit reference or exact URL, same scope and same model/
dictionary hashes. If the model changed, rescore both snapshots using one
implementation. Compare points and criterion states, then independently close
findings as RESOLVED/PARTLY RESOLVED/OPEN/NOT VERIFIABLE with quotations.
Do not treat a score gain as proof of corrected content.

## Calibration and future types
Review samples across all five bands with experienced POD advisers and record
disagreements, false positives and repeated-run consistency. Until this happens,
expert calibration is NOT VERIFIED. Publish tests separately from host UI tests.
Do not extend BO points to BR/TO/TR/RDR or Achievements. Achievements needs its
own future model; the coordinator's reporting period 2025-07-01 to 2026-12-31
is not a stated submission deadline.

For an explicit changed-model comparison, use compare --rescore (or rescore=true in compare_bo_scores). Both saved snapshots are recalculated with the current rules; recorded original totals are labelled separately. The report states whether the actual follow-up date has reached the two-month due date; an early comparison is not represented as a completed two-month review.

A full published-BO audit includes this separate score by default. A narrow editing task need not run every check. Do not refuse supported content findings merely because scope verification or some scoring fields are unavailable.
