# SEO Audit: expeditehcs.com

**Date:** 2026-11-16  
**Tool:** claude-seo v2.6.2 (scripts run inline; specialist agents not loaded in this session)  
**Scope:** all 17 URLs in the XML sitemap (16 live + 1 that returns 404), plus robots.txt, llms.txt, headers, schema, rendering and lab performance  
**Business type detected:** B2B healthcare staffing and Health IT consulting agency (hybrid: national service area, physical HQ in Alpharetta, GA). The site is aimed at two audiences: hospitals hiring staff and nurses looking for jobs.

---

## Executive summary

### SEO Health Score: **68 / 100**

| Category | Weight | Score | Weighted |
|---|---|---|---|
| Technical SEO | 22% | 72 | 15.8 |
| Content Quality | 23% | 65 | 15.0 |
| On-Page SEO | 20% | 68 | 13.6 |
| Schema / Structured Data | 10% | 55 | 5.5 |
| Performance (CWV) | 10% | 60 | 6.0 |
| AI Search Readiness | 10% | 88 | 8.8 |
| Images | 5% | 75 | 3.8 |
| **Total** | | | **68** |

The foundations are good. Pages are server-rendered, each has a self-referencing canonical, robots.txt is clean, AI crawler policy is unusually well done, and there is a valid llms.txt. What holds the score down is a few specific problems: the job-posting markup, a broken `www.` host, an 8.8 MB video on every page view, and thin trust signals for a healthcare-adjacent business.

### Top 5 critical / high issues
1. **`www.expeditehcs.com` has an invalid TLS certificate** (hostname mismatch). Anyone who types `www.`, or follows an old backlink to it, gets a browser security warning and cannot reach the site. (High)
2. **JobPosting markup breaks Google's job-posting rules.** All 18 postings sit on one listing page (`/nursing-careers/`), and every one is marked `jobLocationType: TELECOMMUTE` (fully remote) although they are on-site bedside roles in named cities. Google says this can lead to a structured-data manual action and removal from Google for Jobs. (High)
3. **An 8.8 MB video downloads on every homepage visit, mobile included.** The same 4.5 MB MP4 autoplays in the hero and again in the footer, and the two references use different URL forms (`https://expeditehcs.com/images/…` and `./images/…`), so it is downloaded twice. The footer copy appears on all 16 pages. (High)
4. **The sitemap lists a URL that returns 404:** `/case-study/healthcare-data-management/`. (High)
5. **Case studies have no named clients, authors, or dates**, and the "500+ clients / 10,000+ professionals placed" figures appear only in llms.txt, not on the site. That weakens E-E-A-T for a healthcare (YMYL-adjacent) brand, and AI answers may cite claims visitors can't verify. (Medium-High)

### Top 5 quick wins
1. Remove the dead case-study URL from `sitemap.xml`, or publish the page (5 minutes).
2. Point the footer video at the same absolute URL as the hero, or replace it with its poster image. That saves about 4.5 MB on every page (15 minutes).
3. Change `jobLocationType` and remove `TELECOMMUTE` from on-site jobs (15 minutes).
4. Add `Strict-Transport-Security` in Apache (5 minutes).
5. Shorten 12 titles to 60 characters or fewer and 11 meta descriptions to 160 or fewer (1 hour).

---

## Technical SEO: 72

**What works**
- HTTP → HTTPS is a single-hop 301 (`http://expeditehcs.com/` → `https://expeditehcs.com/`).
- Real 404s: an unknown URL returns 404, not a soft-404 200.
- Every live page has a self-referencing canonical, `index, follow`, `lang="en"`, a viewport tag and UTF-8.
- robots.txt is reachable, declares the sitemap, and has explicit groups for 16 crawlers.
- The XML sitemap is valid (17 URLs, no duplicates, no cross-host URLs).
- `/about` → `/about/` 301s to the trailing-slash form consistently.
- `X-Content-Type-Options`, `X-Frame-Options` and `Referrer-Policy` are present.

**Findings**

| Severity | Finding | Evidence | Fix |
|---|---|---|---|
| High | `www.` host serves a certificate that doesn't cover it | `SSL: no alternative certificate subject name matches target host name 'www.expeditehcs.com'` (curl and Python both fail) | Reissue the certificate with both `expeditehcs.com` and `www.expeditehcs.com` (Let's Encrypt or cPanel AutoSSL covers both), then 301 `www` → apex. The same problem exists on `www.expeditets.co.in`. |
| High | Sitemap URL returns 404 | `/case-study/healthcare-data-management/` → 404. It isn't linked from the case-study hub, so it is sitemap-only. | Publish the page and link it from `/case-study/`, or remove it from the sitemap. |
| Medium | No HSTS header | `Strict-Transport-Security` not sent | `Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"` once `www` has a valid certificate. |
| Low | Every sitemap `lastmod` is identical (2026-10-19) | 17/17 share one date | Generate `lastmod` from each page's real modification time; identical dates teach Google to ignore the field. |
| Low | No Content-Security-Policy or Permissions-Policy | Headers absent | Start with `Content-Security-Policy-Report-Only`. |
| Info | `Vary: User-Agent` on HTML | Response header | Fine if intentional. It reduces CDN cache hit rates; drop it unless content really differs by user agent. |

