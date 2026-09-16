import json
from utils.af_utils import load_json


def test_pipeline_defined():
    """The pipeline is wired: 6 jobs in order, all proof_checks present."""
    from pipeline.af_pipeline import run_pipeline

    config = {
        "pipeline": {"niche": "test", "geography": "test"},
        "scoring_weights": {"hiring_urgency": 1},
    }
    result = run_pipeline(config)
    assert result["status"] == "pipeline_defined"
    assert result["job_count"] == 6
    job_names = [s["job"] for s in result["steps"]]
    assert job_names == [
        "lead_research",
        "icp_scoring",
        "outreach_generation",
        "crm_update",
        "meeting_brief",
        "daily_report",
    ]
    # Every step must have proof_checks populated
    for step in result["steps"]:
        assert "proof_checks" in step, f"{step['job']} missing proof_checks"
        assert isinstance(step["proof_checks"], dict)
