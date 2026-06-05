from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import json
import logging


class GoldWriter:
    """Build the joined analytics layer from OpenFDA events and DuckDB labels."""

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

        events = openfda_silver.get("data", [])
        labels = duckdb_silver.get("data", [])
        enriched_events = self._join_events_with_labels(events, labels)

        # Basic data quality checks
        total = len(enriched_events)
        matched_records = sum(1 for r in enriched_events if r.get("label_match"))
        enrichment_ratio = matched_records / total if total else 0
        dq_warnings = []
        if total == 0:
            dq_warnings.append("no_enriched_events")
        if enrichment_ratio < 0.5 and total > 0:
            dq_warnings.append("low_enrichment_ratio")


        gold_payload = {
            "metadata": {
                "gold_written_at": timestamp.isoformat(),
                "openfda_run_id": openfda_silver.get("metadata", {}).get("run_id"),
                "duckdb_run_id": duckdb_silver.get("metadata", {}).get("run_id"),
                "gold_path": str(folder_path),
                "grain": "one row per OpenFDA report-drug-reaction enriched with DuckDB label data",
                "enriched_record_count": total,
                "enriched_matched_count": matched_records,
                "enrichment_ratio": round(enrichment_ratio, 4),
                "data_quality_warnings": dq_warnings,
            },
            "tables": {
                "enriched_safety_events": enriched_events,
                "drug_safety_summary": self._drug_safety_summary(enriched_events),
                "business_question_answers": self._business_question_answers(enriched_events),
            },
        }

        file_path = folder_path / f"gold_pharma_safety_{timestamp.strftime('%H%M%S')}.json"
        gold_payload["metadata"]["gold_file"] = str(file_path)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(gold_payload, f, indent=2)

        return gold_payload

    def _join_events_with_labels(self, events: list[dict], labels: list[dict]) -> list[dict]:
        labels_by_key = {
            label.get("drug_key"): label
            for label in labels
            if label.get("drug_key")
        }

        enriched = []
        for event in events:
            label = labels_by_key.get(event.get("drug_key"), {})
            enriched.append(
                {
                    **event,
                    "label_drug_name": label.get("drug_name"),
                    "manufacturer": label.get("manufacturer"),
                    "indication": label.get("indication"),
                    "approval_year": label.get("approval_year"),
                    "label_match": bool(label),
                }
            )
        return enriched

    def _drug_safety_summary(self, records: list[dict]) -> list[dict]:
        grouped = defaultdict(
            lambda: {
                "total_reports": 0,
                "serious_reports": 0,
                "death_reports": 0,
                "hospitalization_reports": 0,
                "reactions": Counter(),
                "drug": None,
                "manufacturer": None,
                "indication": None,
            }
        )

        for record in records:
            drug_key = record.get("drug_key") or "unknown"
            group = grouped[drug_key]
            group["drug"] = group["drug"] or record.get("label_drug_name") or record.get("drug")
            group["manufacturer"] = group["manufacturer"] or record.get("manufacturer")
            group["indication"] = group["indication"] or record.get("indication")
            group["total_reports"] += 1
            group["serious_reports"] += int(record.get("serious") is True)
            group["death_reports"] += int(record.get("death") is True)
            group["hospitalization_reports"] += int(record.get("hospitalization") is True)
            if record.get("reaction"):
                group["reactions"][record["reaction"]] += 1

        summary = []
        for drug_key, values in grouped.items():
            total_reports = values["total_reports"]
            summary.append(
                {
                    "drug_key": drug_key,
                    "drug": values["drug"],
                    "manufacturer": values["manufacturer"],
                    "indication": values["indication"],
                    "total_reports": total_reports,
                    "serious_reports": values["serious_reports"],
                    "serious_rate": round(values["serious_reports"] / total_reports, 4),
                    "death_reports": values["death_reports"],
                    "hospitalization_reports": values["hospitalization_reports"],
                    "top_reaction": values["reactions"].most_common(1)[0][0] if values["reactions"] else None,
                }
            )

        return sorted(summary, key=lambda row: row["serious_reports"], reverse=True)

    def _business_question_answers(self, records: list[dict]) -> list[dict]:
        summary = self._drug_safety_summary(records)
        if not summary:
            return []

        highest_serious_count = max(summary, key=lambda row: row["serious_reports"])
        highest_serious_rate = max(summary, key=lambda row: row["serious_rate"])
        matched_records = sum(1 for record in records if record.get("label_match"))

        return [
            {
                "question": "Which drug has the highest number of serious reports?",
                "answer": highest_serious_count.get("drug"),
                "metric": highest_serious_count.get("serious_reports"),
            },
            {
                "question": "Which drug has the highest serious report rate?",
                "answer": highest_serious_rate.get("drug"),
                "metric": highest_serious_rate.get("serious_rate"),
            },
            {
                "question": "How many OpenFDA rows were enriched with DuckDB label data?",
                "answer": matched_records,
                "metric": f"{matched_records}/{len(records)}",
            },
        ]
