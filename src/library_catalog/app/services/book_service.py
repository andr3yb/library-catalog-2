from typing import List, Optional
from fastapi import Depends

from src.library_catalog.app.interfaces.book_service_interface import IBookService
from src.library_catalog.app.schemas.book import BookCreate
from src.library_catalog.app.models.book import Book
from src.library_catalog.app.repositories.book_repository import BookRepository


class BookService(IBookService):
    def __init__(self, repo: BookRepository = Depends()):
        self.repo = repo

    async def get_all_books(self, limit: int, offset: int) -> List[Book]:
        return await self.repo.get_all(limit, offset)

    async def get_book(self, book_id: int) -> Optional[Book]:
        return await self.repo.get_by_id(book_id)

    async def create_book(self, book_data: BookCreate) -> Book:
        return await self.repo.create(book_data)

    async def update_book(self, book_id: int, book_data: BookCreate) -> Optional[Book]:
        return await self.repo.update(book_id, book_data)

    async def delete_book(self, book_id: int) -> bool:
        return await self.repo.delete(book_id)
