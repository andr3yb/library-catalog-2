from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends

from src.library_catalog.app.models import book as book_models
from src.library_catalog.app.schemas import book as book_schemas
from src.library_catalog.app.interfaces.book_repository_interface import IBookRepository
from src.library_catalog.app.integrations.open_library import OpenLibraryClient
from src.library_catalog.app.database import get_session


class BookRepository(IBookRepository):
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.openlibrary_client = OpenLibraryClient()

    async def get_all(self, limit: int, offset: int):
        query = select(book_models.Book).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, book_id: int):
        result = await self.session.execute(
            select(book_models.Book).where(book_models.Book.id == book_id)
        )
        return result.scalar_one_or_none()

    async def create(self, book_data: book_schemas.BookCreate):
        extra = await self.openlibrary_client.fetch_by_title(book_data.title) or {}

        new_book = book_models.Book(
            title=book_data.title,
            author=book_data.author,
            year=book_data.year,
            genre=book_data.genre,
            pages=book_data.pages,
            available=book_data.available,
            description=extra.get("description"),
            cover_url=extra.get("cover_url"),
            rating=extra.get("rating"),
        )

        self.session.add(new_book)
        await self.session.commit()
        await self.session.refresh(new_book)
        return new_book

    async def update(self, book_id: int, updated_data: book_schemas.BookCreate):
        book = await self.get_by_id(book_id)
        if not book:
            return None

        for field, value in updated_data.dict().items():
            setattr(book, field, value)

        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def delete(self, book_id: int):
        book = await self.get_by_id(book_id)
        if not book:
            return None

        await self.session.delete(book)
        await self.session.commit()
        return book
