from . import rep


def main():
    while True:
        res = rep.rep(input('pily> '))
        if res:
            print(res)
