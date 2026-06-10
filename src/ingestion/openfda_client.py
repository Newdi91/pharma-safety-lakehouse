"""OpenFDA client.

This client fetches adverse event data from the OpenFDA public API.

Notes on the `search` parameter in `fetch`:
- The OpenFDA API supports a `search` query parameter allowing filtered
  requests (for example, `patient.drug.medicinalproduct:"Aspirin"`).
- In this project `search` is optional: if provided it will be sent to the
  API to narrow results; if omitted the API will return the default (unfiltered)
  results up to the requested `limit`.
- The pipeline's `run_pipeline` entrypoint passes a default `PHARMA_OPENFDA_SEARCH`
  from the settings when the user does not supply a `--search` argument. Keep
  `search` optional to allow both default demo runs (Aspirin) and free-form
  queries for exploration.

The parameter is therefore useful but not mandatory; we keep it for flexibility.
"""

import requests
from configs.settings import OPENFDA_BASE_URL


class OpenFDAClient:

    def __init__(self, timeout=10):
        self.base_url = OPENFDA_BASE_URL
        self.timeout = timeout
        self.source_name = "openfda"

    def fetch(self, limit: int = 10, search: str | None = None) -> dict:
        """Fetch data from OpenFDA.

        Args:
            limit: number of records to request (API `limit` param).
            search: optional OpenFDA search expression to filter results.

        Returns:
            Parsed JSON response from the OpenFDA API.
        """

        params = {"limit": limit}
        if search:
            params["search"] = search

        response = requests.get(
            self.base_url,
            params=params,
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        if "results" not in data:
            raise ValueError("Invalid API response: missing 'results'")

        return data
    
