#!/usr/bin/env python3
"""Evidence completeness, dates, taxonomy and conservative review gates."""
import argparse
import csv
from datetime import date
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / 'references'
COMMON = ('title', 'summary', 'description', 'sdg', 'partner_role',
          'partnership_types', 'partner_size', 'market_keywords')
SPECIFIC = {
    'BO': ('advantages',), 'BR': ('technical',),
    'TO': ('advantages', 'stage', 'ipr', 'technology_keywords'),
    'TR': ('technical', 'technology_keywords'),
    'RDR': ('technology_keywords', 'framework_program', 'call_identifier',
            'coordinator_required', 'eoi_deadline', 'call_deadline'),
}
PARTNERSHIPS = {
    'BO': ('Commercial agreement', 'Investment agreement', 'Outsourcing agreement', 'Supplier agreement'),
    'BR': ('Commercial agreement', 'Investment agreement', 'Outsourcing agreement', 'Supplier agreement'),
    'TO': ('Investment agreement', 'Commercial agreement with technical assistance', 'Research & development cooperation agreement'),
    'TR': ('Investment agreement', 'Commercial agreement with technical assistance', 'Research & development cooperation agreement'),
    'RDR': ('Research & development cooperation agreement',),
}
LIMITS = {'title': 256, 'summary': 500, 'description': 4000, 'partner_role': 4000}


def populated(value):
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value) and all(populated(item) for item in value)
    if isinstance(value, dict):
        return bool(value)
    return isinstance(value, bool)  # False is a valid No for coordinator_required.


def verify_taxonomy(kind, entries):
    filenames = {'market': 'taxonomy-market-selectable.csv', 'technology': 'taxonomy-technology-selectable.csv',
                 'nace': 'taxonomy-nace-full.csv', 'sdg': 'taxonomy-sdg.csv'}
    with (BASE / filenames[kind]).open(encoding='utf-8-sig') as stream:
        catalogue = {row.get('Code', row['Label']): row for row in csv.DictReader(stream)}
    findings = []
    seen = set()
    for item in entries:
        code = str(item.get('label' if kind == 'sdg' else 'code', '')) if isinstance(item, dict) else str(item)
        row = catalogue.get(code)
        status = 'VALID SNAPSHOT CODE' if row else 'UNKNOWN OR NONSELECTABLE CODE'
        if code in seen:
            status = 'DUPLICATE'
        elif row and isinstance(item, dict) and item.get('label') and item['label'] != row['Label']:
            status = 'CODE-LABEL MISMATCH'
        seen.add(code)
        findings.append({'code': code, 'status': status, 'label': row['Label'] if row else None})
    return {'snapshot': '2024', 'entries': findings,
            'count_status': 'OVER LIMIT' if kind in ('market', 'technology') and len(entries) > 5 else 'PASS',
            'semantic_relevance': 'REQUIRES EVIDENCE-BASED REVIEW'}


def date_checks(fields, today=None):
    today = today or date.today()
    result = {}
    dates = {}
    for key in ('eoi_deadline', 'call_deadline'):
        try:
            dates[key] = date.fromisoformat(str(fields.get(key, '')))
            result[key] = 'EXPIRED' if dates[key] < today else 'CURRENT'
        except ValueError:
            result[key] = 'UNVERIFIED: supply ISO YYYY-MM-DD date'
    if len(dates) == 2:
        gap = (dates['call_deadline'] - dates['eoi_deadline']).days
        result['gap_days'] = gap
        result['ordering'] = 'PASS' if gap > 0 else 'INVALID'
        result['preparation_time'] = 'ADVISER CHECK: no universal minimum imposed'
    return result


def verdict(issues, evidence_complete, operational_confirmed, independent_review):
    if not evidence_complete:
        return 'REVIEW LIMITED'
    if any(issue['severity'] in ('BLOCKER', 'MAJOR') for issue in issues):
        return 'RETURN FOR REVISION'
    if not operational_confirmed or not independent_review:
        return 'REVIEW LIMITED'
    return 'READY AFTER MINOR EDITS' if issues else 'READY'


