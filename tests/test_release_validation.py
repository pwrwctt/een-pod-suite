import sys
from pathlib import Path
import tempfile
import unittest
import yaml

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import build


class ReleaseTests(unittest.TestCase):
    def test_real_frontmatter_and_links_for_every_distribution(self):
        paths=[ROOT/'chatgpt/een-pod-suite',ROOT/'claude/een-pod-suite']
        paths+=list((ROOT/'opencode/.opencode/skills').iterdir())
        for path in paths:
            if path.is_dir():build.validate_skill(path)

    def test_invalid_yaml_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'een-pod-suite';path.mkdir()
            (path/'SKILL.md').write_text('---\nname: een-pod-suite\ndescription: Profiles: eligibility\n---\n')
            with self.assertRaisesRegex(ValueError,'Invalid YAML'):build.validate_skill(path)

    def test_missing_nested_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'een-pod-suite';path.mkdir();(path/'references').mkdir()
            (path/'SKILL.md').write_text('---\nname: een-pod-suite\ndescription: valid\n---\n')
            (path/'references/version.md').write_text('v'+build.VERSION)
            (path/'references/nested.md').write_text('Run `scripts/missing.py`.')
            with self.assertRaisesRegex(ValueError,'Missing referenced file'):build.validate_skill(path)

    def test_claude_zip_frontmatter_parses(self):
        # Source check here; release procedure also verifies the produced archives.
        data=yaml.safe_load((ROOT/'claude/een-pod-suite/SKILL.md').read_text().split('---',2)[1])
        self.assertIsInstance(data['description'],str)
        self.assertLessEqual(len(data['description']),200)
