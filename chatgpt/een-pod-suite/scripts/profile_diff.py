#!/usr/bin/env python3
"""Compare supplied profile versions without inferring issue resolution."""
import argparse
import difflib
import json
from pathlib import Path


def compare(before, after):
    changes = []
    for field in sorted(set(before) | set(after)):
        old, new = before.get(field), after.get(field)
        if old == new:
            continue
        old_text = json.dumps(old, ensure_ascii=False) if not isinstance(old, str) else old
        new_text = json.dumps(new, ensure_ascii=False) if not isinstance(new, str) else new
        changes.append({'field': field, 'before': old, 'after': new,
                        'diff': list(difflib.unified_diff(old_text.splitlines(), new_text.splitlines(), lineterm='')),
                        'review': 'Verify new claims against supplied evidence; rerun affected checks'})
    return {'changes': changes, 'issue_resolution': 'Requires reviewer evidence; textual changes alone do not close issues.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before'); parser.add_argument('after')
    args = parser.parse_args()
    print(json.dumps(compare(json.loads(Path(args.before).read_text()), json.loads(Path(args.after).read_text())), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
