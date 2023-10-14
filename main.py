import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests.exceptions import HTTPError
from pathvalidate import sanitize_filename
from urllib.parse import urlsplit, unquote



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

def get_image_source(book_url):
    base_url = 'https://tululu.org'
    response = requests.get(book_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    img_src = soup.find(class_='bookimage').find('img')['src']
    if img_src:
        image_link = urljoin(base_url, img_src)
        print(f"Ссылка на изображение: {image_link}")
    else:
        print("Не удалось найти ссылку на изображение.")

    return image_link

def download_txt(response, title, path, book_id):
    sanitized_title = sanitize_filename(title)
    filename = f"{book_id}.{sanitized_title}.txt"
    with open(os.path.join(path, filename), 'w', encoding='utf-8') as file:
        file.write(response.text)


def download_image(image_url, img_path, book_id):
    response = requests.get(image_url)
    response.raise_for_status()

    split_url = urlsplit(image_url)
    path = unquote(split_url.path)
    extension = path.split('.')[-1] if '.' in path else None
    imagename = f"{book_id}.{extension}"

    with open(os.path.join(img_path, imagename), 'wb') as image:
        image.write(response.content)


def main(url, download_url, path, img_path):
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
        image_link = get_image_source(book_url)
        download_txt(response, title, path, book_id)
        download_image(image_link, img_path, book_id)


if __name__ == "__main__":
    os.makedirs('books', exist_ok=True)
    os.makedirs('images', exist_ok=True)
    path = './books/'
    img_path = './images/'
    url = 'https://tululu.org/b'
    download_url = 'https://tululu.org/txt.php?id='
    main(url, download_url, path, img_path)