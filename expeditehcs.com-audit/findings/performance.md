# Performance (CWV): 60/100

## What works
- Lab LCP 1.4 s mobile / 0.9 s desktop
- CLS 0.00 mobile / 0.065 desktop

## Findings
- **[High] 8.8 MB video payload**: Same 4.5 MB MP4 fetched twice via different URLs; footer video on every page. *Fix:* Single URL, preload=none, compress, poster on mobile.
- **[Medium] PNG logos**: 16 PNGs, 48–77 KB each. *Fix:* SVG/WebP.
- **[Low] No LCP hints/speculation rules**: No fetchpriority or speculationrules. *Fix:* Add hints.
