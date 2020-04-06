#!/usr/bin/env python3

import re


class BoolSheetError(Exception):
    pass


class BoolSheetSymbolError(BoolSheetError):
    def __init__(self, symbols):
        self.symbols = symbols

    @property
    def msg(self):
        return 'Invalid Symbols Error: {}\n'.format(self.symbols)


class BoolSheetOperandError(BoolSheetError):
    def __init__(self, operand):
        self.operand = operand

    @property
    def msg(self):
        return 'Invalid Operand Usage Error: {}\n'.format(self.operand)


class BoolSheetParenthesesError(BoolSheetError):
    def __init__(self, pars):
        self.pars = pars

    @property
    def msg(self):
        return 'Invalid Parentheses Error: {}\n'.format(self.pars)


class BoolSheet:
    def __init__(self, expstr):
        self.expstr = expstr.replace(' ', '').upper()

    def _check_symbols(self):
        """ check allowed symbols: ~, [a-z], +, ()
        """

        pattern_allowed = re.compile(r'[^\(\)\+~a-z]', re.IGNORECASE)
        match_allowed = pattern_allowed.findall(self.expstr)

        if match_allowed:
            raise BoolSheetSymbolError(match_allowed)

    def _check_operands(self):
        """ check misused operands: ~+, ~), ++, +), (+
        """

        pattern_operand = re.compile(r'\+{2,}|~[\+\)]|\+\)|\(\+',
                                     re.IGNORECASE)
        match_operand = pattern_operand.findall(self.expstr)

        if match_operand:
            raise BoolSheetOperandError(match_operand)

    def _check_parentheses(self):
        pars = ''.join([p for p in self.expstr if p in '()'])

        count = 0
        for p in pars:
            if p == '(':
                count += 1
            else:
                count -= 1
            if count < 0:
                raise BoolSheetParenthesesError(pars)

        if count != 0:
            raise BoolSheetParenthesesError(pars)

    def to_lst(self):
        """ Check allowed symbols, misused operands and parentheses match
        """

        self._check_symbols()
        self._check_operands()
        self._check_parentheses()

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
        return self.nest(symbols)[1]

    def __str__(self):
        return self.expstr


def main():
    boolexp = input('Enter your boolsheet: ')
    boolsheet = BoolSheet(boolexp)

    try:
        print(boolsheet.expstr, '==>', boolsheet.to_graph())
    except (BoolSheetSymbolError, BoolSheetOperandError,
            BoolSheetParenthesesError) as err:
        print(err.msg)


if __name__ == '__main__':
    main()
