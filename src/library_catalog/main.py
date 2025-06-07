from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.library_catalog.database import SessionLocal, engine
from src.library_catalog.models import Base
from src.library_catalog import schemas
from src.library_catalog.repository import BookRepository

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Dependency
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

@app.get("/")
async def root():
    return {"message": "Library Catalog API"}

@app.get("/books", response_model=List[schemas.BookRead])
async def get_books(
    author: Optional[str] = None,
    genre: Optional[str] = None,
    session: AsyncSession = Depends(get_session)
):
    repo = BookRepository(session)
    books = await repo.get_all()
    if author:
        books = [b for b in books if b.author == author]
    if genre:
        books = [b for b in books if b.genre == genre]
    return books


@app.get("/books/{book_id}", response_model=schemas.BookRead)
async def get_book(
    book_id: int,
    session: AsyncSession = Depends(get_session)
):
    repo = BookRepository(session)
    book = await repo.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book


@app.post("/books", response_model=schemas.BookRead)
async def create_book(
    book: schemas.BookCreate,
    session: AsyncSession = Depends(get_session)
):
    repo = BookRepository(session)
    return await repo.create(book)


@app.put("/books/{book_id}", response_model=schemas.BookRead)
async def update_book(
    book_id: int,
    updated_book: schemas.BookCreate,
    session: AsyncSession = Depends(get_session)
):
    repo = BookRepository(session)
    updated = await repo.update(book_id, updated_book)
    if not updated:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return updated


@app.delete("/books/{book_id}")
async def delete_book(
    book_id: int,
    session: AsyncSession = Depends(get_session)
):
    repo = BookRepository(session)
    deleted = await repo.delete(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return {"detail": "Книга удалена"}