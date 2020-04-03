#!/usr/bin/env python3

import re


class Error(Exception):
    pass


class InvalidSymbols(Error):
    def __init__(self, symbols):
        self.symbols = symbols

    @property
    def msg(self):
        return 'Invalid Symbols Error: {}'.format(self.symbols)


class BoolSheet:
    def __init__(self, expstr):
        self.expstr = expstr.replace(' ', '')

    def to_lst(self):
        pattern = re.compile(r'[^\(\)\+~a-z]', re.IGNORECASE)
        match = pattern.findall(self.expstr)

        if match:
            raise InvalidSymbols(match)

        return list(self.expstr)

    def graph(parsexp):
        pass


def main():
    try:
        exp = '(~A + B)C'
        print('Input: {}'.format(exp))
        bs = BoolSheet(exp)
        print('Expression: {}, Symbols: {}\n'.format(bs.expstr, bs.to_lst()))
    except InvalidSymbols as err:
        print(err.msg)
        return

    try:
        exp = '(A + B*)C ?'
        print('Input: {}'.format(exp))
        bs = BoolSheet(exp)
        print('Expression: {}, Symbols: {}\n'.format(bs.expstr, bs.to_lst()))
    except InvalidSymbols as err:
        print(err.msg)
        return


if __name__ == '__main__':
    main()
