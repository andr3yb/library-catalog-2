import pytest
from unittest.mock import AsyncMock
from src.library_catalog.app.services.book_service import BookService
from src.library_catalog.app.schemas.book import BookCreate
from src.library_catalog.app.models.book import Book


@pytest.fixture
def fake_repo():
    repo = AsyncMock()
    return repo


@pytest.fixture
def service(fake_repo):
    return BookService(repo=fake_repo)


@pytest.mark.asyncio
async def test_get_all_books(service, fake_repo):
    fake_repo.get_all.return_value = [Book(id=1, title="Test Book")]
    books = await service.get_all_books(limit=10, offset=0)
    assert len(books) == 1
    assert books[0].title == "Test Book"
    fake_repo.get_all.assert_called_once_with(10, 0)


@pytest.mark.asyncio
async def test_create_book(service, fake_repo):
    book_data = BookCreate(
        title="New Book",
        author="Author",
        year=2020,
        genre="Fiction",
        pages=100,
        available=True,
    )
    fake_repo.create.return_value = Book(id=1, **book_data.model_dump())
    book = await service.create_book(book_data)
    assert book.title == "New Book"
    fake_repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_delete_book(service, fake_repo):
    fake_repo.delete.return_value = True
    result = await service.delete_book(1)
    assert result is True
    fake_repo.delete.assert_called_once_with(1)
