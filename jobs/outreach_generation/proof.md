# proof.md — outreach_generation

## Evidence rules

- `company_name` must match the input company profile exactly.
- `email_copy` and `linkedin_copy` must reference only data present in the company profile and ICP score.
- Follow-up timing must be stated clearly (e.g., "Follow-up 1: 3 days after initial email").

## No invented data rules

- Do NOT invent decision maker names.
- Do NOT invent email addresses.
- Do NOT invent company details, pain points, or hiring signals.
- Do NOT claim relationships or past interactions that did not occur.

## Tone rules

- Professional and concise.
- No hype, no exaggeration.
- Factual framing based on hiring signals and ICP angle.

## Schema compliance

- Output must match `/af_bd_schemas/outreach_package.json` exactly.
- Required fields: `company_name`, `email_copy`, `linkedin_copy`, `follow_up_sequence`.
- `follow_up_sequence` must be an array.
- Output must be valid JSON.

## Fail conditions

FAIL the output if:
- Any invented data appears (names, emails, details).
- The output is not valid JSON.
- The output does not match the schema.
- `email_copy` or `linkedin_copy` is empty when input data is sufficient.
- Any claim is made that cannot be traced to the input.
