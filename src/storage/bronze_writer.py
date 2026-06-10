from datetime import datetime, timezone
from pathlib import Path
import json
import uuid


class BronzeWriter:

    def __init__(self, source: str, base_path: str = "data/bronze", schema_version: str = "1.0.0"):
        self.base_path = Path(base_path)
        self.source = source
        self.schema_version = schema_version

    def save(self, payload: dict, query_params: dict | None = None) -> dict:
        timestamp = datetime.now(timezone.utc)
        run_id = uuid.uuid4().hex

        folder_path = (
            self.base_path
            / self.source
            / str(timestamp.year)
            / str(timestamp.month).zfill(2)
            / str(timestamp.day).zfill(2)
        )
        folder_path.mkdir(parents=True, exist_ok=True)

        filename = f"bronze_{self.source}_{timestamp.strftime('%H%M%S')}_{run_id}.json"
        file_path = folder_path / filename

        enriched_data = {
            "metadata": {
                "timestamp": timestamp.isoformat(),
                "run_id": run_id,
                "source": self.source,
                "schema_version": self.schema_version,
                "query_params": query_params or {},
                "bronze_path": str(file_path),
            },
            "data": payload,
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(enriched_data, f, indent=2)

        return enriched_data
