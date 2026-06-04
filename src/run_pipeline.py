from ingestion.openfda_client import OpenFDAClient
from ingestion.duckdb_client import DuckDBClient

from transformations.openfda_transformer import transform_openfda
from transformations.duckdb_transformer import transform_duckdb

from storage.bronze_writer import BronzeWriter
from storage.silver_writer import SilverWriter

from pipeline.ingestion_pipeline import IngestionPipeline

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():

    source = "openfda"   #"duckdb" or "openfda"

    if source == "openfda":

        client = OpenFDAClient()
        client_args = {"limit": 5}
        transform_fn = transform_openfda

    elif source == "duckdb":

        client = DuckDBClient("data/warehouse/pharma.duckdb")
        client_args = {"query": "SELECT * FROM drug_labels"}
        transform_fn = transform_duckdb

    else:
        raise ValueError("Unknown source")

    bronze_writer = BronzeWriter(source=source)
    silver_writer = SilverWriter(source=source)

    pipeline = IngestionPipeline(
        client=client,
        transform_fn=transform_fn,
        bronze_writer=bronze_writer,
        silver_writer=silver_writer,
        logger=logger
    )

    result = pipeline.run(**client_args)

    logger.info("Pipeline finished")


if __name__ == "__main__":
    main()