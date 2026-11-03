# Output fields

Which fields Meta fills in depends on the ad. AdSonar requests the right set by default;
override with `--fields id,page_name,...`.

## Always requested

| Field | Meaning |
|-------|---------|
| `id` | Ad Library archive ID |
| `page_id`, `page_name` | Advertiser's page |
| `ad_creation_time` | When the ad was created |
| `ad_delivery_start_time`, `ad_delivery_stop_time` | When it started / stopped running |
| `ad_creative_bodies` | Ad text (one entry per creative variant) |
| `ad_creative_link_titles`, `ad_creative_link_descriptions`, `ad_creative_link_captions` | Headline, description and display URL of the link card |
| `ad_snapshot_url` | Link to the rendered ad. Append `&access_token=YOUR_TOKEN` to open it |
| `publisher_platforms` | Facebook, Instagram, Messenger, Audience Network, Threads |
| `languages` | Languages of the creative |

## Political and issue ads (`--ad-type POLITICAL_AND_ISSUE_ADS`)

| Field | Meaning |
|-------|---------|
| `bylines` | "Paid for by" disclaimer |
| `currency` | Currency of `spend` |
| `spend` | Range; CSV columns `spend_lower`, `spend_upper` |
| `impressions` | Range; CSV columns `impressions_lower`, `impressions_upper` |
| `estimated_audience_size` | Range; CSV columns `estimated_audience_size_lower/_upper` |
| `demographic_distribution` | Share of impressions by age and gender (JSON in CSV) |
| `delivery_by_region` | Share of impressions by region (JSON in CSV) |

## EU / UK ads (`--eu-fields`)

| Field | Meaning |
|-------|---------|
| `eu_total_reach` | Estimated people reached in the EU |
| `target_ages`, `target_gender`, `target_locations` | Advertiser's targeting choices |
| `beneficiary_payers` | Who benefits from and who paid for the ad |

## CSV conventions
- Lists of plain values (e.g. platforms) are joined with ` | `.
- Ranges are split into `_lower` / `_upper` columns.
- Nested objects and lists of objects are stored as JSON strings.
