# Action Plan: expeditehcs.com

Current SEO Health Score: **68/100**. Expected after Phases 1–2: **about 80**.

## Phase 1: Critical fixes (Week 1)

| # | Priority | Action | Owner | Effort |
|---|---|---|---|---|
| 1 | High | Reissue the TLS certificate to cover `www.expeditehcs.com` and add a 301 `www` → `https://expeditehcs.com/`. Do the same for `www.expeditets.co.in`. | Hosting | 30 min |
| 2 | High | Remove `jobLocationType: "TELECOMMUTE"` from all 18 JobPosting objects. | Dev | 15 min |
| 3 | High | Remove `/case-study/healthcare-data-management/` from `sitemap.xml`, or publish the page and link it from `/case-study/`. | Dev / Content | 5 min – 1 day |
| 4 | High | Make the footer video `src` identical to the hero's absolute URL, and add `preload="none"` to the footer video. | Dev | 15 min |
| 5 | Medium | Add the `Strict-Transport-Security` header (after #1). | Hosting | 5 min |

## Phase 2: High-impact improvements (Weeks 2–3)

| # | Priority | Action | Effort |
|---|---|---|---|
| 6 | High | Build one URL per job (`/jobs/<role>-<city>-<state>/`) with a single JobPosting each, including `baseSalary`, `identifier`, real `datePosted` and `validThrough`; remove JobPosting from `/nursing-careers/`; link the listing to the detail pages. | 2–3 days |
| 7 | High | Re-encode the hero video to ≤ 1.5 MB (720p H.264 + WebM), use a poster image only on mobile and for `prefers-reduced-motion`, and lazy-start the footer video. | 0.5 day |
| 8 | Medium | Rewrite 12 titles (≤ 60 characters) and 11 meta descriptions (≤ 160) with the keyword first. | 2 h |
| 9 | Medium | Rewrite generic H1s on home, `/healthcare-staffing/` and `/contact/` around target terms. | 1 h |
| 10 | Medium | Add a "Request Staff" CTA in the hero (visible on mobile) and a "Find Nursing Jobs" secondary CTA. | 2 h |
| 11 | Medium | Merge the duplicate Organization JSON-LD into one `@id` node; use `EmploymentAgency` site-wide; remove the unused `SearchAction`. | 1 h |
| 12 | Medium | Add `aria-label` or alt text to the 8 icon/image links per page; set alt on the footer logo; replace the "Learn More" anchors. | 1 h |

## Phase 3: Content and authority (Month 2)

| # | Priority | Action |
|---|---|---|
| 13 | Medium-High | Give each case study a date, a named author with credentials, and a client name or attributed testimonial where permitted; add `Article` schema. |
| 14 | Medium | Expand About with leadership bios and photos, a Joint Commission Quality Check link, and minority/woman-owned certification details. |
| 15 | Medium | Put the "500+ clients / 10,000+ placed / since 2008" stats on-site with context, or remove them from llms.txt so the two match. |
| 16 | Medium | Expand the `/case-study/` hub (116 words) with an intro and a one-line outcome per case. |
| 17 | Medium | Create service-plus-location pages for core markets (for example "Travel Nurse Staffing in Georgia", "ICU Travel Nurse Jobs in Atlanta") from real job inventory. |
| 18 | Low | Convert PNG client logos to SVG/WebP; add width/height to SVGs; self-host Google Fonts. |
| 19 | Low | Reconsider blocking `CCBot`; optionally publish `llms-full.txt`. |

## Phase 4: Monitoring (ongoing)

- Connect Google Search Console and GA4, and add a PageSpeed/CrUX API key, so the next audit includes real field data and indexing status.
- Use the Search Console **Rich results** and **Job postings** reports to confirm the JobPosting fixes are accepted.
- Keep sitemap `lastmod` tied to real edits; remove filled jobs within 24 hours.
- Re-run the audit after Phase 2 and save a drift baseline (`drift_baseline.py`).
