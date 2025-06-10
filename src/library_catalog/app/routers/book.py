from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.library_catalog.app.schemas.book import BookCreate, BookRead
from src.library_catalog.app.services.book_service import BookService

router = APIRouter()

@router.get("/", response_model=List[BookRead])
async def list_books(service: BookService = Depends()):
    return await service.get_all_books()

@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, service: BookService = Depends()):
    book = await service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book

@router.post("/", response_model=BookRead, status_code=201)
async def create_book(book: BookCreate, service: BookService = Depends()):
    return await service.create_book(book)

@router.put("/{book_id}", response_model=BookRead)
async def update_book(book_id: int, book_data: BookCreate, service: BookService = Depends()):
    updated_book = await service.update_book(book_id, book_data)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return updated_book

@router.delete("/{book_id}")
async def delete_book(book_id: int, service: BookService = Depends()):
    success = await service.delete_book(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return {"detail": "Книга удалена"}
