#!/usr/bin/env python3
"""Read an operator-supplied official EEN profile detail URL. No discovery/search."""
import argparse
from html.parser import HTMLParser
import json
import re
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

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1
        if tag == 'title':
            self.in_title = True
        if tag in ('p','div','li','br','h1','h2','h3','h4','dt','dd','section','article','tr'):
            self.text.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.hidden = max(0, self.hidden - 1)
        if tag == 'title':
            self.in_title = False
        if tag in ('p','div','li','h1','h2','h3','h4','dt','dd','section','article','tr'):
            self.text.append('\n')

    def handle_data(self, data):
        if self.hidden:
            return
        if self.in_title:
            self.title.append(data)
        else:
            self.text.append(data)

    def visible_text(self):
        lines = [re.sub(r'\s+', ' ', line).strip() for line in ''.join(self.text).splitlines()]
        return '\n'.join(line for line in lines if line)


def read_page(url):
    official_url(url)
    request = Request(url, headers={'User-Agent': 'EEN-POD-Suite/2.5 (public profile lookup)', 'Accept': 'text/html'})
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
        return {'status':'FOUND EXACT','url':final,'reference':reference,'title':' '.join(page.title).strip(),'public_text':text,'source':'Official public EEN website'}
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
