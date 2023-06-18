from typing import Optional
import more_itertools

from . import types


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

    def read_atom(self) -> types.ValueAtom:
        return types.ValueAtom(value=self.consume())

    def read(self) -> Optional[types.Value]:
        self.consume_space()

        peek: Optional[str] = self.chars.peek(None)

        if peek is None:
            return None

        return self.read_atom()
