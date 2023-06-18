from typing import Optional


def read(arg: str) -> str:
    return arg


def eval(arg: str) -> str:
    return arg


def print(arg: str) -> str:
    return arg


def rep(arg: str) -> Optional[str]:
    return print(eval(read(arg)))
