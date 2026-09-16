# SKILL.md — icp_scoring (AF_QualificationAgent)

## Purpose

Score each company profile from `lead_research` against the Ideal Customer Profile (ICP). Produce deterministic ICP score objects following `/af_bd_schemas/icp_score.json`.

This job runs immediately after `lead_research` in the pipeline.

## When to use

- After `lead_research` produces company profiles.
- When the BD team needs to prioritize which companies to pursue.
- When scoring weights need to be recalibrated for a campaign.

## Inputs

The orchestrator passes exactly this JSON object:

```json
{
  "companies": [
    {
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
    }
  ],
  "scoring_weights": {
    "hiring_urgency": 1.0,
    "team_size_fit": 1.0,
    "budget_signals": 1.0,
    "industry_fit": 1.0,
    "tech_maturity": 1.0
  }
}
```

Field rules:
- `companies` — required. Array of valid company profiles from `lead_research`.
- `scoring_weights` — required. All weights numeric and ≥ 0.
- If any weight is missing or invalid → return `[]`.
- If `companies` is empty → return `[]`.
- If any required field is missing → return `[]`.

## Steps

1. **Validate input.** Confirm `companies` is present and is an array. Confirm `scoring_weights` has all five numeric weights ≥ 0. If invalid → return `[]`.
2. **Score each company.** For each company in `companies`, compute five dimension scores (0–20 each):
   - Hiring urgency
   - Team size fit
   - Budget signals
   - Industry fit
   - Tech maturity
3. **Compute final score.** `icp_score = sum(score_breakdown.values())`. Must be 0–100.
4. **Derive recommended angle.** From observable signals only. Examples:
   - "High hiring urgency — lead with speed of delivery."
   - "Strong tech maturity — lead with senior engineering talent."
   - "Industry match — lead with niche-specific candidate pools."
   - "Budget signals weak — lead with flexible engagement models."
5. **Write reasoning.** Factual, concise, 1–3 sentences, based solely on the company profile. No assumptions.
6. **Return JSON array.** Output must be a JSON array of ICP score objects. No commentary outside JSON.

## Decisions

- **Unknown data:** If a signal is missing, score that dimension as 0. Never fabricate budget signals, tech maturity, or industry fit.
- **Score caps:** Each dimension max 20. Total max 100. Integer values only.
- **Recommended angle:** Derived from observable signals only. No speculative language.
- **No external lookups:** This job does not fetch external data. It operates only on the company profiles provided.

## Definition of done

- Returns a JSON array of ICP scoring objects
- Every object matches `/af_bd_schemas/icp_score.json`
- `icp_score` is integer 0–100
- `score_breakdown` values are integers 0–20
- `recommended_angle` and `reasoning` derived from observable signals only
- No commentary outside JSON

## Edge cases

- **Empty companies:** Return `[]`.
- **Invalid scoring weights:** Return `[]`.
- **All signals missing:** Score 0 across all dimensions, `recommended_angle = ""`, `reasoning = ""`.
- **Weak signals:** Score conservatively. Never inflate.

## Schema contract

Output matches: `/af_bd_schemas/icp_score.json`

```json
[
  {
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
  }
]
```

## Scoring dimensions

### A. Hiring Urgency (0–20)
Based on hiring_signals count + recency.
- Many open roles → higher score
- Repeated postings → higher score
- No hiring signals → 0

### B. Team Size Fit (0–20)
Based on team_size field.
- If team_size unknown → 0
- If team_size aligns with niche → higher score

### C. Budget Signals (0–20)
Derived ONLY from observable indicators:
- Funding announcements (news)
- Large hiring waves
- Senior roles being hired
- If no signals → 0

### D. Industry Fit (0–20)
Based on industry field.
- If industry matches niche → higher score
- If unknown → 0

### E. Tech Maturity (0–20)
Derived from:
- Presence of engineering roles
- Presence of technical leadership
- Public tech stack mentions (news, job posts)
- If no signals → 0

## Files

- `files/templates/icp_score_template.json` — blank template
- `files/examples/` — example inputs and outputs

## Proof requirements

See `proof.md`. Scores must cite evidence from the company profile. No invented metrics.

## Notes

See `notes.md`. Log scoring discrepancies, calibration issues, and edge cases.
