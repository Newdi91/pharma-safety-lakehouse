from ingestion.openfda_client import OpenFDAClient
from storage.bronze_writer import BronzeWriter
from pipeline.ingestion_pipeline import IngestionPipeline
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():

    
    client = OpenFDAClient(timeout=10)
    writer = BronzeWriter("openfda", base_path="data/bronze")

    pipeline = IngestionPipeline(
        client=client,
        writer=writer,
        logger=logger
    )

    pipeline.run(limit=5)


if __name__ == "__main__":
    main()
   

   

