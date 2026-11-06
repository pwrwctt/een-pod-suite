import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'chatgpt/een-pod-suite/scripts/bo_quality_score.py'
spec = importlib.util.spec_from_file_location('bo_quality_score', SOURCE)
bo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bo)


def padded(prefix, length):
    return (prefix + ' Evidence of the agreed cooperation is documented.' * 100)[:length]


def example():
    return {'profile_type': 'BO', 'profile_status': 'PUBLISHED',
            'reference': 'SYNTHETIC-BO-FIXTURE', 'country': 'PL',
            'fields': {
                'title': 'Polish producer seeks a commercial agreement for equipment distribution',
                'summary': padded('A Polish manufacturer offers equipment through a commercial agreement. ', 300),
                'description': padded('Established in Poland, the Polish company seeks a commercial agreement. ', 1000),
                'advantages': padded('Tests show a documented 20 percent reduction in energy demand. ', 250),
                'partner_role': padded('The partner will operate under a commercial agreement and provide distribution. ', 350),
                'partnership_types': ['Commercial agreement']}}


class ScoreTests(unittest.TestCase):
    def score(self, profile=None, **kwargs):
        return bo.score_profile(example() if profile is None else profile, evaluated_on='2026-11-06', **kwargs)

    def test_all_twelve_criteria_and_maximum(self):
        result = self.score()
        self.assertEqual(result['score'], 8)
        self.assertEqual(result['band'], 'Excellent')
        self.assertEqual(len(result['criteria']), 12)
        self.assertTrue(result['scoring_complete'])
        self.assertEqual(result['sql_equivalence'].split(':')[0], 'NOT VERIFIED')

    def test_worst_case_minus_four(self):
        profile = example()
        profile['fields'] = {'title':'X'*50, 'summary':'X'*40,
            'description':'unique innovative best', 'advantages':'', 'partner_role':'we',
            'partnership_types':['Commercial agreement']}
        result = self.score(profile)
        self.assertEqual(result['score'], -4)
        self.assertEqual(result['band'], 'Poor')

    def test_every_band_boundary(self):
        for points, expected in [(-4,'Poor'),(1,'Poor'),(2,'Weak'),(3,'Weak'),(4,'Fair'),(5,'Fair'),(6,'Good'),(7,'Good'),(8,'Excellent')]:
            self.assertEqual(bo.band(points), expected)
        for value in (-5,9,True,2.5):
            with self.assertRaises(ValueError): bo.band(value)

    def test_scope_only_bo_published_and_test_exclusion(self):
        for kind in ('BR','TO','TR','RDR'):
            profile=example();profile['profile_type']=kind
            self.assertEqual(self.score(profile)['status'],'NOT APPLICABLE')
        for status in ('DRAFT','EXPIRED','ARCHIVED'):
            profile=example();profile['profile_status']=status
            self.assertEqual(self.score(profile)['status'],'NOT APPLICABLE')
        profile=example();profile['known_test_profile']=True
        self.assertEqual(self.score(profile)['status'],'EXCLUDED TEST PROFILE')
        profile=example();profile['fields']={key:'123' for key in bo.TEXT_FIELDS}
        self.assertEqual(self.score(profile)['status'],'EXCLUDED TEST PROFILE')

    def test_metadata_aliases_and_unverified_status(self):
        profile=example()
        profile['profiletype_code']=profile.pop('profile_type')
        profile['profilestatus_name']=profile.pop('profile_status')
        self.assertEqual(self.score(profile)['status'],'COMPLETE')
        profile.pop('profilestatus_name')
        result=self.score(profile)
        self.assertEqual(result['status'],'SCOPE UNVERIFIED')
        self.assertFalse(result['recommended_actions']['automatic_action'])
        self.assertNotEqual(result['recommended_actions']['status'],'DRAFT RECOMMENDATIONS ONLY')

    def test_simulation_has_no_operational_recommendations(self):
        profile=example();profile['profile_status']='DRAFT'
        result=self.score(profile,mode='simulation')
        self.assertEqual(result['score'],8)
        self.assertEqual(result['status'],'SIMULATION')
        self.assertFalse(result['scope']['published_scope_confirmed'])

    def test_missing_is_unknown_not_empty(self):
        result=self.score({'profile_type':'BO','profile_status':'PUBLISHED','fields':{}})
        self.assertIsNone(result['score'])
        self.assertEqual(result['score_range'],{'min':-4,'max':8})
        self.assertEqual(result['possible_bands'],['Poor','Weak','Fair','Good','Excellent'])
        profile=example();profile['fields'].pop('advantages')
        result=self.score(profile)
        self.assertEqual(result['criteria']['P6']['state'],'UNKNOWN')
        self.assertIsNone(result['criteria']['N1']['value'])
        profile['fields']['advantages']=''
        result=self.score(profile)
        self.assertEqual(result['criteria']['P6']['state'],'NOT MET')
        self.assertFalse(result['criteria']['N1']['value'])

    def test_public_nonvisibility_overrides_supplied_value(self):
        profile=example();profile['not_visible']=['advantages']
        self.assertEqual(self.score(profile)['criteria']['P6']['state'],'UNKNOWN')

    def test_title_length_boundaries(self):
        for size, expected in [(39,False),(40,True),(256,True),(257,False)]:
            profile=example();profile['fields']['title']=padded('A Polish commercial agreement ',size)
            self.assertIs(self.score(profile)['criteria']['P2']['value'],expected)

    def test_summary_length_boundaries(self):
        for size, expected in [(249,False),(250,True),(500,True),(501,False)]:
            profile=example();profile['fields']['summary']=padded('A Polish manufacturer seeks a commercial agreement. ',size)
            self.assertIs(self.score(profile)['criteria']['P3']['value'],expected)

    def test_description_advantages_and_partner_boundaries(self):
        for key, criterion, sizes, prefix in [
            ('description','P5',[(799,False),(800,True),(4000,True),(4001,False)],'A Polish company seeks a commercial agreement. '),
            ('advantages','P6',[(199,False),(200,True)],'A documented reduction of 20 percent. '),
            ('partner_role','P7',[(299,False),(300,True)],'The partner seeks a commercial agreement. ')]:
            for size, expected in sizes:
                profile=example();profile['fields'][key]=padded(prefix,size)
                self.assertIs(self.score(profile)['criteria'][criterion]['value'],expected)

    def test_all_caps_has_two_score_effects(self):
        profile=example();profile['fields']['title']=profile['fields']['title'].upper()
        result=self.score(profile)
        self.assertFalse(result['criteria']['P2']['value'])
        self.assertTrue(result['criteria']['N3']['value'])
        self.assertEqual(result['score'],6)

    def test_summary_copy_and_description_opening(self):
        profile=example()
        profile['fields']['title']=padded('A Polish commercial agreement. ',300)
        profile['fields']['summary']=profile['fields']['title']
        result=self.score(profile)
        self.assertFalse(result['criteria']['P3']['value'])
        self.assertTrue(result['criteria']['N4']['value'])
        profile=example();profile['fields']['description']=profile['fields']['summary']+padded(' Other details. ',700)
        self.assertFalse(self.score(profile)['criteria']['P3']['value'])

    def test_n4_is_raw_prefix_not_normalised(self):
        profile=example();profile['fields']['summary']=profile['fields']['title'][:40]+padded(' Additional facts. ',260)
        self.assertTrue(self.score(profile)['criteria']['N4']['value'])
        profile['fields']['summary']=profile['fields']['summary'].swapcase()
        self.assertFalse(self.score(profile)['criteria']['N4']['value'])

    def test_country_demonyms_and_unknown_dictionary(self):
        for origin, demonym in [('TR','Turkish'),('NL','Dutch'),('BE','Belgian'),('ES','Spanish')]:
            profile=example();profile['country']=origin
            profile['fields']['summary']=padded(demonym+' company seeks a commercial agreement. ',300)
            profile['fields']['description']=padded(demonym+' company proposes a commercial agreement. ',1000)
            self.assertTrue(self.score(profile)['criteria']['P4']['value'])
        profile=example();profile['country']='UNLISTED'
        self.assertIsNone(self.score(profile)['criteria']['P4']['value'])
        profile['country_terms']=['Polish']
        self.assertTrue(self.score(profile)['criteria']['P4']['value'])

    def test_meaningless_digits_still_pass_proxy_not_semantic_audit(self):
        profile=example();profile['fields']['advantages']='1'+(' text'*50)
        self.assertTrue(self.score(profile)['criteria']['P6']['value'])
        self.assertIn('SEPARATE',self.score(profile)['semantic_audit'])

    def test_p1_does_not_require_same_agreement_and_p8_checks_all(self):
        profile=example();profile['fields']['description']=padded('The Polish company seeks a supplier agreement. ',1000)
        result=self.score(profile)
        self.assertTrue(result['criteria']['P1']['value'])
        self.assertFalse(result['criteria']['P8']['value'])
        profile=example();profile['fields']['partnership_types'].append('Investment agreement')
        self.assertFalse(self.score(profile)['criteria']['P8']['value'])
        profile['fields']['partnership_types']=['An unknown label']
        self.assertIsNone(self.score(profile)['criteria']['P8']['value'])

    def test_pronoun_boundaries(self):
        profile=example()
        self.assertFalse(self.score(profile)['criteria']['N1']['value'])
        profile['fields']['advantages']+=' Business opportunities are described.'
        self.assertFalse(self.score(profile)['criteria']['N1']['value'])
        profile['fields']['advantages']+=' The US market is mentioned.'
        self.assertTrue(self.score(profile)['criteria']['N1']['value'])
        profile=example()
        profile['fields']['advantages']+=' We can document this.'
        self.assertTrue(self.score(profile)['criteria']['N1']['value'])

    def test_marketing_counts_distinct_terms_not_repetition(self):
        profile=example();profile['fields']['advantages']+=' unique unique unique'
        self.assertFalse(self.score(profile)['criteria']['N2']['value'])
        profile['fields']['advantages']+=' innovative best'
        self.assertTrue(self.score(profile)['criteria']['N2']['value'])

    def test_all_action_bands_are_drafts_and_never_sent(self):
        for quality in ('Poor','Weak','Fair','Good','Excellent'):
            result=bo.actions({'status':'COMPLETE','band':quality})
            text=' '.join(result['steps'])
            self.assertFalse(result['automatic_action'])
            self.assertEqual('Guidelines Compliance' in text,quality=='Poor')
            self.assertEqual('owner notification' in text,quality in ('Weak','Fair','Good'))
            self.assertEqual('Quality Clinic' in text,quality in ('Poor','Weak'))

    def test_two_calendar_months_and_month_end(self):
        self.assertEqual(bo.add_months(bo.date(2026,12,31)).isoformat(),'2027-02-28')
        self.assertEqual(self.score()['recheck_due'],'2027-01-06')

    def test_comparison_identity_model_and_evidence(self):
        before=self.score()
        profile=example();profile['fields']['title']=profile['fields']['title'].upper()
        after=self.score(profile)
        comparison=bo.compare_runs(before,after)
        self.assertEqual(comparison['score_delta'],-2)
        self.assertEqual(len(comparison['criterion_changes']),2)
        self.assertFalse(comparison['at_or_after_due'])
        after['model_sha256']='changed'
        with self.assertRaises(ValueError):bo.compare_runs(before,after)
        rescored=bo.rescore_and_compare(before,after)
        self.assertEqual(rescored['score_delta'],-2)
        self.assertTrue(rescored['rescored_with_current_model'])
        after=self.score();after['identity']['reference']='ANOTHER'
        with self.assertRaises(ValueError):bo.compare_runs(before,after)

    def test_invalid_inputs_and_no_mutation(self):
        profile=example()
        original=json.loads(json.dumps(profile))
        self.score(profile)
        self.assertEqual(profile,original)
        for key,value in [('title',123),('partnership_types','Commercial agreement')]:
            bad=example();bad['fields'][key]=value
            with self.assertRaises(ValueError):self.score(bad)
        bad=example();bad['known_test_profile']='false'
        with self.assertRaises(ValueError):self.score(bad)

    def test_cli_and_packaged_copies(self):
        completed=subprocess.run([sys.executable,str(SOURCE),'score',str(ROOT/'docs/examples/bo-scoring-input.json'),'--mode','simulation','--evaluated-on','2026-11-06'],capture_output=True,text=True,timeout=10)
        self.assertEqual(completed.returncode,0,completed.stderr)
        self.assertEqual(json.loads(completed.stdout)['status'],'SIMULATION')
        for path in [ROOT/'claude/een-pod-suite/scripts/bo_quality_score.py',*ROOT.glob('opencode/.opencode/skills/*/scripts/bo_quality_score.py')]:
            self.assertEqual(path.read_bytes(),SOURCE.read_bytes())
