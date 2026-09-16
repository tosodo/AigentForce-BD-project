# Examples — daily_report

## Example input

```json
{
  "date": "2026-09-16",
  "activities": [
    {
      "type": "lead_research",
      "company_name": "AlphaTech",
      "details": "SaaS company, London, hiring backend engineers",
      "timestamp": "2026-09-16T10:00:00Z"
    },
    {
      "type": "icp_scoring",
      "company_name": "AlphaTech",
      "details": "ICP score 65",
      "timestamp": "2026-09-16T11:00:00Z"
    },
    {
      "type": "outreach",
      "company_name": "AlphaTech",
      "details": "Email sent",
      "timestamp": "2026-09-16T12:00:00Z"
    }
  ],
  "top_opportunities": [
    {
      "company_name": "AlphaTech",
      "icp_score": 65,
      "reason": "High hiring urgency, SaaS industry fit"
    }
  ],
  "risks": [
    {
      "description": "No decision maker identified for AlphaTech",
      "severity": "medium"
    }
  ]
}
```

## Example output shape

```json
{
  "date": "2026-09-16",
  "leads_generated": 1,
  "qualified_leads": 1,
  "outreach_sent": 1,
  "meetings_booked": 0,
  "top_opportunities": [
    {
      "company_name": "AlphaTech",
      "icp_score": 65,
      "reason": "High hiring urgency, SaaS industry fit"
    }
  ],
  "risks": [
    {
      "description": "No decision maker identified for AlphaTech",
      "severity": "medium"
    }
  ]
}
```

## No activities → zeros

If there are no activities, all metrics are 0, and `top_opportunities` and `risks` are empty arrays.
