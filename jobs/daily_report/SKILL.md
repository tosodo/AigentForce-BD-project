# SKILL.md — daily_report

## Purpose

Generate a daily BD activity report. Produce a `daily_report.json` containing date, leads generated, qualified leads, outreach sent, meetings booked, top opportunities, and risks.

This job runs at the end of each BD day or when the orchestrator requests a summary.

## When to use

- End of day, when the BD team needs a summary of activity.
- When the orchestrator requests a pipeline status report.
- When leadership needs a daily snapshot of BD performance.

## Inputs

The orchestrator passes exactly this JSON object:

```json
{
  "date": "2026-09-16",
  "activities": [
    {
      "type": "lead_research | icp_scoring | outreach | crm_update | meeting | other",
      "company_name": "",
      "details": "",
      "timestamp": ""
    }
  ],
  "top_opportunities": [
    {
      "company_name": "",
      "icp_score": 0,
      "reason": ""
    }
  ],
  "risks": [
    {
      "description": "",
      "severity": "low | medium | high"
    }
  ]
}
```

Field rules:
- `date` — required. ISO date format.
- `activities` — optional. Array of activity records.
- `top_opportunities` — optional. Array of top opportunity summaries.
- `risks` — optional. Array of risk descriptions with severity.

## Steps

1. **Validate input.** Confirm `date` is present. If missing → return an error object.
2. **Tally metrics.** Count leads generated, qualified leads, outreach sent, meetings booked from `activities`.
3. **Identify top opportunities.** From `top_opportunities` input or from the highest ICP scores in the pipeline.
4. **List risks.** From `risks` input or from pipeline issues (e.g., low ICP scores, no decision makers identified).
5. **Return output.** Return a `daily_report.json` object.

## Decisions

- **Metric counting:** Count activities by type. Each `lead_research` activity counts as a lead generated. Each `icp_scoring` with score > 0 counts as qualified. Each `outreach` counts as outreach sent. Each `meeting` counts as meeting booked.
- **Top opportunities:** Select the top 3–5 companies by ICP score. If no ICP scores available, use qualitative reasoning.
- **Risks:** Include any pipeline gaps, missing data, or integration issues.

## Definition of done

- Returns a `daily_report.json` object
- `date` matches input
- Metrics are numeric and counted from activities
- `top_opportunities` is an array of top companies
- `risks` is an array of risk descriptions
- No invented data

## Edge cases

- **No activities:** Report zeros for all metrics. Note "no activity recorded."
- **No top opportunities:** Return empty array. Note "no qualified opportunities."
- **No risks:** Return empty array. Note "no risks identified."

## Schema contract

Output matches: `/af_bd_schemas/daily_report.json`

```json
{
  "date": "",
  "leads_generated": 0,
  "qualified_leads": 0,
  "outreach_sent": 0,
  "meetings_booked": 0,
  "top_opportunities": [],
  "risks": []
}
```

## Files

- `files/templates/daily_report_template.json` — blank template
- `files/examples/` — example inputs and outputs

## Proof requirements

See `proof.md`. Metrics must be counted from activities. No invented numbers.

## Notes

See `notes.md`. Log metric discrepancies, missing data, and reporting gaps.
