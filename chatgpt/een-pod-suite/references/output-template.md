# Output templates

## Complete profile draft

Use the fields relevant to the chosen profile type:

**Profile type:** BO / BR / TO / TR / RDR\
**Classification confidence:** High / Medium / Low

**Title**

**Short Summary**\
`Character count: N/500`

**Full Description**

**Advantages & Innovations**\
Only when required/relevant.

**Technical specification / expertise sought**\
Only when required/relevant.

**Stage of development**\
TO mandatory; TR optional when useful.

**IPR status / IPR notes**\
TO mandatory; TR optional when useful.

**Sustainable Development Goal(s)**

**Expected role of partner**

**Type and size of partner**

**Type of Partnership**

**Market keywords**\
Up to 5 exact codes/labels when verified against the bundled/current taxonomy.

**Technology keywords**\
When required/relevant; up to 5 exact codes/labels.

**Target countries**

**RDR call details**\
Only for RDR.

**Open items before submission**
- MISSING INPUT
- OPERATIONAL CHECK
- CONFIDENTIALITY CHECK
- CURRENT-VERSION CHECK

## Quality review

**Decision:** READY / READY AFTER MINOR EDITS / RETURN FOR REVISION

Then:
1. Blockers
2. Major issues
3. Minor issues
4. Field-by-field status
5. Minimal corrections
6. Questions needed to resolve remaining issues


## API-backed profile review header

When reviewing data from the Partner Web Service, prepend:

**Data source:** Partner Web Service\
**POD Reference:** ...\
**Profile type:** ...\
**API visibility:** FULL / LIMITED / UNKNOWN\
**Profile status:** ...\
**Last modified:** ...\
**Open for EOI:** true / false / not returned\
**Public URL:** ... / not returned

If visibility is `LIMITED`, do not issue completeness blockers based on hidden `null` / `N/A` values.

## Taxonomy provenance

When recommending Market/Technology keywords, state one:
- `Live Partner Web Service reference data`
- `Bundled 2024 taxonomy snapshot fallback`

For live labels, use UUID-based identity/hierarchy.
