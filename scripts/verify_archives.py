#!/usr/bin/env python3
"""Verify every release ZIP member against its source distribution."""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def verify():
    version = (ROOT / 'VERSION').read_text().strip()
    targets = [
        (ROOT/'chatgpt/een-pod-suite', ROOT/'dist/chatgpt/skill.zip', 'een-pod-suite/'),
        (ROOT/'claude/een-pod-suite', ROOT/f'dist/claude/een-pod-suite-claude-v{version}.zip', 'een-pod-suite/'),
        (ROOT/'opencode', ROOT/f'dist/opencode/een-pod-suite-opencode-v{version}.zip', ''),
    ]
    for source, archive, prefix in targets:
        expected = {prefix + path.relative_to(source).as_posix(): path
                    for path in source.rglob('*') if path.is_file()
                    and '__pycache__' not in path.parts and path.suffix != '.pyc'}
        with zipfile.ZipFile(archive) as package:
            names = package.namelist()
            if len(names) != len(set(names)) or set(names) != set(expected):
                raise ValueError(f'Member inventory mismatch: {archive}')
            if package.testzip() is not None:
                raise ValueError(f'Corrupt ZIP: {archive}')
            for name, path in expected.items():
                if package.read(name) != path.read_bytes():
                    raise ValueError(f'Content mismatch: {archive}: {name}')
        print(f'Verified {archive.relative_to(ROOT)}: {len(expected)} files')


if __name__ == '__main__':
    verify()
