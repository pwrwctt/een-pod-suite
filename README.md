# EEN POD Suite

**AI skills and Python utilities for preparing, reviewing and retrieving Enterprise Europe Network partnering profiles.**

EEN POD Suite helps Enterprise Europe Network (EEN) advisers turn client information into structured cooperation profiles for the Partnering Opportunities Database (POD). It combines profile-writing guidance, eligibility checks, taxonomy references, deterministic field-limit checks and authenticated profile retrieval in a reusable workflow.

**Current version: 2.4** · [Changelog](CHANGELOG.md) · [Source policy](chatgpt/een-pod-suite/references/source-policy.md) · [Validation report](opencode/VALIDATION.md)

The repository provides a unified skill for a compatible ChatGPT skills environment and nine modular skills for OpenCode. Its Python helpers can also be run independently. The skills guide an AI assistant; the scripts perform specific lookup, validation and retrieval tasks. Final editorial review and submission remain with the adviser.

## Who it is for

- **EEN advisers** preparing cooperation profiles from client interviews, technical notes or existing drafts.
- **Profile reviewers** checking eligibility, clarity, partner roles, field completeness, anonymity and taxonomy selection.
- **Teams managing a profile portfolio** retrieving authorised profile data and checking publication status, expiry dates and availability for expressions of interest.
- **Developers and skill maintainers** integrating POD workflows into a compatible AI environment or extending the included Python tools.

## Supported profile types

| Code | Profile type | Typical purpose |
| --- | --- | --- |
| BO | Business Offer | Offer products or services through a medium- or long-term cooperation arrangement. |
| BR | Business Request | Find suppliers, products, services or other business inputs for a cooperation need. |
| TO | Technology Offer | Offer an innovative technology, process or know-how for technology transfer. |
| TR | Technology Request | Find technology or expertise to address a defined technical need. |
| RDR | Research & Development Request | Find partners for a concrete research and development project linked to an eligible funding call. |

The suite helps select a profile type from the actual cooperation objective and client eligibility. A direct sales request does not become a partnering opportunity merely by changing its wording. See the [eligibility guidance](chatgpt/een-pod-suite/references/intake-eligibility.md) and [profile-type rules](chatgpt/een-pod-suite/references/profile-types.md).

## Capabilities

### Profile preparation and quality review

- Assess client eligibility, cooperation purpose and missing input before drafting.
- Draft and revise titles, short summaries, descriptions, advantages, technical requirements and expected partner roles.
- Explain why a proposed partnership type fits the opportunity and how the cooperation would work.
- Optimise titles and summaries for clear discovery and partner matching.
- Review drafts against Partnering Profile Quality Guidelines (PPQG) v1.2, with findings separated from unverified assumptions.
- Check anonymity, confidential information and consistency across profile fields.
- Review RDR call and project information when supplied, including structured fields returned by the API.

### Field readiness and taxonomy selection

- Count characters and report exceeded limits for BO, BR, TO and TR fields.
- Check Market and Technology keyword counts against the five-keyword limit.
- Search bundled Technology, Market, NACE and Sustainable Development Goal (SDG) taxonomy CSVs.
- Retrieve live Market and Technology reference data through the authenticated Partner Web Service.
- Distinguish optional form controls from mandatory content requirements.

The [form-readiness helper](chatgpt/een-pod-suite/scripts/form_readiness.py) checks lengths and keyword counts. It does not determine eligibility, semantic quality or whether every required field has been completed. An empty field passing a length check still needs editorial review.

### Profile discovery and API retrieval

- Read the exact official profile detail URL supplied by the operator.
- Verify the displayed POD Reference on that supplied page before quality review.
- Retrieve authorised Cooperation Profiles using documented type, status, country and date filters.
- Iterate profile and reference-data pages through Python functions.
- Classify API content visibility as `FULL`, `LIMITED` or `UNKNOWN` before assessing completeness.
- Interpret available lifecycle metadata, including status, publication and expiry dates, `openForEOI` and `publicURL`.
- Support review of attachment and Video Pitch metadata when returned.

The URL reader requires an operator-supplied exact detail URL and verifies the displayed POD Reference. It does not discover profiles by number or name. If the operator provides only an identifier or name, request the exact detail URL.

### Portfolio and dissemination workflows

The suite includes guidance for incremental profile retrieval using modification dates, taxonomy updates using UUIDs, and saved-query or dissemination workflows. Python iterator functions can support custom synchronisation code. Persistent storage, scheduling, checkpointing and automated merges must be implemented by the consuming application.

## Repository structure

```text
chatgpt/een-pod-suite/        Unified skill, references and Python helpers
opencode/.opencode/skills/   Nine specialised OpenCode skills
opencode/manifest.json      Suite version and module inventory
shared/                     Shared references and utilities
scripts/build.py            Release archive builder
tests/                     Automated API regression tests
docs/TEST-CASES.md          Manual regression scenarios
dist/chatgpt/skill.zip      Packaged ChatGPT skill
dist/opencode/              Versioned OpenCode archives
VERSION                     Authoritative suite version
CHANGELOG.md                Release history
```

## Reader & Audit Agent

