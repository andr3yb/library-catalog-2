from abc import ABC, abstractmethod
from typing import Optional


class IOpenLibraryClient(ABC):
    @abstractmethod
    async def fetch_by_title(self, title: str) -> Optional[dict]:
        pass
