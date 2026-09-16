# Examples — meeting_brief

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
    "decision_makers": [
      {
        "full_name": "Jane Smith",
        "role": "Head of Talent",
        "email": "",
        "linkedin_url": ""
      }
    ],
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
    "reasoning": "Active hiring signals."
  },
  "meeting_context": {
    "meeting_type": "discovery",
    "meeting_date": "2026-09-20",
    "attendees": ["Jane Smith"]
  }
}
```

## Example output shape

```json
{
  "company_summary": "AlphaTech is a SaaS company based in London, UK, with 50-100 employees. They are currently hiring 3 backend engineers and looking to scale their engineering team quickly.",
  "decision_maker_summary": "Jane Smith is the Head of Talent at AlphaTech. She is likely the key contact for hiring-related discussions.",
  "recommended_questions": [
    "What is your timeline for filling the backend engineer roles?",
    "How are you currently sourcing senior engineering talent?",
    "What challenges are you facing in filling these positions quickly?",
    "How does your team structure support rapid hiring?",
    "What would success look like for this hiring cycle?"
  ],
  "value_map": [
    {
      "need": "Scale engineering team quickly",
      "value": "Fast access to pre-screened senior backend engineers"
    },
    {
      "need": "Fill senior positions",
      "value": "Targeted outreach to passive candidates in SaaS"
    }
  ]
}
```
