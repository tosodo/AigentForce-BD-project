# Examples — lead_research

## Example input

```json
{
  "niche": "SaaS companies hiring SDRs",
  "geography": "London, UK",
  "min_company_count": 5,
  "max_companies": 10,
  "allowed_sources": ["job_board", "careers_page", "linkedin_public", "news"]
}
```

## Example output shape

```json
[
  {
    "company_name": "Example SaaS Ltd",
    "website": "https://example.com",
    "industry": "SaaS",
    "hq_location": "London, UK",
    "team_size": "",
    "hiring_signals": [
      "Hiring 2 SDRs (job_board, 2026-09-15)"
    ],
    "decision_makers": [],
    "pain_points": ["Scaling sales team"]
  }
]
```

## Invalid input → empty output

Input missing `niche`, `geography`, or `allowed_sources` → return `[]`.
