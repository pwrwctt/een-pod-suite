---
name: een-pod-profile-lookup
description: Retrieve and extract an EEN profile only from the exact official profile detail URL supplied by the operator, verify its displayed POD Reference and hand visible content to quality review. No reference or name discovery.
---

# EEN POD profile URL reader

Read `references/version.md` for version questions and `references/profile-lookup.md` for the URL-only workflow.

Require the operator's exact profile detail URL. Use `scripts/profile_url.py` when direct public retrieval is available. Verify the displayed POD Reference before extracting content. Hand the profile to `een-pod-profile-quality-reviewer` for an audit.

If only a number or name is supplied, ask for the exact detail URL. Do not build search URLs, search the public site, guess a slug, scan API results or substitute another profile. If reading fails, request a text/HTML export of the same page.
