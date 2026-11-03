<h1 align="center">📡 AdSonar</h1>

<p align="center">
  <strong>See what every advertiser is running, straight from Meta's official Ad Library API.</strong>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white">
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-0A7BBB">
  <img alt="License" src="https://img.shields.io/badge/license-commercial-555">
  <img alt="Data source" src="https://img.shields.io/badge/data-official%20Graph%20API-1877F2">
</p>

---

AdSonar searches Meta's Ad Library (Facebook, Instagram, Messenger, Threads and Audience Network)
and exports clean JSON, JSONL or CSV, ready for spreadsheets, BI dashboards or your own scripts.

It talks only to the **official Graph API `ads_archive` endpoint**, with no browser automation or page
scraping, so it doesn't break when the website changes and it stays within Meta's terms.

## ✨ Features

- 🔎 **Search your way.** Keywords (any order or exact phrase) or specific advertiser page IDs.
- 🌍 **Filter precisely.** Countries, ad type, active/inactive, platform, language, media type, date range.
- 📊 **Transparency data.** Spend, impressions and demographics for political ads; reach and targeting for EU/UK ads.
- 📄 **Export anywhere.** JSON, JSONL or analysis-ready CSV, with ranges split into columns.
- ♻️ **Resilient.** Automatic pagination, plus retries with backoff on rate limits and outages.
- 🐍 **CLI and Python API.** Use it from the terminal or `import adsonar` in your own code.
- 🪶 **Lightweight.** One dependency (`requests`), Python 3.9+, any OS.

## 🚀 Quick start

```bash
pip install .
```

```bash
cp .env.example .env
```

Put your Meta access token in `.env` ([how to get one](docs/SETUP.md)), then:

```bash
adsonar --search "running shoes" --countries GB,DE,FR -n 200 -o output/shoes.csv
```

```
[INFO] Page 1: 100 ads
[INFO] Page 2: 100 ads
[INFO] Wrote 200 ads to output/shoes.csv (csv)
[INFO] Top advertisers: ...
```

## 📚 Recipes

**All live ads from specific advertisers** (page IDs are in the advertiser's Ad Library URL):
```bash
adsonar --page-ids 15087023444,20531316728 -c ALL --eu-fields -o output/competitors.json
```

**Political ads with spend and demographics:**
```bash
adsonar -q "climate" --ad-type POLITICAL_AND_ISSUE_ADS -c US --status ALL --since 2026-01-01 -o output/climate.csv
```

**Instagram-only video ads, exact phrase:**
```bash
adsonar -q "free trial" --exact --platforms INSTAGRAM --media-type VIDEO -c GB -o output/trials.jsonl
```

**Everything, no limit:**
```bash
adsonar -q "solar panels" -c DE -n 0 -o output/solar.csv
```

## ⚙️ Options

| Option | Meaning |
|--------|---------|
| `-q, --search` | Keywords in the ad text (`--exact` for an exact phrase) |
| `--page-ids` | Comma-separated advertiser page IDs |
| `-c, --countries` | ISO country codes the ads reached, or `ALL` (default `US`) |
| `--ad-type` | `ALL`, `POLITICAL_AND_ISSUE_ADS`, `HOUSING_ADS`, `EMPLOYMENT_ADS`, `FINANCIAL_PRODUCTS_AND_SERVICES_ADS` |
| `--status` | `ACTIVE` (default), `INACTIVE`, `ALL` |
| `--platforms` | `FACEBOOK,INSTAGRAM,MESSENGER,AUDIENCE_NETWORK,THREADS` |
| `--languages` | ISO 639-1 codes, e.g. `en,es` |
| `--media-type` | `ALL`, `IMAGE`, `MEME`, `VIDEO`, `NONE` |
| `--since`, `--until` | Delivery date range, `YYYY-MM-DD` |
| `--eu-fields` | Add EU/UK reach and targeting fields |
| `--fields` | Request exactly these fields |
| `-n, --max-items` | Max ads (default 100, `0` = all) |
| `-o, --output` | Output file; format from extension (`.json`, `.jsonl`, `.csv`) or `-f` |
| `--token` | Access token (default `$META_ACCESS_TOKEN` or `.env`) |
| `--api-version` | Graph API version (default `v23.0`) |
| `--env-file` | Settings file to load (default `.env`) |
| `-v`, `--quiet` | More or less logging |

All output fields are described in [docs/FIELDS.md](docs/FIELDS.md).

## 🐍 Python API

```python
from adsonar import AdLibraryClient
from adsonar.export import write_ads

client = AdLibraryClient(access_token="EAAB...")
ads = list(client.iter_ads(max_items=50, countries=["GB"], search_terms="coffee"))

for ad in ads:
    print(ad["page_name"], ad.get("ad_creative_bodies"))

write_ads(ads, "output/coffee.csv", "csv")
```

See [examples/competitor_watch.py](examples/competitor_watch.py) for a multi-competitor tracker.

## 📌 What data Meta returns

| Ads | What you get |
|-----|--------------|
| **Political / issue ads**, any country | Everything: creative, dates, platforms, spend, impressions, audience size, demographic and regional breakdowns, "paid for by" |
| **Any ad delivered in the EU or UK** | Creative, dates, platforms, snapshot link; with `--eu-fields` also reach and targeting |
| Commercial ads outside the EU/UK | Generally **not available** through the API |

For commercial competitor research, search EU countries or `GB`.

Image and video files aren't included in API results. Each ad's `ad_snapshot_url` opens the rendered ad.

## 🧪 Development

```bash
pip install -e .
```

```bash
python -m unittest discover -s tests -t . -v
```

Tests use a fake HTTP session, so they need no token or network access. CI runs them on Python 3.9 to 3.13.

## 📄 License and disclaimer

AdSonar is commercial software. See [LICENSE](LICENSE) for terms of use.

AdSonar is an independent product and is **not affiliated with, endorsed by or sponsored by Meta Platforms, Inc.**
"Meta", "Facebook" and "Instagram" are trademarks of Meta Platforms, Inc. Each user must have their own Meta
developer account and access token, and is responsible for complying with Meta's
[Platform Terms](https://developers.facebook.com/terms/) and Ad Library API terms.
