#!/usr/bin/env python3
"""Local interpretation of the 2026 BO pilot; not an EISMEA assessment."""
import argparse
import calendar
from copy import deepcopy
from datetime import date
import hashlib
import json
from pathlib import Path
import re

BASE = Path(__file__).resolve().parents[1] / 'references'
MODEL_BYTES = (BASE / 'bo-scoring-model.json').read_bytes()
MODEL = json.loads(MODEL_BYTES)
COUNTRY_BYTES = (BASE / 'bo-country-terms.json').read_bytes()
COUNTRIES = json.loads(COUNTRY_BYTES)['countries']
TEXT_FIELDS = ('title', 'summary', 'description', 'advantages', 'partner_role')


def band(score):
    if type(score) is not int or not -4 <= score <= 8:
        raise ValueError('Score must be an integer between -4 and 8')
    return next(row['band'] for row in MODEL['bands'] if row['min'] <= score <= row['max'])


def normalise(text):
    return ' '.join(text.casefold().split())


def mentions(text, phrase):
    return bool(re.search(r'(?<!\w)' + re.escape(phrase).replace(r'\ ', r'\s+') + r'(?!\w)', text, re.I))


def conjunction(*values):
    if False in values:
        return False
    return None if None in values else True


def add_months(value, months=2):
    month = value.month - 1 + months
    year = value.year + month // 12
    month = month % 12 + 1
    return date(year, month, min(value.day, calendar.monthrange(year, month)[1]))


def selected_terms(selected):
    keys = {key.casefold(): key for key in MODEL['agreements']}
    if any(value.casefold() not in keys for value in selected):
        return None
    return [keys[value.casefold()] for value in selected]


