import sys

from run_pipeline import main


# Convenience runner for DuckDB extraction.
#
# If the user does not explicitly pass a --source argument, this script
# appends `--source duckdb` to sys.argv so that run_pipeline will ingest only
# the DuckDB source.
#
# This also supports CLI forms like `python src/run_duckdb_client.py` and
# respects explicit source arguments if provided.
if __name__ == "__main__":
    if not any(arg == "--source" or arg.startswith("--source=") for arg in sys.argv):
        sys.argv.extend(["--source", "duckdb"])
    main()