## Content quality: 65

**What works:** service pages are substantive (`/nursing-careers/` 1,518 words, `/job-seekers/` 1,429, `/healthcare-staffing/` 767). Case studies are 530–716 words with concrete metrics. Content is in the initial HTML, with no JavaScript dependency.

| Severity | Finding | Evidence | Fix |
|---|---|---|---|
| Medium-High | Case studies are anonymous and undated, with no author | For example "A national health system operating 14 acute care hospitals…", with no client name, quote attribution, date or byline on any of the 6 | Add a date, an author (a named recruiter or IT lead with credentials), and a named client or permissioned testimonial where possible. Even "Regional health system, Southeast US (2025)" plus a named Expedite lead adds credibility. |
| Medium | Thin case-study hub | `/case-study/`: 116 words | Add an intro covering services and outcomes, and a one-line result per case. |
| Medium | Claims differ between llms.txt and the site | llms.txt says "500+ clients", "10,000+ professionals placed" and "97% retention". The pages show 5 days / 95% / 97% and "thousands of nurses". 500+ and 10,000+ appear nowhere on-site. | Put the same verifiable figures on the About page, or remove them from llms.txt. AI systems quote llms.txt. |
| Medium | Thin trust signals on About | 393 words; no leadership names or photos, licences or certification proof | Add a leadership team with bios, a link to the Joint Commission certification (Quality Check listing), minority/woman-owned certification body and number, and an address map. |
| Low | Brand ambiguity | About page title: "About Expedite Healthcare Solutions — DBA Expedite Talent Solutions"; the header links to Expedite Talent Solutions | Use one primary brand per domain; keep the DBA in the footer and in schema `alternateName`. |

## On-page SEO: 68

| Severity | Finding | Evidence | Fix |
|---|---|---|---|
| Medium | 12 of 16 titles exceed about 60 characters | Home 73, `/healthcare-staffing/` 84, `/job-seekers/` 79, `/healthcare-it-solutions/` 76… | For example, home: "Healthcare Staffing Agency & Health IT \| Expedite HCS" (53). Put the keyword first and the brand last and short. |
| Medium | 11 meta descriptions exceed 160 characters | Home 226, `/nursing-careers/` 211, `/healthcare-staffing/` 206 | Trim to 140–155 characters with one CTA. |
| Medium | Generic H1s on money pages | `/healthcare-staffing/` H1: "Let's Start Something Big Together"; `/contact/`: "Let's Connect"; home H1 lacks "healthcare staffing agency" | `/healthcare-staffing/` → "Healthcare Staffing Services: Allied, Clinical & Non-Clinical". Home → "Healthcare Staffing Agency: Nurses Placed in 5 Days". |
| Medium | 8 links per page have no accessible text | Icon or image links to `/healthcare-it-solutions/`, `/healthcare-staffing/`, `/nursing-careers/`, `/job-seekers/` and case studies; the footer logo has `alt=""` | Add `aria-label` or descriptive `alt` (the footer logo alt should be "Expedite Healthcare Solutions home"). |
| Low | Generic anchors | 5 × "Learn More" on home | "Explore healthcare staffing services", etc. |
| Low | Heading-level skips | Home, staffing, IT, nursing, contact, legal pages (H2 → H4) | Use sequential levels. |
| Medium (conversion) | No hiring CTA above the fold on mobile | Mobile hero shows only "Discover the world of Expedite ↓"; "Get in Touch" is desktop-only in the top bar | Add a "Request Staff" button in the hero, and a secondary "Find Nursing Jobs" button. |

## Schema / structured data: 55

**Present:** Organization (all pages), WebSite with SearchAction, WebPage, LocalBusiness, BreadcrumbList, FAQPage, SpeakableSpecification (home); Service and BreadcrumbList (staffing, IT); EmploymentAgency, FAQPage and 18 × JobPosting (`/nursing-careers/`). All blocks parse as valid JSON-LD.

