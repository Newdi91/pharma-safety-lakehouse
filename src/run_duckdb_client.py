from ingestion.duckdb_client import DuckDBClient
from transformations.duckdb_transformer import transform_duckdb
from storage.bronze_writer import BronzeWriter
from storage.silver_writer import SilverWriter
from pipeline.ingestion_pipeline import IngestionPipeline
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():

    query = "SELECT * FROM drug_labels"

    client = DuckDBClient("data/warehouse/pharma.duckdb")

    transform_fn = transform_duckdb

    bronze_writer = BronzeWriter(source="duckdb")
    silver_writer = SilverWriter(source="duckdb")

    pipeline = IngestionPipeline(
        client=client,
        transform_fn=transform_fn,
        bronze_writer=bronze_writer,
        silver_writer=silver_writer,
        logger=logger
    )

    result = pipeline.run(query=query)

    logger.info("Pipeline finished")
    

if __name__ == "__main__":
    main()