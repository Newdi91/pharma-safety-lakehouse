def transform_duckdb(payload: dict) -> list[dict]:
    
    data = payload.get("data", {})   

    columns = data.get("columns", [])
    rows = data.get("rows", [])

    result = []

    for row in rows:
        result.append(dict(zip(columns, row)))

    return result