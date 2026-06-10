from pathlib import Path

from storage.bronze_writer import BronzeWriter
from storage.gold_writer import GoldWriter
from storage.silver_writer import SilverWriter


def test_bronze_writer_adds_run_metadata(tmp_path):
    writer = BronzeWriter("openfda", base_path=str(tmp_path), schema_version="test")

    payload = writer.save({"results": []}, query_params={"limit": 5})

    metadata = payload["metadata"]
    assert metadata["source"] == "openfda"
    assert metadata["schema_version"] == "test"
    assert metadata["query_params"] == {"limit": 5}
    assert Path(metadata["bronze_path"]).exists()


def test_silver_writer_records_count(tmp_path):
    writer = SilverWriter("openfda", base_path=str(tmp_path))

    payload = writer.save({"data": [{"report_id": "1"}]})

    assert payload["data"][0]["report_id"] == "1"
    assert "metadata" not in payload


def test_gold_writer_joins_openfda_events_with_duckdb_labels(tmp_path):
    writer = GoldWriter(base_path=str(tmp_path))
    openfda_silver = {
        "metadata": {"run_id": "openfda-run"},
        "data": [
            {
                "report_id": "1",
                "drug": "ASPIRIN",
                "drug_key": "aspirin",
                "reaction": "HEADACHE",
                "serious": True,
                "death": False,
                "hospitalization": True,
                "received_date": "2026-01-01",
            }
        ],
    }
    duckdb_silver = {
        "metadata": {"run_id": "duckdb-run"},
        "data": [
            {
                "drug_name": "Aspirin",
                "drug_key": "aspirin",
                "manufacturer": "Bayer",
                "indication": "Pain relief",
            }
        ],
    }

    payload = writer.save(openfda_silver, duckdb_silver)

    enriched = payload["tables"]["enriched_safety_events"][0]
    summary = payload["tables"]["drug_safety_summary"][0]

    assert enriched["manufacturer"] == "Bayer"
    assert enriched["label_match"] is True
    assert summary["drug"] == "Aspirin"
    assert summary["serious_reports"] == 1
