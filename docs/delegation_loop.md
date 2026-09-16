# Delegation Loop — Operating Contract

This document defines the AigentForce BD operating system: every agent is a **job**, each with four components. The orchestrator enforces the loop.

## The four components

1. **SKILL.md** — Process layer. Purpose, when to use, inputs, steps, decisions, definition of done, edge cases.
2. **files/** — Toolbox layer. Templates, scripts, reference data, examples, rules, checklists.
3. **proof.md** — Verification layer. Evidence rules, no-invented-data rules, schema compliance, tone rules, fail conditions.
4. **notes.md** — Compounding layer. Failure log, root causes, durable fixes, improvements to SKILL.md and files/.

## Job execution order (pipeline)

1. `jobs/lead_research` — Discover companies matching niche + geography
2. `jobs/icp_scoring` — Score ICP fit on company profiles
3. `jobs/outreach_generation` — Generate email, LinkedIn, and follow-up copy
4. `jobs/crm_update` — Sync to CRM (create/update/log)
5. `jobs/meeting_brief` — Prepare pre-meeting briefing
6. `jobs/daily_report` — Generate daily BD activity summary

## Orchestrator contract

The orchestrator (`orchestrator/af_orchestrator.py`):

- Loads SKILL.md for each job
- Loads proof.md and applies verification rules
- Loads notes.md for failure history
- Runs jobs in pipeline order
- Logs failures into notes.md
- Returns validated outputs only

## Autonomy rules

**Allowed:**
- Create missing job folders
- Create missing SKILL.md / files / proof / notes
- Improve existing job definitions
- Add new tools to files/
- Update proof rules when failures occur
- Restructure pipeline for correctness
- Enforce deterministic behavior
- Refuse outputs that violate proof.md

**Forbidden:**
- Hallucinate data
- Invent emails, names, or signals
- Bypass proof rules
- Modify repo visibility
- Push without explicit auth
- Skip steps in the Delegation Loop

## BD-specific rules

- Hiring signals must trace to a source (job_board, careers_page, news, linkedin_public)
- ICP scores must cite evidence from the company profile
- Outreach must follow templates in files/templates/
- CRM updates must follow the crm_update schema
- Meeting briefs must be factual and based on available data
- Daily reports must be numeric and validated against activities

## One step at a time

The orchestrator executes one job at a time. After each step, it stops and waits for confirmation before proceeding to the next.

## Self-improvement

When a failure occurs:
1. Log it in notes.md with date, failure, root cause
2. Diagnose the root cause
3. Add a durable fix to SKILL.md or files/
4. Update proof.md if the failure reveals a gap

This creates self-improving agents over time.
