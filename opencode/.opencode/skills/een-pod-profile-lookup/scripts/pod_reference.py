#!/usr/bin/env python3
"""Generate an official POD search URL or retrieve a verified public profile.

Default operation is offline. --fetch enables public HTTP lookup; --url reads a
known official profile URL directly. No Partner Web Service key is required.
"""
import argparse
from html.parser import HTMLParser
import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

PREFIX_RE = re.compile(r'^(?:BO|BR|TO|TR|RDR)', re.I)
TYPICAL_RE = re.compile(r'^(?:BO|BR|TO|TR|RDR)[A-Z]{2}[0-9]{8,14}$', re.I)
BASE = 'https://een.ec.europa.eu'


def normalise(value):
    return re.sub(r'\s+', '', value).upper()


def search_term(value):
    value = value.strip()
    return normalise(value) if TYPICAL_RE.fullmatch(normalise(value)) else re.sub(r'\s+', ' ', value)


def build_url(reference):
    return BASE + '/partnering-opportunities?' + urlencode({'f[0]': 'k:' + search_term(reference)})


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
        self.links = []
        self.profile_links = []
        self.div_depth = 0
        self.title_divs = []
        self.active_profile_link = None
        self.hidden = 0
        self.title = []
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = set(attrs.get('class', '').split())
        if tag == 'div':
            self.div_depth += 1
            if 'ecl-content-block__title' in classes:
                self.title_divs.append(self.div_depth)
        if tag == 'a' and not self.hidden and self.title_divs and {'ecl-link', 'ecl-link--standalone'} <= classes and attrs.get('href'):
            self.active_profile_link = {'href': attrs['href'], 'text': ''}
            self.profile_links.append(self.active_profile_link)
        if tag in ('script', 'style'):
            self.hidden += 1
        if tag == 'title':
            self.in_title = True
        if tag == 'a':
            href = dict(attrs).get('href')
            if href:
                self.links.append(href)
        if tag in ('p','div','li','br','h1','h2','h3','h4','dt','dd','section','article','tr'):
            self.text.append('\n')

    def handle_endtag(self, tag):
        if tag == 'a':
            self.active_profile_link = None
        if tag == 'div':
            if self.title_divs and self.title_divs[-1] == self.div_depth:
                self.title_divs.pop()
            self.div_depth = max(0, self.div_depth - 1)
        if tag in ('script', 'style'):
            self.hidden = max(0, self.hidden - 1)
        if tag == 'title':
            self.in_title = False
        if tag in ('p','div','li','h1','h2','h3','h4','dt','dd','section','article','tr'):
            self.text.append('\n')

    def handle_data(self, data):
        if self.hidden:
            return
        if self.active_profile_link is not None:
            self.active_profile_link['text'] += data
        if self.in_title:
            self.title.append(data)
        else:
            self.text.append(data)

    def visible_text(self):
        lines = [re.sub(r'\s+', ' ', line).strip() for line in ''.join(self.text).splitlines()]
        return '\n'.join(line for line in lines if line)


def read_page(url):
    official_url(url)
    request = Request(url, headers={'User-Agent': 'EEN-POD-Suite/2.3 (public profile lookup)', 'Accept': 'text/html'})
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


def verify_profile(reference, url, page):
    text = page.visible_text()
    refs = re.findall(r'\bPOD\s+Reference\s*:?\s*((?:BO|BR|TO|TR|RDR)[A-Z]{2}\d{8,14})\b', text, re.I)
    refs = {normalise(r) for r in refs}
    by_reference = bool(TYPICAL_RE.fullmatch(normalise(reference)))
    if refs == {normalise(reference)} or (not by_reference and len(refs) == 1 and search_term(reference).casefold() in re.sub(r'\s+', ' ', text).casefold()):
        return {'status': 'FOUND EXACT', 'reference': next(iter(refs)), 'query': search_term(reference), 'url': url,
                'title': ' '.join(page.title).strip(), 'public_text': text,
                'source': 'Official public EEN website'}
    if refs:
        return {'status': 'REFERENCE MISMATCH', 'displayed_references': sorted(refs), 'url': url}
    return {'status': 'UNRESOLVED', 'url': url,
            'reason': 'No displayed POD Reference could be verified. The page may be incomplete or require rendering.'}


