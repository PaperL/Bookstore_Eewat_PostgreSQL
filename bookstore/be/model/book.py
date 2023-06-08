import base64
import random
from sqlalchemy import Column, Integer, LargeBinary, Text
from be.model.database import getDatabaseBase
from fe.access.book import Book


Base = getDatabaseBase()


class BookTable(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    title = Column(Text)
    author = Column(Text)
    publisher = Column(Text)
    original_title = Column(Text)
    translator = Column(Text)
    pub_year = Column(Text)
    pages = Column(Integer)
    price = Column(Integer)
    currency_unit = Column(Text)
    binding = Column(Text)
    isbn = Column(Text)
    author_intro = Column(Text)
    book_intro = Column(Text)
    content = Column(Text)
    tags = Column(Text)
    picture = Column(LargeBinary)

    @staticmethod
    def get_book_count(session):
        return session.query(BookTable).count()

    @staticmethod
    def get_book_info(session, start, size):
        books = []
        results = session.query(BookTable).order_by(
            BookTable.id).offset(start).limit(size)
        for row in results:
            book = Book()
            book.id = row.id
            book.title = row.title
            book.author = row.author
            book.publisher = row.publisher
            book.original_title = row.original_title
            book.translator = row.translator
            book.pub_year = row.pub_year
            book.pages = row.pages
            book.price = row.price
            book.currency_unit = row.currency_unit
            book.binding = row.binding
            book.isbn = row.isbn
            book.author_intro = row.author_intro
            book.book_intro = row.book_intro
            book.content = row.content
            tags = row.tags
            picture = row.picture

            for tag in tags.split("\n"):
                if tag.strip() != "":
                    book.tags.append(tag)

            for i in range(0, random.randint(0, 9)):
                if picture is not None:
                    encode_str = base64.b64encode(picture).decode('utf-8')
                    book.pictures.append(encode_str)

            books.append(book)

        return books
