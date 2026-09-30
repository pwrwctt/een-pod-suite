#!/usr/bin/env python3
"""Normalise an EEN POD reference and build the official filtered lookup URL."""
import argparse
import re
from urllib.parse import urlencode

PREFIX_RE = re.compile(r"^(?:BO|BR|TO|TR|RDR)", re.I)
TYPICAL_RE = re.compile(r"^(?:BO|BR|TO|TR|RDR)[A-Z]{2}[0-9]{8,14}$", re.I)

def normalise(value: str) -> str:
    return re.sub(r"\s+", "", value).upper()

def build_url(reference: str) -> str:
    ref = normalise(reference)
    query = urlencode({"f[0]": f"k:{ref}"})
    return f"https://een.ec.europa.eu/partnering-opportunities?{query}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("reference")
    args = ap.parse_args()
    ref = normalise(args.reference)
    print(f"reference={ref}")
    print(f"known_prefix={'yes' if PREFIX_RE.match(ref) else 'no'}")
    print(f"typical_format={'yes' if TYPICAL_RE.fullmatch(ref) else 'no'}")
    print(f"url={build_url(ref)}")

if __name__ == "__main__":
    main()
