from typing import Any


def transform_duckdb(payload: dict) -> list[dict]:
    data = payload.get("data", {}) or {}
    columns = data.get("columns", []) or []
    rows = data.get("rows", []) or []

    result: list[dict[str, Any]] = []
    for row in rows:
        record = dict(zip(columns, row))
        record["drug_key"] = normalize_drug_key(record.get("drug_name"))
        result.append(record)

    return result


def normalize_drug_key(value: Any) -> str | None:
    if value is None:
        return None
    return str(value).strip().lower()
