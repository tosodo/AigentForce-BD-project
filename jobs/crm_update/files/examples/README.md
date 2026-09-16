# Examples — crm_update

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
    "reasoning": "Active hiring signals."
  },
  "outreach_package": {
    "company_name": "AlphaTech",
    "email_copy": "...",
    "linkedin_copy": "...",
    "follow_up_sequence": ["Follow-up 1", "Follow-up 2", "Follow-up 3"]
  },
  "crm_action": "create_lead",
  "crm_id": ""
}
```

## Example output shape

```json
{
  "action": "create_lead",
  "fields": {
    "company_name": "AlphaTech",
    "website": "https://alphatech.com",
    "industry": "SaaS",
    "hq_location": "London, UK",
    "team_size": "50-100",
    "icp_score": 65,
    "recommended_angle": "High hiring urgency — lead with speed of delivery.",
    "outreach_status": "pending",
    "created_at": "2026-09-16T10:00:00Z"
  }
}
```
