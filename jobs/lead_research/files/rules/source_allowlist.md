# Source Allowlist — lead_research

## Allowed sources

- **job_board** — public job listings (e.g., external job boards)
- **careers_page** — company careers/jobs pages
- **linkedin_public** — publicly visible LinkedIn company/role pages
- **news** — public news articles about hiring or company growth

## Forbidden sources

- Private LinkedIn data (non-public profiles)
- Paid databases
- CRM data
- Email inference from patterns
- Any source not explicitly listed in allowed_sources

## Rule

Only query sources that appear in the job input's `allowed_sources` array. If a source is not in that array, do not use it.
