from be import conf
import re
import base64


import re
import base64
from be import conf
from be.model.book import BookTable
from be.model.database import getDatabaseSession


def serializable(book):
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "publisher": book.publisher,
        "original_title": book.original_title,
        "translator": book.translator,
        "pub_year": book.pub_year,
        "price": book.price,
        "binding": book.binding,
        "tags": book.tags,
        "picture": base64.b64encode(book.picture).decode('utf-8')
    }


class Search:

    def book_info(self, book_id: str, isbn: str):
        try:
            if book_id is not None:
                book_info = getDatabaseSession().query(BookTable).filter_by(id=book_id).first()
            elif isbn is not None:
                book_info = getDatabaseSession().query(BookTable).filter_by(isbn=isbn).first()
            else:
                raise BaseException("book_id and isbn both are None")
        except Exception as e:
            return 401, str(e)
        return 200, serializable(book_info)

    def fuzzy_search(self, term: str, store_id: str, page_size: int, page_id: int):
        if page_size is None:
            page_size = conf.default_page_size
        if page_id is None:
            page_id = 0
        # Escape special characters in the search term
        term = re.escape(term)
        # Search term in books' `title`, `author`, `publisher`, `original_title`, `translator`, `tags`, `content` and return all searched books
        try:
            book_list = []
            query = (
                getDatabaseSession().query(BookTable)
                .filter(
                    BookTable.title.ilike(f"%{term}%")
                    | BookTable.author.ilike(f"%{term}%")
                    | BookTable.publisher.ilike(f"%{term}%")
                    | BookTable.original_title.ilike(f"%{term}%")
                    | BookTable.translator.ilike(f"%{term}%")
                    | BookTable.tags.ilike(f"%{term}%")
                    | BookTable.content.ilike(f"%{term}%")
                )
            )

            if store_id is not None:
                session = getDatabaseSession()
                query = (
                    session.query(BookTable.id, BookTable.title, BookTable.author, BookTable.publisher, BookTable.original_title,
                                  BookTable.translator, BookTable.pub_year, BookTable.price, BookTable.binding, BookTable.tags, BookTable.picture)
                    .join(Store)
                    .join(BookTable, Store.book_id == BookTable.id)
                    .filter(
                        Store.store_id == store_id,
                        or_(
                            BookTable.title.ilike(f'%{term}%'),
                            BookTable.author.ilike(f'%{term}%'),
                            BookTable.publisher.ilike(f'%{term}%'),
                            BookTable.original_title.ilike(f'%{term}%'),
                            BookTable.translator.ilike(f'%{term}%'),
                            BookTable.tags.ilike(f'%{term}%'),
                            BookTable.content.ilike(f'%{term}%')
                        )
                    )
                    # .offset(page_id * page_size)
                    # .limit(page_size)
                )

            total_results = query.count()
            results = (
                query.order_by(BookTable.id)
                .offset(page_id * page_size)
                .limit(page_size)
                .all()
            )

            for row in results:
                book = serializable(row)
                book_list.append(book)

        except Exception as e:
            return 501, str(e)

        return 200, {"books": book_list, "total_results": total_results}
