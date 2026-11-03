# Changelog

All notable changes to AdSonar are documented here. Versions follow [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-11-03

### Added
- `adsonar` command-line tool and `AdLibraryClient` Python API for Meta's official Ad Library API (`ads_archive`).
- Search by keywords (any-order or exact phrase) or advertiser page IDs.
- Filters: countries, ad type, active status, platforms, languages, media type, delivery date range.
- Optional EU/UK transparency fields (`--eu-fields`) and automatic political-ad fields.
- Automatic pagination with a `--max-items` limit.
- Retry with exponential backoff on rate limits and transient errors.
- Export to JSON, JSONL and CSV (ranges split into lower/upper columns).
- `.env` file support, `--quiet` / `--verbose` logging, top-advertiser summary.
