from ingestion.openfda_client import OpenFDAClient
from storage.raw_writer import RawWriter
from pipeline import IngestionPipeline
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():

    client = OpenFDAClient(timeout=10)
    writer = RawWriter(base_path="data/raw/openfda")

    pipeline = IngestionPipeline(
        client=client,
        writer=writer,
        logger=logger
    )

    pipeline.run(limit=5)


if __name__ == "__main__":
    main()
   

   

# base_fields = [
#     "safetyreportid",
#     "receivedate",
#     "transmissiondate",
#     "serious"
# ]

# nested_fields = [
#     "patient"
# ]

# patient_fields = [
#     "drug",
#     "reaction"
# ] 

