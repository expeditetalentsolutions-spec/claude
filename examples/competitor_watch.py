"""Example: track several competitors' live ads in the UK and save one CSV each.

Usage:
    python examples/competitor_watch.py 15087023444 20531316728
"""

import sys
from pathlib import Path

from adsonar import AdLibraryClient
from adsonar.envfile import load_env_file
from adsonar.export import write_ads

import os


def main(page_ids):
    load_env_file()
    client = AdLibraryClient(os.environ.get("META_ACCESS_TOKEN", ""))
    for page_id in page_ids:
        ads = list(
            client.iter_ads(
                max_items=500,
                countries=["GB"],
                page_ids=[page_id],
                active_status="ACTIVE",
            )
        )
        name = ads[0].get("page_name", page_id) if ads else page_id
        out = Path("output") / f"competitor_{page_id}.csv"
        write_ads(ads, out, "csv")
        print(f"{name}: {len(ads)} active ads -> {out}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
