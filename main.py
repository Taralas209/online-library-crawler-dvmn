import requests
import os
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response, book_url):
    if response.url != book_url or response.history:
        raise HTTPError(f"Redirection occurred from {book_url} to {response.url}")


def get_book_title(book_url):
    response = requests.get(book_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    if title_tag:
        title_text = title_tag.text.split('::')
        title = title_text[0].strip()
        print(f"Заголовок: {title}")
    else:
        print("Не удалось найти заголовок.")

    return title

def download_txt(response, title, path, book_id):
    sanitized_title = sanitize_filename(title)
    filename = f"{book_id}.{sanitized_title}.txt"
    with open(os.path.join(path, filename), 'w', encoding='utf-8') as file:
        file.write(response.text)


def main(url, download_url, path):
    for book_id in range(1, 11):
        book_url = f"{url}{book_id}"
        book_url_to_download = f"{download_url}{book_id}"

        try:
            response = requests.get(book_url_to_download)
            response.raise_for_status()
            check_for_redirect(response, book_url_to_download)

        except HTTPError as e:
            print(f"Error occurred for book {book_id}: {e}")
            continue

        title = get_book_title(book_url)
        download_txt(response, title, path, book_id)


if __name__ == "__main__":
    os.makedirs('books', exist_ok=True)
    path = "./books/"
    url = 'https://tululu.org/b'
    download_url = 'https://tululu.org/txt.php?id='
    main(url, download_url, path)