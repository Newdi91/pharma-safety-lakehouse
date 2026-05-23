from datetime import datetime, timezone
from pathlib import Path

class RawWriter():
    def __init__(self, base_path : str):
        self.base_path = Path(base_path)

    def save(self, data : dict):

        timestamp = datetime.now(timezone.utc)
        year = timestamp.year
        month = timestamp.month
        day = timestamp.day

        folder_path = self.base_path / str(year) / str(month) / str(day)
        folder_path.mkdir(parents=True, exist_ok=True)

        
