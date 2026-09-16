# Examples — outreach_generation

## Example input

```json
{
  "company": {
    "company_name": "AlphaTech",
    "website": "https://alphatech.com",
    "industry": "SaaS",
    "hq_location": "London, UK",
    "team_size": "50-100",
    "hiring_signals": ["Hiring 3 backend engineers (job_board)"],
    "decision_makers": [],
    "pain_points": ["Scaling engineering team quickly"]
  },
  "icp_score": {
    "company_name": "AlphaTech",
    "icp_score": 65,
    "score_breakdown": {
      "hiring_urgency": 16,
      "team_size_fit": 12,
      "budget_signals": 8,
      "industry_fit": 15,
      "tech_maturity": 14
    },
    "recommended_angle": "High hiring urgency — lead with speed of delivery.",
    "reasoning": "AlphaTech has active hiring signals."
  },
  "use_templates": true
}
```

## Example output shape

```json
{
  "company_name": "AlphaTech",
  "email_copy": "Subject: AlphaTech — Speed up your engineering hiring\n\nHi Hiring Team,\n\nI noticed AlphaTech is hiring 3 backend engineers. Given your focus on scaling the engineering team quickly, I thought this might be relevant.\n\nWe can help you move faster on senior engineering hires.\n\nWould you be open to a brief conversation?\n\nBest,\nAigentForce",
  "linkedin_copy": "Hi AlphaTech team,\n\nNoticed you're hiring backend engineers. Thought you might find this relevant given your scaling focus.\n\nOpen to a quick chat?\n\nAigentForce",
  "follow_up_sequence": [
    "Follow-up 1: 3 days after initial email — brief re-send.",
    "Follow-up 2: 7 days after initial email — reiterate value.",
    "Follow-up 3: 14 days after initial email — final check-in."
  ]
}
```
