from enum import Enum


class BookFields(Enum):
    TITLE = 'title'
    AUTHOR = 'author'
    YEAR = 'year'

    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in cls._value2member_map_
