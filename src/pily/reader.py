from typing import Optional
import more_itertools

from . import types
from . import subr


TERMINATING_MACRO_CHARS = '"\'()*,;`'
NON_TERMINATING_MACRO_CHARS = '#'


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

        if peek in TERMINATING_MACRO_CHARS:
            raise NotImplementedError()

        if peek in NON_TERMINATING_MACRO_CHARS:
            raise NotImplementedError()

        if peek == '\\':
            raise NotImplementedError()

        if peek == '|':
            raise NotImplementedError()

        return self.read_atom()
