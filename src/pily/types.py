## Errors

import pydantic


class PilyError(Exception):
    pass


class ReaderError(PilyError):
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


class ValueInteger(ValueAtom):
    value: int


class ValueFloat(ValueAtom):
    value: float


class ValueString(ValueAtom):
    value: str


class ValueChar(ValueAtom):
    value: str


class ValueMultiple(ValueAtom):
    values: list[Value]


## Cache

class Const(pydantic.BaseModel):
    pass

const = Const()
