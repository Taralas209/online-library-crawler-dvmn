import os
import time
import requests
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests.exceptions import HTTPError
from pathvalidate import sanitize_filename
from urllib.parse import urlsplit, unquote


MAX_RETRIES = 5
RETRY_DELAY = 3

def check_for_redirect(response, book_url):
    if response.history:
        raise HTTPError(f"Redirection occurred from {book_url} to {response.url}")


def parse_book_page(book_url, url):
    response = requests.get(book_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.find('h1')
    title = title_tag.text.split('::')[0].strip() if title_tag else None

    bookimage = soup.find(class_='bookimage')
    img = bookimage.find('img') if bookimage else None
    img_src = img['src'] if img else None
    image_link = urljoin(url, img_src) if img_src else None

    content_div = soup.find('div', id="content")
    comments_elements = content_div.find_all('span', class_='black') if content_div else []
    comments = [comment.text for comment in comments_elements]

    genre_elements = content_div.find('span', class_='d_book').find_all('a') if content_div else []
    genres = [genre.text for genre in genre_elements]

    return title, image_link, comments, genres


def download_txt(response, title, comments, path, book_id):
    sanitized_title = sanitize_filename(title)
    filename = f"{book_id}.{sanitized_title}.txt"
    with open(os.path.join(path, filename), 'w', encoding='utf-8') as file:
        for comment in comments:
            file.write(comment + '\n\n')
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


def main():
    parser = argparse.ArgumentParser(description="Download books from tululu.org")
    parser.add_argument("--start_id", type=int, default=1, help="ID of the first book to download")
    parser.add_argument("--end_id", type=int, default=10, help="ID of the last book to download")

    args = parser.parse_args()

    path = './books/'
    img_path = './images/'
    url = 'https://tululu.org'

    os.makedirs(path, exist_ok=True)
    os.makedirs(img_path, exist_ok=True)

    for book_id in range(args.start_id, args.end_id + 1):
        book_url = f"{url}/b{book_id}"
        book_url_to_download = f"{url}/txt.php"
        book_url_to_check = f"{url}/txt.php?id={book_id}"

        retries = 0
        while retries < MAX_RETRIES:
            try:
                response = requests.get(book_url_to_download, params={'id': book_id})
                response.raise_for_status()
                check_for_redirect(response, book_url_to_check)
                break

            except HTTPError as e:
                print(f"Error occurred for book {book_id}: {e}")
                break

            except requests.ConnectionError:
                retries += 1
                print(f"Connection error for book {book_id}. Retry {retries}/{MAX_RETRIES}...")
                time.sleep(RETRY_DELAY)

        title, image_link, comments, genres = parse_book_page(book_url, url)
        if 'Научная фантастика' in genres:
            download_txt(response, title, comments, path, book_id)
            download_image(image_link, img_path, book_id)


if __name__ == "__main__":
        main()