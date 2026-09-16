# AigentForce BD Project

A modular, bottom-up, deterministic BD workflow for recruitment firms, built on the Delegation Loop operating system.

## Architecture

```
jobs/                      # Six Delegation Loop jobs (pipeline order)
├── lead_research          # Discover companies matching niche + geography
├── icp_scoring            # Score ICP fit on company profiles
├── outreach_generation    # Generate email, LinkedIn, and follow-up copy
├── crm_update             # Sync to CRM (create/update/log)
├── meeting_brief          # Prepare pre-meeting briefing
└── daily_report           # Generate daily BD activity summary

af_bd_schemas/             # JSON contracts between jobs
agents/                    # Legacy agent instructions (deprecated in favor of jobs/)
pipeline/                  # Pipeline wiring: Research → Qualification → Outreach → CRM → Meeting Brief → Daily Report
orchestrator/              # CLI entry point, loads SKILL.md, proof.md, notes.md
utils/                     # JSON loading, schema validation, audit logging
docs/                      # Architecture, usage, delegation loop documentation
tests/                     # Pytest suites
integrations/              # CRM/email/LinkedIn stubs
logs/                      # Audit trail (JSONL)
.github/workflows/         # CI/CD (GitHub Actions)
```

## Delegation Loop

Every job has four components:

1. **SKILL.md** — Process layer
2. **files/** — Toolbox layer
3. **proof.md** — Verification layer
4. **notes.md** — Compounding layer

See `docs/delegation_loop.md` for the full operating contract.

## Deterministic rules

1. No fabrication of companies, people, or contact details
2. Unknown fields → `""` or `[]`
3. No email pattern inference
4. No commentary outside JSON output
5. Every run produces structurally consistent output

## Audit log

Each pipeline run appends a JSONL line to `logs/pipeline_runs.jsonl`.

## Setup

1. Create a Python virtual environment:
   ```bash
   python orchestrator/af_orchestrator.py config.json
   ```
2. Install dependencies (see `requirements.txt`).

## Running the pipeline

```bash
python orchestrator/af_orchestrator.py config.json
```

## License

Proprietary — AigentForce.