def review(data, today=None):
    if not isinstance(data, dict) or not isinstance(data.get('fields', {}), dict):
        raise ValueError('Provide a profile object with a fields object')
    if data.get('scope', 'draft') not in ('draft', 'public'):
        raise ValueError('Scope must be draft or public')
    for flag in ('semantic_review_complete', 'operational_confirmed', 'independent_review', 'form_limits_confirmed'):
        if flag in data and type(data[flag]) is not bool:
            raise ValueError(f'{flag} must be a boolean supplied by the reviewer')
    kind = data['profile_type']
    if kind not in SPECIFIC:
        raise ValueError('Unsupported profile type')
    fields = data.get('fields', {})
    for key in ('title', 'summary', 'description', 'partner_role', 'advantages', 'technical', 'stage', 'ipr'):
        if key in fields and not isinstance(fields[key], str):
            raise ValueError(f'{key} must be original field text')
    for key in ('market_keywords', 'technology_keywords', 'sdg', 'target_countries'):
        if key in fields and not isinstance(fields[key], list):
            raise ValueError(f'{key} must be a list; preserve exact codes as strings')
    public = data.get('scope', 'draft') == 'public'
    not_visible = set(data.get('not_visible', []))
    issues = []
    statuses = {}
    required = set(COMMON + SPECIFIC[kind])
    evidence_complete = True
    for key in sorted(required | set(fields)):
        if populated(fields.get(key)):
            statuses[key] = 'PRESENT: semantic review required'
        elif key in not_visible or public:
            statuses[key] = 'NOT VISIBLE IN PUBLIC PROFILE' if public else 'NOT PROVIDED'
            if key in required:
                evidence_complete = False
        elif key in required:
            statuses[key] = 'MISSING REQUIRED INPUT'
            issues.append({'severity': 'BLOCKER', 'field': key, 'rule': 'PPQG v1.2 field matrix', 'evidence': 'Supplied draft field is empty'})
        else:
            statuses[key] = 'OPTIONAL / EMPTY'
    if len(str(fields.get('summary', ''))) > 500:
        issues.append({'severity': 'BLOCKER', 'field': 'summary', 'rule': 'PPQG v1.2: 500 characters', 'evidence': len(fields['summary'])})
    if kind != 'RDR':
        limits = {**LIMITS, 'advantages': 2000}
        if kind in ('BR', 'TR'):
            limits['technical'] = 2000
        for field, limit in limits.items():
            if field != 'summary' and len(fields.get(field, '')) > limit:
                issues.append({'severity': 'BLOCKER' if data.get('form_limits_confirmed') else 'MAJOR',
                               'field': field, 'rule': 'Confirmed form limit' if data.get('form_limits_confirmed') else 'Provisional template-era limit; verify current form',
                               'evidence': {'characters': len(fields[field]), 'limit': limit}})
    if kind == 'TO':
        for key, allowed in {'stage': ('Concept stage','Under development','Lab tested','Available for demonstration','Already on the market'),
                             'ipr': ('No IPR applied','Secret know-how','IPR applied but not yet granted','IPR granted')}.items():
            if populated(fields.get(key)) and fields[key] not in allowed:
                evidence_complete = False
                statuses[key] = 'CURRENT-VERSION CHECK: not a bundled option'
    types = fields.get('partnership_types', [])
    if isinstance(types, str):
        types = [types]
    if len(types) > 3:
        issues.append({'severity': 'MAJOR', 'field': 'partnership_types', 'rule': 'Normally 1–3; adviser justification required', 'evidence': types})
    if any(value not in PARTNERSHIPS[kind] for value in types):
        issues.append({'severity': 'BLOCKER', 'field': 'partnership_types', 'rule': 'PPQG v1.2 Annex II', 'evidence': types})
    taxonomy = {}
    for key, taxonomy_kind in [('market_keywords', 'market'), ('technology_keywords', 'technology'), ('sdg', 'sdg')]:
        if isinstance(fields.get(key), list):
            taxonomy[key] = verify_taxonomy(taxonomy_kind, fields[key])
            check = taxonomy[key]
            if check['count_status'] != 'PASS' or any(x['status'] != 'VALID SNAPSHOT CODE' for x in check['entries']):
                issues.append({'severity': 'MAJOR', 'field': key, 'rule': 'Bundled 2024 selectable taxonomy and maximum-five rule', 'evidence': check})
        elif populated(fields.get(key)):
            evidence_complete = False
            statuses[key] = 'UNVERIFIED TAXONOMY: supply exact code list'
    country = str(fields.get('country', '')).strip().casefold()
    if country and any(str(value).strip().casefold() == country for value in fields.get('target_countries', [])):
        issues.append({'severity': 'MAJOR', 'field': 'target_countries', 'rule': 'PPQG v1.2 p30: exclude own country', 'evidence': country})
    dates = date_checks(fields, today) if kind == 'RDR' else {}
    if any(value == 'EXPIRED' for value in dates.values()) or dates.get('ordering') == 'INVALID':
        issues.append({'severity': 'BLOCKER', 'field': 'call_dates', 'rule': 'RDR current call and preparation sequence', 'evidence': dates})
    if any(str(value).startswith('UNVERIFIED') for value in dates.values()):
        evidence_complete = False
    supplied_issues = data.get('reviewer_issues', [])
    if any(issue.get('severity') not in ('BLOCKER', 'MAJOR', 'MINOR') or not issue.get('evidence') or not issue.get('rule') for issue in supplied_issues):
        raise ValueError('Reviewer issues require severity, evidence and rule')
    issues.extend(supplied_issues)
    # Presence checks cannot establish semantic quality or actual operational work.
    evidence_complete = evidence_complete and data.get('semantic_review_complete', False)
    return {'profile_type': kind, 'fields': statuses, 'taxonomy': taxonomy, 'dates': dates,
            'issues': issues, 'verdict': verdict(issues, evidence_complete,
                data.get('operational_confirmed', False) and (kind == 'RDR' or data.get('form_limits_confirmed', False)),
                data.get('independent_review', False)),
            'scope': 'Advisory checks; no publication, no automatic semantic approval.',
            'operational_checks': ['Profile owner/client linkage, Client Card, Action Plan and adviser confirmation',
                'Confirm template-era limits against the current form; original templates are not bundled']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='UTF-8 JSON profile and evidence flags')
    parser.add_argument('--as-of', help='ISO date for repeatable date checks')
    args = parser.parse_args()
    result = review(json.loads(Path(args.input).read_text()), date.fromisoformat(args.as_of) if args.as_of else None)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
