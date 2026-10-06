import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('url_reader',ROOT/'chatgpt/een-pod-suite/scripts/profile_url.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
URL='https://een.ec.europa.eu/partnering-opportunities/example-profile'
REF='BOAL20261006010'

class UrlTests(unittest.TestCase):
    def test_detail_url_is_the_only_requested_page(self):
        page=m.PublicPage();page.feed('<div>POD Reference</div><div>'+REF+'</div><p>Public content</p>')
        with patch.object(m,'read_page',return_value=(URL,page)) as read:
            result=m.read_profile(URL)
            self.assertEqual(result['reference'],REF)
            self.assertEqual(result['status'],'FOUND EXACT')
            read.assert_called_once_with(URL)
    def test_number_name_and_search_page_are_rejected(self):
        for value in [REF,'Tour operator','https://een.ec.europa.eu/partnering-opportunities?f%5B0%5D=k%3A'+REF]:
            with self.assertRaises(ValueError):m.read_profile(value)
    def test_expected_reference_only_checks_detail_identity(self):
        page=m.PublicPage();page.feed('<p>POD Reference '+REF+'</p>')
        with patch.object(m,'read_page',return_value=(URL,page)) as read:
            self.assertEqual(m.read_profile(URL,'BOAL20261006011')['status'],'REFERENCE MISMATCH')
            read.assert_called_once_with(URL)
    def test_access_failure_does_not_trigger_search(self):
        with patch.object(m,'read_page',side_effect=HTTPError(URL,403,'Forbidden',{},None)) as read:
            self.assertEqual(m.read_profile(URL)['status'],'ACCESS BLOCKED')
            read.assert_called_once_with(URL)
    def test_search_helpers_removed_from_distribution(self):
        self.assertFalse(hasattr(m,'build_url'))
        self.assertFalse(hasattr(m,'lookup'))
        self.assertFalse(list(ROOT.glob('chatgpt/**/pod_reference.py')))
        self.assertFalse(list(ROOT.glob('opencode/**/pod_reference.py')))
    def test_copies_match(self):
        expected=(ROOT/'chatgpt/een-pod-suite/scripts/profile_url.py').read_bytes()
        for p in ROOT.glob('opencode/**/profile_url.py'):self.assertEqual(p.read_bytes(),expected)
if __name__=='__main__':unittest.main()
