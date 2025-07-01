import abc
import logging
from typing import Any, Dict, Optional

import aiohttp


class BaseApiClient(abc.ABC):
    BASE_URL: str

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abc.abstractmethod
    async def request(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Абстрактный метод запроса"""
        pass

    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.BASE_URL}{endpoint}"
        self.logger.debug(f"GET Request: {url} | Params: {params}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as e:
            self.logger.error(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return None
