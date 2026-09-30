---
name: een-pod-profile-lookup
description: Find and extract a published Enterprise Europe Network POD profile by exact POD Reference, such as BOCL20240903021, using the official EEN partnering-opportunities search. Use when the user asks to find, show, inspect, verify, audit or quality-check a profile by BO/BR/TO/TR/RDR reference; verify the full-page POD Reference before extracting content and hand the exact public profile to the quality reviewer when requested.
---

# EEN POD profile lookup

For suite-version questions, read `references/version.md`.

Read `references/profile-lookup.md` for the complete lookup workflow and failure handling.

Use `scripts/pod_reference.py` to normalise a supplied POD Reference and generate the official filtered EEN lookup URL when useful.

If quality verification is requested:
1. find the exact official profile;
2. verify the full-page POD Reference;
3. extract only public fields actually present;
4. hand the extracted profile to `een-pod-profile-quality-reviewer`.

Never guess a profile slug or review a merely similar search result.
