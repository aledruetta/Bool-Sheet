#!/usr/bin/env python3

import re


class Error(Exception):
    pass


class BoolSheetSymbolError(Error):
    def __init__(self, symbols):
        self.symbols = symbols

    @property
    def msg(self):
        return 'Invalid Symbols Error: {}\n'.format(self.symbols)


class BoolSheetOperandError(Error):
    def __init__(self, operand):
        self.operand = operand

    @property
    def msg(self):
        return 'Invalid Operand Usage Error: {}\n'.format(self.operand)


class BoolSheet:
    def __init__(self, expstr):
        self.expstr = expstr.replace(' ', '')

    def to_lst(self):
        pattern_allowed = re.compile(r'[^\(\)\+~a-z]', re.IGNORECASE)
        match_allowed = pattern_allowed.findall(self.expstr)

        pattern_operand = re.compile(r'\+{2,}|~[\+\)]|\+\)', re.IGNORECASE)
        match_operand = pattern_operand.findall(self.expstr)

        if match_allowed:
            raise BoolSheetSymbolError(match_allowed)
        if match_operand:
            raise BoolSheetOperandError(match_operand)

        return list(self.expstr)

    def nest(self, symbols):
        nested = []
        i = 0

        while i < len(symbols):
            if symbols[i] == '(':
                symbols, sub = self.nest(symbols[i+1:])
                nested.append(sub)
                i = 0
            elif symbols[i] == ')':
                return symbols[i+1:], nested
            else:
                nested.append(symbols[i])
                i += 1

        return None, nested

    def to_graph(self):
        symbols = self.to_lst()
        return self.nest(symbols)


def main():
    test = 0

    test += 1
    print('Test {}: Allowed symbols'.format(test))
    try:
        exp = '(~A + B)C'
        print('Input: {}'.format(exp))
        bs = BoolSheet(exp)
        print('Expression: {}, Symbols: {}\n'.format(bs.expstr, bs.to_lst()))
    except (BoolSheetSymbolError, BoolSheetOperandError) as err:
        print(err.msg)

    test += 1
    print('Test {}: Not allowed symbols'.format(test))
    try:
        exp = '(A + B*)C ?'
        print('Input: {}'.format(exp))
        bs = BoolSheet(exp)
        print('Expression: {}, Symbols: {}\n'.format(bs.expstr, bs.to_lst()))
    except (BoolSheetSymbolError, BoolSheetOperandError) as err:
        print(err.msg)

    test += 1
    print('Test {}: Generate graph representation'.format(test))
    try:
        exp = '(~A + B)C'
        print('Input: {}'.format(exp))
        bs = BoolSheet(exp)
        print('Expression: {}, Symbols: {}\n'.format(bs.expstr, bs.to_graph()))
    except (BoolSheetSymbolError, BoolSheetOperandError) as err:
        print(err.msg)

    test += 1
    print('Test {}: Generate graph representation'.format(test))
    try:
        exp = '~(A + B + ~(C + ~D))~C'
        print('Input: {}'.format(exp))
        bs = BoolSheet(exp)
        print('Expression: {}, Symbols: {}\n'.format(bs.expstr, bs.to_graph()))
    except (BoolSheetSymbolError, BoolSheetOperandError) as err:
        print(err.msg)

    test += 1
    print('Test {}: Disjunction repetition'.format(test))
    try:
        exp = '~(A ~+++ (B~) ~+ ~C+)~C'
        print('Input: {}'.format(exp))
        bs = BoolSheet(exp)
        print('Expression: {}, Symbols: {}\n'.format(bs.expstr, bs.to_graph()))
    except (BoolSheetSymbolError, BoolSheetOperandError) as err:
        print(err.msg)


if __name__ == '__main__':
    main()
