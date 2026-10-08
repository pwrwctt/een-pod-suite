#!/usr/bin/env python3
"""Generate the Claude distribution from the canonical unified skill."""
from pathlib import Path
import re
import shutil
import json

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTION = ('Prepare and audit EEN partnering profiles: eligibility, drafting, taxonomy, '
               'field limits and quality review. Audit only an operator-supplied exact profile URL or supplied text.')
RUNTIME = '''
## Claude execution

Use this skill in Claude when preparing or reviewing EEN partnering profiles.
Resolve references and scripts relative to this installed skill directory.
Use available browsing, code execution or explicitly connected read-only MCP tools
to read only the operator-supplied official detail URL. Run the bundled Python
helpers only when code execution is available. Network access depends on the
Claude environment; installing this skill does not enable browsing or connect MCP.
If reading is unavailable or fails, request the same profile's text/HTML export
and state which content could not be verified. Never substitute another profile.
'''


def expected_files():
    source = ROOT / 'chatgpt/een-pod-suite'
    files = {}
    for path in sorted(source.rglob('*')):
        relative = path.relative_to(source)
        if (not path.is_file() or relative.parts[0] == 'agents'
                or '__pycache__' in relative.parts or path.suffix == '.pyc'):
            continue
        data = path.read_bytes()
        if relative.as_posix() == 'SKILL.md':
            content = re.sub(r'^description:.*$', lambda _: 'description: ' + json.dumps(DESCRIPTION),
                             data.decode(), count=1, flags=re.MULTILINE)
            content = content.replace('## Route the task', RUNTIME + '\n## Route the task', 1)
            data = content.encode()
        files[relative.as_posix()] = data
    return files


def validate_claude():
    target = ROOT / 'claude/een-pod-suite'
    expected = expected_files()
    actual = {p.relative_to(target).as_posix(): p.read_bytes()
              for p in target.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}
    if expected != actual:
        raise ValueError('Claude distribution is stale; run python scripts/sync_claude.py')
    if len(DESCRIPTION) > 200:
        raise ValueError('Claude skill description exceeds 200 characters')


def main():
    target = ROOT / 'claude/een-pod-suite'
    if target.exists():
        shutil.rmtree(target)
    for relative, data in expected_files().items():
        path = target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    validate_claude()
    print('Claude distribution synchronised from the canonical unified skill.')


if __name__ == '__main__':
    main()
