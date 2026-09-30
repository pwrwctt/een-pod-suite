# EEN POD Suite v2.1 for OpenCode

This project contains seven modular Agent Skills under `.opencode/skills/`.

## Skills

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

## v2.1

Adds exact public profile lookup by POD Reference and suite-version self-reporting.
