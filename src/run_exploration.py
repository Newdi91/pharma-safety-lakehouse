"""
Explore the latest Gold layer output from the pharma safety pipeline.

Displays a summary of tables, record counts, and sample data from the
most recent gold JSON file.

Usage:
    python src/run_exploration.py
"""

import json
from pathlib import Path


def find_latest_gold_file() -> Path:
    """Find the most recently created gold JSON file."""
    gold_dir = Path("data/gold/pharma_safety")
    candidates = sorted(gold_dir.rglob("*.json"), reverse=True)
    if not candidates:
        raise FileNotFoundError(f"No gold files found. Run: python src/run_pipeline.py --source all")
    return candidates[0]


def load_json(path: Path) -> dict:
    """Load and return JSON file contents."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def print_summary(payload: dict) -> None:
    """Print a structured summary of the gold payload."""
    print("\n=== Gold Layer Summary ===\n")
    
    tables = payload.get("tables")
    if tables:
        print("Tables:")
        for name, records in tables.items():
            count = len(records) if isinstance(records, list) else 0
            print(f"  - {name}: {count} records")
    
    metadata = payload.get("metadata")
    if metadata:
        print("\nMetadata:")
        for key, value in metadata.items():
            print(f"  {key}: {value}")



def print_sample(payload: dict) -> None:
    """Print a sample record from enriched_safety_events."""
    tables = payload.get("tables")
    if tables:
        events = tables.get("enriched_safety_events")
        if events:
            print("\nSample enriched_safety_event:")
            print(json.dumps(events[0], indent=2))



def main() -> None:
    """Load and display the latest gold file."""
    try:
        latest = find_latest_gold_file()
        payload = load_json(latest)
        
        print(f"\nFile: {latest}")
        print_summary(payload)
        print_sample(payload)
        
    except FileNotFoundError as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
