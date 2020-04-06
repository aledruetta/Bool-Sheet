#!/usr/bin/env python3


class BoolSheetError(Exception):
    pass


class BoolSheetSymbolError(BoolSheetError):
    def __init__(self, symbols):
        self.symbols = symbols

    @property
    def msg(self):
        return 'Invalid Symbols Error: {}\n'.format(self.symbols)


class BoolSheetVariableError(BoolSheetError):
    @property
    def msg(self):
        return 'Expression Without Variables Error!\n'


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


def main():
    pass


if __name__ == '__main__':
    main()
