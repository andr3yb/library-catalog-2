from abc import ABC, abstractmethod
from typing import List, Optional

from src.library_catalog.app.schemas.book import BookCreate
from src.library_catalog.app.models.book import Book


class IBookService(ABC):

    @abstractmethod
    async def get_all_books(self) -> List[Book]:
        pass

    @abstractmethod
    async def get_book(self, book_id: int) -> Optional[Book]:
        pass

    @abstractmethod
    async def create_book(self, book_data: BookCreate) -> Book:
        pass

    @abstractmethod
    async def update_book(self, book_id: int, book_data: BookCreate) -> Optional[Book]:
        pass

    @abstractmethod
    async def delete_book(self, book_id: int) -> bool:
        pass
