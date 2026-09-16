# proof.md — icp_scoring

## Evidence rules

- Every score must be traceable to a signal in the company profile.
- `hiring_urgency` must cite hiring_signals count or recency.
- `team_size_fit` must cite the team_size field or note it is unknown.
- `budget_signals` must cite a funding announcement, large hiring wave, or senior role — or be 0 if none.
- `industry_fit` must cite the industry field or note it is unknown.
- `tech_maturity` must cite engineering roles, technical leadership, or public tech stack mentions — or be 0 if none.

## No invented data rules

- Do NOT fabricate budget signals.
- Do NOT fabricate tech maturity.
- Do NOT infer financial capability or internal strategy.
- Do NOT invent industry fit without an industry field.
- Do NOT inflate scores.

## Schema compliance

- Every output object must match `/af_bd_schemas/icp_score.json` exactly.
- `icp_score` must be integer 0–100.
- `score_breakdown` values must be integers 0–20.
- `recommended_angle` and `reasoning` must be strings.
- Output must be a JSON array. No commentary outside JSON.

## Tone and word count rules

- `reasoning`: factual, 1–3 sentences.
- `recommended_angle`: concise, derived from signals.
- No speculative or psychological language.

## Fail conditions

FAIL the output if:
- Any score is not an integer or outside its range.
- Any budget signal, tech maturity, or industry fit is invented.
- The total score does not equal the sum of the breakdown.
- The output is not valid JSON.
- The output does not match the schema.
- Any commentary appears outside the JSON array.
