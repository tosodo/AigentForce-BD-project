# SKILL.md — lead_research (AF_ResearchAgent)

## Purpose

Discover companies that match a given niche and geography. Produce structured company profiles strictly following `/af_bd_schemas/company_profile.json`.

This job is the entry point of the AigentForce BD pipeline. All downstream jobs depend on its output.

## When to use

- A new BD campaign begins with a niche + geography target.
- The orchestrator invokes this job before any scoring, outreach, CRM sync, or meeting prep.
- Re-run when campaign parameters change or when the lead list needs refreshing.

## Inputs

The orchestrator passes exactly this JSON object:

```json
{
  "niche": "",
  "geography": "",
  "min_company_count": 0,
  "max_companies": 0,
  "allowed_sources": [
    "job_board",
    "careers_page",
    "linkedin_public",
    "news"
  ]
}
```

Field rules:
- `niche` — required
- `geography` — required
- `allowed_sources` — required
- `min_company_count` — optional
- `max_companies` — optional
- If any required field is missing → return `[]`

## Steps

1. **Validate input.** Confirm niche, geography, and allowed_sources are present. If not → return `[]`.
2. **Query allowed sources only.** Use only the data sources listed in `allowed_sources`. Forbidden sources include private LinkedIn data, paid databases, CRM data, and any source not in the allow-list.
3. **Filter by niche + geography.** Keep only companies that match both.
4. **Prioritize by hiring signals.** Prefer companies with clear hiring signals (recent job posts, careers pages, hiring announcements).
5. **Build company profiles.** For each qualifying company, produce a `company_profile.json` object.
6. **Enforce schema compliance.** Every output object must match the schema exactly. Unknown fields → `""` or `[]`.
7. **Cap output size.** Never exceed `max_companies`. If fewer companies are found than `min_company_count`, return what you have without guessing.
8. **Return JSON array.** Output must be a JSON array of company profiles. No commentary outside the JSON.

## Decisions

- **Source gating:** Only use allowed_sources. If a signal comes from a disallowed source, discard it.
- **Email handling:** Never invent email patterns. If email is not explicitly available from a safe public source, leave it as `""`.
- **LinkedIn URL:** Include only if a public profile is clearly identified.
- **Decision makers:** Only include people whose role clearly relates to hiring or talent (Head of Talent, HR Director, Engineering Manager, Recruitment Lead).
- **Pain points:** Derive from observable signals only. Rapid hiring → "Scaling team quickly." Repeated posts for same role → "Struggling to fill role." No speculation.

## Definition of done

- Returns a JSON array of company profiles
- Every object matches `/af_bd_schemas/company_profile.json`
- No fabricated companies, people, or contact details
- No commentary outside JSON
- Output respects `max_companies` cap

## Edge cases

- **No companies found:** Return `[]`. Do not explain. Do not guess.
- **Partial data:** Unknown fields → `""` or `[]`. Never fabricate.
- **Too many results:** Respect `max_companies`. Prioritize strongest hiring signals.
- **Fewer than min_company_count:** Return what you have. Do not pad.
- **Invalid input:** Missing required fields → return `[]`.

## Schema contract

Output matches: `/af_bd_schemas/company_profile.json`

```json
[
  {
    "company_name": "",
    "website": "",
    "industry": "",
    "hq_location": "",
    "team_size": "",
    "hiring_signals": [],
    "decision_makers": [
      {
        "full_name": "",
        "role": "",
        "email": "",
        "linkedin_url": ""
      }
    ],
    "pain_points": []
  }
]
```

## Files

- `files/templates/company_profile_template.json` — blank template
- `files/rules/source_allowlist.md` — allowed vs forbidden sources
- `files/examples/` — example inputs and outputs

## Proof requirements

See `proof.md`. All hiring signals must trace to a source. No invented emails, names, team sizes, or companies.

## Notes

See `notes.md`. Log failures, diagnose root causes, add durable fixes.
