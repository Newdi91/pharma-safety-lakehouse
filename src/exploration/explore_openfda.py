import json
from pathlib import Path
from pprint import pprint


def inspect_openfda_file(path: Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    print("\nTop-level keys:", sorted(data.keys()))
    payload = data.get("data", {})
    print("Data keys:", sorted(payload.keys()))

    results = payload.get("results")
    if isinstance(results, list) and results:
        first_record = results[0]
        print("\nFirst record keys:", sorted(first_record.keys()))
        if "patient" in first_record:
            print("Patient keys:", sorted(first_record["patient"].keys()))
        print("\nSample record:")
        pprint(first_record)
    else:
        print("No results found in OpenFDA payload.")


if __name__ == "__main__":
    path = Path("data/raw/openfda")
    if path.exists():
        files = sorted(path.rglob("*.json"), reverse=True)
        if files:
            inspect_openfda_file(files[0])
        else:
            print("No OpenFDA JSON files found under data/raw/openfda.")
    else:
        print("OpenFDA raw data path does not exist: data/raw/openfda")
