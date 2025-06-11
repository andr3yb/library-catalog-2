from typing import Optional
import os

from .base import BaseApiClient
from src.library_catalog.app.interfaces.open_library_interface import IOpenLibraryClient

class OpenLibraryClient(BaseApiClient, IOpenLibraryClient):
    BASE_URL = os.getenv("OPEN_LIBRARY_BASE_URL")

    async def request(self, endpoint: str, params: Optional[dict] = None) -> Optional[dict]:
        return await self._get(endpoint, params)

    async def fetch_by_title(self, title: str) -> Optional[dict]:
        data = await self.request("/search.json", {"title": title})
        if not data or not data.get("docs"):
            return None

        doc = data["docs"][0]
        return {
            "description": doc.get("first_sentence", {}).get("value") if isinstance(doc.get("first_sentence"), dict) else doc.get("first_sentence"),
            "cover_url": f"http://covers.openlibrary.org/b/id/{doc['cover_i']}-L.jpg" if doc.get("cover_i") else None,
            "rating": doc.get("ratings_average"),
        }
