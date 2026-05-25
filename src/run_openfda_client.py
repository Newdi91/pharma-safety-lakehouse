from ingestion.openfda_client import OpenFDAClient
from storage.raw_writer import RawWriter
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():

    logger.info("Starting OpenFDA ingestion")

    client = OpenFDAClient(timeout=10)
    writer = RawWriter(base_path="data/raw/openfda")

    data = client.get_adverse_events(limit=5)

    if not data:
        logger.error("API returned empty response")
        return

    file_path = writer.save(data)

    logger.info(f"Saved raw data to {file_path}")
    logger.info("Ingestion completed")


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

