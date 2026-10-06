#!/usr/bin/env python3
"""EEN Partner Web Service helper for POD profiles and Market/Technology labels.

Uses only Python standard library. API key is read from EEN_API_KEY.
Event API is intentionally not implemented.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "https://b2b.een.ec.europa.eu/v1"
NULL_UUID = "00000000-0000-0000-0000-000000000000"

PROFILE_TYPES = {"BO", "BR", "TO", "TR", "RDR"}
PROFILE_STATUSES = {
    "DRAFT",
    "DRAFT_ACCEPTED",
    "DRAFT_REJECTED",
    "CLIENT_VALIDATION_PENDING",
    "ARCHIVED",
    "EXPIRED",
    "FLAGGED",
    "ON_HOLD",
    "REJECTED",
    "UNDER_REVIEW",
    "UNDER_VALIDATION",
    "PUBLISHED",
}
COMPARISON_DATES = {"Created", "LastModified", "PublicationDate"}
SORT_ORDERS = {"ASC", "DESC"}
LABEL_TYPES = {"market_keyword", "technology_keyword"}


class EenApiError(RuntimeError):
    pass


def base_url() -> str:
    return os.getenv("EEN_B2B_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def api_key() -> str:
    value = os.getenv("EEN_API_KEY")
    if not value:
        raise EenApiError(
            "EEN_API_KEY is not set. Partner Web Service also requires IP whitelisting."
        )
    return value


def _clean_scalar(value: Any) -> Any:
    if isinstance(value, str):
        value = value.strip()
    return value


def _request_json(path: str, params: list[tuple[str, str]]) -> dict[str, Any]:
    query = urlencode(params, doseq=True)
    url = f"{base_url()}{path}"
    if query:
        url = f"{url}?{query}"

    req = Request(
        url,
        headers={
            "accept": "application/json",
            "X-API-KEY": api_key(),
        },
        method="GET",
    )

    try:
        with urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw)
    except HTTPError as exc:
        if exc.code in (401, 403):
            raise EenApiError(
                f"Partner Web Service access denied (HTTP {exc.code}). "
                "Check EEN_API_KEY and IP whitelisting."
            ) from exc
        raise EenApiError(f"Partner Web Service HTTP error: {exc.code}") from exc
    except URLError as exc:
        raise EenApiError(f"Partner Web Service network error: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise EenApiError("Partner Web Service returned invalid JSON.") from exc


def build_profiles_params(
    *,
    page_index: int = 1,
    page_size: int = 200,
    profile_types: list[str] | None = None,
    statuses: list[str] | None = None,
    countries: list[str] | None = None,
    comparison_date: str = "Created",
    sort_order: str = "ASC",
    from_date: str | None = None,
    to_date: str | None = None,
) -> list[tuple[str, str]]:
    if page_index < 1:
        raise ValueError("Profiles PageIndex must be >= 1.")
    if page_size <= 0 or page_size > 200:
        raise ValueError("Profiles PageSize must be between 1 and 200.")
    if comparison_date not in COMPARISON_DATES:
        raise ValueError(f"Unsupported ComparisonDate: {comparison_date}")
    if sort_order not in SORT_ORDERS:
        raise ValueError(f"Unsupported SortOrder: {sort_order}")

    params: list[tuple[str, str]] = [
        ("PageIndex", str(page_index)),
        ("PageSize", str(page_size)),
        ("ComparisonDate", comparison_date),
        ("SortOrder", sort_order),
    ]

    for value in profile_types or []:
        code = value.upper()
        if code not in PROFILE_TYPES:
            raise ValueError(f"Unsupported profile type: {value}")
        params.append(("ProfileTypes", code))

    for value in statuses or []:
        code = value.upper()
        if code not in PROFILE_STATUSES:
            raise ValueError(f"Unsupported profile status: {value}")
        params.append(("ProfileStatuses", code))

    for value in countries or []:
        params.append(("Countries", value.upper()))

    if from_date:
        params.append(("FromDate", from_date))
    if to_date:
        params.append(("ToDate", to_date))

    return params


def fetch_profiles_page(**kwargs: Any) -> dict[str, Any]:
    return _request_json("/profiles", build_profiles_params(**kwargs))


def iter_profiles(
    *,
    page_size: int = 200,
    max_pages: int | None = None,
    **kwargs: Any,
):
    page = 1
    seen = 0
    while True:
        payload = fetch_profiles_page(page_index=page, page_size=page_size, **kwargs)
        data = payload.get("data") or {}
        items = data.get("items") or []
        for item in items:
            yield item

        info = data.get("pagingInfo") or {}
        seen += 1
        if max_pages is not None and seen >= max_pages:
            return
        if not info.get("hasNext"):
            return
        page += 1


def is_na(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value.strip().upper() == "N/A")


def profile_visibility(item: dict[str, Any]) -> str:
    """Classify visibility conservatively using the guide's limited-item pattern."""
    core_fields = ("title", "shortSummary", "description", "expectedRoleOfThePartner")
    if not all(field in item for field in core_fields):
        return "UNKNOWN"
    core = [
        item.get("title"),
        item.get("shortSummary"),
        item.get("description"),
        item.get("expectedRoleOfThePartner"),
    ]
    if all(is_na(v) for v in core):
        return "LIMITED"
    if any(isinstance(v, str) and v.strip() and not is_na(v) for v in core[:3]):
        return "FULL"
    return "UNKNOWN"


