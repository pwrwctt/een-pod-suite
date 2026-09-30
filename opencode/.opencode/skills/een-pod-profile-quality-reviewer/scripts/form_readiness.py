#!/usr/bin/env python3
import argparse, json
COMMON={"title":256,"summary":500,"description":4000,"partner_role":4000}
PROFILE={"BO":{"advantages":2000},"BR":{"advantages":2000,"technical":2000},"TO":{"advantages":2000},"TR":{"advantages":2000,"technical":2000}}
def check(text,limit):
    n=len(text or "")
    return {"characters":n,"limit":limit,"status":"PASS" if n<=limit else f"OVER LIMIT by {n-limit}"}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("profile_type",choices=["BO","BR","TO","TR"])
    for x in ["title","summary","description","advantages","technical"]:
        p.add_argument("--"+x.replace("_","-"),dest=x,default="")
    p.add_argument("--partner-role",dest="partner_role",default="")
    p.add_argument("--market-keywords",nargs="*",default=[])
    p.add_argument("--technology-keywords",nargs="*",default=[])
    a=p.parse_args(); vals=vars(a); limits=dict(COMMON); limits.update(PROFILE[a.profile_type])
    out={"profile_type":a.profile_type,"fields":{}}
    for k,v in limits.items(): out["fields"][k]=check(vals.get(k,""),v)
    out["keywords"]={}
    for k,items in [("market",a.market_keywords),("technology",a.technology_keywords)]:
        n=len(items); out["keywords"][k]={"count":n,"limit":5,"status":"PASS" if n<=5 else f"OVER LIMIT by {n-5}"}
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
