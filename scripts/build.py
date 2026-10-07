#!/usr/bin/env python3
"""Build portable release archives using the Python standard library."""
from pathlib import Path
import json
import re
import zipfile
from sync_claude import validate_claude

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / 'VERSION').read_text().strip()


def validate_skill(path):
    text = (path / 'SKILL.md').read_text()
    if not text.startswith('---\n') or len(text.split('---', 2)) != 3:
        raise ValueError(f'Missing skill front matter: {path}')
    front = text.split('---', 2)[1]
    for key in ('name', 'description'):
        if not re.search(rf'^{key}:\s*\S', front, re.MULTILINE):
            raise ValueError(f'Missing {key}: {path}')
    if f'v{VERSION}' not in (path / 'references/version.md').read_text():
        raise ValueError(f'Version mismatch: {path}')
    for ref in re.findall(r'`((?:references|scripts)/[^`\s]+)`', text):
        if not (path / ref).is_file():
            raise ValueError(f'Missing referenced file: {path / ref}')


def archive(source, output, prefix=''):
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as z:
        for path in sorted(source.rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
                z.write(path, prefix + path.relative_to(source).as_posix())
    print(output)


def main():
    chat = ROOT / 'chatgpt/een-pod-suite'
    validate_skill(chat)
    claude = ROOT / 'claude/een-pod-suite'
    validate_claude()
    validate_skill(claude)
    manifest = json.loads((ROOT / 'opencode/manifest.json').read_text())
    modules = ROOT / 'opencode/.opencode/skills'
    if manifest['version'] != VERSION or set(manifest['skills']) != {p.name for p in modules.iterdir() if p.is_dir()}:
        raise ValueError('Manifest version or module list mismatch')
    for name in manifest['skills']:
        validate_skill(modules / name)
    archive(chat, ROOT / 'dist/chatgpt/skill.zip', 'een-pod-suite/')
    archive(claude, ROOT / f'dist/claude/een-pod-suite-claude-v{VERSION}.zip', 'een-pod-suite/')
    archive(ROOT / 'opencode', ROOT / f'dist/opencode/een-pod-suite-opencode-v{VERSION}.zip')


if __name__ == '__main__':
    main()
