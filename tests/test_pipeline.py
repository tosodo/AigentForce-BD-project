from pipeline.af_pipeline import run_pipeline

def test_pipeline_empty():
    def r(_): return []
    def q(_): return []
    result = run_pipeline(r, q, {})
    assert result["status"] == "no_companies_found"
