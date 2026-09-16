# af_utils.py
import json

def load_json(path):
    with open(path, "r", encoding="utf8") as f:
        return json.load(f)

def log_jsonl(path, obj):
    with open(path, "a", encoding="utf8") as f:
        f.write(json.dumps(obj) + "\n")
