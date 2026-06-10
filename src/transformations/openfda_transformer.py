from datetime import datetime
from typing import Any


def transform_openfda(payload: dict) -> list[dict]:
    rows: list[dict[str, Any]] = []
    metadata = payload.get("metadata", {})
    source_system = metadata.get("source")
    run_id = metadata.get("run_id")
    ingestion_ts = metadata.get("timestamp")

    records = payload.get("data", {}).get("results", [])
    for record in records:
        report_id = record.get("safetyreportid")
        serious = to_bool(record.get("serious"))
        death = to_bool(record.get("seriousnessdeath"))
        hospitalization = to_bool(record.get("seriousnesshospitalization"))
        received_date = normalize_date(record.get("receivedate"))

        patient = record.get("patient", {}) or {}
        sex = normalize_sex(patient.get("patientsex"))
        drugs = patient.get("drug") or [None]
        reactions = patient.get("reaction") or [None]

        if not isinstance(drugs, list):
            drugs = [drugs]
        if not isinstance(reactions, list):
            reactions = [reactions]

        for drug_record in drugs:
            drug_name = safe_get(drug_record, "medicinalproduct")
            drug_role = safe_get(drug_record, "drugcharacterization")

            for reaction in reactions:
                rows.append(
                    {
                        "report_id": report_id,
                        "sex": sex,
                        "drug": drug_name,
                        "drug_key": normalize_drug_key(drug_name),
                        "drug_role": drug_role,
                        "reaction": safe_get(reaction, "reactionmeddrapt"),
                        "serious": serious,
                        "death": death,
                        "hospitalization": hospitalization,
                        "received_date": received_date,
                        "run_id": run_id,
                        "source_system": source_system,
                        "ingestion_timestamp": ingestion_ts,
                    }
                )
    return rows


def safe_get(obj: Any, key: str) -> Any:
    if not obj or not isinstance(obj, dict):
        return None
    return obj.get(key)


def normalize_drug_key(value: Any) -> str | None:
    if value is None:
        return None
    return str(value).strip().lower()


def to_bool(value: Any) -> bool | None:
    if value in [1, "1", True]:
        return True
    if value in [0, "0", False]:
        return False
    return None


def normalize_sex(value: Any) -> str | None:
    if value in [1, "1"]:
        return "M"
    if value in [2, "2"]:
        return "F"
    return None


def normalize_date(date_str: Any) -> str | None:
    if not date_str:
        return None

    try:
        return datetime.strptime(str(date_str), "%Y%m%d").date().isoformat()
    except ValueError:
        return str(date_str)
