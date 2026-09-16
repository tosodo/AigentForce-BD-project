# proof.md — lead_research

## Evidence rules

Every hiring signal in a company profile must be traceable to a source:

- Each item in `hiring_signals` must include a source type in parentheses where possible:
  - `"Hiring 3 backend engineers (job_board, 2026-09-10)"`
  - `"Open roles: Talent Acquisition Partner (careers_page)"`
- Source types: `job_board`, `careers_page`, `news`, `linkedin_public`
- If no source is available, do not include the signal.

## No invented data rules

- Do NOT invent companies.
- Do NOT invent decision makers.
- Do NOT invent contact details (email, LinkedIn URL).
- Do NOT infer email patterns (e.g., firstname.lastname@domain.com).
- Do NOT fabricate team sizes, industries, or locations.
- Do NOT speculate on pain points without observable signals.

## Schema compliance

- Every output object must match `/af_bd_schemas/company_profile.json` exactly.
- Required fields present: `company_name`, `website`, `industry`, `hq_location`, `team_size`, `hiring_signals`, `decision_makers`, `pain_points`.
- `decision_makers` items must have: `full_name`, `role`, `email`, `linkedin_url`.
- Unknown fields → `""` or `[]`.
- Output must be a JSON array. No commentary outside JSON.

## Tone and word count rules

- No commentary outside the JSON array.
- Hiring signal text: short, factual, sourced.
- No speculative or psychological language about companies or decision makers.

## Fail conditions

FAIL the output if:
- Any company is invented.
- Any email or LinkedIn URL is guessed.
- Any hiring signal lacks a source.
- The output is not valid JSON.
- The output does not match the schema.
- Any commentary appears outside the JSON array.
