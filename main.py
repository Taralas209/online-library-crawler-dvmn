import requests
import os


def main(url, path):
    for book in range(1,11):
        book_url = f"{url}{book}"
        response = requests.get(book_url)
        response.raise_for_status()
        filename = f"id{book}.txt"
        with open(os.path.join(path, filename), 'w', encoding='utf-8') as file:
            file.write(response.text)


if __name__ == "__main__":
    os.makedirs('books', exist_ok=True)
    path = "./books/"
    url = 'https://tululu.org/txt.php?id='
    main(url, path)