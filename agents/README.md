# EEN POD Reader & Audit Agent — v2.7

## Tools

- `get_public_profile(url, expected_reference?)`: read the supplied detail page and verify its displayed POD Reference. The optional reference is an identity check only.
- `check_form_limits(profile_type, fields, market_keywords?, technology_keywords?)`: local character/count checks.
- `review_profile_input(profile, as_of?)`: advisory completeness, supplied taxonomy and date checks with explicit reviewer gates.
- `search_taxonomy(kind, query, mode?, limit?)`: offline exact-code or curated bilingual semantic candidates, with reasons. Scores are diagnostic, not official assessments.

The skill provides audit rules. If only a profile number or name is supplied, ask for the exact URL. If reading the page fails, request a text/HTML export of that page; never perform discovery as fallback.

## Local process

Python 3.10+ and the standard library are sufficient:

```bash
python chatgpt/een-pod-suite/scripts/reader_mcp.py
```

This exposes newline-delimited MCP JSON-RPC over stdin/stdout. Configure the host with the absolute script path using `mcp.example.json`. The process is not installed automatically.

## ChatGPT connection

ChatGPT requires a hosted HTTPS MCP endpoint and compatible authentication. The skill archive contains instructions and code, not a live connection.

```bash
python chatgpt/een-pod-suite/scripts/reader_mcp.py --http --host 127.0.0.1 --port 8080
```

No tool publishes or modifies POD records. The server still needs authorised network access to the supplied page; it does not bypass site or network restrictions.

## Validation

```bash
python -m unittest discover -s tests -v
python scripts/build.py
```

See [the agent contract](../chatgpt/een-pod-suite/references/reader-agent.md) and [the URL-only audit workflow](../chatgpt/een-pod-suite/references/profile-lookup.md).

The agent exposes four read-only tools: supplied URL reading, form limits, evidence checks and offline taxonomy search. Use the skill's bundled 2024 taxonomy for keyword recommendations.

Use semantic search for candidate generation and review_profile_input for supplied evidence. Neither tool establishes independent review, eligibility or current data automatically. Read process-extensions.md for evidence ledger, consistent verdicts and extensions.
