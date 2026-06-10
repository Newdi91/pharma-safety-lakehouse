class IngestionPipeline:

    def __init__(self, client, transform_fn, bronze_writer, silver_writer, logger):
        self.client = client
        self.transform = transform_fn
        self.bronze_writer = bronze_writer
        self.silver_writer = silver_writer
        self.logger = logger

    def run(self, **kwargs):
        self.logger.info(f"Starting {self.client.source_name} pipeline")

        raw_payload = self.client.fetch(**kwargs)
        bronze_payload = self.bronze_writer.save(raw_payload)

        self.logger.info("Bronze saved")

        records = self.transform(bronze_payload)
        silver_payload = {
            "metadata": {"record_count": len(records)},
            "data": records,
        }

        silver_file = self.silver_writer.save(silver_payload)
        self.logger.info("Silver saved")

        return {
            "bronze": bronze_payload,
            "silver": silver_file,
        }
