import csv
from datetime import date
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'chatgpt/een-pod-suite/scripts'
def load(name):
    spec=importlib.util.spec_from_file_location(name,SCRIPTS/(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
checks=load('profile_checks');lookup=load('taxonomy_lookup');diff=load('profile_diff')


class ReviewTests(unittest.TestCase):
    def test_empty_and_partial_profiles_never_ready(self):
        for kind in checks.SPECIFIC:
            for scope in ('draft','public'):
                result=checks.review({'profile_type':kind,'scope':scope,'fields':{}})
                self.assertNotIn(result['verdict'],('READY','READY AFTER MINOR EDITS'))
                if scope=='public':self.assertFalse(result['issues'])

    def test_major_and_review_gates(self):
        self.assertEqual(checks.verdict([{'severity':'MAJOR'}],True,True,True),'RETURN FOR REVISION')
        self.assertEqual(checks.verdict([],True,True,False),'REVIEW LIMITED')
        self.assertEqual(checks.verdict([{'severity':'MINOR'}],True,True,True),'READY AFTER MINOR EDITS')

    def test_dates_expired_inverted_and_valid(self):
        now=date(2026,10,8)
        result=checks.date_checks({'eoi_deadline':'2026-11-10','call_deadline':'2026-11-01'},now)
        self.assertEqual(result['ordering'],'INVALID')
        result=checks.date_checks({'eoi_deadline':'2026-09-01','call_deadline':'2026-12-01'},now)
        self.assertEqual(result['eoi_deadline'],'EXPIRED')
        self.assertIn('UNVERIFIED',checks.date_checks({},now)['call_deadline'])

    def test_taxonomy_duplicates_unknown_labels_and_counts(self):
        result=checks.verify_taxonomy('market',['01003','01003',{'code':'01003','label':'invented'},'FAKE'])
        self.assertEqual(result['entries'][1]['status'],'DUPLICATE')
        self.assertEqual(result['entries'][3]['status'],'UNKNOWN OR NONSELECTABLE CODE')
        self.assertEqual(checks.verify_taxonomy('market',[{'code':'01003','label':'invented'}])['entries'][0]['status'],'CODE-LABEL MISMATCH')
        self.assertEqual(checks.verify_taxonomy('market',['01003']*6)['count_status'],'OVER LIMIT')

    def test_boolean_claims_cannot_be_truthy_strings(self):
        with self.assertRaises(ValueError):checks.review({'profile_type':'BO','independent_review':'false'})

    def test_own_country_is_reported(self):
        result=checks.review({'profile_type':'BO','fields':{'country':'Poland','target_countries':['Poland']}})
        self.assertTrue(any(item['field']=='target_countries' for item in result['issues']))

    def test_diff_does_not_claim_issue_resolution(self):
        result=diff.compare({'summary':'Original claim'},{'summary':'New claim'})
        self.assertEqual(result['changes'][0]['before'],'Original claim')
        self.assertIn('Requires reviewer evidence',result['issue_resolution'])

    def test_all_five_golden_profile_types(self):
        for case in json.loads((ROOT/'tests/fixtures/review-cases.json').read_text()):
            result=checks.review(case['input'],date(2026,10,8))
            self.assertEqual(result['verdict'],case['expected_verdict'],case['id'])
    def test_confirmed_long_title_blocks_otherwise_confirmed_profile(self):
        case=json.loads((ROOT/'tests/fixtures/review-cases.json').read_text())[0]['input']
        case['fields']['title']='x'*257
        self.assertEqual(checks.review(case)['verdict'],'RETURN FOR REVISION')


class SemanticTests(unittest.TestCase):
    def test_exact_code_and_leading_zeros(self):
        self.assertEqual(lookup.search('market','01003')[0]['code'],'01003')

    def test_bilingual_concepts_improve_over_lexical(self):
        for query,kind,expected in [('oczyszczanie ścieków','technology','10004003'),('sztuczna inteligencja','technology','01003003'),('energia wiatrowa','market','06003003')]:
            candidates=lookup.search(kind,query,limit=10)
            self.assertIn(expected,[x['code'] for x in candidates],query)
            self.assertFalse(lookup.search(kind,query,mode='lexical'),query)
            self.assertTrue(any(isinstance(reason,dict) for x in candidates for reason in x['reasons']))
        self.assertIn(lookup.search('technology','oczyszczanie ścieków')[0]['code'],('10004001','10004002'))

    def test_unknown_concept_is_not_fabricated(self):
        self.assertEqual(lookup.search('technology','qxzv9999'),[])

    def test_all_semantic_results_exist_in_snapshot(self):
        with (checks.BASE/'taxonomy-technology-selectable.csv').open(encoding='utf-8-sig') as stream:
            rows=list(csv.DictReader(stream))
        codes={r['Code'] for r in rows}
        for query in ('sewage','ai','recycling','medical device'):
            self.assertTrue(all(item['code'] in codes for item in lookup.search('technology',query)))
