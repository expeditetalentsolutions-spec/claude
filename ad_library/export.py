"""Write ads to JSON, JSONL or CSV."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

# Preferred column order for CSV; any other fields are appended after these.
CSV_COLUMNS = [
    "id",
    "page_id",
    "page_name",
    "ad_creation_time",
    "ad_delivery_start_time",
    "ad_delivery_stop_time",
    "publisher_platforms",
    "languages",
    "ad_creative_bodies",
    "ad_creative_link_titles",
    "ad_creative_link_descriptions",
    "ad_creative_link_captions",
    "ad_snapshot_url",
    "bylines",
    "currency",
    "spend_lower",
    "spend_upper",
    "impressions_lower",
    "impressions_upper",
    "estimated_audience_size_lower",
    "estimated_audience_size_upper",
    "eu_total_reach",
]

RANGE_FIELDS = ("spend", "impressions", "estimated_audience_size")


def flatten_ad(ad: Dict[str, Any]) -> Dict[str, Any]:
    """Make one ad CSV-friendly: split ranges, join lists, JSON-encode the rest."""
    row: Dict[str, Any] = {}
    for key, value in ad.items():
        if key in RANGE_FIELDS and isinstance(value, dict):
            row[f"{key}_lower"] = value.get("lower_bound", "")
            row[f"{key}_upper"] = value.get("upper_bound", "")
        elif isinstance(value, list) and all(isinstance(v, (str, int, float)) for v in value):
            row[key] = " | ".join(str(v) for v in value)
        elif isinstance(value, (list, dict)):
            row[key] = json.dumps(value, ensure_ascii=False)
        else:
            row[key] = value
    return row


def write_ads(ads: Iterable[Dict[str, Any]], path: Path, fmt: str) -> int:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    ads = list(ads)

    if fmt == "json":
        path.write_text(json.dumps(ads, ensure_ascii=False, indent=2), encoding="utf-8")
    elif fmt == "jsonl":
        with path.open("w", encoding="utf-8") as fh:
            for ad in ads:
                fh.write(json.dumps(ad, ensure_ascii=False) + "\n")
    elif fmt == "csv":
        rows = [flatten_ad(ad) for ad in ads]
        extra: List[str] = []
        for row in rows:
            for key in row:
                if key not in CSV_COLUMNS and key not in extra:
                    extra.append(key)
        present = {k for row in rows for k in row}
        columns = [c for c in CSV_COLUMNS if c in present] + extra
        with path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=columns or ["id"], extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
    else:
        raise ValueError(f"Unsupported format: {fmt}")
    return len(ads)
