from dataclasses import dataclass, field, fields
from uuid import UUID, uuid4
from typing import Never

from src.enums import BookStatus


def skipped_some_statuses(provided_status: str) -> Never:
    valid_statuses = ", ".join(status for status in BookStatus)
    raise ValueError(
        "Invalid status provided: {}. Use the following: {}"
        .format(provided_status, valid_statuses)
    )


@dataclass
class BookSchema:

    title: str
    author: str
    year: int
    status: BookStatus = field(default=BookStatus.AVAILABLE)
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        self.validate_fields()

    def validate_fields(self) -> None:
        """
        Method to validate fields. Raises ValueError if any field is invalid.
        :return: None
        """
        fields_in_dataclass = set([attr.name for attr in fields(self)])
        for field_name in fields_in_dataclass:
            attr_value = getattr(self, field_name)
            if isinstance(attr_value, str):
                if not (6 <= len(attr_value) <= 36):
                    raise ValueError("String field must be between 6 and 36 characters")
            elif isinstance(attr_value, int):
                if not (1900 <= attr_value <= 2100):
                    raise ValueError("Year must be between 1900 and 2100")
            elif isinstance(attr_value, BookStatus):
                if attr_value.value not in BookStatus:
                    raise ValueError("Invalid status provided")
