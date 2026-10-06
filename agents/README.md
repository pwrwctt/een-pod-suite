# EEN POD Reader & Audit Agent — v2.4

The agent audits an existing profile only from the exact official detail URL supplied by the operator. Number/name discovery and API identifier scanning have been removed.

## Tools

- `get_public_profile(url, expected_reference?)`: read the supplied detail page and verify its displayed POD Reference. The optional reference is an identity check only.
- `get_live_labels(data_type, page?, page_size?)`: read current Market/Technology labels with authorised API access.
- `check_form_limits(profile_type, fields, market_keywords?, technology_keywords?)`: local character/count checks.

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

HTTP mode requires server-side `EEN_AGENT_TOKEN` and accepts Bearer authentication at `/mcp`. It implements stateless POST requests, not OAuth. A compatible OAuth gateway is required where the host requires OAuth. Public page reading requires no EEN API key. Live labels require server-side `EEN_API_KEY` and EEN IP whitelisting.

No tool publishes or modifies POD records. The server still needs authorised network access to the supplied page; it does not bypass site or network restrictions.

## Validation

```bash
python -m unittest discover -s tests -v
python scripts/build.py
```

See [the agent contract](../chatgpt/een-pod-suite/references/reader-agent.md) and [the URL-only audit workflow](../chatgpt/een-pod-suite/references/profile-lookup.md).
