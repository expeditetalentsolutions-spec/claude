# AI Search Readiness: 88/100

## What works
- All major AI crawlers explicitly allowed
- No WAF challenges
- Valid llms.txt
- Server-rendered content
- FAQPage + Speakable

## Findings
- **[Low] CCBot blocked**: Common Crawl disallowed. *Fix:* Reconsider.
- **[Low] No llms-full.txt**: 404. *Fix:* Optional.
