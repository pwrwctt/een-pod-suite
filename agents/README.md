# EEN POD Reader & Audit Agent

This agent connects the existing EEN POD Suite skill to four read-only MCP tools. The host model performs the audit using the skill; the MCP server retrieves data and checks counts. No additional autonomous model, profile-writing endpoint or publication action is introduced.

The agent contract is [reader-agent.md](../chatgpt/een-pod-suite/references/reader-agent.md). The runnable server is [reader_mcp.py](../chatgpt/een-pod-suite/scripts/reader_mcp.py), included in the ChatGPT skill archive. Python 3.10+ and the standard library are sufficient.

## Tools

| Tool | Purpose | Access |
| --- | --- | --- |
| `get_public_profile` | Read a public page and verify its displayed POD Reference | Public HTTPS; no API key |
| `get_api_profile` | Scan up to five authorised API pages for an exact reference | Server-side EEN_API_KEY and IP whitelisting |
| `get_live_labels` | Read one Market/Technology reference-data page | Same authorised API access |
| `check_form_limits` | Check BO/BR/TO/TR character limits and keyword counts | Local computation |

Public HTML retrieval has the same site and network restrictions as any HTTP client. It is not a browser renderer or a way to bypass HTTP 403. API lookup is bounded and may not find a record outside the scanned pages. Tool errors and missing credentials do not establish that a profile is unavailable.

## Local MCP connection

Run from the repository root:

```bash
python chatgpt/een-pod-suite/scripts/reader_mcp.py
```

This starts newline-delimited JSON-RPC on stdin/stdout. Configure an MCP-capable host with the same Python command and the absolute server path. [mcp.example.json](mcp.example.json) is a configuration template; replace its path with the actual installed path. It does not install itself.

For OpenCode, copy `opencode/.opencode/skills/` and `opencode/.opencode/agents/` into the project's `.opencode/` directory. Merge the following MCP entry into the project's `opencode.json`, replacing the server path and preserving existing settings:

```json
{
  "mcp": {
    "een_pod_reader": {
      "type": "local",
      "command": ["python", "/absolute/path/to/een-pod-suite/chatgpt/een-pod-suite/scripts/reader_mcp.py"],
      "enabled": true
    }
  }
}
```

Then invoke the `een-pod-auditor` agent with the reference and, preferably, its direct official URL. API operations need EEN_API_KEY inherited securely by the server process. Restrict the host's additional tools according to your organisation's policy; server tools themselves expose no write operations.

## Remote MCP connection for ChatGPT

ChatGPT cannot connect to a local stdio process solely by installing a skill ZIP. Host the same server on an authorised runtime with a working route to EEN, then connect its HTTPS MCP endpoint using the host's supported authentication flow.

```bash
python chatgpt/een-pod-suite/scripts/reader_mcp.py --http --host 127.0.0.1 --port 8080
```

HTTP mode requires a secret `EEN_AGENT_TOKEN` and accepts `Authorization: Bearer <token>`. It supports stateless Streamable HTTP POST requests at `/mcp`; it does not provide OAuth discovery, OAuth login or an SSE stream. Put it behind an HTTPS gateway, and use gateway OAuth when the host requires OAuth. Keep the backend private; supply credentials through a secret manager. If accessing the Partner Web Service, the runtime's outbound IP must be whitelisted by EEN.

This repository does not provision hosting, whitelist an IP, configure OAuth or install a ChatGPT connector. A deployment and a verified connection are required before claiming remote availability. Installation of the updated skill supplies the agent instructions and code, not a live endpoint.

## Example task

> Use the EEN POD Reader & Audit Agent to retrieve and audit BOAL20261006010 at https://een.ec.europa.eu/partnering-opportunities/albanian-tour-operator-and-dmc-seeking-international-partnerships. Verify the exact reference, identify the source and visibility, and assess only retrieved content against PPQG v1.2.

The example preserves a user-supplied target; it is not a claim that this environment successfully retrieved the live page.

## Verification

```bash
python -m unittest discover -s tests -v
python scripts/build.py
```

Transport and tool tests exercise initialization, discovery, parameter validation, error redaction, mocked retrieval and local form checks. Live EEN access must be verified in the deployment environment before operational use.
