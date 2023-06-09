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

# class BookDB:

#     def get_book_count(self):
#         session = getDatabaseSession()
#         return len(session.query(BookTable).all())

#     def get_book_info(self, start, size) -> List[Book]:
#         books = []
#         session = getDatabaseSession()
#         result = session.query(BookTable).order_by(
#             BookTable.id).offset(start).limit(size).all()
#         for row in result:
#             book = Book()
#             book.id = row.id
#             book.title = row.title
#             book.author = row.author
#             book.publisher = row.publisher
#             book.original_title = row.original_title
#             book.translator = row.translator
#             book.pub_year = row.pub_year
#             book.pages = row.pages
#             book.price = row.price
#             book.currency_unit = row.currency_unit
#             book.binding = row.binding
#             book.isbn = row.isbn
#             book.author_intro = row.author_intro
#             book.book_intro = row.book_intro
#             book.content = row.content
#             tags = row.tags
#             picture = row.picture

#             for tag in tags.split("\n"):
#                 if tag.strip() != "":
#                     book.tags.append(tag)
#             for i in range(0, random.randint(0, 9)):
#                 if picture is not None:
#                     encode_str = base64.b64encode(picture).decode('utf-8')
#                     book.pictures.append(encode_str)
#             books.append(book)

#         return books
