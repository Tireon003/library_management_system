from typing import TypeVar, Sequence
from dataclasses import fields

from src.schemas import BookSchema

DC = TypeVar('DC', bound=BookSchema)


def display_data(data: Sequence[DC]) -> None:
    """
    Displays data in a table format.
    :param data: A sequence of data to display.
    :return: None
    """
    if not data:
        print("No data to display.")
        return

    field_names = [field.name for field in fields(data[0])]

    header = (len(f"{len(data)}")+2) * " " + " | ".join(f"{name: <36}" for name in field_names)
    print(header)
    print("-" * len(header))

    for index, item in enumerate(data):
        row = " | ".join(f"{getattr(item, name): <36}" for name in field_names)
        print(f"{index + 1}. {row}")

    print("-" * len(header), f"Found {len(data)} items", sep="\n")
