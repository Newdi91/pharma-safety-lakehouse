from datetime import datetime, timezone
from pathlib import Path
import json
import uuid
import logging
from typing import List

from models.schemas import SilverOpenFDA, SilverDuckDB


logger = logging.getLogger(__name__)


class SilverWriter:

    def __init__(self, source: str, base_path: str = "data/silver"):
        self.base_path = Path(base_path)
        self.source = source

    def _validate_records(self, records: List[dict]) -> tuple[list, list]:
        valid = []
        errors = []

        Model = SilverOpenFDA if self.source == "openfda" else SilverDuckDB

        for idx, rec in enumerate(records):
            try:
                m = Model(**rec)
                valid.append(m.dict())
            except Exception as e:
                errors.append({"index": idx, "error": str(e), "record": rec})

        return valid, errors

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

        metadata = payload.setdefault("metadata", {})

        records = payload.get("data", []) or []
        valid, errors = self._validate_records(records)

        metadata["silver_path"] = str(file_path)
        metadata["silver_written_at"] = timestamp.isoformat()
        metadata["record_count"] = len(records)
        metadata["valid_record_count"] = len(valid)
        metadata["invalid_record_count"] = len(errors)
        if errors:
            metadata["validation_errors"] = errors
            logger.warning("Silver validation found %s invalid records for source=%s", len(errors), self.source)

        out_payload = {"metadata": metadata, "data": valid}

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(out_payload, f, indent=2)

        return out_payload
