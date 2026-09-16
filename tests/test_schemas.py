import json
import glob

def test_json_schemas_parse():
    for f in glob.glob("af_bd_schemas/*.json"):
        with open(f, "r", encoding="utf8") as fp:
            json.load(fp)
