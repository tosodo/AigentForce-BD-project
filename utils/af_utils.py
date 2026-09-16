# af_utils.py
"""AigentForce BD utilities: JSON loading, schema validation, audit logging."""

import json
import os
from datetime import datetime, timezone


def load_json(path):
    """Load a JSON file. Returns parsed object."""
    with open(path, "r", encoding="utf8") as f:
        return json.load(f)


def save_json(path, obj):
    """Save an object as JSON atomically."""
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, path)


def log_jsonl(path, obj):
    """Append a JSON object as a line to a JSONL file."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "a", encoding="utf8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def validate_schema(instance, schema):
    """Basic JSON schema validation against a schema dict.
    Returns list of error strings (empty if valid).
    Supports: type checks for object/array/string/number/integer/boolean,
    required fields, and basic range checks.
    """
    errors = []

    def _check(value, schema_obj, path):
        schema_type = schema_obj.get("type")
        if schema_type == "object":
            if not isinstance(value, dict):
                errors.append(f"{path}: expected object, got {type(value).__name__}")
                return
            required = schema_obj.get("required", [])
            props = schema_obj.get("properties", {})
            for req in required:
                if req not in value:
                    errors.append(f"{path}.{req}: missing required field")
            for key, val in value.items():
                if key in props:
                    _check(val, props[key], f"{path}.{key}")
                # Additional properties allowed by default
        elif schema_type == "array":
            if not isinstance(value, list):
                errors.append(f"{path}: expected array, got {type(value).__name__}")
                return
            items = schema_obj.get("items")
            if items:
                for i, item in enumerate(value):
                    _check(item, items, f"{path}[{i}]")
        elif schema_type == "string":
            if not isinstance(value, str):
                errors.append(f"{path}: expected string, got {type(value).__name__}")
        elif schema_type == "integer":
            if not isinstance(value, int) or isinstance(value, bool):
                errors.append(f"{path}: expected integer, got {type(value).__name__}")
            else:
                minimum = schema_obj.get("minimum")
                maximum = schema_obj.get("maximum")
                if minimum is not None and value < minimum:
                    errors.append(f"{path}: value {value} < minimum {minimum}")
                if maximum is not None and value > maximum:
                    errors.append(f"{path}: value {value} > maximum {maximum}")
        elif schema_type == "number":
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                errors.append(f"{path}: expected number, got {type(value).__name__}")
        elif schema_type == "boolean":
            if not isinstance(value, bool):
                errors.append(f"{path}: expected boolean, got {type(value).__name__}")

    _check(instance, schema, "$")
    return errors


def now_iso():
    """Return current UTC timestamp in ISO 8601."""
    return datetime.now(timezone.utc).isoformat()


def ensure_dir(path):
    """Ensure a directory exists."""
    os.makedirs(path, exist_ok=True)
