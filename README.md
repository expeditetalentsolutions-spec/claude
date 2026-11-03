# Meta Ad Library search tool

Searches Meta's **Ad Library** (Facebook, Instagram, Messenger, Threads, Audience Network)
through the **official Graph API `ads_archive` endpoint** and exports results to JSON, JSONL or CSV.
No browser automation or HTML scraping is involved, so it doesn't break when the site changes
and stays within Meta's terms.

## What data you can get

Meta's API returns different amounts of data depending on the ad:

| Ads | What the API returns |
|-----|----------------------|
| **Political / issue ads**, all countries | Full detail: creative text, dates, platforms, snapshot link, spend and impression ranges, audience size, demographic and regional breakdowns, "paid for by" bylines |
| **Any ad delivered in the EU or UK** | Creative text, dates, platforms, snapshot link, plus (with `--eu-fields`) EU reach, targeted ages, gender and locations, payer/beneficiary |
| Other commercial ads outside the EU/UK | Generally **not returned** by the API (they're only visible on the Ad Library website) |

So for commercial competitor research, search with `--countries` set to EU countries or `GB`.

## Setup (one time)

1. Go to <https://www.facebook.com/ID> and **confirm your identity** (government ID; can take a day or two).
2. Create an app at <https://developers.facebook.com/apps> (type "Business" is fine).
3. Accept the Ad Library API terms at <https://www.facebook.com/ads/library/api>.
4. Generate a **user access token** in the [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
   for your app. Short-lived tokens last ~1 hour; exchange it for a long-lived (~60 day) token
   via the [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/) → "Extend Access Token".
5. Install and configure:

```bash
pip install -r requirements.txt
```

```bash
export META_ACCESS_TOKEN="your-token-here"
```

## Usage

```bash
python -m ad_library --search "running shoes" --countries GB,DE,FR -n 200 -o output/shoes.csv
```

```bash
python -m ad_library --page-ids 15087023444 --countries ALL --status ALL --eu-fields -o output/page.json
```

```bash
python -m ad_library -q "climate" --ad-type POLITICAL_AND_ISSUE_ADS -c US --since 2026-01-01 -o output/climate.jsonl
```

Key options (run `python -m ad_library --help` for all):

| Option | Meaning |
|--------|---------|
| `-q, --search` | Keywords in ad text (`--exact` for exact phrase) |
| `--page-ids` | Comma-separated advertiser page IDs (find one in an ad's Ad Library page URL) |
| `-c, --countries` | ISO codes the ads reached, comma-separated, or `ALL` (default `US`) |
| `--ad-type` | `ALL`, `POLITICAL_AND_ISSUE_ADS`, `HOUSING_ADS`, `EMPLOYMENT_ADS`, `FINANCIAL_PRODUCTS_AND_SERVICES_ADS` |
| `--status` | `ACTIVE` (default), `INACTIVE`, `ALL` |
| `--platforms` | `FACEBOOK,INSTAGRAM,MESSENGER,AUDIENCE_NETWORK,THREADS` |
| `--since / --until` | Delivery date range, `YYYY-MM-DD` |
| `--eu-fields` | Also request EU/UK transparency fields |
| `-n, --max-items` | Max ads to fetch (default 100, `0` = all) |
| `-o, --output` | Output path; format is picked from the extension (`.json`, `.jsonl`, `.csv`) or `-f` |
| `--api-version` | Graph API version (default `v23.0`, or `$META_API_VERSION`) |

The tool follows pagination automatically and backs off and retries on rate limits
(error codes 4, 17, 32, 613, 80004) and transient 5xx errors.

CSV output joins list fields with ` | `, splits spend/impression ranges into `_lower` / `_upper`
columns, and stores nested breakdowns as JSON strings.

### Creative images and videos

The API doesn't return image or video files. Each ad has an `ad_snapshot_url` that opens the
rendered ad (with its media) in a browser; opening it requires appending your access token.

## Use from Python

```python
from ad_library import AdLibraryClient

client = AdLibraryClient(access_token="...")
for ad in client.iter_ads(max_items=50, countries=["GB"], search_terms="coffee"):
    print(ad["page_name"], ad.get("ad_creative_bodies"))
```

## Tests

```bash
python -m unittest discover -s tests -t . -v
```

The tests use a fake HTTP session, so they need no token or network.
