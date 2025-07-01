from fastapi import FastAPI
from src.library_catalog.app.database import init_db
from src.library_catalog.app.routers.book import router as book_router


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
async def root():
    return {"message": "Library Catalog API"}


app.include_router(book_router, prefix="/books", tags=["Books"])
