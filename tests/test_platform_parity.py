"""Guard generated Claude content and cross-platform release versions."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('sync_claude', ROOT / 'scripts/sync_claude.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class PlatformParityTests(unittest.TestCase):
    def test_claude_matches_canonical_skill(self):
        sync.validate_claude()
        self.assertFalse((ROOT / 'claude/een-pod-suite/agents/openai.yaml').exists())

    def test_all_platform_versions_match(self):
        version = (ROOT / 'VERSION').read_text().strip()
        manifest = json.loads((ROOT / 'opencode/manifest.json').read_text())
        self.assertEqual(manifest['version'], version)
        paths = [ROOT / 'chatgpt/een-pod-suite', ROOT / 'claude/een-pod-suite']
        paths += [ROOT / 'opencode/.opencode/skills' / name for name in manifest['skills']]
        for path in paths:
            self.assertIn(f'v{version}', (path / 'references/version.md').read_text(), str(path))

    def test_canonical_changes_require_claude_update(self):
        from unittest.mock import patch
        changed = dict(sync.expected_files())
        changed['references/new-guidance.md'] = b'New mandatory guidance'
        with patch.object(sync, 'expected_files', return_value=changed):
            with self.assertRaisesRegex(ValueError, 'stale'):
                sync.validate_claude()


if __name__ == '__main__':
    unittest.main()