def lookup(reference, direct_url=None):
    reference = search_term(reference)
    if not reference:
        raise ValueError("Search term must not be empty.")
    by_reference = bool(TYPICAL_RE.fullmatch(reference))
    attempts = []

    def retrieve(url):
        try:
            return read_page(url)
        except HTTPError as exc:
            attempts.append({'url': url, 'status': 'ACCESS BLOCKED' if exc.code in (401,403,429) else 'HTTP ERROR', 'http_status': exc.code})
        except (URLError, OSError) as exc:
            attempts.append({'url': url, 'status': 'NETWORK ERROR', 'reason': str(exc.reason if isinstance(exc, URLError) else exc)})
        except ValueError as exc:
            attempts.append({'url': url, 'status': 'UNRESOLVED', 'reason': str(exc)})
        return None

    if direct_url:
        official_url(direct_url)
        path = urlsplit(direct_url).path.rstrip('/')
        if path == '/partnering-opportunities' or path.endswith('/partnership-contact'):
            raise ValueError('--url must identify a profile detail page, not a search or enquiry form.')
        result = retrieve(direct_url)
        if result:
            data = verify_profile(reference, *result)
            data['attempts'] = attempts
            return data
    else:
        result = retrieve(build_url(reference))
        if result:
            url, page = result
            candidates = []
            for link in page.profile_links:
                target = urljoin(url, link['href'])
                try:
                    official_url(target)
                except ValueError:
                    continue
                path = urlsplit(target).path.rstrip('/')
                if path != '/partnering-opportunities' and not path.endswith('/partnership-contact') and target not in [c['url'] for c in candidates]:
                    candidates.append({'url': target, 'title': re.sub(r'\s+', ' ', link['text']).strip()})
            if not by_reference:
                exact_titles = [c for c in candidates if c['title'].casefold() == re.sub(r'\s+', ' ', reference).casefold()]
                if len(exact_titles) == 1:
                    candidates = exact_titles
                elif len(candidates) > 1:
                    return {'status': 'AMBIGUOUS', 'query': reference, 'candidates': candidates, 'reason': 'Multiple matching search cards; select a profile before auditing.'}
            for target in candidates[:10]:
                candidate = retrieve(target['url'])
                if candidate:
                    data = verify_profile(reference, *candidate)
                    if data['status'] == 'FOUND EXACT':
                        data['search_url'] = url
                        data['attempts'] = attempts
                        return data
            attempts.append({'url': url, 'status': 'UNRESOLVED', 'reason': 'No exact detail page verified from this search response. Search or indexing may be incomplete.'})
    states = {item['status'] for item in attempts}
    status = 'UNRESOLVED'
    if states == {'ACCESS BLOCKED'}:
        status = 'ACCESS BLOCKED'
    elif states == {'NETWORK ERROR'}:
        status = 'NETWORK ERROR'
    return {'status': status, 'reference': reference, 'attempts': attempts,
            'reason': 'Retrieval did not establish profile availability. Do not report the profile as nonexistent or unpublished.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('reference')
    parser.add_argument('--fetch', action='store_true', help='Retrieve and verify the public profile as JSON')
    parser.add_argument('--url', help='Known official profile detail URL; implies --fetch')
    args = parser.parse_args()
    reference = search_term(args.reference)
    if args.fetch or args.url:
        try:
            data = lookup(reference, args.url)
        except ValueError as exc:
            data = {'status': 'INVALID INPUT', 'reason': str(exc)}
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0 if data['status'] == 'FOUND EXACT' else 2
    print(f'reference={reference}')
    print(f'known_prefix={"yes" if PREFIX_RE.match(reference) else "no"}')
    print(f'typical_format={"yes" if TYPICAL_RE.fullmatch(reference) else "no"}')
    print(f'url={build_url(reference)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
