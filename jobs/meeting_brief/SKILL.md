# SKILL.md — meeting_brief

## Purpose

Prepare a pre-meeting brief for a qualified company. Produce a `meeting_brief.json` containing a company summary, decision maker summary, recommended questions, and a value map.

This job runs after `crm_update` in the pipeline. It prepares the BD team for a meeting with a high-ICP company.

## When to use

- After a company is qualified and a meeting is scheduled.
- When the BD team needs a concise briefing before a call.
- When meeting preparation needs to be standardized.

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
  "meeting_context": {
    "meeting_type": "discovery | follow_up | pitch",
    "meeting_date": "",
    "attendees": []
  }
}
```

Field rules:
- `company` — required. Company profile from `lead_research`.
- `icp_score` — required. ICP score from `icp_scoring`.
- `meeting_context` — optional. Meeting type, date, and attendees.

## Steps

1. **Validate input.** Confirm `company` and `icp_score` are present. If either is missing → return an error object.
2. **Write company summary.** Concise summary of the company based on the profile.
3. **Write decision maker summary.** For each decision maker in the profile, summarize their role and relevance.
4. **Generate recommended questions.** Based on pain points, hiring signals, and ICP angle.
5. **Build value map.** Map the company's needs to the BD offering, tied to the ICP angle.
6. **Return output.** Return a `meeting_brief.json` object.

## Decisions

- **Question quality:** Questions must be open-ended and tied to observable signals. No yes/no questions.
- **Value map:** Map each pain point or hiring signal to a specific value proposition. No invented solutions.
- **Conciseness:** Keep summaries factual and brief.

## Definition of done

- Returns a `meeting_brief.json` object
- `company_summary` is a concise, factual summary
- `decision_maker_summary` covers each decision maker
- `recommended_questions` is an array of open-ended questions
- `value_map` is an array mapping needs to value propositions
- No invented data

## Edge cases

- **No decision makers:** Note that no decision makers are identified. Questions can still be prepared for the company generally.
- **No pain points:** Focus questions on hiring signals and ICP angle instead.
- **Low ICP score:** Still prepare a brief but note the weaker fit.

## Schema contract

Output matches: `/af_bd_schemas/meeting_brief.json`

```json
{
  "company_summary": "",
  "decision_maker_summary": "",
  "recommended_questions": [],
  "value_map": []
}
```

## Files

- `files/templates/meeting_brief_template.json` — blank template
- `files/examples/` — example inputs and outputs

## Proof requirements

See `proof.md`. Meeting brief must be factual and based only on available data.

## Notes

See `notes.md`. Log question quality issues, value map gaps, and briefing effectiveness.
