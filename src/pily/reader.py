from typing import Optional
from collections.abc import Callable
import more_itertools

from . import types
from . import subr


TERMINATING_MACRO_CHARS = ' "\'()*,;`'
NON_TERMINATING_MACRO_CHARS = '#'


def consume(chars: more_itertools.peekable) -> str:
    return next(chars)


def consume_space(chars: more_itertools.peekable) -> None:
    while (peek := chars.peek(None)):
        if not peek.isspace():
            return

        consume(chars)


def consume_expect(chars: more_itertools.peekable, expected: str) -> None:
    consume_space(chars)

    if chars.peek(None) != expected:
        raise ValueError(f'Expected {expected}')


def read_double_quote(chars: more_itertools.peekable) -> types.Value:
    consume(chars)  # consume start "
    s = ''.join(subr.takewhile_inclusive(lambda c: c != '"', chars))

    consume(chars)  # consume end "

    return types.ValueString(value=s)


def read_single_quote(chars: more_itertools.peekable) -> types.Value:
    consume(chars)  # consume start '
    v = read(chars, recursive_p=True)

    return types.ValueCons(
        car=types.ValueSymbol(name='quote'),
        cdr=types.ValueCons(car=v, cdr=types.ValueSymbol(name='nil'))
    )


def read_left_paren(chars: more_itertools.peekable) -> types.Value:
    consume(chars)  # consume start (
    consume_space(chars)

    if chars.peek(None) == ')':
        consume(chars)  # consume end )
        return types.ValueSymbol(name='nil')

    car = types.ValueCons(car=read(chars, recursive_p=True), cdr=types.ValueSymbol(name='nil'))
    cur = car

    while True:
        consume_space(chars)

        if chars.peek(None) == ')':
            consume(chars)  # consume end )
            break

        if chars.peek(None) == '.':
            cur.cdr = read(chars, recursive_p=True)
            consume_expect(chars, ')')  # consume end )
            break

        cur.cdr = types.ValueCons(car=read(chars, recursive_p=True), cdr=types.ValueSymbol(name='nil'))
        cur = cur.cdr

    return car


def read_right_paren(chars: more_itertools.peekable) -> types.Value:
    consume(chars)  # consume )
    raise types.ReaderError('unexpected )')


def read_semicolon(chars: more_itertools.peekable) -> types.Value:
    while True:
        res = read_char(chars, eof_error_p=False, eof_value=types.ValueChar(value='\n'))
        if isinstance(res, types.ValueChar) and res.value == '\n':
            break

    return types.ValueMultiple(values=[])


macro_handler: dict[str, Callable[[more_itertools.peekable], types.Value]] = {
    '"': read_double_quote,
    "'": read_single_quote,
    '(': read_left_paren,
    ')': read_right_paren,
    '*': NotImplementedError(),
    ',': NotImplementedError(),
    ';': read_semicolon,
    '`': NotImplementedError(),
    '#': NotImplementedError(),
}


def read_atom(chars: more_itertools.peekable) -> types.Value:
    s = ''.join(subr.takewhile_inclusive(lambda c: c not in TERMINATING_MACRO_CHARS, chars))
    consume_space(chars)

    i, _ = subr.trap(lambda: int(s))
    if i is not None:
        return types.ValueInteger(value=i)

    f, _ = subr.trap(lambda: float(s))
    if f is not None:
        return types.ValueFloat(value=f)

    return types.ValueSymbol(name=s)


def read_char(
    chars: more_itertools.peekable,
    eof_error_p: bool = True,
    eof_value: types.Value = types.ValueSymbol(name='nil'),
    recursive_p: bool = False,
) -> types.Value:
    peek: Optional[str] = chars.peek(None)

    if peek is None:
        if eof_error_p:
            raise types.ReaderError('unexpected EOF')
        return eof_value

    return types.ValueChar(value=consume(chars))


def read(
    chars: more_itertools.peekable,
    eof_error_p: bool = True,
    eof_value: types.Value = types.ValueSymbol(name='nil'),
    recursive_p: bool = False,
) -> types.Value:
    consume_space(chars)

    peek: Optional[str] = chars.peek(None)

    if peek is None:
        if eof_error_p:
            raise types.ReaderError('unexpected EOF')
        return eof_value

    if peek in TERMINATING_MACRO_CHARS or peek in NON_TERMINATING_MACRO_CHARS:
        handler = macro_handler.get(peek)
        if not handler:
            raise NotImplementedError()

        return handler(chars)

    if peek == '\\':
        raise NotImplementedError()

    if peek == '|':
        raise NotImplementedError()

    return read_atom(chars)
