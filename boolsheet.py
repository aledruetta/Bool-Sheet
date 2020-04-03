#!/usr/bin/env python3

import re


class Error(Exception):
    pass


class InvalidSymbols(Error):
    def __init__(self, exp):
        self.expression = exp

    @property
    def msg(self):
        print('Invalid Symbols Error: ', self.expression)


class BoolSheet:
    def __init__(self, expstr):
        self.expstr = expstr.replace(' ', '')

    def parse(self):
        pattern = re.compile(r'[^\(\)\+~a-z]', re.IGNORECASE)
        match = pattern.findall(self.expstr)

        try:
            if match:
                raise InvalidSymbols(match)
        except InvalidSymbols as err:
            err.msg
            raise

        return list(self.expstr)

    def graph(parsexp):
        pass


def main():
    try:
        exp = '(~A + B)C'
        bs = BoolSheet(exp)
        print('Input: {}'.format(exp))
        print('Expression: {}, Symbols: {}\n'.format(bs.expstr, bs.parse()))
    except InvalidSymbols:
        return

    try:
        exp = '(A + B*)C ?'
        bs = BoolSheet(exp)
        print('Input: {}'.format(exp))
        print('Expression: {}, Symbols: {}\n'.format(bs.expstr, bs.parse()))
    except InvalidSymbols:
        return


if __name__ == '__main__':
    main()
