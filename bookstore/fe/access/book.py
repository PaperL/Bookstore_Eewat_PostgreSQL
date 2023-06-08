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
