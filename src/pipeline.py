class IngestionPipeline:

    def __init__(self, client, writer, logger):
        self.client = client
        self.writer = writer
        self.logger = logger

    def run(self, limit=5):
        self.logger.info(f"Starting {self.client.source_name} pipeline")

        data = self.client.get_adverse_events(limit=limit)

        file_path = self.writer.save(data)

        self.logger.info(f"Saved raw data to: {file_path}")
        self.logger.info("Pipeline completed successfully")