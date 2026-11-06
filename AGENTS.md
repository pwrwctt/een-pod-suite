# AGENTS.md

Maintain and release the EEN POD Suite.

- Read `VERSION` as the version source of truth.
- Every release must update and validate ChatGPT, OpenCode and Claude together. Never publish a single-platform update with the other platforms left stale.
- Use `chatgpt/een-pod-suite/` as the canonical unified skill. Run `python scripts/sync_claude.py` after changing it; preserve Claude-specific adaptation in that generator.
- Apply relevant content and helper changes to all affected OpenCode modules, update every distributed version reference and the OpenCode manifest, and build all three archives.
- Run `python scripts/sync_opencode.py` for common resources. Preserve specialised SKILL.md bodies and verify their routing. Use `requirements-dev.txt` for real YAML release validation.
- Keep source-provenance limitations explicit; never fabricate missing source templates or current-system verification. Review evidence and verdict gates before publication.
- Run the complete automated tests and `python scripts/build.py` before publishing. The build must reject an out-of-date Claude distribution.
- Do not invent EEN/POD requirements or taxonomy codes.
- Treat PPQG v1.2 as the primary bundled profile-quality baseline.
- Distinguish live/current POD data from bundled 2024 snapshots.
- Verify exact POD Reference before reviewing a published profile.
- Apply `shared/references/form-schema.md` for BO/BR/TO/TR operational limits.
- Do not make optional fields mandatory merely because a form control exists.
- Update CHANGELOG.md for release-impacting changes.
- Validate/build before tagging a release.

- BO pilot points must retain source/implementation provenance, unknown-data bounds and separation from PPQG compliance/readiness. Never infer a proven violation merely from lost points or claim parity with unprovided source SQL.
- If local execution is unavailable, stage the release on a release branch, run the full suite/build on GitHub Actions and promote only the tested source plus generated distributions. Do not claim UI/expert calibration was run.

- Verify ZIP member inventory/content with `python scripts/verify_archives.py`. GitHub Actions release-branch builds may persist generated archives after tests pass; promote that checked commit without forcing main.
