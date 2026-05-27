import requests
from configs.settings import OPENFDA_BASE_URL


class OpenFDAClient:

    def __init__(self, timeout=10):
        self.base_url = OPENFDA_BASE_URL
        self.timeout = timeout
        self.source_name = "openfda"
        
    def get_adverse_events(self, limit=10):

        params = {"limit": limit}

        response = requests.get(
            self.base_url,
            params=params,
            timeout=self.timeout
        )

        response.raise_for_status()

        data = response.json()

        if "results" not in data:
            raise ValueError("Invalid API response: missing 'results'")

        return data
    