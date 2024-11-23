import json
from collections.abc import Iterator
from contextlib import contextmanager
import dotenv
import os

dotenv.load_dotenv()

book_storage_file = os.getenv("BOOK_STORAGE_NAME")


class BookStorage:
    """
    Class for working with book storage. Implements a simple json-storage
    """
    def __init__(self, storage_name: str = book_storage_file) -> None:
        self._storage_name = storage_name
        self._memoized_storage: dict = {}

    def _get_storage(self) -> dict:
        if not os.path.exists(self._storage_name):
            with open(self._storage_name, "x") as file:
                json.dump(self._memoized_storage, file)
        with open(self._storage_name, "r") as file:
            storage_payload = json.load(file)
            self._memoized_storage = storage_payload
            return self._memoized_storage

    def _set_storage(self) -> None:
        try:
            with open(self._storage_name, "w") as file:
                json.dump(self._memoized_storage, file)
        except FileNotFoundError:
            with open(self._storage_name, "x") as file:
                json.dump(self._memoized_storage, file)

    @contextmanager
    def storage(self) -> Iterator[dict]:
        try:
            yield self._get_storage()
        finally:
            self._set_storage()

