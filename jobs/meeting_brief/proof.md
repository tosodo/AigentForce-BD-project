# proof.md — meeting_brief

## Evidence rules

- `company_summary` must be based on the company profile fields.
- `decision_maker_summary` must be based on the decision makers in the profile.
- `recommended_questions` must be tied to pain points, hiring signals, or ICP angle.
- `value_map` entries must map a need to a value proposition.

## No invented data rules

- Do NOT invent company details.
- Do NOT invent decision maker information.
- Do NOT invent solutions or value propositions not tied to the BD offering.
- Do NOT speculate on company strategy or internal plans.

## Tone rules

- Professional, concise, factual.
- Questions should be open-ended and relevant.
- Value map should be specific, not generic.

## Schema compliance

- Output must match `/af_bd_schemas/meeting_brief.json` exactly.
- Required fields: `company_summary`, `decision_maker_summary`, `recommended_questions`, `value_map`.
- `recommended_questions` must be an array of strings.
- `value_map` must be an array.
- Output must be valid JSON.

## Fail conditions

FAIL the output if:
- Any invented data appears.
- Questions are yes/no or not tied to signals.
- Value map entries are generic or invented.
- The output is not valid JSON.
- The output does not match the schema.