def score_profile(profile, mode='published', evaluated_on=None):
    if not isinstance(profile, dict) or not isinstance(profile.get('fields', {}), dict):
        raise ValueError('Supply a profile object and a fields object')
    if mode not in ('published', 'simulation'):
        raise ValueError('Mode must be published or simulation')
    evaluated = date.fromisoformat(evaluated_on) if evaluated_on else date.today()
    kind = profile.get('profile_type', profile.get('profiletype_code'))
    status = profile.get('profile_status', profile.get('profilestatus_name'))
    if kind is not None and not isinstance(kind, str):
        raise ValueError('profile_type must be text')
    if status is not None and not isinstance(status, str):
        raise ValueError('profile_status must be text')
    kind = kind.upper() if kind else None
    status = status.upper() if status else None
    if 'known_test_profile' in profile and type(profile['known_test_profile']) is not bool:
        raise ValueError('known_test_profile must be boolean')
    if kind != 'BO':
        return {'status': 'NOT APPLICABLE' if kind else 'SCOPE UNVERIFIED',
                'reason': 'The pilot model applies only to explicitly identified BO profiles.'}
    if mode == 'published' and status and status != 'PUBLISHED':
        return {'status': 'NOT APPLICABLE', 'reason': 'Draft, expired and archived profiles are outside published pilot scope.'}
    fields = profile.get('fields', {})
    hidden = profile.get('not_visible', [])
    if not isinstance(hidden, list) or any(not isinstance(key, str) for key in hidden):
        raise ValueError('not_visible must be an array of field names')
    for key in TEXT_FIELDS:
        if key in fields and fields[key] is not None and not isinstance(fields[key], str):
            raise ValueError(key + ' must be original field text or null')
    selected = fields.get('partnership_types')
    if selected is not None and (not isinstance(selected, list) or any(not isinstance(value, str) for value in selected)):
        raise ValueError('partnership_types must be an array of exact agreement names or null')
    visible_values = [fields[key] for key in TEXT_FIELDS if isinstance(fields.get(key), str) and fields[key].strip()]
    test_pattern = len(visible_values) >= 3 and all(value.strip() == '123' for value in visible_values)
    if profile.get('known_test_profile') or test_pattern:
        return {'status': 'EXCLUDED TEST PROFILE', 'reason': 'Operator-confirmed test or all-visible-field 123 pattern.'}

    def field(key):
        return None if key in hidden else fields.get(key)

    def agreements_in(value):
        if value is None:
            return None
        return any(mentions(value, phrase) for aliases in MODEL['agreements'].values() for phrase in aliases)

    title, summary, description, advantages, partner = [field(key) for key in TEXT_FIELDS]
    criteria = {}
    def record(key, passed, evidence):
        criteria[key] = {'criterion': MODEL['criteria'][key],
                         'state': 'UNKNOWN' if passed is None else 'MET' if key.startswith('P') and passed else 'NOT MET' if key.startswith('P') else 'TRIGGERED' if passed else 'NOT TRIGGERED',
                         'value': passed, 'contribution': None if passed is None else (1 if key.startswith('P') else -1) * int(passed),
                         'evidence': evidence}

    record('P1', conjunction(agreements_in(title), agreements_in(description)),
           {'title_mentions': [key for key, aliases in MODEL['agreements'].items() if title is not None and any(mentions(title, alias) for alias in aliases)],
            'description_mentions': [key for key, aliases in MODEL['agreements'].items() if description is not None and any(mentions(description, alias) for alias in aliases)]})
    record('P2', None if title is None else 40 <= len(title) <= 256 and not title.isupper(),
           {'characters': None if title is None else len(title), 'all_caps': None if title is None else title.isupper()})
    copy_title = None if summary is None or title is None else bool(summary.strip()) and normalise(summary) == normalise(title)
    copy_opening = None if summary is None or description is None else bool(summary.strip()) and normalise(description).startswith(normalise(summary))
    no_copy = False if copy_title is True or copy_opening is True else None if copy_title is None or copy_opening is None else True
    record('P3', conjunction(None if summary is None else 250 <= len(summary) <= 500, no_copy),
           {'characters': None if summary is None else len(summary), 'copies_title': copy_title, 'copies_description_opening': copy_opening})

    origin = profile.get('country', fields.get('country'))
    if origin is not None and not isinstance(origin, str):
        raise ValueError('country must be a country code/name or null')
    terms = profile.get('country_terms')
    dictionary = 'operator-supplied terms' if terms is not None else 'local dictionary; not the source SQL country table'
    if terms is not None:
        if not isinstance(terms, list) or not terms or any(not isinstance(term, str) or not term.strip() for term in terms):
            raise ValueError('country_terms must be a nonempty string array')
        if not origin:
            terms = None
    elif origin:
        terms = next((values for code, values in COUNTRIES.items()
                      if origin.casefold() == code.casefold() or any(origin.casefold() == value.casefold() for value in values)), None)
    country_summary = None if summary is None or not terms else any(mentions(summary, term) for term in terms)
    country_description = None if description is None or not terms else any(mentions(description, term) for term in terms)
    record('P4', conjunction(country_summary, country_description),
           {'origin': origin, 'terms': terms, 'dictionary': dictionary,
            'summary_matches': [term for term in (terms or []) if summary is not None and mentions(summary, term)],
            'description_matches': [term for term in (terms or []) if description is not None and mentions(description, term)]})
    record('P5', None if description is None else 800 <= len(description) <= 4000,
           {'characters': None if description is None else len(description)})
    digits = [] if advantages is None else re.findall(r'\d+', advantages)
    record('P6', None if advantages is None else len(advantages) >= 200 and bool(digits),
           {'characters': None if advantages is None else len(advantages), 'digits': digits,
            'limitation': 'Digits do not establish meaningful quantified advantages.'})
    record('P7', None if partner is None else len(partner) >= 300,
           {'characters': None if partner is None else len(partner)})
    selected = None if 'partnership_types' in hidden else selected
    canonical = None if selected is None else selected_terms(selected)
    consistency = None
    missing_mentions = {}
    if canonical is not None:
        checks = []
        for key, text in [('summary', summary), ('description', description), ('partner_role', partner)]:
            missing_mentions[key] = None if text is None else [name for name in canonical if not any(mentions(text, phrase) for phrase in MODEL['agreements'][name])]
            checks.append(None if text is None else not missing_mentions[key])
        consistency = conjunction(bool(canonical), *checks)
    record('P8', consistency, {'selected': selected, 'missing_mentions': missing_mentions,
                              'limitation': 'Keyword proxy, not semantic coherence. Unknown agreement labels require clarification.'})

    available_text = '\n'.join(value for value in [title, summary, description, advantages, partner] if value is not None)
    missing_text = any(value is None for value in [title, summary, description, advantages, partner])
    pronouns = [{'term': match.group(0), 'excerpt': available_text[max(0,match.start()-25):match.end()+25]}
                for match in re.finditer(r'(?<!\w)(?:we|our|us|you|your)(?!\w)', available_text, re.I)]
    record('N1', True if pronouns else None if missing_text else False,
           {'matches': pronouns, 'limitation': 'Regex may penalise US or quoted text; adviser must inspect context.'})
    marketing = [key for key, aliases in MODEL['marketing_terms'].items() if any(mentions(available_text, alias) for alias in aliases)]
    record('N2', True if len(marketing) >= 3 else None if missing_text else False,
           {'distinct_terms': marketing, 'count': len(marketing), 'dictionary': 'Illustrative source terms only; distinct-term interpretation.'})
    record('N3', None if title is None else title.isupper(), {'title': title})
    duplicate = None if title is None or summary is None else len(title) >= 40 and len(summary) >= 40 and title[:40] == summary[:40]
    record('N4', duplicate, {'title_prefix': None if title is None else title[:40],
                             'summary_prefix': None if summary is None else summary[:40],
                             'comparison': 'Raw case-sensitive first 40 characters of both fields.'})

    known_total = sum(row['contribution'] for row in criteria.values() if row['contribution'] is not None)
    unknown = [key for key, row in criteria.items() if row['value'] is None]
    low = known_total - sum(key.startswith('N') for key in unknown)
    high = known_total + sum(key.startswith('P') for key in unknown)
    bands = list(dict.fromkeys(band(value) for value in range(low, high+1)))
    complete = not unknown
    confirmed = status == 'PUBLISHED' and mode == 'published'
    label = 'SIMULATION' if mode == 'simulation' else 'COMPLETE' if confirmed and complete else 'PARTIAL' if confirmed else 'SCOPE UNVERIFIED'
    result = {'status': label, 'model_id': MODEL['id'], 'implementation_version': MODEL['implementation_version'],
              'model_sha256': hashlib.sha256(MODEL_BYTES).hexdigest(), 'country_dictionary_sha256': hashlib.sha256(COUNTRY_BYTES).hexdigest(),
              'source_snapshot': MODEL['source_snapshot'], 'sql_equivalence': 'NOT VERIFIED: local documented interpretation',
              'identity': {'reference': profile.get('reference'), 'url': profile.get('url')},
              'scope': {'profile_type': kind, 'profile_status': status, 'published_scope_confirmed': confirmed, 'mode': mode},
              'evaluated_on': evaluated.isoformat(), 'recheck_due': add_months(evaluated).isoformat(),
              'criteria': criteria, 'score': known_total if complete else None,
              'score_range': {'min': low, 'max': high}, 'band': bands[0] if len(bands) == 1 else None,
              'possible_bands': bands, 'unknown_criteria': unknown, 'scoring_complete': complete,
              'maturity_note': 'Scoring minima are pilot point conditions, not new mandatory PPQG rules.',
              'semantic_audit': 'SEPARATE: inspect offer, eligibility, partner purpose, evidence, abbreviations, spelling and confidentiality.',
              'input_snapshot': {key: deepcopy(profile[key]) for key in ('profile_type','profiletype_code','profile_status','profilestatus_name','fields','country','country_terms','reference','url','not_visible','known_test_profile') if key in profile}}
    result['recommended_actions'] = actions(result)
    return result