The suite includes an agent contract and a runnable MCP server exposing three read-only tools: direct profile URL reading, live Market/Technology labels and field-limit checks. The skill supplies the audit rules; the host model uses those tools to collect evidence. See the [agent setup guide](agents/README.md) for local OpenCode/Codex configuration and remote ChatGPT requirements.

The updated skill archive contains the agent instructions and server code. It does not create a live MCP connection: ChatGPT requires a hosted HTTPS endpoint and supported authentication. No tool modifies or publishes POD records.

## Installation

### Obtain the repository

```bash
git clone https://github.com/pwrwctt/een-pod-suite.git
cd een-pod-suite
```

If the repository is private, authenticate with a GitHub account authorised to access it. You can also download the source or release archives from GitHub.

### Unified ChatGPT skill

Use [dist/chatgpt/skill.zip](dist/chatgpt/skill.zip) with a ChatGPT environment that supports installing skills. Follow that environment's skill installation process; if it accepts unpacked skills, install the complete `chatgpt/een-pod-suite/` directory, preserving its `SKILL.md`, `references/`, `scripts/` and `agents/` contents.

After installation, ask: **“Which version of EEN POD Suite is installed?”** The expected answer for this release is `EEN POD Suite v2.4`.

Script execution, browsing and authenticated API retrieval require the corresponding capabilities in the host environment. Availability of a skill installation interface depends on that environment.

### Modular OpenCode skills

Copy the contents of `opencode/.opencode/skills/` into your project's `.opencode/skills/` directory. Preserve each module's directory structure. If the project already has skills, merge the directories and review any name conflicts.

Alternatively, extract [een-pod-suite-opencode-v2.4.zip](dist/opencode/een-pod-suite-opencode-v2.4.zip) and copy its `.opencode/` contents into the project.

| Skill | Responsibility |
| --- | --- |
| `een-pod-suite` | Route requests and coordinate the overall workflow. |
| `een-pod-intake` | Assess eligibility, profile type and missing input. |
| `een-pod-profile-drafter` | Prepare structured profile drafts. |
| `een-pod-title-summary-optimizer` | Improve titles and short summaries. |
| `een-pod-keywords-classifier` | Select and verify taxonomy entries. |
| `een-pod-profile-quality-reviewer` | Perform an independent quality review. |
| `een-pod-profile-lookup` | Read an operator-supplied exact profile detail URL. |
| `een-pod-dissemination-queries` | Explain dissemination and saved-query workflows. |
| `een-pod-api` | Retrieve authorised profiles and live Market/Technology labels. |

### Standalone Python tools

Use **Python 3.10 or later**. The included helpers, build script and automated tests use the Python standard library; no third-party packages are required.

Run the examples below from the repository root. Add `--help` to an individual script or API subcommand to inspect its options.

## Using the skills

### Prepare a new profile

Provide the client's country and organisation type, the offer or need, supporting evidence, desired cooperation arrangement, partner requirements and anonymity preference. Identify unknown facts explicitly.

Example request:

> Use EEN POD Suite to assess these client notes, recommend a profile type and draft the relevant fields. List missing information separately, explain the proposed partnership and perform an independent quality review before presenting the final draft.

The recommended sequence is **intake → drafting → title and summary → taxonomy selection → independent quality review**. For BO, BR, TO and TR, add deterministic form-readiness checks before final approval.

### Review an existing published profile

Supply the exact official profile detail URL:

> Audit the profile at https://een.ec.europa.eu/partnering-opportunities/albanian-tour-operator-and-dmc-seeking-international-partnerships. Verify the displayed POD Reference and review only retrieved content against the suite's quality guidance.

A number or profile name alone is insufficient: the skill asks for the exact URL and does not search for it. If that URL cannot be read, provide an authorised text/HTML export of the same profile.

### Review API data

> Review this authorised Partner Web Service profile response. Report its POD Reference, source, visibility, status and open-for-EOI value before assessing quality. Explain which fields cannot be reviewed.

`LIMITED` records must not receive missing-field defects merely because protected content is `null` or `N/A`. `UNKNOWN` visibility requires explicit uncertainty. Publication status and openness to expressions of interest are assessed separately.

## Command-line examples

### Read the supplied profile detail URL

```bash
python chatgpt/een-pod-suite/scripts/profile_url.py \
  https://een.ec.europa.eu/partnering-opportunities/albanian-tour-operator-and-dmc-seeking-international-partnerships
```

The optional `--expected-reference` checks identity on this page only. The reader does not search by reference or name and does not follow search-result cards. A failed read is reported without triggering discovery. See the [URL audit workflow](chatgpt/een-pod-suite/references/profile-lookup.md).

### Search an offline taxonomy snapshot

```bash
python chatgpt/een-pod-suite/scripts/taxonomy_lookup.py technology "water treatment" --limit 5
python chatgpt/een-pod-suite/scripts/taxonomy_lookup.py market "medical" --limit 5
```

Results are ranked candidates from the bundled **2024 snapshot**. Review the labels and hierarchy before selecting entries. Use verified live Market/Technology data when current values are required.

### Check field lengths and keyword counts

