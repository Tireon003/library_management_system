from enum import Enum


class CommandType(Enum):
    HELP = "/help"
    ADD = "/add"
    SEARCH = "/search"
    EXIT = "/exit"
    REMOVE = "/remove"
    LIST = "/list"
    UPDATE = "/update_status"

    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in cls._value2member_map_
