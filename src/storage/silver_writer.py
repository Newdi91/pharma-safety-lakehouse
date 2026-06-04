from datetime import datetime, timezone
from pathlib import Path
import json
import uuid


class SilverWriter:

    def __init__(self, source: str, base_path: str = "data/silver"):
        self.base_path = Path(base_path)
        self.source = source

    def save(self, payload: dict) -> dict:

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


        with open(file_path, "w") as f:
            json.dump(payload, f, indent=2)

        
        return payload