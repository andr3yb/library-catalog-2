from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.library_catalog.app.schemas.book import BookCreate
from src.library_catalog.app.models.book import Book
from src.library_catalog.app.repositories.book_repository import BookRepository


class BookService:
    def __init__(self, session: AsyncSession):
        self.repo = BookRepository(session)

    async def get_all_books(self) -> List[Book]:
        return await self.repo.get_all()

    async def get_book(self, book_id: int) -> Optional[Book]:
        return await self.repo.get_by_id(book_id)

    async def create_book(self, book_data: BookCreate) -> Book:
        return await self.repo.create(book_data)

    async def update_book(self, book_id: int, book_data: BookCreate) -> Optional[Book]:
        return await self.repo.update(book_id, book_data)

    async def delete_book(self, book_id: int) -> bool:
        return await self.repo.delete(book_id)
