# SKILL.md — crm_update

## Purpose

Sync company and lead data to the CRM. Produce a `crm_update.json` object that specifies the action and fields to update.

This job runs after `outreach_generation` in the pipeline. It ensures CRM records reflect the latest research, scoring, and outreach state.

## When to use

- After outreach is generated for a company.
- When a company's qualification status changes.
- When CRM fields need to be updated with ICP scores or outreach status.

## Inputs

The orchestrator passes exactly this JSON object:

```json
{
  "company": {
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
  },
  "icp_score": {
    "company_name": "",
    "icp_score": 0,
    "score_breakdown": {
      "hiring_urgency": 0,
      "team_size_fit": 0,
      "budget_signals": 0,
      "industry_fit": 0,
      "tech_maturity": 0
    },
    "recommended_angle": "",
    "reasoning": ""
  },
  "outreach_package": {
    "company_name": "",
    "email_copy": "",
    "linkedin_copy": "",
    "follow_up_sequence": []
  },
  "crm_action": "create_lead | update_lead | update_company | log_interaction",
  "crm_id": ""
}
```

Field rules:
- `company` — required. Company profile from `lead_research`.
- `icp_score` — required. ICP score from `icp_scoring`.
- `crm_action` — required. One of: `create_lead`, `update_lead`, `update_company`, `log_interaction`.
- `crm_id` — optional. CRM record ID if updating an existing record.

## Steps

1. **Validate input.** Confirm `company`, `icp_score`, and `crm_action` are present. If any is missing → return an error object.
2. **Determine action.** Map `crm_action` to the appropriate CRM operation.
3. **Build fields object.** Populate fields with company data, ICP score, outreach status, and timestamps.
4. **Return output.** Return a `crm_update.json` object.

## Decisions

- **create_lead:** Use when the company is new to the CRM. Include all available company data, ICP score, and outreach status.
- **update_lead:** Use when updating an existing lead. Only update fields that have changed.
- **update_company:** Use when updating company-level fields (industry, location, team size, pain points).
- **log_interaction:** Use when logging an outreach interaction. Include timestamp, channel (email/LinkedIn), and outcome.

## Definition of done

- Returns a `crm_update.json` object
- `action` is one of the four valid actions
- `fields` contains the relevant data for the action
- No invented data

## Edge cases

- **No CRM ID:** For `update_lead` or `update_company`, if no `crm_id` is provided, treat as `create_lead`.
- **Partial data:** Only include fields that are present in the input. Do not fabricate CRM fields.

## Schema contract

Output matches: `/af_bd_schemas/crm_update.json`

```json
{
  "action": "",
  "fields": {}
}
```

## Files

- `files/templates/crm_update_template.json` — blank template
- `files/examples/` — example inputs and outputs

## Proof requirements

See `proof.md`. CRM updates must be factual and based only on available data.

## Notes

See `notes.md`. Log CRM sync issues, field mapping problems, and integration failures.
