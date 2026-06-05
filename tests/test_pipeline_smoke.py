import json
from pathlib import Path

import logging
from pipeline.ingestion_pipeline import IngestionPipeline
from transformations.openfda_transformer import transform_openfda
from transformations.duckdb_transformer import transform_duckdb
from storage.bronze_writer import BronzeWriter
from storage.silver_writer import SilverWriter
from storage.gold_writer import GoldWriter


class FakeOpenFDAClient:
    source_name = "openfda"

    def fetch(self, limit=1, search=None):
        # Return a payload similar to the real OpenFDA API response (top-level 'results')
        return {
            "results": [
                {
                    "safetyreportid": "R1",
                    "receivedate": "20260101",
                    "serious": 1,
                    "seriousnessdeath": 0,
                    "seriousnesshospitalization": 0,
                    "patient": {
                        "patientsex": 1,
                        "drug": [{"medicinalproduct": "Aspirin", "drugcharacterization": "1"}],
                        "reaction": [{"reactionmeddrapt": "Headache"}]
                    }
                }
            ]
        }


class FakeDuckDBClient:
    source_name = "duckdb"

    def fetch(self, query: str):
        return {"columns": ["drug_name", "manufacturer", "indication", "approval_year"], "rows": [["Aspirin", "Bayer", "Pain", 2000]]}


def test_pipeline_smoke(tmp_path):
    bronze_base = str(tmp_path / "data" / "bronze")
    silver_base = str(tmp_path / "data" / "silver")
    gold_base = str(tmp_path / "data" / "gold")

    # OpenFDA pipeline
    openfda_client = FakeOpenFDAClient()
    bronze_writer = BronzeWriter(source="openfda", base_path=bronze_base, schema_version="1.0.0")
    silver_writer = SilverWriter(source="openfda", base_path=silver_base)

    logger = logging.getLogger("test_pipeline")
    logger.addHandler(logging.NullHandler())
    pipeline = IngestionPipeline(client=openfda_client, transform_fn=transform_openfda, bronze_writer=bronze_writer, silver_writer=silver_writer, logger=logger)
    openfda_result = pipeline.run(limit=1)

    assert "bronze" in openfda_result
    assert "silver" in openfda_result
    assert openfda_result["silver"]["metadata"]["valid_record_count"] >= 1

    # DuckDB pipeline
    duck_client = FakeDuckDBClient()
    bronze_writer_db = BronzeWriter(source="duckdb", base_path=bronze_base, schema_version="1.0.0")
    silver_writer_db = SilverWriter(source="duckdb", base_path=silver_base)

    pipeline_db = IngestionPipeline(client=duck_client, transform_fn=transform_duckdb, bronze_writer=bronze_writer_db, silver_writer=silver_writer_db, logger=logger)
    duck_result = pipeline_db.run(query="SELECT * FROM drug_labels")

    assert duck_result["silver"]["metadata"]["valid_record_count"] >= 1

    # Gold join
    gold_writer = GoldWriter(base_path=gold_base)
    gold_payload = gold_writer.save(openfda_result["silver"], duck_result["silver"])

    assert "tables" in gold_payload
    assert "enriched_safety_events" in gold_payload["tables"]
    assert gold_payload["metadata"]["enriched_record_count"] >= 1