```bash
python chatgpt/een-pod-suite/scripts/form_readiness.py BO \
  --title "A business cooperation opportunity" \
  --summary "A concise summary of the offer and intended partnership." \
  --partner-role "Describe the partner's expected responsibilities."
```

The JSON output includes character counts, limits and `PASS` or `OVER LIMIT by N` results. The supplied BO/BR/TO/TR form guidance sets a 256-character title limit, a 500-character summary limit and 4,000-character limits for descriptions and partner roles. Additional 2,000-character limits apply to profile-specific fields. See the [field-limit reference](shared/references/form-schema.md) for applicability and optionality.

### Preview API filters without credentials

```bash
python chatgpt/een-pod-suite/scripts/een_b2b_api.py profiles \
  --profile-type TO --status PUBLISHED --country PL --dry-run

python chatgpt/een-pod-suite/scripts/een_b2b_api.py labels \
  technology_keyword --page 0 --dry-run
```

`--dry-run` prints the encoded query parameters and makes no network request.

### Retrieve authorised API data

Configure `EEN_API_KEY` through your runtime's secret manager or another secure environment-variable mechanism. The organisation's calling IP must also be whitelisted for the Partner Web Service. Do not place the key in source files, prompts, command examples or committed configuration.

```bash
python chatgpt/een-pod-suite/scripts/een_b2b_api.py profiles \
  --profile-type TO --status PUBLISHED --page-index 1 --page-size 200

python chatgpt/een-pod-suite/scripts/een_b2b_api.py labels \
  market_keyword --page 0 --page-size 200

python chatgpt/een-pod-suite/scripts/een_b2b_api.py visibility profile.json
```

The default base URL is `https://b2b.een.ec.europa.eu/v1`. `EEN_B2B_BASE_URL` can select a trusted test endpoint; it receives the configured API key, so use it deliberately.

- `profiles` and `labels` retrieve a single page. Profiles pagination starts at **1**; label pagination starts at **0**.
- `visibility` classifies a saved profile JSON object locally and requires no API credentials.
- For application integrations, use `iter_profiles()` and `iter_labels()` to traverse pages. See the [API helper](chatgpt/een-pod-suite/scripts/een_b2b_api.py).
- HTTP 401/403 indicates an access problem requiring credential or IP-whitelisting checks.

API commands can return non-public information visible to the calling organisation. Keep output in an authorised location and do not automatically republish it.

## Sources and scope

The suite's references use the following source hierarchy:

| Source | Role |
| --- | --- |
| Partnering Profile Quality Guidelines v1.2, September 2024 | Primary baseline for eligibility, mandatory content and profile quality. |
| Partner Webservices user guide, 19 May 2026 | Basis cited by the integration references for Cooperation Profiles and Market/Technology API behaviour. |
| Official public EEN partnering-opportunities website | Operator-supplied detail-page reading and identity verification. |
| EEN Glossary 2024 v3 | Terminology. |
| Managing Queries for Widgets and Ticker, 13 December 2024 | Dissemination and saved-query guidance. |
| Bundled EEN taxonomy workbook and CSVs | Offline 2024 taxonomy snapshot. |

Verified current authoritative data takes precedence over bundled snapshots. The implemented live taxonomy workflow covers Market and Technology labels; it does not establish live NACE or SDG retrieval. See the [source policy](chatgpt/een-pod-suite/references/source-policy.md).

Version 2.3 provides drafting and review assistance plus read-only API helpers. It does not submit, publish or modify profiles in POD, integrate the Events API, or provide a scheduled synchronisation service. A successful check or polished draft is not a guarantee of acceptance by EEN.

## Security and data handling

- Read the [API security guidance](chatgpt/een-pod-suite/references/api-security.md) before authenticated use.
- Keep `EEN_API_KEY` in runtime secrets and out of Git, logs and generated reports.
- Respect API access restrictions and the confidentiality of unpublished profiles and client information.
- Check anonymity in text and available media metadata according to the client's decision.
- Review redistribution rights for bundled EEN Community documents, templates and taxonomy files before sharing them or making the repository public. Access to this repository does not itself establish permission to redistribute those sources.

## Development and validation

```bash
python -m unittest discover -s tests -v
python scripts/build.py
```

The tests cover API filter validation, pagination, visibility classification, error handling and consistency of the distributed API helpers. URL-reader tests verify that discovery is absent, identifiers alone are rejected, and reading is limited to the supplied page. Tests use mocked responses and do not establish live website or Partner Web Service compatibility or verify all editorial rules.

The build script checks skill front matter, referenced files, version consistency and the OpenCode module inventory before creating:

- `dist/chatgpt/skill.zip`
- `dist/opencode/een-pod-suite-opencode-v2.4.zip`

For additional editorial regression scenarios, see [docs/TEST-CASES.md](docs/TEST-CASES.md). The [validation report](opencode/VALIDATION.md) records which checks were actually performed.

Use [VERSION](VERSION) as the version source of truth and [CHANGELOG.md](CHANGELOG.md) for release changes. Release tags follow the `vX.Y` naming convention. Maintainers should keep shared and distributed helper copies consistent, update the changelog for release-impacting changes, and validate and build before tagging a release.
