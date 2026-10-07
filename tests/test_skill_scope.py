from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
class SkillScopeTests(unittest.TestCase):
    def test_active_skill_has_no_restricted_service_integration(self):
        banned=re.compile(r'Partner\s+Web\s*Services?|EEN_API_KEY|een_b2b_api|een-pod-api|get_live_labels|\bAPI\b',re.I)
        for directory in ('chatgpt','opencode','shared'):
            for p in (ROOT/directory).rglob('*'):
                if not p.is_file() or '__pycache__' in p.parts:continue
                self.assertNotIn(p.name,{'een_b2b_api.py','partner-webservice.md','api-security.md','api-quality-review.md','taxonomy-api.md'})
                if p.suffix in ('.md','.py','.yaml','.json'):
                    self.assertIsNone(banned.search(p.read_text()),str(p))
        self.assertFalse((ROOT/'opencode/.opencode/skills/een-pod-api').exists())
if __name__=='__main__':unittest.main()
