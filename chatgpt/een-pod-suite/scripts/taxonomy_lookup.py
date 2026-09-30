#!/usr/bin/env python3
"""Search EEN POD taxonomy CSV snapshots bundled with the skill."""
import argparse, csv, re
from pathlib import Path

def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower())

def score(query, label):
    q = norm(query)
    l = norm(label)
    if not q:
        return 0
    if q == l:
        return 100
    if q in l:
        return 80 + min(15, len(q) * 15 // max(1, len(l)))
    qtok = set(re.findall(r"[a-z0-9]+", q))
    ltok = set(re.findall(r"[a-z0-9]+", l))
    if not qtok or not ltok:
        return 0
    overlap = len(qtok & ltok) / len(qtok)
    return int(overlap * 70)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["technology","market","nace","sdg"])
    ap.add_argument("query")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--references", default=None)
    args = ap.parse_args()

    base = Path(args.references) if args.references else Path(__file__).resolve().parents[1] / "references"
    if args.kind == "technology":
        fn = base / "taxonomy-technology-selectable.csv"
        label_col = "Label"
    elif args.kind == "market":
        fn = base / "taxonomy-market-selectable.csv"
        label_col = "Label"
    elif args.kind == "nace":
        fn = base / "taxonomy-nace-full.csv"
        label_col = "Label"
    else:
        fn = base / "taxonomy-sdg.csv"
        label_col = "Label"

    with fn.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    ranked = sorted(
        ((score(args.query, r.get(label_col,"")), r) for r in rows),
        key=lambda x: (-x[0], x[1].get(label_col,""))
    )
    for s, r in ranked[:args.limit]:
        if s <= 0:
            break
        print(f"{s:3d}\t{r.get('Code','')}\t{r.get(label_col,'')}\tL{r.get('Level','')}")
if __name__ == "__main__":
    main()
