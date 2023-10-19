# Online Library Scraper

## Description
This program is designed to download science fiction books from the [tululu.org](https://tululu.org/) website. You can specify a range of book identifiers to download, and the program will fetch them for you.

## Installation
1. Install Python from the [official website](https://www.python.org/downloads/).
2. Download the code to your computer.
3. Install the dependencies using `pip` (or `pip3` if you have both Python 2 and Python 3 installed):

```bash
pip install -r requirements.txt
```

## Usage
Run the program from the command line.
Use the --start_id and --end_id arguments to specify the range of book identifiers you want to download. For example:

```bash
python main.py --start_id <start_ID> --end_id <end_ID>
```
Where <start_ID> is the identifier of the first book to download, and <end_ID> is the identifier of the last book.

Example:
```bash
python main.py --start_id 1 --end_id 10
```
or
```bash
python main.py 1 10
```
This will download books with identifiers from 1 to 10 inclusive.

After the program has finished running, the books will be saved in the ./books/ directory, and the cover images will be stored in the ./images/ directory.

Note: Make sure you have all the required libraries installed before running the program.

## Program Features Overview
### Function ``check_for_redirect(response, book_url)``
This function checks if a redirect occurred when trying to download a book. If a redirect occurred, the function raises an error.

### Function ``parse_book_page(book_url, url)``
This function parses the tululu.org book page and extracts the following information:

- Book title
- Link to the book cover
- Comments about the book
- Book genres

### Function ``download_txt(response, title, comments, path, book_id)``
This function downloads the text of the book and saves it to a file with a name based on the book's identifier and title. Comments about the book are also added to the beginning of the file.

### Function ``download_image(image_url, img_path, book_id)``
This function downloads the book cover and saves it to the specified directory with a filename based on the book's identifier.

### Function ``main(start_id=1, end_id=10)``
This is the main program function. It sets initial parameters, creates the necessary directories, and initiates the book download process.

### Command-Line Argument Parser
The program also includes a command-line argument parser that allows the user to specify the identifiers of the first and last books to download.

## Project Goals
This code was written for educational purposes as part of an online course for web developers on [dvmn.org](https://dvmn.org/).