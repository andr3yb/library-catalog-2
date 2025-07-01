from sqlalchemy import Column, Integer, String, Boolean, Float
from src.library_catalog.app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    pages = Column(Integer, nullable=False)
    available = Column(Boolean, default=True)

    description = Column(String, nullable=True)
    cover_url = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
