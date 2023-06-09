import base64
import random
from sqlalchemy import Boolean, Column, Integer, LargeBinary, Text, DateTime
from be.model.database import getDatabaseBase, getDatabaseSession
from be.model.user import User
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
            book.id = str(row.id)
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


class StoreBook(Base):
    __tablename__ = 'store'

    store_id = Column(Text, primary_key=True)
    book_id = Column(Text, primary_key=True)
    book_info = Column(Text)
    stock_level = Column(Integer)


class UserStore(Base):
    __tablename__ = 'user_store'

    user_id = Column(Text, primary_key=True)
    store_id = Column(Text, primary_key=True)


class NewOrder(Base):
    __tablename__ = 'new_order'

    order_id = Column(Text, primary_key=True, unique=True, nullable=False)
    user_id = Column(Text, nullable=False)
    store_id = Column(Text, nullable=False)
    order_time = Column(DateTime, nullable=False)
    total_price = Column(Integer, nullable=False)
    paid = Column(Boolean, nullable=False)
    cancelled = Column(Boolean, nullable=False)
    delivered = Column(Boolean, nullable=False)


class NewOrderDetail(Base):
    __tablename__ = 'new_order_detail'

    order_id = Column(Text, primary_key=True, nullable=False)
    book_id = Column(Text, primary_key=True, nullable=False)
    count = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)


def user_id_exist(user_id) -> bool:
    result = getDatabaseSession().query(User).filter(User.user_id == user_id).all()
    return len(result) != 0


def book_id_exist(store_id, book_id):
    result = getDatabaseSession().query(StoreBook).filter(
        StoreBook.store_id == store_id, StoreBook.book_id == str(book_id)).all()
    return len(result) != 0


def store_id_exist(store_id):
    result = getDatabaseSession().query(UserStore).filter(
        UserStore.store_id == store_id).all()
    return len(result) != 0
