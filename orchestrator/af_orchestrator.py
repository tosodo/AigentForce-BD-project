# af_orchestrator.py
# CLI entry point for running the BD pipeline

import json
from pipeline.af_pipeline import run_pipeline
from utils.af_utils import load_json, log_jsonl

def main():
    config = load_json("config.json")

    # Placeholder agent functions
    def research_agent(payload):
        return []

    def qualification_agent(companies):
        return []

    result = run_pipeline(research_agent, qualification_agent, config)

    log_jsonl("logs/pipeline_runs.jsonl", result)

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
