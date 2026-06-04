import duckdb


class DuckDBClient:

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.source_name = "duckdb"

    def fetch(self, query: str) -> dict:
        conn = duckdb.connect(self.db_path)

        result = conn.execute(query).fetchall()
        columns = [desc[0] for desc in conn.description]

        conn.close()

        return {
            "columns": columns,
            "rows": result
        }