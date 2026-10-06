import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('pod', ROOT/'chatgpt/een-pod-suite/scripts/pod_reference.py')
pod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pod)
REF = 'BOAL20261006010'
URL = pod.BASE + '/partnering-opportunities/example-profile'


def page(html):
    p = pod.PublicPage()
    p.feed(html)
    return p


class LookupTests(unittest.TestCase):
    def test_markup_separated_reference_is_verified(self):
        p = page('<title>Example</title><div>POD Reference</div><div>'+REF+'</div><h2>Summary</h2><p>Visible text.</p>')
        result = pod.verify_profile(REF, URL, p)
        self.assertEqual(result['status'], 'FOUND EXACT')
        self.assertIn('Visible text.', result['public_text'])

    def test_search_snippet_and_script_do_not_verify_identity(self):
        for html in ['<p>'+REF+'</p>', '<script>POD Reference '+REF+'</script>']:
            self.assertEqual(pod.verify_profile(REF, URL, page(html))['status'], 'UNRESOLVED')

    def test_mismatch_is_not_audited(self):
        self.assertEqual(pod.verify_profile(REF, URL, page('<p>POD Reference BOAL20261006011</p>'))['status'], 'REFERENCE MISMATCH')

    def test_direct_url_avoids_search_and_indexing(self):
        with patch.object(pod,'read_page',return_value=(URL,page('<p>POD Reference '+REF+'</p>'))) as read:
            self.assertEqual(pod.lookup(REF,URL)['status'], 'FOUND EXACT')
            read.assert_called_once_with(URL)

    def test_403_is_access_failure_not_absence(self):
        with patch.object(pod,'read_page',side_effect=HTTPError(URL,403,'Forbidden',{},None)):
            result=pod.lookup(REF)
            self.assertEqual(result['status'], 'ACCESS BLOCKED')
            self.assertEqual(result['attempts'][0]['http_status'],403)
            self.assertNotIn('NOT FOUND', str(result))

    def test_network_failure_is_distinct(self):
        with patch.object(pod,'read_page',side_effect=URLError('Proxy unavailable')):
            self.assertEqual(pod.lookup(REF)['status'], 'NETWORK ERROR')

    def test_empty_search_does_not_establish_unpublished_status(self):
        with patch.object(pod,'read_page',return_value=(pod.build_url(REF),page('<p>No results</p>'))):
            self.assertEqual(pod.lookup(REF)['status'], 'UNRESOLVED')

    def test_discovered_href_is_used_not_guessed(self):
        search = page('<article><p>'+REF+'</p><a href="/partnering-opportunities/example-profile">Details</a></article>')
        detail = page('<p>POD Reference '+REF+'</p>')
        with patch.object(pod,'read_page',side_effect=[(pod.build_url(REF),search),(URL,detail)]) as read:
            self.assertEqual(pod.lookup(REF)['status'], 'FOUND EXACT')
            self.assertEqual(read.call_args_list[1].args,(URL,))

    def test_external_or_credential_urls_are_rejected(self):
        for url in ['http://een.ec.europa.eu/partnering-opportunities/x','https://example.com/partnering-opportunities/x','https://user:pass@een.ec.europa.eu/partnering-opportunities/x']:
            with self.assertRaises(ValueError): pod.lookup(REF,url)

    def test_enquiry_page_is_not_profile(self):
        with self.assertRaises(ValueError): pod.lookup(REF,pod.BASE+'/partnering-opportunities/partnership-contact?guid=example')

    def test_copies_match(self):
        expected=(ROOT/'chatgpt/een-pod-suite/scripts/pod_reference.py').read_bytes()
        for p in ROOT.glob('opencode/**/pod_reference.py'):
            self.assertEqual(p.read_bytes(),expected)


if __name__=='__main__': unittest.main()