def profile_summary(item: dict[str, Any]) -> dict[str, Any]:
    profile_type = item.get("profileType") or {}
    status = item.get("profileStatus") or {}
    return {
        "id": item.get("id"),
        "reference": item.get("reference"),
        "profileType": profile_type.get("code"),
        "profileStatus": status.get("name"),
        "visibility": profile_visibility(item),
        "created": item.get("created"),
        "lastModified": item.get("lastModified"),
        "publicationDate": item.get("publicationDate"),
        "expirationDate": item.get("expirationDate"),
        "openForEOI": item.get("openForEOI"),
        "publicURL": item.get("publicURL"),
        "title": item.get("title"),
    }


def find_profile_by_reference(reference: str, **kwargs: Any) -> dict[str, Any] | None:
    """Scan authorised results for exact reference.

    No undocumented API filter is used.
    """
    target = reference.strip().upper()
    for item in iter_profiles(**kwargs):
        if str(item.get("reference") or "").strip().upper() == target:
            return item
    return None


def build_label_descriptor(
    data_type: str,
    from_date: str | None = None,
    to_date: str | None = None,
) -> str:
    if data_type not in LABEL_TYPES:
        raise ValueError(f"Unsupported label data type: {data_type}")

    parts = ["dataTypeId", "equals", data_type]
    if from_date:
        parts.extend(["FromDate", "equals", from_date])
    if to_date:
        parts.extend(["ToDate", "equals", to_date])
    return "^".join(parts)


def build_label_params(
    *,
    data_type: str,
    page: int = 0,
    page_size: int = 200,
    from_date: str | None = None,
    to_date: str | None = None,
) -> list[tuple[str, str]]:
    if page < 0:
        raise ValueError("ReferenceData page is 0-based and must be >= 0.")
    if page_size <= 0:
        raise ValueError("page_size must be > 0.")
    return [
        ("page", str(page)),
        ("page_size", str(page_size)),
        (
            "Filter.Descriptor",
            build_label_descriptor(data_type, from_date=from_date, to_date=to_date),
        ),
    ]


def fetch_labels_page(**kwargs: Any) -> dict[str, Any]:
    return _request_json("/refdrupal/label", build_label_params(**kwargs))


def iter_labels(
    *,
    data_type: str,
    page_size: int = 200,
    from_date: str | None = None,
    to_date: str | None = None,
    active_only: bool = False,
    max_pages: int | None = None,
):
    page = 0
    seen = 0
    while True:
        payload = fetch_labels_page(
            data_type=data_type,
            page=page,
            page_size=page_size,
            from_date=from_date,
            to_date=to_date,
        )
        items = payload.get("items") or []
        for item in items:
            if active_only and str(item.get("isActive")) != "True":
                continue
            yield item

        info = payload.get("pagingInfo") or {}
        seen += 1
        if max_pages is not None and seen >= max_pages:
            return

        current = int(info.get("currentPage", page))
        total_pages = int(info.get("totalPages", current + 1))
        if current + 1 >= total_pages:
            return
        page = current + 1


