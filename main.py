from src.app import App
from src.services import BookService
from src.storages import BookStorage


def main() -> None:
    book_service = BookService.init_service(BookStorage)
    app = App(book_service)
    app.run()


if __name__ == "__main__":
    main()
