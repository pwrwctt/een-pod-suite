---
name: een-pod-profile-lookup
description: Retrieve and extract an EEN profile only from the exact official profile detail URL supplied by the operator, verify its displayed POD Reference and hand visible content to quality review. No reference or name discovery.
---

# EEN POD profile URL reader

Read `references/version.md` for version questions and `references/profile-lookup.md` for the URL-only workflow.

Require the operator's exact profile detail URL. Use `scripts/profile_url.py` when direct public retrieval is available. Verify the displayed POD Reference before extracting content. Hand the profile to `een-pod-profile-quality-reviewer` for an audit.

If only a number or name is supplied, ask for the exact detail URL. Do not build search URLs, search the public site, guess a slug, search results or substitute another profile. If reading fails, request a text/HTML export of the same page.

## Evidence and extended process

Read `references/process-extensions.md` and `references/source-provenance.md` for completeness, consistency, targeted interviews, version comparison, EoI drafts and partner-fit assessment. Explicit user instructions take priority over workflow preferences; never invent facts or verification. Record the actual second-review method and adviser confirmation.

For form/readiness tasks read `references/form-schema.md` and use `scripts/form_readiness.py` for populated BO/BR/TO/TR fields. Use `scripts/profile_checks.py` for completeness, exact taxonomy, country and RDR date checks. A length PASS does not establish submission readiness. Public nonvisibility requires a limited review, not an invented omission. For semantic taxonomy use `scripts/taxonomy_lookup.py` and inspect candidate reasons; for version comparison use `scripts/profile_diff.py`.
