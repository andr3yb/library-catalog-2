import os
from typing import Optional

from .base import BaseApiClient


class JsonBinClient(BaseApiClient):
    def __init__(self):
        super().__init__()
        self.BIN_ID = os.getenv("JSONBIN_BIN_ID")
        self.API_KEY = os.getenv("JSONBIN_API_KEY")
        self.BASE_URL = f"https://api.jsonbin.io/v3/b/{self.BIN_ID}"
        self.HEADERS = {
            "X-Master-Key": self.API_KEY,
            "Content-Type": "application/json"
        }

    async def request(self, endpoint: str = "", params: Optional[dict] = None) -> Optional[dict]:
        return await self._get(endpoint or "", params)

    async def fetch_books(self) -> list:
        data = await self.request()
        return data.get("record", []) if data else []

    async def save_books(self, books: list) -> bool:
        import aiohttp
        try:
            async with aiohttp.ClientSession() as session:
                async with session.put(self.BASE_URL, headers=self.HEADERS, json=books) as response:
                    response.raise_for_status()
                    return True
        except Exception as e:
            self.logger.error(f"Error saving books to JSONBin: {e}")
            return False
