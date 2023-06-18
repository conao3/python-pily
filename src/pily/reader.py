from typing import Optional
from collections.abc import Callable
import more_itertools

from . import types
from . import subr


TERMINATING_MACRO_CHARS = '"\'()*,;`'
NON_TERMINATING_MACRO_CHARS = '#'


def read_double_quote(chars: more_itertools.peekable) -> types.Value:
    next(chars)  # consume start "
    s = ''.join(subr.takewhile_inclusive(lambda c: c != '"', chars))

    next(chars)  # consume end "

    return types.ValueString(value=s)


macro_handler: dict[str, Callable[[more_itertools.peekable], types.Value]] = {
    '"': read_double_quote,
    "'": NotImplementedError(),
    '(': NotImplementedError(),
    ')': NotImplementedError(),
    '*': NotImplementedError(),
    ',': NotImplementedError(),
    ';': NotImplementedError(),
    '`': NotImplementedError(),
    '#': NotImplementedError(),
}


class Reader:
    def __init__(self, chars: more_itertools.peekable):
        self.chars = chars

    def consume(self) -> str:
        return next(self.chars)

    def consume_space(self) -> None:
        while (peek := self.chars.peek(None)):
            if not peek.isspace():
                return

            self.consume()

    def read_atom(self) -> types.Value:
        s = ''.join(subr.takewhile_inclusive(lambda c: c not in TERMINATING_MACRO_CHARS, self.chars))

        i, _ = subr.trap(lambda: int(s))
        if i is not None:
            return types.ValueInteger(value=i)

        f, _ = subr.trap(lambda: float(s))
        if f is not None:
            return types.ValueFloat(value=f)

        return types.ValueSymbol(name=s)

    def read(self) -> Optional[types.Value]:
        self.consume_space()

        peek: Optional[str] = self.chars.peek(None)

        if peek is None:
            return None

        if peek in TERMINATING_MACRO_CHARS or peek in NON_TERMINATING_MACRO_CHARS:
            handler = macro_handler.get(peek)
            if not handler:
                raise NotImplementedError()

            return handler(self.chars)

        if peek == '\\':
            raise NotImplementedError()

        if peek == '|':
            raise NotImplementedError()

        return self.read_atom()
