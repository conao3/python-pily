from typing import Optional

import more_itertools

from . import reader


def read(arg: str) -> str:
    reader_ = reader.Reader(more_itertools.peekable(arg))
    return str(reader_.read())


def eval(arg: str) -> str:
    return arg


def print(arg: str) -> str:
    return arg


def rep(arg: str) -> Optional[str]:
    return print(eval(read(arg)))
