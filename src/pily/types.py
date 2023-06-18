## Errors

import pydantic


class PilyError(Exception):
    pass


class LexerError(PilyError):
    pass


class ParserError(PilyError):
    pass


class RuntimeError(PilyError):
    pass


## Values

class Value(pydantic.BaseModel):
    pass


class ValueAtom(Value):
    value: str


## Cache

class Const(pydantic.BaseModel):
    pass

const = Const()
