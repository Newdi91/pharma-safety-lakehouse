# Pharma Safety Lakehouse

Beginner-friendly data engineering portfolio project.

Two sources (OpenFDA API and DuckDB) → Bronze (raw) → Silver (normalized) → Gold (joined) pipeline.

## Architecture

```text
OpenFDA API ──→ Bronze ──→ Silver ─┐
                                    ├──→ Gold
DuckDB       ──→ Bronze ──→ Silver ─┘
```

- **Bronze**: raw source data + metadata (timestamp, run_id, source)
- **Silver**: normalized records only (no metadata)
- **Gold**: joined analytics with enriched events and aggregated safety metrics

## Quick Start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python src/setup_duckdb.py
python src/run_pipeline.py --source all --limit 25
pytest
```

## Usage

```bash
# Run one source
python src/run_pipeline.py --source openfda --limit 25
python src/run_pipeline.py --source duckdb

# Run both sources and build Gold
python src/run_pipeline.py --source all --limit 25

# Explore generated JSON output
python src/run_exploration.py --file data/gold/pharma_safety
```

## Design

- `src/run_pipeline.py`: pipeline orchestration
- `src/run_openfda_client.py`: A wrapper to execute OpenFDA exclusively
- `src/run_duckdb_client.py`: A wrapper to execute DuckDB exclusively
- `src/run_exploration.py`: JSON exploration
- `src/storage`: Bronze, Silver, Gold writers that persist clean JSON payloads
- `src/transformations`: normalization and `drug_key` generation

## Configuration

Environment variables (all optional):

| Variable | Default |
| --- | --- |
| `PHARMA_SOURCE` | `all` |
| `PHARMA_OPENFDA_LIMIT` | `25` |
| `PHARMA_OPENFDA_SEARCH` | `patient.drug.medicinalproduct:"Aspirin"` |
| `PHARMA_DUCKDB_PATH` | `data/warehouse/pharma.duckdb` |
| `PHARMA_DUCKDB_QUERY` | `SELECT * FROM drug_labels` |
| `PHARMA_BRONZE_PATH` | `data/bronze` |
| `PHARMA_SILVER_PATH` | `data/silver` |
| `PHARMA_GOLD_PATH` | `data/gold` |

## Outputs

```bash
# Check the latest Gold file
jq . data/gold/pharma_safety/YYYY/MM/DD/gold_pharma_safety_HHMMSS.json | less
```

Gold contains:
- `tables.enriched_safety_events`: OpenFDA events + manufacturer, indication, label_match flag
- `tables.drug_safety_summary`: one row per drug with total_reports, serious_reports

## Documentation

- [Architecture](docs/architecture.md)
- [Data Model](docs/data_model.md)
