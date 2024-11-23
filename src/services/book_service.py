from typing import Type, Self

from src.enums import BookStatus, BookFields
from src.exceptions import (
    BookNotFoundException,
    InvalidBookStatusException,
    InvalidBookFieldException,
)
from src.schemas import BookSchema
from src.storages import BookStorage


class BookService:
    """
    Class for interact with book storage. Implements a service layer
    """
    def __init__(self, book_storage: BookStorage) -> None:
        self._book_storage = book_storage

    @classmethod
    def init_service(cls, book_storage: Type[BookStorage]) -> Self:
        """
        Method for init service
        :param book_storage: Class of book storage
        :return: New instance of BookService class
        """
        return cls(book_storage())

    def add_book(self, book: BookSchema) -> None:
        """
        Method for add book to storage. Creates a new book and adds it to storage
        :param book: Book dataclass schema
        :return: None
        """
        with self._book_storage.storage() as storage:
            storage[f"{book.id}"] = dict(
                title=book.title,
                author=book.author,
                year=book.year,
                status=book.status.value,
            )

    def remove_book(self, book_id: str) -> None:
        """
        Method for remove book from storage
        :param book_id: book UUID string value
        :return: None
        """
        with self._book_storage.storage() as storage:
            if not storage.get(book_id):
                raise BookNotFoundException(book_id)
            del storage[book_id]

    def get_all_books(self, limit: int = 0) -> list[BookSchema]:
        """
        Method for get all books from storage
        :param limit: limit of books (optional)
        :return: list of books
        """
        all_books = []
        with self._book_storage.storage() as storage:
            for book_id, book_data in storage.items():
                all_books.append(BookSchema(
                    id=book_id,
                    title=book_data["title"],
                    author=book_data["author"],
                    year=book_data["year"],
                    status=book_data["status"],
                ))
        if limit == 0:
            return all_books
        elif limit > 0:
            return all_books[:limit]
        else:
            return all_books[limit:]

    def get_books_by_field(
            self,
            field: str,
            value: str,
            limit: int | None = None
    ) -> list[BookSchema]:
        """
        Method for get books by provided field
        :param field: field of book
        :param value: value of field
        :param limit: limit of books (optional)
        :return: list of books
        """
        books = []

        if not BookFields.has_value(field):
            raise InvalidBookFieldException(field)

        with self._book_storage.storage() as storage:
            for book_id, book_data in storage.items():
                field_value = f"{book_data[field].casefold().strip()}"
                if value.casefold().strip() in field_value:
                    books.append(BookSchema(
                        id=book_id,
                        title=book_data["title"],
                        author=book_data["author"],
                        year=book_data["year"],
                        status=book_data["status"],
                    ))

        if not limit:
            return books
        elif limit > 0:
            return books[:limit]
        else:
            return books[limit:]

    def update_book_status(self, book_id: str, status: str) -> None:
        """
        Method for update book status
        :param book_id: book UUID string value
        :param status: new status of book
        :return: None
        """
        with self._book_storage.storage() as storage:
            if not storage.get(book_id):
                raise BookNotFoundException(book_id)
            if not BookStatus.has_value(status):
                raise InvalidBookStatusException(status)
            storage[book_id]["status"] = status
