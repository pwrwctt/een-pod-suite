# EEN POD Suite

Current version: **2.3**

Repository for maintaining the Enterprise Europe Network Partnering Opportunities Database skill suite.

## Targets
- `chatgpt/een-pod-suite/` — single ChatGPT Skill.
- `opencode/.opencode/skills/` — modular OpenCode suite.
- `shared/` — shared rules/scripts.
- `dist/` — generated release artifacts.

## Main capabilities
- BO / BR / TO / TR / RDR classification and drafting
- exact public POD lookup by reference
- independent quality review
- Technology / Market / SDG taxonomy support
- dissemination/query guidance
- BO/BR/TO/TR form-readiness checks
- installed-version reporting
- Partner Web Service profiles and live Market/Technology reference data
- API visibility, lifecycle metadata and incremental synchronisation

## Versioning
`VERSION` is the source of truth. Release tags use `vX.Y`.

## Build
Run `python scripts/build.py` (Python standard library only).
Run API regression tests with `python -m unittest discover -s tests -v`.

## Confidentiality
Before making the repository public, review redistribution rights for bundled EEN Community documents, templates and taxonomy files.
