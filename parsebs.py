#!/usr/bin/env python3

import re


class Error(Exception):
    pass


class InvalidSymbols(Error):
    def __init__(self, exp):
        self.expression = exp

    @property
    def msg(self):
        print('Invalid symbols: ', self.expression)


def parse(boolexp):
    boolexp = boolexp.replace(' ', '')
    pattern = re.compile(r'[^\(\)\+~a-z]', re.IGNORECASE)
    match = pattern.findall(boolexp)

    try:
        if match:
            raise InvalidSymbols(match)
    except InvalidSymbols as err:
        err.msg
        return

    bexp_lst = list(boolexp)
    print('Symbols: ', bexp_lst)


def main():
    pass


if __name__ == '__main__':
    main()
