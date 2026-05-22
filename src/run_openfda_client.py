import logging
from ingestion.openfda_client import OpenFDAClient


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def main():

    logger.info("Starting OpenFDA ingestion")

    client = OpenFDAClient(timeout=10)

    data = client.get_adverse_events(limit=5)

    logger.debug(f"Top level keys: {list(data.keys())}")
    logger.debug(f"Result keys: {list(data['results'][0].keys())}")

    logger.info(f"Fetched {len(data['results'])} records")

    if not data:
        logger.error("API returned empty response")
        return

    logger.info("Ingestion completed successfully")


if __name__ == "__main__":
    main()

base_fields = [
    "safetyreportid",
    "receivedate",
    "transmissiondate",
    "serious"
]

nested_fields = [
    "patient"
]

patient_fields = [
    "drug",
    "reaction"
] 

