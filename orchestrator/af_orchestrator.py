# af_orchestrator.py
# CLI entry point for running the AigentForce BD pipeline.
# Loads Delegation Loop (SKILL.md, proof.md, notes.md) for each job.
# Applies proof checks (schema + content) after each job.
# Logs failures to the audit log (logs/pipeline_runs.jsonl by default).

import json
import os
import sys

# Ensure the project root is on sys.path so pipeline/ and utils/ are importable.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from pipeline.af_pipeline import run_pipeline
from utils.af_utils import load_json, log_jsonl


def main():
    if len(sys.argv) < 2:
        print("Usage: python orchestrator/af_orchestrator.py <config.json>")
        sys.exit(1)

    config_path = sys.argv[1]
    config = load_json(config_path)

    audit_log = config.get("orchestrator", {}).get("audit_log", "logs/pipeline_runs.jsonl")

    # The pipeline now applies proof checks to every step.
    result = run_pipeline(config, audit_log_path=audit_log)

    # Also log the top-level pipeline result.
    log_jsonl = __import__("utils.af_utils", fromlist=["log_jsonl"]).log_jsonl
    log_jsonl(audit_log, result)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
