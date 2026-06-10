from datetime import datetime, timezone
from pathlib import Path
import json
import uuid


class SilverWriter:

    def __init__(self, source: str, base_path: str = "data/silver"):
        self.base_path = Path(base_path)
        self.source = source

    def save(self, payload: dict) -> dict:
        records = payload.get("data", []) or []
        silver_payload = {
            "metadata": {"record_count": len(records)},
            "data": records,
        }

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

        filename = f"silver_{self.source}_{timestamp.strftime('%H%M%S')}_{run_id}.json"
        file_path = folder_path / filename

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(silver_payload, f, indent=2)

        return silver_payload
