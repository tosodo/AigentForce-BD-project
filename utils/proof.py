# proof.py
"""Delegation Loop proof enforcement.

Applies structured checks derived from each job's proof.md:
- Schema compliance (reuses af_utils.validate_schema)
- No invented data checks (emails, names, fabricated fields)
- Source tracing (hiring signals must include source references)
- ICP score integrity (icp_score must equal sum of breakdown)
- No commentary outside JSON

Each check returns a list of (rule_name, message) tuples.
Empty list = passed.

Usage:
    failures = run_all_checks("lead_research", instance, schema)
    # failures is list of (check_name, message)
"""

import re

from utils.af_utils import validate_schema


def check_schema_compliance(instance, schema):
    """Delegate to af_utils.validate_schema. Returns list of error strings."""
    if schema is None:
        return []
    return validate_schema(instance, schema)


def check_no_invented_emails(instance):
    """Check that email fields in decision_makers are not placeholder guesses.

    Accepts a list of company dicts OR a single company dict.
    """
    issues = []
    # Normalize to list
    if isinstance(instance, dict):
        instance = [instance]
    if not isinstance(instance, list):
        return issues

    for i, company in enumerate(instance):
        if not isinstance(company, dict):
            continue
        decision_makers = company.get("decision_makers", [])
        if not isinstance(decision_makers, list):
            continue
        for j, dm in enumerate(decision_makers):
            if not isinstance(dm, dict):
                continue
            email = dm.get("email", "")
            if not isinstance(email, str):
                continue
            email_stripped = email.strip()
            if not email_stripped:
                continue  # empty = unknown, acceptable
            if "@" not in email_stripped:
                issues.append(
                    (f"no_invented_emails", f"company[{i}].decision_makers[{j}].email "
                     f"missing '@' — likely fabricated: {email!r}")
                )
            elif email_stripped.lower() in ("tbd", "todo", "email", "e-mail", "-", "n/a"):
                issues.append(
                    (f"no_invented_emails", f"company[{i}].decision_makers[{j}].email "
                     f"is a placeholder: {email!r}")
                )
    return issues


def check_no_invented_names(instance):
    """Check that full_name fields in decision_makers are not placeholder guesses.

    Accepts a list of company dicts OR a single company dict.
    """
    issues = []
    # Normalize to list
    if isinstance(instance, dict):
        instance = [instance]
    if not isinstance(instance, list):
        return issues

    placeholder_names = {"", "-", "tbd", "todo", "name", "full name", "n/a", "nan"}

    for i, company in enumerate(instance):
        if not isinstance(company, dict):
            continue
        decision_makers = company.get("decision_makers", [])
        if not isinstance(decision_makers, list):
            continue
        for j, dm in enumerate(decision_makers):
            if not isinstance(dm, dict):
                continue
            name = dm.get("full_name", "")
            if not isinstance(name, str):
                continue
            if name.strip().lower() in placeholder_names:
                issues.append(
                    (f"no_invented_names", f"company[{i}].decision_makers[{j}].full_name "
                     f"is a placeholder: {name!r}")
                )
    return issues


def check_source_tracing(instance):
    """Check that hiring_signals include source references in parentheses.

    Accepts a list of company dicts OR a single company dict.
    """
    issues = []
    # Normalize to list
    if isinstance(instance, dict):
        instance = [instance]
    if not isinstance(instance, list):
        return issues

    valid_sources = {"job_board", "careers_page", "news", "linkedin_public"}

    for i, company in enumerate(instance):
        if not isinstance(company, dict):
            continue
        signals = company.get("hiring_signals", [])
        if not isinstance(signals, list):
            continue
        for j, signal in enumerate(signals):
            if not isinstance(signal, str):
                issues.append(
                    (f"source_tracing", f"company[{i}].hiring_signals[{j}] "
                     f"is not a string: {type(signal).__name__}")
                )
                continue
            if not signal.strip():
                issues.append(
                    (f"source_tracing", f"company[{i}].hiring_signals[{j}] is empty")
                )
                continue
            # Look for parenthetical source reference
            match = re.search(r"\(([^)]+)\)", signal)
            if not match:
                issues.append(
                    (f"source_tracing", f"company[{i}].hiring_signals[{j}] "
                     f"has no source reference in parentheses: {signal!r}")
                )
                continue
            # Check that at least one valid source type is mentioned
            sources_text = match.group(1).lower()
            if not any(src in sources_text for src in valid_sources):
                issues.append(
                    (f"source_tracing", f"company[{i}].hiring_signals[{j}] "
                     f"has unrecognized source: {match.group(1)!r} in {signal!r}")
                )
    return issues


