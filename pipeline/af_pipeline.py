# af_pipeline.py
# Deterministic pipeline wiring: Research → Qualification → Outreach (stub)

def run_pipeline(research_agent, qualification_agent, input_payload):
    # Step 1: Research
    companies = research_agent(input_payload)

    if not companies:
        return {
            "status": "no_companies_found",
            "results": []
        }

    # Step 2: Qualification
    scores = qualification_agent(companies)

    return {
        "status": "ok",
        "results": scores
    }
