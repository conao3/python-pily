from typing import Optional

import more_itertools

from . import types
from . import reader


def read(arg: str) -> Optional[types.Value]:
    reader_ = reader.Reader(more_itertools.peekable(arg))
    return reader_.read()


def eval(arg: Optional[types.Value]) -> Optional[types.Value]:
    if arg:
        return arg

    return None


def print(arg: Optional[types.Value]) -> Optional[str]:
    if arg:
        return str(arg)

    return None


def rep(arg: str) -> Optional[str]:
    return print(eval(read(arg)))
