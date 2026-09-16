# proof.md — crm_update

## Evidence rules

- `action` must be one of the four valid actions: `create_lead`, `update_lead`, `update_company`, `log_interaction`.
- `fields` must contain only data present in the input company profile, ICP score, or outreach package.
- Timestamps must be ISO 8601 format.

## No invented data rules

- Do NOT invent CRM field values.
- Do NOT fabricate company data.
- Do NOT invent interaction outcomes.

## Schema compliance

- Output must match `/af_bd_schemas/crm_update.json` exactly.
- Required fields: `action`, `fields`.
- `action` must be a string.
- `fields` must be an object.
- Output must be valid JSON.

## Fail conditions

FAIL the output if:
- `action` is not one of the four valid actions.
- `fields` contains invented data.
- The output is not valid JSON.
- The output does not match the schema.