| Severity | Finding | Evidence | Fix |
|---|---|---|---|
| High | JobPosting on a listing page | 18 JobPosting objects on `/nursing-careers/`, which has no per-job detail pages. Google requires the markup on the page for that single job only. | Create one URL per job (for example `/jobs/cardiac-telemetry-rn-stockbridge-ga/`) with one JobPosting each; remove JobPosting from the listing page. |
| High | `jobLocationType: TELECOMMUTE` on on-site jobs | Every posting, for example "Cardiac Telemetry RN", with `jobLocation` Stockbridge, GA | Remove `jobLocationType` (use it only for 100% remote roles). Misrepresenting remote status is a listed policy violation. |
| Medium | JobPosting missing `baseSalary` and `identifier` | Keys present: title, description, datePosted, validThrough, employmentType, hiringOrganization, jobLocation… | Add `baseSalary` (a weekly range for travel roles) and an `identifier`. Salary strongly affects click-through in Google for Jobs. |
| Medium | Every posting expires 2026-12-31, and all were posted 2026-10-01 | Bulk dates | Use real dates per job; update `validThrough` or remove filled jobs promptly. |
| Medium | Duplicate, inconsistent Organization nodes on the homepage | Two Organization nodes, one without `@id`, with different `sameAs` lists (one includes expeditets.com) | Keep one Organization with `@id` `https://expeditehcs.com/#organization` and reference it everywhere. |
| Low | `/job-seekers/` (1,429 words of job content) has no JobPosting | Organization only | Covered by the per-job pages above. |
| Low | Case studies have no Article schema | Organization only | Add `Article` with `author`, `datePublished`, `publisher`. |
| Low | `WebSite` → `SearchAction` with no site search | No search UI found | Remove it, or implement search. |
| Info | `LocalBusiness` could be more specific | Generic type on home | Use `EmploymentAgency` (already used on `/nursing-careers/`) consistently. |

## Performance: 60

PageSpeed Insights / CrUX field data could not be fetched: Google's keyless quota was rate-limited and no API key is configured. The figures below are lab measurements in headless Chromium through this environment's proxy, so treat them as rough.

| Metric | Mobile (Pixel 7) | Desktop | Threshold |
|---|---|---|---|
| TTFB | 676 ms | 193 ms | < 800 ms |
| LCP | 1.44 s (hero paragraph) | 0.90 s (H1) | < 2.5 s ✅ |
| CLS | 0.00 | 0.065 | < 0.1 ✅ |
| Requests | 35 | 35 | |
| Page weight | **≈ 9.6 MB** (8.8 MB video, 755 KB images) | same | |

| Severity | Finding | Fix |
|---|---|---|
| High | 4.5 MB MP4 downloaded twice on home and once on every other page (footer) | Use one identical absolute URL; set `preload="none"` on the footer video and start it with IntersectionObserver; serve a ≤ 1.5 MB 720p H.264 plus WebM/AV1, and a poster-only version on mobile (`(max-width: 768px)`) and for `prefers-reduced-motion`. |
| Medium | 16 PNGs (client logos about 55–61 KB each, logo 77 KB) | Convert logos to SVG or WebP; the header logo can be SVG. |
| Low | 6 SVG images without width/height | Add dimensions to prevent shifts (desktop CLS 0.065 is close to the limit). |
| Low | No `fetchpriority="high"` on the LCP element and no speculation rules | Add `<script type="speculationrules">` to prerender `/healthcare-staffing/` and `/nursing-careers/`. |
| Info | Google Fonts loaded from a third party | Self-host the font and `preload` it. |

## AI search readiness: 88

**Strong.** Content is server-rendered (462 words without JS). robots.txt names and allows GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-SearchBot, Claude-User, PerplexityBot, Google-Extended, Applebot(-Extended) and Bingbot, and none are challenged by a WAF (all returned 200 in the user-agent test). `llms.txt` is present and well-formed (3.6 KB). FAQPage and Speakable markup exist on home.

| Severity | Finding | Fix |
|---|---|---|
| Medium | llms.txt claims not backed by on-site content (see Content) | Align them. |
| Low | `CCBot` is blocked | Common Crawl feeds many AI and search datasets and backlink tools; blocking it reduces AI visibility. Reconsider. |
| Low | No `llms-full.txt` (404) | Optional: publish the full service and case-study text. |
| Info | No Markdown negotiation, WebMCP or `.well-known` agent files | Not needed for a staffing site today. |

## Images: 75

44 `<img>` on home: 25 SVG, 16 PNG, 15 with `loading="lazy"`. One image has no alt (the Facebook tracking pixel, which is fine). 4 have empty alt: decorative arrows (correct) and the footer logo, which links home and needs alt text. 6 SVGs lack dimensions. Formats: see Performance.

---

## Not covered in this run
- **Google Search Console, GA4 and CrUX field data:** no Google credentials configured.
- **Backlinks (Moz, Bing, Common Crawl), DataForSEO SERP positions, Google Business Profile and Maps:** no API keys, and this environment only allows the Expedite domains.
- **Off-site NAP consistency** (directories, GBP) needs network access beyond the allowed domains.
- **Browser sandbox:** Chromium ran as root in this container, so pages were rendered without Chromium's sandbox.
