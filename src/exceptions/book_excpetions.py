from uuid import UUID


class BookNotFoundException(Exception):

    def __init__(self, book_id: UUID) -> None:
        super().__init__()
        self.book_id = book_id


class InvalidBookStatusException(Exception):

    def __init__(self, status: str) -> None:
        super().__init__()
        self.status = status


class InvalidBookFieldException(Exception):

    def __init__(self, field: str) -> None:
        super().__init__()
        self.field = field
