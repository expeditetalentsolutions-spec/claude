"""Command-line entry point: python -m ad_library --help"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional

from .client import DEFAULT_API_VERSION, EU_FIELDS, AdLibraryClient, AdLibraryError, default_fields
from .export import write_ads

LOGGER = logging.getLogger("ad_library")


def _csv_list(value: str) -> List[str]:
    return [v.strip() for v in value.split(",") if v.strip()]


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="ad_library",
        description="Search Meta's Ad Library through the official Graph API and export results.",
    )
    p.add_argument("-q", "--search", help="Keywords to search for in ad text.")
    p.add_argument("--page-ids", type=_csv_list, help="Comma-separated Facebook page IDs.")
    p.add_argument(
        "-c", "--countries", type=_csv_list, default=["US"],
        help="Comma-separated ISO country codes the ads reached, or ALL (default: US).",
    )
    p.add_argument(
        "--ad-type", default="ALL",
        choices=["ALL", "POLITICAL_AND_ISSUE_ADS", "HOUSING_ADS", "EMPLOYMENT_ADS", "FINANCIAL_PRODUCTS_AND_SERVICES_ADS"],
    )
    p.add_argument("--status", default="ACTIVE", choices=["ACTIVE", "INACTIVE", "ALL"])
    p.add_argument(
        "--exact", action="store_true",
        help="Match the search as an exact phrase instead of any-order keywords.",
    )
    p.add_argument("--platforms", type=_csv_list, help="e.g. FACEBOOK,INSTAGRAM,MESSENGER,AUDIENCE_NETWORK,THREADS")
    p.add_argument("--languages", type=_csv_list, help="ISO 639-1 codes, e.g. en,es")
    p.add_argument("--media-type", choices=["ALL", "IMAGE", "MEME", "VIDEO", "NONE"])
    p.add_argument("--since", help="Delivered on/after this date (YYYY-MM-DD).")
    p.add_argument("--until", help="Delivered on/before this date (YYYY-MM-DD).")
    p.add_argument("--fields", type=_csv_list, help="Override the requested fields.")
    p.add_argument("--eu-fields", action="store_true", help="Also request EU/UK transparency fields (reach, targeting).")
    p.add_argument("-n", "--max-items", type=int, default=100, help="Stop after this many ads (default 100, 0 = no limit).")
    p.add_argument("--page-size", type=int, default=100, help="Ads per API request (max 1000).")
    p.add_argument("-o", "--output", default="output/ads.json", help="Output file path.")
    p.add_argument("-f", "--format", choices=["json", "jsonl", "csv"], help="Output format (default: from file extension).")
    p.add_argument("--token", help="Access token (default: $META_ACCESS_TOKEN).")
    p.add_argument("--api-version", default=os.environ.get("META_API_VERSION", DEFAULT_API_VERSION))
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args(argv)

    if not args.search and not args.page_ids:
        p.error("provide --search and/or --page-ids")
    if not args.format:
        ext = Path(args.output).suffix.lower().lstrip(".")
        args.format = ext if ext in {"json", "jsonl", "csv"} else "json"
    return args


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    token = args.token or os.environ.get("META_ACCESS_TOKEN", "")

    fields = args.fields or default_fields(args.ad_type)
    if args.eu_fields:
        fields = fields + [f for f in EU_FIELDS if f not in fields]

    try:
        client = AdLibraryClient(token, api_version=args.api_version)
        ads = list(
            client.iter_ads(
                max_items=args.max_items or None,
                countries=args.countries,
                search_terms=args.search,
                page_ids=args.page_ids,
                ad_type=args.ad_type,
                active_status=args.status,
                search_type="KEYWORD_EXACT_PHRASE" if args.exact else "KEYWORD_UNORDERED",
                platforms=args.platforms,
                languages=args.languages,
                media_type=args.media_type,
                date_min=args.since,
                date_max=args.until,
                fields=fields,
                page_size=args.page_size,
            )
        )
    except (ValueError, AdLibraryError) as err:
        LOGGER.error("%s", err)
        return 1

    count = write_ads(ads, Path(args.output), args.format)
    LOGGER.info("Wrote %d ads to %s (%s)", count, args.output, args.format)
    return 0


if __name__ == "__main__":
    sys.exit(main())