def actions(result):
    if result.get('status') != 'COMPLETE':
        return {'status': 'ADVISER REVIEW REQUIRED', 'steps': ['Confirm scope and complete evidence before operational action.'], 'automatic_action': False}
    quality = result['band']
    steps = []
    if quality == 'Poor':
        steps += ['Prepare Guidelines Compliance flag for adviser verification, with concrete PPQG non-compliance evidence.',
                  'Invite drafter to POD Quality Clinic through the authorised coordinator.']
    if quality in ('Weak', 'Fair', 'Good'):
        steps.append('Prepare owner notification identifying improvements.')
    if quality == 'Weak':
        steps.append('Invite drafter to POD Quality Clinic through the authorised coordinator.')
    if quality == 'Excellent':
        steps.append('No specific remedial action prescribed by the coordinator message; retain semantic audit.')
    steps.append('Repeat assessment after two calendar months using the same model implementation.')
    return {'status': 'DRAFT RECOMMENDATIONS ONLY', 'steps': steps, 'automatic_action': False,
            'flag_comment_template': 'Profile [reference], criterion [id]. Quotation: [observed text]. PPQG [section/page]: [rule]. Confirmed non-compliance: [explanation]. Requested correction: [facts-based edit].',
            'owner_message_template': 'The BO review identified improvements in [fields]. Evidence: [quotations]. Suggested corrections: [edits/questions]. Pilot band [band] is separate from the PPQG content audit.',
            'clinic_topics': ['Cooperation purpose', 'WHY/HOW and partner role', 'Evidence behind advantages', 'Summary and partnership consistency'],
            'limitation': 'Point loss alone is not proof of PPQG non-compliance. No flag, notification or invitation was sent.'}


