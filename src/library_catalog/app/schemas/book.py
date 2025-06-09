from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    year: int
    genre: str
    pages: int
    available: bool = True

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: int
    description: Optional[str] = None
    cover_url: Optional[str] = None
    rating: Optional[float] = None

    class Config:
        from_attributes = True

