from datetime import datetime


def transform_openfda(payload: dict) -> list[dict]:

    rows = []

    
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
        
        patient = record.get("patient", {})

        sex = normalize_sex(patient.get("patientsex"))

        drugs = patient.get("drug", [])
        reactions = patient.get("reaction", [])

        
        if not drugs:
            drugs = [None]
        if not reactions:
            reactions = [None]

        
        for d in drugs:
            drug_name = safe_get(d, "medicinalproduct")
            drug_role = safe_get(d, "drugcharacterization")

            for r in reactions:

                rows.append({

                   
                    "report_id": report_id,
                    "sex": sex,
                    "drug": drug_name,
                    "drug_role": drug_role,
                    "reaction": safe_get(r, "reactionmeddrapt"),

                    "serious": serious,
                    "death": death,
                    "hospitalization": hospitalization,

                    "received_date": received_date,

                    
                    "run_id": run_id,
                    "source_system": source_system,
                    "ingestion_timestamp": ingestion_ts
                })

    return rows



def safe_get(obj, key):
    if not obj:
        return None
    return obj.get(key)


def to_bool(value):
    if value in [1, "1", True]:
        return True
    if value in [0, "0", False]:
        return False
    return None


def normalize_sex(value):
    """
    OpenFDA:
    1 = male
    2 = female
    """
    if value in [1, "1"]:
        return "M"
    if value in [2, "2"]:
        return "F"
    return None


def normalize_date(date_str):
    if not date_str:
        return None

    try:
        return datetime.strptime(date_str, "%Y%m%d").date().isoformat()
    except Exception:
        return date_str