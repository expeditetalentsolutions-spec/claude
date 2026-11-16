# Schema / Structured Data: 55/100

## What works
- Valid JSON-LD on every page
- Organization, Service, FAQPage, BreadcrumbList, EmploymentAgency present

## Findings
- **[High] JobPosting on listing page**: 18 JobPostings on /nursing-careers/. *Fix:* One job per detail URL.
- **[High] TELECOMMUTE on on-site jobs**: All postings marked remote with physical locations. *Fix:* Remove jobLocationType.
- **[Medium] JobPosting missing baseSalary/identifier**: Recommended properties absent. *Fix:* Add salary ranges and IDs.
- **[Medium] Duplicate Organization nodes**: Two inconsistent Organization nodes on home. *Fix:* Single @id node.
- **[Low] No Article schema on case studies**: Organization only. *Fix:* Add Article with author and dates.
