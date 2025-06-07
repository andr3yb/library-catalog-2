import json
from typing import List
from pathlib import Path
from src.library_catalog.models import Book

BOOKS_FILE = Path("books.json")


def load_books() -> List[Book]:
    if not BOOKS_FILE.exists():
        return []
    with open(BOOKS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Book(**book) for book in data]


def save_books(books: List[Book]) -> None:
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump([book.dict() for book in books], f, ensure_ascii=False, indent=2)