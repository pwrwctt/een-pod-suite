# EEN POD Suite for Claude — v2.6

This unified skill supports eligibility checks, BO/BR/TO/TR/RDR classification,
drafting, title and summary revision, bundled taxonomy selection, deterministic
field-limit checks and independent quality review against PPQG v1.2.

## Install in Claude

1. Download `dist/claude/een-pod-suite-claude-v2.6.zip` from this repository.
2. Enable Code execution and file creation in your Claude settings. Your
   organisation may also need to enable skills.
3. Open Customize → Skills → + Create skill → Upload a skill.
4. Upload the ZIP without repackaging it, then enable EEN POD Suite.
5. Ask: “Which version of EEN POD Suite is installed?” Expect v2.6.

The ZIP contains `een-pod-suite/SKILL.md` and its `references/` and `scripts/`
directories. It omits OpenAI-specific agent metadata. Its short description is
within Claude's documented 200-character limit.

## Install in Claude Code

Copy the complete `claude/een-pod-suite/` folder to either:

- `.claude/skills/een-pod-suite/` in your project; or
- `~/.claude/skills/een-pod-suite/` for personal use.

Preserve the references and scripts. Use `/een-pod-suite` to invoke it, or ask
Claude to use EEN POD Suite when preparing or reviewing a partnering profile.

## Usage and verification

- Drafting: “Use EEN POD Suite to assess these client notes, identify missing
  facts, draft the appropriate profile and independently review it.”
- Audit: “Use EEN POD Suite to audit this exact official EEN profile detail URL:
  [paste URL]. Verify the displayed POD Reference and cite retrieved evidence.”
- Text review: “Review this supplied profile text using EEN POD Suite. Clearly
  state that its publication identity has not been independently verified.”
- Number-only request: the skill must request the exact detail URL.
- Failed retrieval: request the same profile's text/HTML export; do not search
  for or substitute a different profile.

Code execution, browsing, network permissions and any connected MCP tools depend
on the Claude environment. This ZIP does not activate a connector or guarantee
public-page access. Taxonomy recommendations use the bundled 2024 snapshot.

## Maintenance

Do not hand-edit the generated `claude/een-pod-suite/` directory. Edit the
canonical `chatgpt/een-pod-suite/` content or the Claude adaptation in
`scripts/sync_claude.py`, then run that generator. Every release must also update
and validate ChatGPT and OpenCode. See `AGENTS.md` and the root README.

Packaging and automated checks have been completed. Installation and live
retrieval inside Claude have not been tested in this workspace.

Official guidance:

- [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [Creating custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
