from datetime import datetime, timezone
from pathlib import Path
import json
import uuid


class RawWriter:

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

    def save(self, data: dict):

       
        timestamp = datetime.now(timezone.utc)
        run_id = uuid.uuid4().hex
        
        year = str(timestamp.year)
        month = str(timestamp.month).zfill(2)
        day = str(timestamp.day).zfill(2)

        folder_path = self.base_path / year / month / day
        folder_path.mkdir(parents=True, exist_ok=True)

        
        time_part = timestamp.strftime("%H%M%S")
        filename = f"openfda_{time_part}_{run_id}.json"

        file_path = folder_path / filename

        enriched_data = {
            "metadata": 
            {
                "timestamp": timestamp.isoformat(),
                "run_id": run_id,
                "source": "openfda",
                "record_count": len(data.get("results", []))
            },
            "data": data
        }

        
        with open(file_path, "w") as f:
            json.dump(enriched_data, f, indent=2)

        
        return str(file_path)
    

        
