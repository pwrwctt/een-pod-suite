#!/usr/bin/env python3
"""Read an operator-supplied official EEN profile detail URL. No discovery/search."""
import argparse
from html.parser import HTMLParser
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

def official_url(url):
    parts = urlsplit(url)
    if (parts.scheme != 'https' or parts.hostname != 'een.ec.europa.eu'
            or parts.username or parts.password or parts.port not in (None, 443)):
        raise ValueError('Use an HTTPS URL on een.ec.europa.eu.')
    if not (parts.path == '/partnering-opportunities' or parts.path.startswith('/partnering-opportunities/')):
        raise ValueError('Use an official partnering-opportunities URL.')
    return url


class OfficialRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        official_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class PublicPage(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.hidden = 0
        self.title = []
        self.in_title = False
        self.stack = []
        self.in_h1 = False
        self.heading = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        concealed = bool(self.hidden) or tag in ('script', 'style', 'nav', 'footer') or 'hidden' in attrs or attrs.get('aria-hidden') == 'true'
        if tag not in ('br', 'img', 'input', 'meta', 'link', 'hr', 'source', 'wbr', 'area', 'base', 'embed', 'param', 'track', 'col'):
            self.stack.append((tag, self.hidden))
            self.hidden = int(concealed)
        if concealed:
            return
        if tag == 'title':
            self.in_title = True
        if tag == 'h1':
            self.in_h1 = True
        if tag in ('p','div','li','br','h1','h2','h3','h4','dt','dd','section','article','tr'):
            self.text.append('\n')

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                self.hidden = self.stack[index][1]
                del self.stack[index:]
                break
        if tag == 'title':
            self.in_title = False
        if tag == 'h1':
            self.in_h1 = False
        if tag in ('p','div','li','h1','h2','h3','h4','dt','dd','section','article','tr'):
            self.text.append('\n')

    def handle_data(self, data):
        if self.hidden:
            return
        if self.in_title:
            self.title.append(data)
        else:
            self.text.append(data)
            if self.in_h1:
                self.heading.append(data)

    def visible_text(self):
        lines = [re.sub(r'\s+', ' ', line).strip() for line in ''.join(self.text).splitlines()]
        return '\n'.join(line for line in lines if line)


def read_page(url):
    official_url(url)
    version = re.search(r'v([0-9.]+)', (Path(__file__).resolve().parents[1] / 'references/version.md').read_text()).group(1)
    request = Request(url, headers={'User-Agent': f'EEN-POD-Suite/{version} (public profile reader)', 'Accept': 'text/html'})
    with build_opener(OfficialRedirects()).open(request, timeout=30) as response:
        final = official_url(response.geturl())
        content_type = response.headers.get_content_type()
        if content_type not in ('text/html', 'application/xhtml+xml'):
            raise ValueError('The response is not an HTML profile page.')
        raw = response.read(5_000_001)
        if len(raw) > 5_000_000:
            raise ValueError('HTML response exceeds the lookup size limit.')
        page = PublicPage()
        page.feed(raw.decode(response.headers.get_content_charset() or 'utf-8', errors='replace'))
        return final, page



FIELD_LABELS = {
    'short summary': 'summary', 'summary': 'summary',
    'full description': 'description', 'description': 'description',
    'advantages and innovations': 'advantages', 'advantages and innovation': 'advantages',
    'technical specification or expertise sought': 'technical', 'technical specification': 'technical',
    'technical specification or know-how sought': 'technical',
    'expected role of a partner': 'partner_role', 'expected role of partner': 'partner_role',
    'partner sought': 'partner_role', 'type of partnership': 'partnership_types',
    'type and size of partner': 'partner_size', 'stage of development': 'stage',
    'ipr status': 'ipr', 'intellectual property rights': 'ipr',
    'market keywords': 'market_keywords', 'technology keywords': 'technology_keywords',
    'sustainable development goals': 'sdg', 'target countries': 'target_countries',
    'profile type': 'profile_type', 'country of origin': 'country',
    'framework program': 'framework_program', 'framework programme': 'framework_program',
    'call title and identifier': 'call_identifier', 'deadline for eois': 'eoi_deadline',
    'deadline for call': 'call_deadline', 'coordinator required': 'coordinator_required',
    'pod reference': '_reference', 'profile reference': '_reference',
    'profile published': 'published_date', 'profile valid until': 'valid_until',
    'profile last updated': 'updated_date', 'contact': '_contact',
}


def extract_fields(page):
    """Conservative label-based extraction. Unknown labels remain in public_text."""
    buffers = {}
    current = None
    for line in page.visible_text().splitlines():
        label, separator, remainder = line.partition(':')
        key = FIELD_LABELS.get(label.strip().lower().rstrip(':'))
        if key:
            current = key
            buffers.setdefault(key, [])
            if separator and remainder.strip():
                buffers[key].append(remainder.strip())
        elif current:
            buffers[current].append(line)
    result = {key: '\n'.join(value).strip() for key, value in buffers.items()
              if not key.startswith('_') and value}
    if page.heading:
        result['title'] = ' '.join(page.heading).strip()
    return result


def read_profile(url, expected_reference=None):
    official_url(url)
    path=urlsplit(url).path.rstrip('/')
    if path == '/partnering-opportunities' or path.endswith('/partnership-contact'):
        raise ValueError('Provide the exact profile detail URL, not a search page or enquiry form.')
    try:
        final,page=read_page(url)
        final_path=urlsplit(final).path.rstrip('/')
        if final_path == '/partnering-opportunities' or final_path.endswith('/partnership-contact'):
            raise ValueError('The detail URL redirected to a search page or enquiry form.')
        text=page.visible_text()
        refs=set(re.findall(r'\bPOD\s+Reference\s*:?\s*((?:BO|BR|TO|TR|RDR)[A-Z]{2}\d{8,14})\b',text,re.I))
        refs={r.upper() for r in refs}
        if len(refs)!=1:
            return {'status':'UNRESOLVED','url':final,'reason':'A unique displayed POD Reference could not be verified.'}
        reference=next(iter(refs))
        if expected_reference and reference!=expected_reference.strip().upper():
            return {'status':'REFERENCE MISMATCH','url':final,'reference':reference,'expected_reference':expected_reference}
        fields = extract_fields(page)
        expected = ('title', 'summary', 'description', 'partner_role')
        missing = [key for key in expected if not fields.get(key)]
        substantive = any(fields.get(key) for key in ('summary', 'description', 'partner_role'))
        status = 'FOUND EXACT' if not missing else 'PARTIAL CONTENT' if substantive else 'INSUFFICIENT CONTENT'
        return {'status':status,'url':final,'requested_url':url,'reference':reference,
                'identity_verified':True,'title':fields.get('title',' '.join(page.title).strip()),
                'fields':fields,'visibility':{key:'VISIBLE' if fields.get(key) else 'NOT VISIBLE IN PUBLIC PROFILE' for key in expected},
                'missing_public_fields':missing,'extraction_complete':not missing,
                'retrieved_at':datetime.now(timezone.utc).isoformat(),'method':'direct public HTML; label-based extraction',
                'public_text':text,'source':'Official public EEN website',
                'count_note':'Extracted whitespace is normalised; exact form counts require original field text.'}
    except HTTPError as exc:
        return {'status':'ACCESS BLOCKED' if exc.code in (401,403,429) else 'HTTP ERROR','url':url,'http_status':exc.code}
    except (URLError,OSError) as exc:
        return {'status':'NETWORK ERROR','url':url,'reason':str(exc.reason if isinstance(exc,URLError) else exc)}
    except ValueError as exc:
        return {'status':'UNRESOLVED','url':url,'reason':str(exc)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url',help='Exact official EEN profile detail URL supplied by the operator')
    parser.add_argument('--expected-reference',help='Optional identity check only; never used for discovery')
    args=parser.parse_args()
    try: result=read_profile(args.url,args.expected_reference)
    except ValueError as exc: result={'status':'INVALID INPUT','reason':str(exc)}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['status']=='FOUND EXACT' else 2


if __name__=='__main__': raise SystemExit(main())
