import sqlite3
from typing import List


class Book:
    id: str
    title: str
    author: str
    publisher: str
    original_title: str
    translator: str
    pub_year: str
    pages: int
    price: int
    currency_unit: str
    binding: str
    isbn: str
    author_intro: str
    book_intro: str
    content: str
    tags: List[str]
    pictures: List[bytes]

    def __init__(self):
        self.tags = []
        self.pictures = []


class BookDB:
    def __init__(self, large: bool = False):
        self.large = large
        self.connection = sqlite3.connect('fe/data/book.db')

    def get_book_count(self):
        cur = self.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM book")
        count = cur.fetchone()[0]
        cur.close()
        return count

    def get_book_info(self, start, size) -> List[Book]:
        cur = self.connection.cursor()
        if size > 0:
            cur.execute("SELECT * FROM book LIMIT ?, ?", (start, size))
        else:
            cur.execute("SELECT * FROM book")
        rows = cur.fetchall()
        cur.close()

        books = []
        for row in rows:
            book = Book()
            book.id = row[0]
            book.title = row[1]
            book.author = row[2]
            book.publisher = row[3]
            book.original_title = row[4]
            book.translator = row[5]
            book.pub_year = row[6]
            book.pages = row[7]
            book.price = row[8]
            book.currency_unit = row[9]
            book.binding = row[10]
            book.isbn = row[11]
            book.author_intro = row[12]
            book.book_intro = row[13]
            book.content = row[14]
            book.pictures = []
            for tag in row[15].split("\n"):
                if tag.strip() != "":
                    book.tags.append(tag)

            books.append(book)

        return books