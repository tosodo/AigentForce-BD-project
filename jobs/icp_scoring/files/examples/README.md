# Examples — icp_scoring

## Example input

```json
{
  "companies": [
    {
      "company_name": "AlphaTech",
      "website": "https://alphatech.com",
      "industry": "SaaS",
      "hq_location": "London, UK",
      "team_size": "50-100",
      "hiring_signals": [
        "Hiring 3 backend engineers (job_board)",
        "Open role: Head of Talent (careers_page)"
      ],
      "decision_makers": [],
      "pain_points": ["Scaling engineering team quickly"]
    }
  ],
  "scoring_weights": {
    "hiring_urgency": 1,
    "team_size_fit": 1,
    "budget_signals": 1,
    "industry_fit": 1,
    "tech_maturity": 1
  }
}
```

## Example output shape

```json
[
  {
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
    "reasoning": "AlphaTech has 2 active hiring signals including a senior Talent role, which indicates growing team and urgency. SaaS industry aligns with target niche."
  }
]
```

## Weak signals → zero scores

All signals missing → `icp_score = 0`, all breakdown values 0, `recommended_angle = ""`, `reasoning = ""`.
