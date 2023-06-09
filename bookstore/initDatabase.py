import sqlite3
import sqlalchemy
from sqlalchemy_utils import drop_database, create_database
from sqlalchemy.orm import session

from be.model.database import getDatabaseSession, init_database
from be.model.tables import BookTable

database_url = 'postgresql://postgres:123456@localhost:5432/bookstore'

# Do not drop if run for the first time.
def flush_database():
    drop_database(database_url)
    create_database(database_url)

flush_database()

conn = sqlite3.connect('fe/data/book.db')
cur = conn.cursor()
cur.execute("SELECT * FROM book")
rows = cur.fetchall()
cur.close()
conn.close()

init_database()

for row in rows:
    book = {
        'id': row[0],
        'title': row[1],
        'author': row[2],
        'publisher': row[3],
        'original_title': row[4],
        'translator': row[5],
        'pub_year': row[6],
        'pages': row[7],
        'price': row[8],
        'currency_unit': row[9],
        'binding': row[10],
        'isbn': row[11],
        'author_intro': row[12],
        'book_intro': row[13],
        'content': row[14],
        'tags': row[15],
        'picture': row[16]
    }
    new_book = BookTable(
        id=book['id'],
        title=book['title'],
        author=book['author'],
        publisher=book['publisher'],
        original_title=book['original_title'],
        translator=book['translator'],
        pub_year=book['pub_year'],
        pages=book['pages'],
        price=book['price'],
        currency_unit=book['currency_unit'],
        binding=book['binding'],
        isbn=book['isbn'],
        author_intro=book['author_intro'],
        book_intro=book['book_intro'],
        content=book['content'],
        tags=book['tags'],
        picture=book['picture']
    )
    session = getDatabaseSession()
    session.add(new_book)
    session.commit()

session.close()

# engine = sqlalchemy.create_engine(database_url)

# # Get the list of table names
# table_names = engine.table_names()

# # Print all table names
# for table_name in table_names:
#     print(table_name)