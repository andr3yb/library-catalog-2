from abc import ABC, abstractmethod
from typing import List, Optional
from src.library_catalog.app.schemas.book import BookCreate
from src.library_catalog.app.models.book import Book


class IBookRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Book]:
        pass

    @abstractmethod
    async def get_by_id(self, book_id: int) -> Optional[Book]:
        pass

    @abstractmethod
    async def create(self, book_data: BookCreate) -> Book:
        pass

    @abstractmethod
    async def update(self, book_id: int, book_data: BookCreate) -> Optional[Book]:
        pass

    @abstractmethod
    async def delete(self, book_id: int) -> bool:
        pass
