# af_orchestrator.py
# CLI entry point for running the AigentForce BD pipeline.
# Loads Delegation Loop (SKILL.md, proof.md, notes.md) for each job.

import json
import os
import sys
from datetime import datetime, timezone

from pipeline.af_pipeline import run_pipeline
from utils.af_utils import load_json, log_jsonl, validate_schema


def load_skill(job_folder):
    skill_path = os.path.join(job_folder, "SKILL.md")
    if os.path.exists(skill_path):
        with open(skill_path, "r", encoding="utf8") as f:
            return f.read()
    return None


def load_proof(job_folder):
    proof_path = os.path.join(job_folder, "proof.md")
    if os.path.exists(proof_path):
        with open(proof_path, "r", encoding="utf8") as f:
            return f.read()
    return None


def load_notes(job_folder):
    notes_path = os.path.join(job_folder, "notes.md")
    if os.path.exists(notes_path):
        with open(notes_path, "r", encoding="utf8") as f:
            return f.read()
    return ""


def append_notes(job_folder, entry):
    notes_path = os.path.join(job_folder, "notes.md")
    timestamp = datetime.now(timezone.utc).isoformat()
    with open(notes_path, "a", encoding="utf8") as f:
        f.write(f"\n- {timestamp}: {entry}\n")


def run_job(job_folder, input_data, schema=None):
    """Run a Delegation Loop job: load SKILL.md, apply proof checks, log results."""
    skill = load_skill(job_folder)
    if not skill:
        return {"status": "error", "error": f"No SKILL.md in {job_folder}"}

    proof = load_proof(job_folder)

    # Placeholder: real implementation calls the LLM with SKILL.md as system prompt.
    # Here we return input echoed for structure validation.
    result = {
        "status": "placeholder",
        "job": os.path.basename(job_folder),
        "input": input_data,
    }

    # Schema validation
    if schema:
        errors = validate_schema(result, schema)
        if errors:
            append_notes(job_folder, f"Schema validation failed: {errors}")
            result["status"] = "validation_failed"
            result["errors"] = errors

    # Proof check placeholder (empty - real checks are in proof.md, enforced by agent)
    if proof:
        result["proof_applied"] = os.path.basename(job_folder) + "/proof.md"

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python orchestrator/af_orchestrator.py <config.json>")
        sys.exit(1)

    config_path = sys.argv[1]
    config = load_json(config_path)

    result = run_pipeline(config)
    log_jsonl("logs/pipeline_runs.jsonl", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
