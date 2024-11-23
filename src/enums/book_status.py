from enum import Enum


class BookStatus(Enum):
    AVAILABLE = "available"
    ISSUED = "issued"

    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in cls._value2member_map_
