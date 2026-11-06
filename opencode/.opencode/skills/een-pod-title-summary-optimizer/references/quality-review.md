# Independent quality review

Source basis: Partnering Profile Quality Guidelines v1.2, especially section 3.1 quality-check note and sections 4–6.

The historical v1.2 workflow describes no central pre-publication quality review. The coordinator's 2026 pilot adds checks of published BO profiles; do not present the historical statement as a description of all current review activity. Consortia should therefore establish a pre-publication quality-check and have drafts checked by an experienced colleague.

Record the actual review method. One assistant switching roles is advisory self-review, not proof of a separate colleague's review. Final approval remains with the adviser. Read `references/process-extensions.md` for the evidence ledger and completeness/consistency gates.

## Severity

### BLOCKER
Use when the profile should not be treated as submission-ready, including:
- ineligible client/profile purpose;
- direct-sale/customer-search profile;
- fundamentally wrong BO/BR/TO/TR/RDR type;
- anonymous profile exposes identity/IP;
- offer/request cannot be understood;
- cooperation objective or partner role is materially missing;
- partnership type contradicts the narrative;
- fabricated/unsupported critical facts;
- Short Summary exceeds 500 characters;
- RDR lacks essential call/partner information.

### MAJOR
Use for:
- generic title;
- summary missing core cooperation information;
- marketing claims instead of evidence;
- weak WHY/HOW cooperation explanation;
- vague partner role;
- wrong or over-broad keywords;
- more than 1–3 partnership types without a strong reason;
- material inconsistency between fields.

### MINOR
Use for:
- grammar, concision, local repetition, readability, formatting.

## Field checks

Check:
- eligibility / groundwork flags;
- profile type;
- Title;
- Short Summary character count;
- Full Description as stand-alone text;
- field-specific mandatory content;
- Advantages & Innovations where required;
- Technical specifications where required;
- Stage / IPR for TO;
- SDG;
- Expected role of partner;
- Partnership type(s);
- Type/size of partner;
- Market/Technology keywords and limits;
- target countries;
- media anonymity;
- RDR call fields when applicable.

## Decision

Return REVIEW LIMITED when evidence, semantic review, operational/current-form confirmation or independent review is incomplete. With sufficient evidence, any BLOCKER or unresolved MAJOR requires RETURN FOR REVISION. Only MINOR allows READY AFTER MINOR EDITS. READY requires no issues and adviser-confirmed gates. Public nonvisibility is not proof of an internal omission. Attach rule and quotation to each issue.

Otherwise return one:
- **READY**
- **READY AFTER MINOR EDITS**
- **RETURN FOR REVISION**

A polished style does not compensate for a weak cooperation proposition.

## Pilot-derived BO score

Read `references/bo-quality-scoring.md`. When requested or relevant to the 2026 BO pilot, calculate the supplied source model using `scripts/bo_quality_score.py`; display its implementation version, bounds and limitations. It is separate from the PPQG audit, not an official internal-tool result or submission approval. Do not equate a lost point with confirmed non-compliance. Scoring minima are not new mandatory PPQG requirements. Keep semantic checks excluded from SQL in a separate evidence section.

## Optional internal score

If the user asks for a score, label it:
`Internal diagnostic score — not an official EEN/EISMEA threshold.`

Do not invent numeric acceptance thresholds. The documented bands of the supplied BO pilot may be reported as pilot-derived categories, not general EEN acceptance thresholds.
