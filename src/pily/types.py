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


class ValueCons(Value):
    car: Value
    cdr: Value


class ValueAtom(Value):
    pass


class ValueSymbol(ValueAtom):
    name: str


## Cache

class Const(pydantic.BaseModel):
    pass

const = Const()
