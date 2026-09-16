# SKILL.md — outreach_generation

## Purpose

Generate outreach copy for a scored company. Produce an `outreach_package.json` containing email copy, LinkedIn message copy, and a follow-up sequence.

This job runs after `icp_scoring` in the pipeline. It uses the ICP score and recommended angle to tailor outreach.

## When to use

- After `icp_scoring` produces ICP scores and recommended angles.
- When the BD team is ready to contact a company.
- When outreach templates need to be customized per company.

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
  "use_templates": true
}
```

Field rules:
- `company` — required. A single company profile from `lead_research`.
- `icp_score` — required. The ICP score object from `icp_scoring`.
- `use_templates` — optional. If true, use templates from `files/templates/`.

## Steps

1. **Validate input.** Confirm `company` and `icp_score` are present. If either is missing → return an error object.
2. **Load template.** If `use_templates` is true, load the appropriate template from `files/templates/`.
3. **Personalize.** Fill in company name, industry, pain points, hiring signals, and decision maker info where available.
4. **Align with angle.** Use the `recommended_angle` from ICP scoring to frame the outreach.
5. **Generate email copy.** Write a concise, factual email. No fabricated details.
6. **Generate LinkedIn copy.** Write a shorter version suitable for LinkedIn messaging.
7. **Generate follow-up sequence.** Produce a sequence of follow-up messages (e.g., day 3, day 7, day 14).
8. **Return output.** Return an `outreach_package.json` object.

## Decisions

- **Template usage:** When `use_templates` is true, start from a template and personalize. When false, generate from scratch but still follow the same structure.
- **Personalization limits:** Only use data present in the company profile and ICP score. Do not invent decision maker names, emails, or details.
- **Follow-up cadence:** Default sequence is 3 follow-ups over 2 weeks. Adjust based on hiring urgency if signals support it.
- **Tone:** Professional, concise, factual. No hype.

## Definition of done

- Returns an `outreach_package.json` object
- `email_copy` is a complete, personalized email
- `linkedin_copy` is a complete, shorter LinkedIn message
- `follow_up_sequence` is an array of follow-up messages
- No invented data

## Edge cases

- **No decision maker:** Address outreach to the company or hiring team generally.
- **No pain points:** Focus on the ICP angle and hiring signals instead.
- **Low ICP score:** Still generate outreach but note the weaker fit.

## Schema contract

Output matches: `/af_bd_schemas/outreach_package.json`

```json
{
  "company_name": "",
  "email_copy": "",
  "linkedin_copy": "",
  "follow_up_sequence": []
}
```

## Files

- `files/templates/email_template.txt` — email template
- `files/templates/linkedin_template.txt` — LinkedIn template
- `files/templates/follow_up_template.txt` — follow-up template
- `files/examples/` — example inputs and outputs

## Proof requirements

See `proof.md`. Outreach must be factual and based only on available data. No invented contact details.

## Notes

See `notes.md`. Log template effectiveness, personalization gaps, and tone issues.
