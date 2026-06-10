from ingestion.openfda_client import OpenFDAClient
from ingestion.duckdb_client import DuckDBClient

from transformations.openfda_transformer import transform_openfda
from transformations.duckdb_transformer import transform_duckdb

from storage.bronze_writer import BronzeWriter
from storage.silver_writer import SilverWriter
from storage.gold_writer import GoldWriter
import configs.settings as settings

from pipeline.ingestion_pipeline import IngestionPipeline

import argparse
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Run the Pharma Safety Lakehouse pipeline.")
    parser.add_argument(
        "--source",
        choices=["openfda", "duckdb", "all"],
        help="Source system to ingest. Use 'all' to build the joined Gold layer.",
    )
    parser.add_argument("--limit", type=int, help="OpenFDA API limit.")
    parser.add_argument("--search", help="OpenFDA search expression.")
    parser.add_argument("--query", help="DuckDB SQL query.")
    return parser.parse_args()


def main():
    args = parse_args()
    source = args.source or settings.SOURCE

    logger.info(
        "Starting pipeline source=%s limit=%s search=%s query=%s",
        source,
        args.limit,
        args.search,
        args.query,
    )

    if source == "all":
        openfda_result = run_source("openfda", args)
        duckdb_result = run_source("duckdb", args)
        gold_payload = GoldWriter(base_path=str(settings.GOLD_PATH)).save(
            openfda_result["silver"],
            duckdb_result["silver"],
        )
        logger.info(
            "Gold layer finished: enriched_events=%s summary_rows=%s",
            len(gold_payload["tables"]["enriched_safety_events"]),
            len(gold_payload["tables"]["drug_safety_summary"]),
        )
        return

    result = run_source(source, args)

    logger.info(
        "Pipeline finished for %s: silver_records=%s",
        source,
        result["silver"]["metadata"]["record_count"],
    )


def run_source(source, args):
    if source == "openfda":
        client = OpenFDAClient()
        client_args = {
            "limit": args.limit or settings.OPENFDA_LIMIT,
            "search": args.search or settings.OPENFDA_SEARCH,
        }
        transform_fn = transform_openfda

    elif source == "duckdb":
        client = DuckDBClient(str(settings.DUCKDB_PATH))
        client_args = {"query": args.query or settings.DUCKDB_QUERY}
        transform_fn = transform_duckdb

    else:
        raise ValueError("Unknown source")

    bronze_writer = BronzeWriter(
        source=source,
        base_path=str(settings.BRONZE_PATH),
        schema_version=settings.SCHEMA_VERSION,
    )
    silver_writer = SilverWriter(source=source, base_path=str(settings.SILVER_PATH))

    pipeline = IngestionPipeline(
        client=client,
        transform_fn=transform_fn,
        bronze_writer=bronze_writer,
        silver_writer=silver_writer,
        logger=logger
    )

    return pipeline.run(**client_args)


if __name__ == "__main__":
    main()
