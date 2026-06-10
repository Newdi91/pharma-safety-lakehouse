"""DuckDB client.

This client executes SQL queries against a local DuckDB database file.

Notes on the `query` parameter in `fetch`:
- The DuckDB SQL engine supports arbitrary SELECT queries over in-process tables.
- In this project `query` is parameterized from the configuration, allowing
  different analysis scenarios without code changes.
- The pipeline's `run_pipeline` entrypoint passes a default `PHARMA_DUCKDB_QUERY`
  from the settings when the user does not supply a `--query` argument. Keep
  `query` configurable to allow both standard reference data queries and
  exploratory ad-hoc analysis.

This design mirrors the OpenFDA client structure, ensuring consistency across
the ingestion layer.
"""

import duckdb


class DuckDBClient:
    """Query a local DuckDB database for reference data."""

    def __init__(self, db_path: str):
        """Initialize the DuckDB client.

        Args:
            db_path: filesystem path to the DuckDB database file.
        """
        self.db_path = db_path
        self.source_name = "duckdb"

    def fetch(self, query: str) -> dict:
        """Execute a SQL query against the DuckDB database.

        Args:
            query: SQL SELECT statement to execute.

        Returns:
            Dictionary with keys:
              - `columns`: list of column names from the result set.
              - `rows`: list of tuples representing result rows.
        """
        conn = duckdb.connect(self.db_path)

        result = conn.execute(query).fetchall()
        columns = [desc[0] for desc in conn.description]

        conn.close()

        return {
            "columns": columns,
            "rows": result
        }