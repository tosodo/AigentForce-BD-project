import json
import glob
import os

from utils.proof import run_all_checks
from utils.af_utils import load_json


def _load_schema(name):
    path = f"af_bd_schemas/{name}"
    if os.path.exists(path):
        return load_json(path)
    return None


def test_json_schemas_parse():
    """All 7 schema files must parse cleanly."""
    for f in glob.glob("af_bd_schemas/*.json"):
        with open(f, "r", encoding="utf8") as fp:
            json.load(fp)


def test_icp_score_integrity_passes():
    """icp_score must equal sum of score_breakdown."""
    schema = _load_schema("icp_score.json")
    instance = {
        "company_name": "TestCo",
        "icp_score": 65,
        "score_breakdown": {
            "hiring_urgency": 15,
            "team_size_fit": 12,
            "budget_signals": 10,
            "industry_fit": 15,
            "tech_maturity": 13,
        },
        "recommended_angle": "High hiring urgency.",
        "reasoning": "Active hiring signals.",
    }
    failures = run_all_checks("icp_scoring", instance, schema)
    integrity_failures = [f for f in failures if f[0] == "icp_score_integrity"]
    assert len(integrity_failures) == 0, f" ICP integrity failed: {integrity_failures}"


def test_icp_score_integrity_fails_mismatch():
    """icp_score != sum of breakdown must be caught."""
    schema = _load_schema("icp_score.json")
    instance = {
        "company_name": "TestCo",
        "icp_score": 70,
        "score_breakdown": {
            "hiring_urgency": 15,
            "team_size_fit": 10,
            "budget_signals": 8,
            "industry_fit": 14,
            "tech_maturity": 12,
        },
        "recommended_angle": "test",
        "reasoning": "test",
    }
    failures = run_all_checks("icp_scoring", instance, schema)
    integrity_failures = [f for f in failures if f[0] == "icp_score_integrity"]
    assert len(integrity_failures) >= 1, " ICP integrity should have caught the mismatch"


def test_no_invented_emails_flags_missing_at():
    """email fields without @ must be flagged."""
    schema = _load_schema("company_profile.json")
    instance = {
        "company_name": "TestCo",
        "website": "",
        "industry": "",
        "hq_location": "",
        "team_size": "",
        "hiring_signals": [],
        "decision_makers": [{"full_name": "Jane Doe", "role": "HR", "email": "jane.doe", "linkedin_url": ""}],
        "pain_points": [],
    }
    failures = run_all_checks("lead_research", instance, schema)
    email_failures = [f for f in failures if f[0] == "no_invented_emails"]
    assert len(email_failures) >= 1, " Should have flagged email without @"


def test_no_invented_emails_allows_valid():
    """A valid email from a verified source passes."""
    schema = _load_schema("company_profile.json")
    instance = {
        "company_name": "TestCo",
        "website": "",
        "industry": "",
        "hq_location": "",
        "team_size": "",
        "hiring_signals": [],
        "decision_makers": [{"full_name": "Jane Doe", "role": "HR", "email": "jane@company.com", "linkedin_url": ""}],
        "pain_points": [],
    }
    failures = run_all_checks("lead_research", instance, schema)
    email_failures = [f for f in failures if f[0] == "no_invented_emails"]
    assert len(email_failures) == 0, f" Valid email should not be flagged: {email_failures}"


def test_source_tracing_flags_missing_source():
    """Hiring signals without source references must be flagged."""
    schema = _load_schema("company_profile.json")
    instance = {
        "company_name": "TestCo",
        "website": "",
        "industry": "",
        "hq_location": "",
        "team_size": "",
        "hiring_signals": ["Hiring engineers", "Open roles"],
        "decision_makers": [],
        "pain_points": [],
    }
    failures = run_all_checks("lead_research", instance, schema)
    src_failures = [f for f in failures if f[0] == "source_tracing"]
    assert len(src_failures) >= 2, f" Should flag both signals: {src_failures}"


def test_source_tracing_passes_valid():
    """Hiring signals with valid source references pass."""
    schema = _load_schema("company_profile.json")
    instance = {
        "company_name": "TestCo",
        "website": "",
        "industry": "",
        "hq_location": "",
        "team_size": "",
        "hiring_signals": [
            "Hiring 3 engineers (job_board)",
            "Open role: HR (careers_page)",
        ],
        "decision_makers": [],
        "pain_points": [],
    }
    failures = run_all_checks("lead_research", instance, schema)
    src_failures = [f for f in failures if f[0] == "source_tracing"]
    assert len(src_failures) == 0, f" Valid sources should pass: {src_failures}"


def test_no_commentary_fails_string():
    """A string output (commentary) must be flagged."""
    schema = _load_schema("company_profile.json")
    failures = run_all_checks("lead_research", "Here is my analysis...", schema)
    comm_failures = [f for f in failures if f[0] == "no_commentary"]
    assert len(comm_failures) >= 1, " Commentary string should be flagged"


def test_no_commentary_passes_dict():
    """A dict/list output passes the commentary check."""
    schema = _load_schema("company_profile.json")
    failures = run_all_checks("lead_research", {"company_name": "Test"}, schema)
    comm_failures = [f for f in failures if f[0] == "no_commentary"]
    assert len(comm_failures) == 0, " Dict output should pass commentary check"


def test_no_invented_names_flags_placeholder():
    """Placeholder name values must be flagged."""
    schema = _load_schema("company_profile.json")
    instance = {
        "company_name": "TestCo",
        "website": "",
        "industry": "",
        "hq_location": "",
        "team_size": "",
        "hiring_signals": [],
        "decision_makers": [{"full_name": "full name", "role": "HR", "email": "", "linkedin_url": ""}],
        "pain_points": [],
    }
    failures = run_all_checks("lead_research", instance, schema)
    name_failures = [f for f in failures if f[0] == "no_invented_names"]
    assert len(name_failures) >= 1, f" Placeholder name should be flagged: {name_failures}"
