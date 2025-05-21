import os
import requests

class LinkupApi:
    BASE_URL = "https://api.linkup.so/v1"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("LINKUP_API_KEY")
        if not self.api_key:
            raise ValueError("Missing LINKUP_API_KEY in environment variables")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def search_jobs(self, query: str, location: str = None,
                    page: int = 1, limit: int = 10):
        url = f"{self.BASE_URL}/search"
        params = {
            "q": query,
            "location": location,
            "page": page,
            "limit": limit
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
