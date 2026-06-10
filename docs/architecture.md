# Architecture

## Overview

The pharma safety lakehouse is a three-layer medallion architecture that ingests drug safety data from two sources:

```text
OpenFDA API ──→ Bronze ──→ Silver ─┐
                                    ├──→ Gold
DuckDB       ──→ Bronze ──→ Silver ─┘
```

## Data Flow

1. **Ingest**: `OpenFDAClient` or `DuckDBClient` fetches raw data
2. **Bronze**: `BronzeWriter` persists raw payload with metadata (timestamp, run_id, source)
3. **Transform**: Normalize fields and generate `drug_key` as a join key
4. **Silver**: `SilverWriter` saves normalized records with record count
5. **Gold**: `GoldWriter` joins OpenFDA events with DuckDB drug labels

## Layer Details

### Bronze

- Stores raw source output as received
- Metadata includes: `timestamp`, `run_id`, `source`, `schema_version`, `query_params`
- One file per run per source

### Silver

- Normalized and deduplicated records
- Every record has `drug_key` (lowercase drug name) for joining
- Metadata includes: `record_count`
- Validates record count matches data length

### Gold

- Joined analytics ready for reporting
- **enriched_safety_events**: OpenFDA events + manufacturer, indication, label_match flag
- **drug_safety_summary**: aggregated safety metrics per drug (total_reports, serious_reports)

## Code Organization

```
src/
  configs/settings.py          ← Environment-based configuration
  ingestion/
    openfda_client.py          ← OpenFDA API wrapper
    duckdb_client.py           ← DuckDB SQL wrapper
  transformations/
    openfda_transformer.py     ← Normalize OpenFDA records
    duckdb_transformer.py      ← Normalize DuckDB records
  storage/
    bronze_writer.py           ← Persist raw + metadata
    silver_writer.py           ← Persist normalized + record count
    gold_writer.py             ← Join and aggregate
  pipeline/
    ingestion_pipeline.py      ← Orchestrate: fetch → bronze → transform → silver
  run_pipeline.py             ← CLI: all sources or specific
  run_openfda_client.py       ← Convenience runner for OpenFDA only
  run_duckdb_client.py        ← Convenience runner for DuckDB only
  run_exploration.py          ← Inspect latest gold output
```

## Design Principles

- **Simple**: Plain Python dicts and JSON, no ORM or schema validation library
- **Modular**: Each source has independent client and transformer
- **Observable**: Every layer writes JSON with structured metadata
- **Reusable**: `IngestionPipeline` works for any source

## Usage

```bash
# Run both sources and build Gold
python src/run_pipeline.py --source all --limit 25

# Run one source only
python src/run_pipeline.py --source openfda --limit 25
python src/run_openfda_client.py --limit 50
python src/run_duckdb_client.py

# Explore the latest Gold output
python src/run_exploration.py
```
