from typing import Any
from src.converter.src.classes.Format import Format
from src.converter.src.globals import JSON

import os


def read(str_input: str, format: Format = JSON) -> dict[str, Any]:
    return format.read_function(str_input)


def write(d: dict[str, Any], format: Format = JSON) -> None:
    return format.write_function(d)