def compare_runs(before, after):
    if not isinstance(before, dict) or not isinstance(after, dict) or 'criteria' not in before or 'criteria' not in after:
        raise ValueError('Compare two saved scoring runs')
    one, two = before.get('identity', {}), after.get('identity', {})
    if one.get('reference') and two.get('reference'):
        same = one['reference'] == two['reference']
    else:
        same = bool(one.get('url')) and one.get('url') == two.get('url')
    if not same:
        raise ValueError('A matching explicit reference or exact URL is required; no profile discovery')
    keys = ('model_id','implementation_version','model_sha256','country_dictionary_sha256')
    if any(before.get(key) != after.get(key) for key in keys):
        raise ValueError('Model/dictionary changed: rescore both saved input snapshots with the same implementation')
    if any(before.get('scope', {}).get(key) != after.get('scope', {}).get(key) for key in ('profile_type','profile_status','mode')):
        raise ValueError('Scope changed: compare like-for-like runs')
    first_date = date.fromisoformat(before['evaluated_on'])
    second_date = date.fromisoformat(after['evaluated_on'])
    if second_date < first_date:
        raise ValueError('Follow-up date cannot precede baseline date')
    comparable = before.get('scoring_complete') and after.get('scoring_complete')
    return {'identity': two, 'model_id': after['model_id'],
            'score_before': before.get('score'), 'score_after': after.get('score'),
            'score_delta': after['score'] - before['score'] if comparable else None,
            'band_before': before.get('band'), 'band_after': after.get('band'),
            'recheck_due': before.get('recheck_due'),
            'days_elapsed': (second_date-first_date).days,
            'at_or_after_due': second_date >= add_months(first_date),
            'criterion_changes': [{'id': key, 'before': before['criteria'][key]['state'], 'after': after['criteria'][key]['state']}
                                  for key in before['criteria'] if before['criteria'][key]['state'] != after['criteria'][key]['state']],
            'content_review': 'Reassess previous issues as RESOLVED/PARTLY RESOLVED/OPEN/NOT VERIFIABLE with evidence; score improvement alone does not close them.'}


def rescore_and_compare(before, after):
    if 'input_snapshot' not in before or 'input_snapshot' not in after:
        raise ValueError('Saved input snapshots are required for rescoring')
    rebuilt = [score_profile(run['input_snapshot'],run.get('scope',{}).get('mode','published'),run['evaluated_on']) for run in (before,after)]
    result = compare_runs(*rebuilt)
    result['rescored_with_current_model'] = True
    result['original_recorded_scores'] = {'before':before.get('score'),'after':after.get('score')}
    result['note'] = 'Delta uses freshly rescored snapshots, not mixed-model original totals.'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    scoring = sub.add_parser('score')
    scoring.add_argument('input')
    scoring.add_argument('--mode', choices=('published','simulation'), default='published')
    scoring.add_argument('--evaluated-on')
    compare = sub.add_parser('compare')
    compare.add_argument('before'); compare.add_argument('after')
    compare.add_argument('--rescore', action='store_true', help='Explicitly rescore both snapshots with the current implementation')
    args = parser.parse_args()
    if args.command == 'score':
        output = score_profile(json.loads(Path(args.input).read_text()), args.mode, args.evaluated_on)
    else:
        output = (rescore_and_compare if args.rescore else compare_runs)(json.loads(Path(args.before).read_text()), json.loads(Path(args.after).read_text()))
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
