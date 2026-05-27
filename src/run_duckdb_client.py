from ingestion.duckdb_client import DuckDBClient
from storage.raw_writer import RawWriter
from pipeline import IngestionPipeline  
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():

    logger.info("Starting DuckDB ingestion test")
    
    client = DuckDBClient("data/warehouse/pharma.duckdb")    
    writer = RawWriter(base_path="data/raw/duckdb")
   
    pipeline = IngestionPipeline(
        client=client,
        writer=writer,
        logger=logger
    )

    
    query = "SELECT * FROM drug_labels"

    data = client.get_data(query)

    logger.info("Fetched data from DuckDB")
    logger.info(data["columns"])
    logger.info(data["rows"])

    
    file_path = writer.save(data)

    logger.info(f"Saved DuckDB ingestion to: {file_path}")


if __name__ == "__main__":
    main()