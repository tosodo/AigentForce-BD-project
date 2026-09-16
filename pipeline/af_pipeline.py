# af_pipeline.py
# Deterministic pipeline wiring: Research → Qualification → Outreach → CRM → Meeting Brief → Daily Report
# Each step corresponds to a Delegation Loop job in jobs/.

import os
import json
from datetime import datetime, timezone

from utils.af_utils import load_json, save_json, log_jsonl, validate_schema

# Job folders in pipeline order (Delegation Loop)
JOB_FOLDERS = [
    "jobs/lead_research",
    "jobs/icp_scoring",
    "jobs/outreach_generation",
    "jobs/crm_update",
    "jobs/meeting_brief",
    "jobs/daily_report",
]

# Schema files for each job (optional validation)
SCHEMA_MAP = {
    "lead_research": "af_bd_schemas/company_profile.json",
    "icp_scoring": "af_bd_schemas/icp_score.json",
    "outreach_generation": "af_bd_schemas/outreach_package.json",
    "crm_update": "af_bd_schemas/crm_update.json",
    "meeting_brief": "af_bd_schemas/meeting_brief.json",
    "daily_report": "af_bd_schemas/daily_report.json",
}


def run_pipeline(config):
    """Run the full BD pipeline through all Delegation Loop jobs."""
    results = []
    pipeline_state = {"config": config, "steps": []}

    for job_folder in JOB_FOLDERS:
        job_name = os.path.basename(job_folder)
        schema_path = SCHEMA_MAP.get(job_name)

        # Load schema if available
        schema = None
        if schema_path and os.path.exists(schema_path):
            schema = load_json(schema_path)

        # Prepare input for this job
        input_data = {"job": job_name, "config": config, "previous_results": results}

        # Run job (placeholder — real implementation calls LLM with SKILL.md)
        step_result = {
            "job": job_name,
            "folder": job_folder,
            "status": "not_implemented",
            "message": f"Delegation Loop job '{job_name}' defined. SKILL.md, proof.md, notes.md present.",
        }

        results.append(step_result)
        pipeline_state["steps"].append(step_result)

    pipeline_state["status"] = "pipeline_defined"
    pipeline_state["job_count"] = len(JOB_FOLDERS)
    return pipeline_state
