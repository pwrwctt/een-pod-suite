# EEN POD Suite v2.4 for OpenCode

This project contains 9 modular Agent Skills under `.opencode/skills/`.

## Skills

- `een-pod-api` — Partner Web Service profiles and live Market/Technology reference data

- `een-pod-suite` — orchestrator
- `een-pod-intake`
- `een-pod-profile-drafter`
- `een-pod-title-summary-optimizer`
- `een-pod-keywords-classifier`
- `een-pod-profile-quality-reviewer`
- `een-pod-profile-lookup`
- `een-pod-dissemination-queries`

## Install

Copy `.opencode/` to the root of your OpenCode project.

## Full workflow

`intake → drafter → title/summary → keywords → independent quality review`

Use dissemination/query guidance when required.

## v2 source basis

- Partnering Profile Quality Guidelines v1.2 — September 2024
- EEN Glossary 2024 v3
- Managing Queries for Widgets and Ticker — 13 December 2024
- user-supplied EEN Community SDG/Market/Technology/NACE taxonomy workbook

The UI and taxonomy data are treated as 2024 snapshots. Current live POD data takes precedence when verified.

## v2.4 audit input

Existing-profile audits require an exact official profile detail URL supplied by the operator. Number/name discovery and API identifier scanning were removed. The `een-pod-profile-lookup` module retains its directory name for compatibility but only reads supplied detail URLs.

## Read-only audit agent

The distribution now includes `.opencode/agents/een-pod-auditor.md`. Copy the `agents/` directory alongside the skills and connect the `een_pod_reader` MCP server. The runnable server resides in the repository at `chatgpt/een-pod-suite/scripts/reader_mcp.py`; the OpenCode ZIP does not install or host that process. See `agents/README.md` in the repository for configuration.