def check_icp_score_integrity(instance):
    """Check that icp_score equals the sum of score_breakdown values.

    Also validates ranges: icp_score 0-100, each breakdown 0-20.
    Works on a single object or a list of objects.
    """
    issues = []

    def _check_one(obj, prefix):
        score = obj.get("icp_score")
        breakdown = obj.get("score_breakdown")
        if not isinstance(score, (int, float)) or not isinstance(breakdown, dict):
            return
        breakdown_sum = sum(v for v in breakdown.values() if isinstance(v, (int, float)))
        if score != breakdown_sum:
            issues.append(
                (f"icp_score_integrity", f"{prefix}icp_score ({score}) != "
                 f"sum of score_breakdown ({breakdown_sum})")
            )
        if not (0 <= score <= 100):
            issues.append(
                (f"icp_score_integrity", f"{prefix}icp_score ({score}) out of range 0-100")
            )
        for key, val in breakdown.items():
            if isinstance(val, (int, float)) and not (0 <= val <= 20):
                issues.append(
                    (f"icp_score_integrity", f"{prefix}score_breakdown.{key} ({val}) "
                     f"out of range 0-20")
                )

    if isinstance(instance, list):
        for i, item in enumerate(instance):
            if isinstance(item, dict):
                _check_one(item, f"company[{i}].")
    elif isinstance(instance, dict):
        _check_one(instance, "")
    return issues


def check_no_commentary(instance):
    """Check that the output is JSON (list/dict), not a text string."""
    issues = []
    if isinstance(instance, str):
        issues.append(
            ("no_commentary", "output is a string — commentary detected outside JSON")
        )
    elif not isinstance(instance, (dict, list)):
        issues.append(
            ("no_commentary", f"output is {type(instance).__name__}, expected JSON")
        )
    return issues


def run_all_checks(job_name, instance, schema=None):
    """Run all applicable proof checks for a job output.

    Parameters:
        job_name: one of lead_research, icp_scoring, outreach_generation,
                  crm_update, meeting_brief, daily_report
        instance: the actual output data (list or dict)
        schema: JSON schema dict (from af_bd_schemas/*.json), optional

    Returns:
        List of (check_name, message) tuples for each failure.
        Empty list = all checks passed.
    """
    failures = []

    # 1. Schema compliance (all jobs)
    schema_errors = check_schema_compliance(instance, schema)
    for msg in schema_errors:
        failures.append(("schema_compliance", msg))

    # 2. No invented emails (lead_research output)
    if job_name == "lead_research":
        email_issues = check_no_invented_emails(instance)
        failures.extend(email_issues)

    # 3. No invented names (lead_research output)
    if job_name == "lead_research":
        name_issues = check_no_invented_names(instance)
        failures.extend(name_issues)

    # 4. Source tracing (lead_research output)
    if job_name == "lead_research":
        source_issues = check_source_tracing(instance)
        failures.extend(source_issues)

    # 5. ICP score integrity (icp_scoring output)
    if job_name == "icp_scoring":
        integrity_issues = check_icp_score_integrity(instance)
        failures.extend(integrity_issues)

    # 6. No commentary (all jobs)
    commentary_issues = check_no_commentary(instance)
    failures.extend(commentary_issues)

    return failures
