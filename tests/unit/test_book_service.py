import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.library_catalog.app.database import Base
from src.library_catalog.app.repositories.book_repository import BookRepository
from src.library_catalog.app.schemas.book import BookCreate


@pytest_asyncio.fixture
async def test_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def test_session(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def book_repository(test_session):
    return BookRepository(session=test_session)


@pytest.mark.asyncio
async def test_create_and_get_book(book_repository):
    book_data = BookCreate(
        title="SQLite Real",
        author="Author",
        year=2025,
        genre="Test",
        pages=123,
        available=True,
    )
    created = await book_repository.create(book_data)
    assert created.id is not None
    assert created.title == "SQLite Real"

    found = await book_repository.get_by_id(created.id)
    assert found is not None
    assert found.title == "SQLite Real"


@pytest.mark.asyncio
async def test_get_all_books(book_repository):
    books = await book_repository.get_all(limit=10, offset=0)
    assert books == []

    await book_repository.create(
        BookCreate(
            title="Book One",
            author="A",
            year=2000,
            genre="Fiction",
            pages=100,
            available=True,
        )
    )
    await book_repository.create(
        BookCreate(
            title="Book Two",
            author="B",
            year=2010,
            genre="Non-fiction",
            pages=200,
            available=False,
        )
    )

    books = await book_repository.get_all(limit=10, offset=0)
    assert len(books) == 2
    titles = [b.title for b in books]
    assert "Book One" in titles
    assert "Book Two" in titles


@pytest.mark.asyncio
async def test_update_book(book_repository):
    created = await book_repository.create(
        BookCreate(
            title="Original",
            author="Author",
            year=2020,
            genre="Fiction",
            pages=150,
            available=True,
        )
    )

    updated = await book_repository.update(
        created.id,
        BookCreate(
            title="Updated",
            author="Author New",
            year=2021,
            genre="Drama",
            pages=200,
            available=False,
        ),
    )

    assert updated.title == "Updated"
    assert updated.year == 2021


@pytest.mark.asyncio
async def test_delete_book(book_repository):
    created = await book_repository.create(
        BookCreate(
            title="To Delete",
            author="Someone",
            year=1999,
            genre="Old",
            pages=50,
            available=True,
        )
    )

    deleted = await book_repository.delete(created.id)
    assert deleted is not None
    assert deleted.id == created.id

    should_be_none = await book_repository.get_by_id(created.id)
    assert should_be_none is None
