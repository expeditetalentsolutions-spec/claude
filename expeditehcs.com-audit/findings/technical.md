# Technical SEO: 72/100

## What works
- Single-hop HTTP→HTTPS 301
- Real 404s
- Self-referencing canonicals on all pages
- Clean robots.txt with sitemap
- Valid XML sitemap

## Findings
- **[High] www host has invalid certificate**: Hostname mismatch for www.expeditehcs.com; visitors see a security error. *Fix:* Reissue cert for apex + www; 301 www→apex.
- **[High] Sitemap URL returns 404**: /case-study/healthcare-data-management/ is in sitemap.xml and returns 404. *Fix:* Publish the page or remove it from the sitemap.
- **[Medium] No HSTS**: Strict-Transport-Security not sent. *Fix:* Add HSTS max-age=31536000.
- **[Low] Identical lastmod on all URLs**: 17/17 = 2026-10-19. *Fix:* Use real modification dates.
