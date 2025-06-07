import asyncio
import aiohttp

API_KEY = "$2a$10$IgKasX5z6GKHeKem022j8O2x3DLtVZXMT/2AEAVRbYeU625W8Vce2"
BIN_ID = "6841b21a8960c979a5a5984a"
BASE_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"

HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json"
}

async def fetch_books():
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, headers=HEADERS) as response:
            response.raise_for_status()
            data = await response.json()
            return data["record"]

async def save_books(books: list):
    async with aiohttp.ClientSession() as session:
        async with session.put(BASE_URL, headers=HEADERS, json=books) as response:
            response.raise_for_status()
            return response.status == 200

async def add_book(new_book: dict):
    books = await fetch_books()
    # Генерируем новый ID: макс из существующих + 1 или 1, если пусто
    new_id = max((book.get("id", 0) for book in books), default=0) + 1
    new_book["id"] = new_id
    books.append(new_book)
    success = await save_books(books)
    if success:
        print(f"Книга добавлена с id={new_id}")
    else:
        print("Ошибка при сохранении книги")

async def main():
    print("Загружаю книги с jsonbin.io...")
    books = await fetch_books()
    print("Текущий список книг:")
    print(books)

    # Добавим тестовую книгу
    new_book = {
        "title": "Новая книга",
        "author": "Автор Тест",
        "year": 2025,
        "genre": "Тестовый жанр",
        "pages": 100,
        "available": True
    }
    print("Добавляю новую книгу...")
    await add_book(new_book)

    print("Обновленный список книг:")
    updated_books = await fetch_books()
    print(updated_books)

if __name__ == "__main__":
    asyncio.run(main())
