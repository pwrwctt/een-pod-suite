#!/usr/bin/env python3
"""Synchronise common resources into all specialised OpenCode modules."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = ROOT / 'chatgpt/een-pod-suite'
    for module in (ROOT / 'opencode/.opencode/skills').iterdir():
        if not module.is_dir():
            continue
        for folder, suffixes in [('references', {'.md', '.csv', '.json'}), ('scripts', {'.py'})]:
            for path in (source / folder).iterdir():
                if path.is_file() and path.suffix in suffixes:
                    target = module / folder / path.name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(path.read_bytes())
    print('OpenCode common resources synchronised.')


if __name__ == '__main__':
    main()
