import uuid
import re
from typing import Never

from src.enums import CommandType
from src.exceptions import (
    InvalidCommandException,
    ValidationErrorException,
    BookNotFoundException,
    InvalidBookFieldException,
    InvalidBookStatusException,
)
from src.schemas import BookSchema
from src.services import BookService
from src.utils import display_data


def not_all_commands_processed() -> Never:
    raise RuntimeError("FOR DEV'S: Not all commands processed")


class App:
    """
    Class of main app. Implements application layer
    """

    GREETING = (
        "Welcome to Library management system! Enter /help to get available commands.\n"
    )
    QUOTE_CHARS = "<>"

    def __init__(self, book_service: BookService) -> None:
        self.book_service = book_service

    @staticmethod
    def show_help() -> None:
        """
        Method shows available commands.
        """
        help_text = (
            "Available commands:\n\n"
            "/help - shows available commands\n"
            "/add <title> <author> <year> - adds new book\n"
            "/remove <book_id> - removes book\n"
            "/update_status <book_id> <status> - updates book status\n"
            "/search <field> <value> [limit] - searches books by field and value\n"
            "/list [limit] - shows list of all books\n"
            "/exit - exits program\n"
            "\n"
            "* limit - optional parameter (if negative get books from end of list. Example: -5: shows last 5 books). By default limit not set\n"
        )
        print(help_text)

    def get_book_list(self, limit: str = "0") -> None:
        """
        Method gets and show list of all books. Supports limited output.
        :param limit: Optional parameter to limit number of records to output
        :return: None
        """
        try:
            limit = int(limit)
        except ValueError:
            raise ValidationErrorException

        all_books = self.book_service.get_all_books(limit)
        display_data(all_books)

    def add_new_book(self, title: str, author: str, year: str) -> None:
        """
        Method adds new book to database.
        :param title: Title of book
        :param author: Author of book
        :param year: Year of book
        :return: None
        """
        try:
            year = int(year)
            new_book = BookSchema(
                title=title,
                author=author,
                year=year,
            )
        except ValueError:
            raise ValidationErrorException

        self.book_service.add_book(new_book)
        print(f"SUCCESS. Book {new_book.title} added. UUID: {new_book.id}")

    def remove_book(self, book_id: str) -> None:
        """
        Method removes book from database.
        :param book_id: UUID string value of book
        :return: None
        """
        try:
            uuid.UUID(book_id)
            self.book_service.remove_book(book_id)
            print(f"SUCCESS. Book {book_id} removed.")
        except ValueError:
            raise ValidationErrorException
        except BookNotFoundException as e:
            print(f"ERROR. Book with id: {e.book_id} not found.")

    def update_book_status(self, book_id: str, status: str) -> None:
        """
        Method updates book status.
        :param book_id: UUID string value of book
        :param status: New status of book
        :return: None
        """
        try:
            uuid.UUID(book_id)
            self.book_service.update_book_status(
                book_id=book_id,
                status=status,
            )
            print(f"SUCCESS. Book status updated. Current status: {status}.")
        except ValueError:
            raise ValidationErrorException
        except InvalidBookStatusException as e:
            print(f"ERROR. Received invalid book status: {e.status}.")

    def search_book_by_field(self, field: str, value: str, limit: str) -> None:
        """
        Method searches books by field and value. Supports limited output.
        :param field: Field of book
        :param value: Value of field
        :param limit: Optional parameter to limit number of records to output
        :return: None
        """
        try:
            limit = int(limit)
            books = self.book_service.get_books_by_field(
                field=field,
                value=value,
                limit=limit,
            )
            display_data(books)
        except ValueError:
            raise ValidationErrorException
        except InvalidBookFieldException as e:
            print(f"ERROR. Received invalid book field: {e.field} doesn't exist.")

    @staticmethod
    def handle_command_from_user() -> tuple[str]:
        """
        Method handles command from user.
        :return: tuple of command and parameters
        """
        entered_command = input('~ ')
        pattern = r'(?:"([^"]+)"|\'([^\']+)\'|(\S+))'
        partitioned_command = [match[0] or match[1] or match[2] for match in re.findall(pattern, entered_command)]
        if not (1 <= len(partitioned_command) <= 4):
            raise InvalidCommandException
        return tuple(partitioned_command)

    def run(self) -> None:
        """
        Method runs application in infinity loop.
        :return: None
        """
        print(self.GREETING)
        while True:
            try:
                handled_command = self.handle_command_from_user()
                match handled_command[0]:
                    case CommandType.HELP.value:
                        self.show_help()
                    case CommandType.ADD.value:
                        if len(handled_command) != 4:
                            raise InvalidCommandException
                        self.add_new_book(
                            title=handled_command[1].strip(self.QUOTE_CHARS),
                            author=handled_command[2].strip(self.QUOTE_CHARS),
                            year=handled_command[3],
                        )
                    case CommandType.REMOVE.value:
                        if len(handled_command) != 2:
                            raise InvalidCommandException
                        self.remove_book(handled_command[1])
                    case CommandType.UPDATE.value:
                        if len(handled_command) != 3:
                            raise InvalidCommandException
                        self.update_book_status(
                            book_id=handled_command[1],
                            status=handled_command[2],
                        )
                    case CommandType.SEARCH.value:
                        if len(handled_command) < 3:
                            raise InvalidCommandException
                        self.search_book_by_field(
                            field=handled_command[1],
                            value=handled_command[2].strip(self.QUOTE_CHARS),
                            limit=handled_command[3]
                            if len(handled_command) == 4
                            else "0",
                        )
                    case CommandType.LIST.value:
                        if len(handled_command) > 2:
                            raise InvalidCommandException
                        if len(handled_command) == 2:
                            limit = handled_command[1]
                            self.get_book_list(limit)
                        else:
                            self.get_book_list()
                    case CommandType.EXIT.value:
                        raise EOFError
                    case _:
                        raise ValidationErrorException

            except InvalidCommandException:
                print("ERROR. Wrong command usage. Type /help to get list of available commands.")
            except EOFError:
                print("Exiting...")
                return
            except ValidationErrorException:
                print("ERROR. Invalid parameters entered. Fix entered data and try again.")

