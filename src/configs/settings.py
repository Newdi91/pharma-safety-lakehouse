"""Configuration for the pharma safety lakehouse pipeline.

All settings are loaded from environment variables with sensible defaults.
Prefix all variables with PHARMA_ when setting them in your shell or .env file.

Example .env file:
    PHARMA_OPENFDA_LIMIT=50
    PHARMA_SOURCE=all
    PHARMA_DUCKDB_PATH=data/warehouse/pharma.duckdb
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# OpenFDA API Configuration
OPENFDA_BASE_URL = os.getenv(
    "PHARMA_OPENFDA_BASE_URL",
    "https://api.fda.gov/drug/event.json"
)
OPENFDA_LIMIT = int(os.getenv("PHARMA_OPENFDA_LIMIT", "25"))
OPENFDA_SEARCH = os.getenv(
    "PHARMA_OPENFDA_SEARCH",
    'patient.drug.medicinalproduct:"Aspirin"'
)

# Pipeline Source Control
SOURCE = os.getenv("PHARMA_SOURCE", "all")

# DuckDB Configuration
DUCKDB_PATH = Path(os.getenv("PHARMA_DUCKDB_PATH", "data/warehouse/pharma.duckdb"))
DUCKDB_QUERY = os.getenv("PHARMA_DUCKDB_QUERY", "SELECT * FROM drug_labels")

# Storage Paths
BRONZE_PATH = Path(os.getenv("PHARMA_BRONZE_PATH", "data/bronze"))
SILVER_PATH = Path(os.getenv("PHARMA_SILVER_PATH", "data/silver"))
GOLD_PATH = Path(os.getenv("PHARMA_GOLD_PATH", "data/gold"))

# Schema Version
SCHEMA_VERSION = os.getenv("PHARMA_SCHEMA_VERSION", "1.0.0")
