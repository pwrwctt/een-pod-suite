#!/usr/bin/env python3
"""Build portable release archives using the Python standard library."""
from pathlib import Path
import json
import re
import zipfile
import yaml
import hashlib
from sync_claude import validate_claude

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / 'VERSION').read_text().strip()


def validate_skill(path):
    text = (path / 'SKILL.md').read_text()
    if not text.startswith('---\n') or len(text.split('---', 2)) != 3:
        raise ValueError(f'Missing skill front matter: {path}')
    front = text.split('---', 2)[1]
    try:
        metadata = yaml.safe_load(front)
    except yaml.YAMLError as exc:
        raise ValueError(f'Invalid YAML: {path}') from exc
    if not isinstance(metadata, dict):
        raise ValueError(f'Front matter must be a mapping: {path}')
    for key in ('name', 'description'):
        if not isinstance(metadata.get(key), str) or not metadata[key].strip():
            raise ValueError(f'Missing {key}: {path}')
    name = metadata['name']
    if name != path.name or len(name) > 64 or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise ValueError(f'Invalid skill name: {path}')
    limit = 200 if 'claude' in path.parts else 1024
    if len(metadata['description']) > limit:
        raise ValueError(f'Description too long: {path}')
    if 'compatibility' in metadata and not isinstance(metadata['compatibility'], str):
        raise ValueError(f'Invalid compatibility: {path}')
    if f'v{VERSION}' not in (path / 'references/version.md').read_text():
        raise ValueError(f'Version mismatch: {path}')
    for document in path.rglob('*.md'):
        for ref in re.findall(r'`((?:references|scripts)/[^`\s]+)`', document.read_text()):
            if not (path / ref).is_file():
                raise ValueError(f'Missing referenced file: {path / ref} in {document}')
    agent = path / 'agents/openai.yaml'
    if agent.exists():
        config = yaml.safe_load(agent.read_text())
        if not isinstance(config, dict) or not isinstance(config.get('interface'), dict):
            raise ValueError(f'Invalid OpenAI metadata: {agent}')


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
    if (ROOT / 'shared/references/form-schema.md').read_bytes() != (chat / 'references/form-schema.md').read_bytes():
        raise ValueError('Shared operational schema is stale')
    if (ROOT / 'shared/scripts/form_readiness.py').read_bytes() != (chat / 'scripts/form_readiness.py').read_bytes():
        raise ValueError('Shared form helper is stale')
    manifest = json.loads((ROOT / 'opencode/manifest.json').read_text())
    modules = ROOT / 'opencode/.opencode/skills'
    if manifest['version'] != VERSION or set(manifest['skills']) != {p.name for p in modules.iterdir() if p.is_dir()}:
        raise ValueError('Manifest version or module list mismatch')
    for name in manifest['skills']:
        validate_skill(modules / name)
    canonical = chat
    provenance = json.loads((chat / 'references/source-manifest.json').read_text())
    for source in provenance['sources']:
        bundled = chat / 'references' / source['file']
        if hashlib.sha256(bundled.read_bytes()).hexdigest() != source['sha256']:
            raise ValueError(f'Source manifest mismatch: {bundled}')
    for folder in ('references', 'scripts'):
        expected = [p for p in (canonical / folder).iterdir() if p.is_file() and p.suffix in ('.md', '.py', '.csv', '.json')]
        for module in modules.iterdir():
            if module.is_dir():
                for original in expected:
                    target = module / folder / original.name
                    if not target.is_file() or target.read_bytes() != original.read_bytes():
                        raise ValueError(f'Missing/stale OpenCode common resource: {target}')
        for copy in modules.glob(f'*/{folder}/*'):
            original = canonical / folder / copy.name
            if copy.is_file() and original.is_file() and copy.read_bytes() != original.read_bytes():
                raise ValueError(f'OpenCode shared content is stale: {copy}')
    archive(chat, ROOT / 'dist/chatgpt/skill.zip', 'een-pod-suite/')
    archive(claude, ROOT / f'dist/claude/een-pod-suite-claude-v{VERSION}.zip', 'een-pod-suite/')
    archive(ROOT / 'opencode', ROOT / f'dist/opencode/een-pod-suite-opencode-v{VERSION}.zip')


if __name__ == '__main__':
    main()