def normalise_label(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "uuid": item.get("uuid"),
        "name": item.get("name"),
        "acronym": item.get("acronym"),
        "isActive": item.get("isActive"),
        "parentUuid": item.get("parentUuid"),
        "parentName": item.get("parentName"),
        "dataTypeId": item.get("dataTypeId"),
        "dataTypeName": item.get("dataTypeName"),
        "isRoot": item.get("parentUuid") == NULL_UUID,
    }


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)

    pp = sub.add_parser("profiles", help="Fetch a page of profiles")
    pp.add_argument("--page-index", type=int, default=1)
    pp.add_argument("--page-size", type=int, default=200)
    pp.add_argument("--profile-type", action="append", default=[])
    pp.add_argument("--status", action="append", default=[])
    pp.add_argument("--country", action="append", default=[])
    pp.add_argument("--comparison-date", default="Created")
    pp.add_argument("--sort-order", default="ASC")
    pp.add_argument("--from-date")
    pp.add_argument("--to-date")
    pp.add_argument("--dry-run", action="store_true")

    pf = sub.add_parser("find", help="Scan authorised profiles for an exact POD reference")
    pf.add_argument("reference")
    pf.add_argument("--page-size", type=int, default=200)
    pf.add_argument("--profile-type", action="append", default=[])
    pf.add_argument("--status", action="append", default=[])
    pf.add_argument("--country", action="append", default=[])
    pf.add_argument("--comparison-date", default="Created")
    pf.add_argument("--sort-order", default="ASC")
    pf.add_argument("--from-date")
    pf.add_argument("--to-date")
    pf.add_argument("--max-pages", type=int)

    lp = sub.add_parser("labels", help="Fetch Market/Technology reference labels")
    lp.add_argument("data_type", choices=sorted(LABEL_TYPES))
    lp.add_argument("--page", type=int, default=0)
    lp.add_argument("--page-size", type=int, default=200)
    lp.add_argument("--from-date")
    lp.add_argument("--to-date")
    lp.add_argument("--dry-run", action="store_true")

    lv = sub.add_parser("visibility", help="Classify visibility of a saved profile JSON object")
    lv.add_argument("json_file")

    return p


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "profiles":
            kwargs = dict(
                page_index=args.page_index,
                page_size=args.page_size,
                profile_types=args.profile_type,
                statuses=args.status,
                countries=args.country,
                comparison_date=args.comparison_date,
                sort_order=args.sort_order,
                from_date=args.from_date,
                to_date=args.to_date,
            )
            if args.dry_run:
                print(urlencode(build_profiles_params(**kwargs), doseq=True))
                return 0
            print(json.dumps(fetch_profiles_page(**kwargs), ensure_ascii=False, indent=2))
            return 0

        if args.command == "find":
            item = find_profile_by_reference(
                args.reference,
                page_size=args.page_size,
                max_pages=args.max_pages,
                profile_types=args.profile_type,
                statuses=args.status,
                countries=args.country,
                comparison_date=args.comparison_date,
                sort_order=args.sort_order,
                from_date=args.from_date,
                to_date=args.to_date,
            )
            if item is None:
                print("NOT FOUND", file=sys.stderr)
                return 2
            print(json.dumps({
                "summary": profile_summary(item),
                "profile": item,
            }, ensure_ascii=False, indent=2))
            return 0

        if args.command == "labels":
            kwargs = dict(
                data_type=args.data_type,
                page=args.page,
                page_size=args.page_size,
                from_date=args.from_date,
                to_date=args.to_date,
            )
            if args.dry_run:
                print(urlencode(build_label_params(**kwargs), doseq=True))
                return 0
            print(json.dumps(fetch_labels_page(**kwargs), ensure_ascii=False, indent=2))
            return 0

        if args.command == "visibility":
            with open(args.json_file, "r", encoding="utf-8") as f:
                item = json.load(f)
            print(profile_visibility(item))
            return 0

        return 1
    except (EenApiError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
