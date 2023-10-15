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


def get_book_info(book_url, url):
    response = requests.get(book_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.find('h1')
    title = title_tag.text.split('::')[0].strip() if title_tag else None

    img_src = soup.find(class_='bookimage').find('img')['src']
    image_link = urljoin(url, img_src) if img_src else None

    comments_elements = soup.find('div', id="content").find_all('span', class_='black')
    comments = [comment.text for comment in comments_elements]

    genre_elements = soup.find('div', id="content").find('span', class_='d_book').find_all('a')
    genres = [genre.text for genre in genre_elements]

    print(f"Заголовок:{title}\nЖанр:{genres}")

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


def main(start_id=1, end_id=11):
    path = './books/'
    img_path = './images/'
    url = 'https://tululu.org'

    if not os.path.exists(path):
        os.makedirs(path)

    if not os.path.exists(img_path):
        os.makedirs(img_path)

    for book_id in range(start_id, end_id):
        book_url = f"{url}/b{book_id}"
        book_url_to_download = f"{url}/txt.php?id={book_id}"

        try:
            response = requests.get(book_url_to_download)
            response.raise_for_status()
            check_for_redirect(response, book_url_to_download)

        except HTTPError as e:
            print(f"Error occurred for book {book_id}: {e}")
            continue

        title, image_link, comments, genres = get_book_info(book_url, url)
        if 'Деловая литература' in genres:
            download_txt(response, title, comments, path, book_id)
            download_image(image_link, img_path, book_id)


if __name__ == "__main__":
    main()