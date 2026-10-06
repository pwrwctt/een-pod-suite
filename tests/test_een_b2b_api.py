import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('api', ROOT / 'shared/scripts/een_b2b_api.py')
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)


class ApiTests(unittest.TestCase):
    def test_visibility_does_not_confuse_missing_or_blank_fields_with_access(self):
        self.assertEqual(api.profile_visibility({}), 'UNKNOWN')
        core = dict.fromkeys(['title', 'shortSummary', 'description', 'expectedRoleOfThePartner'])
        self.assertEqual(api.profile_visibility(core), 'LIMITED')
        self.assertEqual(api.profile_visibility(dict.fromkeys(core, ' N/A ')), 'LIMITED')
        self.assertEqual(api.profile_visibility(dict.fromkeys(core, ' ')), 'UNKNOWN')
        self.assertEqual(api.profile_visibility({**core, 'title': 'Available profile'}), 'FULL')

    def test_profile_filters_and_bounds(self):
        params = api.build_profiles_params(profile_types=['bo','tr'], statuses=['published'])
        self.assertEqual([v for k,v in params if k == 'ProfileTypes'], ['BO','TR'])
        self.assertNotIn('reference', dict(params))
        for kw in [{'page_index':0},{'page_size':201},{'profile_types':['XX']},{'statuses':['XX']}]:
            with self.assertRaises(ValueError): api.build_profiles_params(**kw)

    def test_profile_pagination_and_exact_reference(self):
        pages = [
            {'data': {'items':[{'reference':'BO1234-extra'}], 'pagingInfo':{'hasNext':True}}},
            {'data': {'items':[{'reference':'BO1234'}], 'pagingInfo':{'hasNext':False}}},
        ]
        with patch.object(api, 'fetch_profiles_page', side_effect=pages) as fetch:
            self.assertEqual(api.find_profile_by_reference(' bo1234 ')['reference'], 'BO1234')
            self.assertEqual([c.kwargs['page_index'] for c in fetch.call_args_list], [1,2])

    def test_label_pagination_and_active_filter(self):
        pages = [
            {'items':[{'isActive':True,'uuid':'a'},{'isActive':False,'uuid':'b'}], 'pagingInfo':{'currentPage':0,'totalPages':2}},
            {'items':[{'isActive':'True','uuid':'c'}], 'pagingInfo':{'currentPage':1,'totalPages':2}},
        ]
        with patch.object(api, 'fetch_labels_page', side_effect=pages) as fetch:
            self.assertEqual([x['uuid'] for x in api.iter_labels(data_type='market_keyword', active_only=True)], ['a','c'])
            self.assertEqual([c.kwargs['page'] for c in fetch.call_args_list], [0,1])

    def test_auth_denial_does_not_expose_key(self):
        with patch.dict(api.os.environ, {'EEN_API_KEY':'test-secret'}), patch.object(api, 'urlopen', side_effect=HTTPError('https://example.com',403,'Forbidden',{},None)):
            with self.assertRaises(api.EenApiError) as ctx: api.fetch_profiles_page()
            self.assertIn('whitelisting', str(ctx.exception))
            self.assertNotIn('test-secret', str(ctx.exception))

    def test_invalid_json(self):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = b'invalid json'
        with patch.dict(api.os.environ, {'EEN_API_KEY':'test-secret'}), patch.object(api,'urlopen',return_value=response):
            with self.assertRaisesRegex(api.EenApiError,'invalid JSON'): api.fetch_profiles_page()

    def test_distributed_helpers_match(self):
        expected = (ROOT / 'shared/scripts/een_b2b_api.py').read_bytes()
        paths = list(ROOT.glob('chatgpt/**/een_b2b_api.py')) + list(ROOT.glob('opencode/**/een_b2b_api.py'))
        self.assertEqual(len(paths), 5)
        for path in paths:
            self.assertEqual(path.read_bytes(), expected)


if __name__ == '__main__': unittest.main()
