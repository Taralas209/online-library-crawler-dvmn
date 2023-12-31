# Парсер онлайн-библиотеки

## Описание
Эта программа предназначена для скачивания научно-фантастических книг с сайта [tululu.org](https://tululu.org/). Вы можете выбрать диапазон идентификаторов книг для скачивания, и программа скачает их для вас.

## Установка
1. Установите Python с [официального сайта](https://www.python.org/downloads/).
2. Скачайте код на свой компьютер
3. Установите зависимости используя `pip` (или `pip3`, если у вас установлены и Python2, и Python3):

```bash
pip install -r requirements.txt
```

## Использование
1. Запустите программу из командной строки.
2. Используйте аргументы --start_id и --end_id для указания диапазона идентификаторов книг, которые вы хотите скачать. Например:

```bash
python main.py --start_id <начальный_ID> --end_id <конечный_ID>
```
Где <начальный_ID> - идентификатор первой книги для скачивания, <конечный_ID> - идентификатор последней книги.

Пример:

```bash
python main.py --start_id 1 --end_id 10
```
или

```bash
python main.py 1 10
```
Это загрузит книги с идентификаторами от 1 до 10 включительно.

После выполнения программы, книги будут сохранены в директории ./books/, а обложки - в директории ./images/.
Примечание: Убедитесь, что у вас установлены все необходимые библиотеки, прежде чем запускать программу.

## Обзор возможностей программы
### Функция ``check_for_redirect(response, book_url)``
Эта функция проверяет, произошло ли перенаправление при попытке загрузки книги. Если произошло перенаправление, функция вызывает ошибку.

### Функция ``parse_book_page(book_url, url)``
Эта функция анализирует страницу книги на сайте tululu.org и извлекает следующую информацию:

- Название книги
- Ссылку на обложку книги
- Комментарии о книге
- Жанры книги

### Функция ``download_txt(response, title, comments, path, book_id)``
Эта функция скачивает текст книги и сохраняет его в файл с именем, основанным на идентификаторе и названии книги. Также комментарии о книге добавляются в начало файла.

### Функция ``download_image(image_url, img_path, book_id)``
Эта функция скачивает обложку книги и сохраняет ее в указанную директорию с именем файла, основанным на идентификаторе книги.

### Функция ``main(start_id=1, end_id=10)``
Это главная функция программы. Она устанавливает начальные параметры, создает необходимые директории и начинает процесс скачивания книг.

### Парсер аргументов командной строки
Программа также включает парсер аргументов командной строки, который позволяет пользователю указать идентификаторы первой и последней книги для скачивания.

## Цели проекта
Этот код был написан в образовательных целях в рамках онлайн-курса для веб-разработчиков на [dvmn.org](https://dvmn.org/).