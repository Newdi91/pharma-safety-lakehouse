from datetime import datetime, timezone
from pathlib import Path
import json


class GoldWriter:
    """Create a simple Gold analytics layer from Silver datasets."""

    def __init__(self, base_path: str = "data/gold"):
        self.base_path = Path(base_path)

    def save(self, openfda_silver: dict, duckdb_silver: dict) -> dict:
        timestamp = datetime.now(timezone.utc)
        folder_path = (
            self.base_path
            / "pharma_safety"
            / str(timestamp.year)
            / str(timestamp.month).zfill(2)
            / str(timestamp.day).zfill(2)
        )
        folder_path.mkdir(parents=True, exist_ok=True)

        events = openfda_silver.get("data", []) or []
        labels = duckdb_silver.get("data", []) or []
        enriched_events = self._join_events_with_labels(events, labels)
        summary = self._drug_safety_summary(enriched_events)

        file_path = folder_path / f"gold_pharma_safety_{timestamp.strftime('%H%M%S')}.json"
        gold_payload = {
            "tables": {
                "enriched_safety_events": enriched_events,
                "drug_safety_summary": summary,
            },
            "metadata": {
                "generated_at": timestamp.isoformat(),
                "record_count": len(enriched_events),
            },
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(gold_payload, f, indent=2)

        return gold_payload

    def _join_events_with_labels(self, events: list[dict], labels: list[dict]) -> list[dict]:
        labels_by_key = {label.get("drug_key"): label for label in labels if label.get("drug_key")}
        enriched = []

        for event in events:
            label = labels_by_key.get(event.get("drug_key"), {})
            enriched.append(
                {
                    **event,
                    "label_drug_name": label.get("drug_name"),
                    "manufacturer": label.get("manufacturer"),
                    "indication": label.get("indication"),
                    "label_match": bool(label),
                }
            )
        return enriched

    def _drug_safety_summary(self, records: list[dict]) -> list[dict]:
        groups: dict[str, dict] = {}

        for record in records:
            drug_key = record.get("drug_key") or "unknown"
            groups.setdefault(
                drug_key,
                {
                    "drug_key": drug_key,
                    "drug": record.get("label_drug_name") or record.get("drug"),
                    "total_reports": 0,
                    "serious_reports": 0,
                },
            )

            groups[drug_key]["total_reports"] += 1
            groups[drug_key]["serious_reports"] += int(record.get("serious") is True)

        return list(groups.values())
