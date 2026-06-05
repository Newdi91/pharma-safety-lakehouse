# Pharma Safety Lakehouse

Beginner-friendly data engineering portfolio project for pharma safety analytics.

The project shows a simple medallion pipeline with two sources:

- OpenFDA API: adverse event reports.
- DuckDB: local drug label reference data.

Both sources are ingested with the same pipeline pattern, saved to Bronze, normalized to Silver, and then joined in Gold to answer business questions about drug safety.

## Architecture

```text
                 +------------------+
                 |  OpenFDA API     |
                 | adverse events   |
                 +---------+--------+
                           |
                           v
                    Bronze openfda
                           |
                           v
                    Silver openfda
                           |
                           v
                    drug_key join
                           ^
                           |
                    Silver duckdb
                           ^
                           |
                    Bronze duckdb
                           ^
                           |
                 +---------+--------+
                 |  DuckDB          |
                 | drug labels      |
                 +------------------+

Gold = enriched safety events + drug safety summary + business question answers
```

## What This Project Demonstrates

| Skill | Where it appears |
| --- | --- |
| Python ETL | `IngestionPipeline`, source clients, transformations, writers |
| API ingestion | OpenFDA client |
| Database ingestion | DuckDB client and setup script |
| Medallion architecture | Bronze raw data, Silver normalized data, Gold joined analytics |
| Data modeling | Shared `drug_key` and joined Gold tables |
| Pharma analytics | Serious reports, reactions, manufacturers, indications |
| Testing | Unit tests for transforms, writers, and pipeline behavior |
| CI | GitHub Actions running `pytest` |
| Databricks awareness | Optional notebook structure that can be imported into Databricks |

## Quick Start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create the local DuckDB source database:

```bash
python src/setup_duckdb.py
```

Run the full pipeline:

```bash
python src/run_pipeline.py --source all --limit 25
```

By default the OpenFDA request searches for Aspirin reports so the demo can join with the local DuckDB label data.

Run one source only:

```bash
python src/run_pipeline.py --source openfda --limit 25
python src/run_pipeline.py --source duckdb
```

Run tests:

```bash
pytest
```

## Outputs

The full run writes:

- `data/bronze/openfda/...`: raw OpenFDA payload with run metadata.
- `data/bronze/duckdb/...`: raw DuckDB query result with run metadata.
- `data/silver/openfda/...`: normalized adverse event rows.
- `data/silver/duckdb/...`: normalized drug label rows.
- `data/gold/pharma_safety/...`: joined analytics layer.

The Gold layer contains:

- `enriched_safety_events`: one event row enriched with manufacturer, indication, and approval year.
- `drug_safety_summary`: one row per drug with total reports, serious reports, serious rate, deaths, hospitalizations, and top reaction.
- `business_question_answers`: simple answers designed for portfolio storytelling.

## Business Questions

The Gold layer is designed to answer questions such as:

- Which drug has the highest number of serious adverse event reports?
- Which drug has the highest serious report rate?
- Which OpenFDA records can be enriched with local drug label data?
- Which manufacturer or indication is associated with the reported safety events?

## Configuration

Runtime settings can be overridden with environment variables prefixed by `PHARMA_`.

| Setting | Default |
| --- | --- |
| `PHARMA_SOURCE` | `all` |
| `PHARMA_OPENFDA_LIMIT` | `25` |
| `PHARMA_OPENFDA_SEARCH` | `patient.drug.medicinalproduct:"Aspirin"` |
| `PHARMA_DUCKDB_PATH` | `data/warehouse/pharma.duckdb` |
| `PHARMA_DUCKDB_QUERY` | `SELECT * FROM drug_labels` |
| `PHARMA_BRONZE_PATH` | `data/bronze` |
| `PHARMA_SILVER_PATH` | `data/silver` |
| `PHARMA_GOLD_PATH` | `data/gold` |

## Documentation

- [Architecture](docs/architecture.md)
- [Data model](docs/data_model.md)
- [Databricks and notebooks](docs/databricks_setup.md)

## Quick Validation

After running the full pipeline (`--source all`) you can quickly inspect data quality metadata written by the Silver and Gold writers. Example:

```bash
# Run the full pipeline (small sample)
python src/run_pipeline.py --source all --limit 25

# Inspect the latest Gold JSON file (example path)
jq . data/gold/pharma_safety/YYYY/MM/DD/gold_pharma_safety_HHMMSS.json | less
```

Look for these metadata keys in the Gold file under `metadata`:

- `enriched_record_count`: number of enriched event rows written to Gold
- `enriched_matched_count`: how many of those had a DuckDB label match
- `enrichment_ratio`: matched/total fraction (0-1)
- `data_quality_warnings`: list of simple DQ warnings such as `low_enrichment_ratio`

The `data/silver/...` JSON files now include `valid_record_count` and `invalid_record_count` in their `metadata`, and `validation_errors` when invalid rows were encountered.

## Domain Note

This is a portfolio project. It demonstrates data engineering patterns for pharma safety analytics, but it is not a validated pharmacovigilance, clinical, or regulatory system.
