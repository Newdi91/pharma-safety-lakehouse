from transformations.duckdb_transformer import transform_duckdb
from transformations.openfda_transformer import transform_openfda


def test_transform_openfda_normalizes_openfda_payload():
    payload = {
        "metadata": {
            "source": "openfda",
            "run_id": "run-1",
            "timestamp": "2026-06-10T12:00:00Z",
        },
        "data": {
            "results": [
                {
                    "safetyreportid": "100",
                    "serious": "1",
                    "seriousnessdeath": "0",
                    "seriousnesshospitalization": "1",
                    "receivedate": "20260101",
                    "patient": {
                        "patientsex": "1",
                        "drug": [{"medicinalproduct": "Aspirin", "drugcharacterization": "1"}],
                        "reaction": [{"reactionmeddrapt": "HEADACHE"}],
                    },
                }
            ]
        },
    }

    rows = transform_openfda(payload)

    assert rows[0]["drug_key"] == "aspirin"
    assert rows[0]["sex"] == "M"
    assert rows[0]["received_date"] == "2026-01-01"
    assert rows[0]["serious"] is True
    assert rows[0]["death"] is False


def test_transform_duckdb_normalizes_duckdb_payload():
    payload = {
        "data": {
            "columns": ["drug_name", "manufacturer", "indication"],
            "rows": [("Aspirin", "Bayer", "Pain relief")],
        }
    }

    records = transform_duckdb(payload)

    assert records[0]["drug_key"] == "aspirin"
    assert records[0]["manufacturer"] == "Bayer"
    assert records[0]["indication"] == "Pain relief"
