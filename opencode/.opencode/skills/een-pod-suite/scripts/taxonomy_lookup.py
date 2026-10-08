#!/usr/bin/env python3
"""Exact codes and offline semantic ranking using curated bilingual concepts."""
import argparse,csv,json,re,unicodedata
from pathlib import Path

def norm(text):
    text=unicodedata.normalize('NFKD',(text or '').casefold()).replace('ł','l')
    text=''.join(c for c in text if not unicodedata.combining(c))
    return ' '.join(re.findall(r'[a-z0-9]+',text))
def contains(text,phrase):
    return (' '+norm(phrase)+' ') in (' '+norm(text)+' ')
def lexical_score(query,label):
    query,label=norm(query),norm(label)
    if not query:return 0
    if query==label:return 200
    if contains(label,query):return 100+min(40,len(query)*40//max(1,len(label)))
    words,target=set(query.split()),set(label.split())
    return int(60*len(words&target)/max(1,len(words)))
def search(kind,query,base=None,mode='semantic',limit=10):
    base=Path(base) if base else Path(__file__).resolve().parents[1]/'references'
    files={'technology':'taxonomy-technology-selectable.csv','market':'taxonomy-market-selectable.csv','nace':'taxonomy-nace-full.csv','sdg':'taxonomy-sdg.csv'}
    with (base/files[kind]).open(encoding='utf-8-sig',newline='') as stream:rows=list(csv.DictReader(stream))
    concepts=json.loads((base/'semantic-concepts.json').read_text())['concepts'] if mode=='semantic' else {}
    matches=[]
    for concept,aliases in concepts.items():
        phrases=[concept]+aliases;evidence=[a for a in phrases if contains(query,a)]
        if evidence:matches.append((concept,phrases,evidence))
    ranked=[]
    for row in rows:
        code,label=row.get('Code',''),row.get('Label','');points=lexical_score(query,label)
        reasons=['lexical label match'] if points else []
        if query.strip()==code:points=1000;reasons=['exact code match']
        context=' '.join(v for k,v in row.items() if k.startswith('Parent_'))
        for concept,phrases,evidence in matches:
            direct=[p for p in phrases if contains(label,p)]
            inherited=[p for p in phrases if contains(context,p)]
            if direct or inherited:
                points+=(110 if contains(label,concept) else 70) if direct else 25
                reasons.append({'concept':concept,'query_terms':evidence,'matched_terms':direct or inherited,'location':'label' if direct else 'parent hierarchy'})
        if points:ranked.append({'score':points,'code':code,'label':label,'level':row.get('Level',''),'reasons':reasons,'snapshot':'2024','selection':'Candidate only; verify relevance against profile evidence'})
    return sorted(ranked,key=lambda x:(-x['score'],x['label'],x['code']))[:max(0,limit)]
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('kind',choices=['technology','market','nace','sdg']);p.add_argument('query');p.add_argument('--limit',type=int,default=10);p.add_argument('--references');p.add_argument('--mode',choices=['semantic','lexical'],default='semantic');p.add_argument('--json',action='store_true')
    a=p.parse_args();results=search(a.kind,a.query,a.references,a.mode,a.limit)
    if a.json:print(json.dumps({'method':'curated concept expansion' if a.mode=='semantic' else 'lexical','embedding_model':None,'results':results},ensure_ascii=False,indent=2))
    else:
        for x in results:print(f"{x['score']:3d}\t{x['code']}\t{x['label']}\tL{x['level']}")
if __name__=='__main__':main()
