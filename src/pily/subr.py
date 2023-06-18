import typing
from typing import Iterable
from collections.abc import Callable

import more_itertools


T = typing.TypeVar('T')
def trap(fn: Callable[[], T]) -> tuple[T, None] | tuple[None, Exception]:
    try:
        return fn(), None
    except Exception as e:
        return None, e


def takewhile_inclusive(pred: Callable[[T], bool], peekable: more_itertools.peekable) -> Iterable[T]:
    while True:
        try:
            x = peekable.peek()
        except StopIteration:
            break

        if pred(x):
            yield next(peekable)
        else:
            break
