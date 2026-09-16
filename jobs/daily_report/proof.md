# proof.md — daily_report

## Evidence rules

- `leads_generated` must equal the count of `lead_research` activities in the input.
- `qualified_leads` must equal the count of `icp_scoring` activities with score > 0.
- `outreach_sent` must equal the count of `outreach` activities.
- `meetings_booked` must equal the count of `meeting` activities.
- `top_opportunities` must be derived from actual ICP scores or pipeline data.
- `risks` must be based on actual pipeline issues.

## No invented data rules

- Do NOT invent activity counts.
- Do NOT invent ICP scores.
- Do NOT invent company names in top opportunities.
- Do NOT fabricate risks.

## Schema compliance

- Output must match `/af_bd_schemas/daily_report.json` exactly.
- `date` must be a string in ISO date format.
- All metric fields must be integers ≥ 0.
- `top_opportunities` and `risks` must be arrays.
- Output must be valid JSON.

## Fail conditions

FAIL the output if:
- Any metric is not counted from activities.
- Any top opportunity or risk is invented.
- The output is not valid JSON.
- The output does not match the schema.
