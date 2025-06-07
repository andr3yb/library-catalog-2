import requests

API_KEY = "$2a$10$IgKasX5z6GKHeKem022j8O2x3DLtVZXMT/2AEAVRbYeU625W8Vce2"
BIN_ID = "6841b21a8960c979a5a5984a"
BASE_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"

HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json"
}

def fetch_books():
    print("Загружаю книги с jsonbin.io...")
    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code == 200:
        books = response.json()["record"]
        print("Книги успешно получены:\n")
        for book in books:
            print(book)
    else:
        print(f"Ошибка при загрузке: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    fetch_books()
