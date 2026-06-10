# Data Model

## Bronze Schema

Raw source payload with operational metadata.

```json
{
  "metadata": {
    "timestamp": "2026-06-11T12:00:00+00:00",
    "run_id": "abc123def456",
    "source": "openfda",
    "schema_version": "1.0.0",
    "query_params": {"limit": 25, "search": "..."}
  },
  "data": { /* raw API response */ }
}
```

## Silver Schema

Normalized records with join key. Silver layer contains only the data array, without metadata.

```json
[
  {
    "report_id": "1",
    "drug": "ASPIRIN",
    "drug_key": "aspirin",
    ...
  }
]
```


### OpenFDA Records

One record per (report_id, drug, reaction) combination:

| Field | Type | Purpose |
| --- | --- | --- |
| `report_id` | string | Unique adverse event ID from FDA |
| `drug` | string | Drug name as reported |
| `drug_key` | string | Lowercase normalized drug name (join key) |
| `reaction` | string | Adverse reaction reported |
| `serious` | boolean | Marked as serious |
| `death` | boolean | Involved death |
| `hospitalization` | boolean | Involved hospitalization |
| `received_date` | date | ISO format |
| `sex` | string | M or F |
| `drug_role` | string | Concomitant or suspected |
| `run_id` | string | Bronze run_id for traceability |
| `source_system` | string | Always "openfda" |
| `ingestion_timestamp` | datetime | Bronze ingestion timestamp |

### DuckDB Records

One record per drug label:

| Field | Type | Purpose |
| --- | --- | --- |
| `drug_name` | string | Official drug name |
| `drug_key` | string | Lowercase normalized drug name (join key) |
| `manufacturer` | string | Drug manufacturer |
| `indication` | string | Primary indication for use |

## Gold Schema

Joined and aggregated analytics layer.

```json
{
  "tables": {
    "enriched_safety_events": [ /* array of joined events */ ],
    "drug_safety_summary": [ /* array of aggregated metrics */ ]
  },
  "metadata": {
    "generated_at": "2026-06-11T12:15:00+00:00",
    "record_count": 42
  }
}
```

### enriched_safety_events

OpenFDA event with matched drug label information:

| Field | Source | Purpose |
| --- | --- | --- |
| All OpenFDA fields | Silver OpenFDA | Original event data |
| `label_drug_name` | Silver DuckDB | Official drug name if matched |
| `manufacturer` | Silver DuckDB | Manufacturer if matched |
| `indication` | Silver DuckDB | Indication if matched |
| `label_match` | Join logic | True if drug_key found in DuckDB |

### drug_safety_summary

Aggregated safety metrics per drug:

| Field | Type | Calculation |
| --- | --- | --- |
| `drug_key` | string | Grouping key |
| `drug` | string | Display name |
| `total_reports` | integer | Count of all records for this drug |
| `serious_reports` | integer | Count where serious=True |
