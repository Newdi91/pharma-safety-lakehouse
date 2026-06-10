import sys

from run_pipeline import main


# Convenience runner for OpenFDA extraction.
#
# If the user does not explicitly pass a --source argument, this script
# appends `--source openfda` to sys.argv so that run_pipeline will ingest only
# the OpenFDA source.
#
# This also supports CLI forms like `python src/run_openfda_client.py` and
# respects explicit source arguments if provided.
if __name__ == "__main__":
    if not any(arg == "--source" or arg.startswith("--source=") for arg in sys.argv):
        sys.argv.extend(["--source", "openfda"])
    main()
