#!/usr/bin/env python3

import re
from exceptions import (
        BoolSheetOperandError,
        BoolSheetSymbolError,
        BoolSheetVariableError,
        BoolSheetParenthesesError)

DEBUG = True


class BoolSheet:
    def __init__(self, expstr):
        self.expstr = expstr.replace(' ', '').upper()

    def _check_symbols(self):
        """ Checks variables and allowed symbols: ~, [a-z], +, ()
        """

        pattern_allowed = re.compile(r'[^\(\)\+~a-z]', re.IGNORECASE)
        match_allowed = pattern_allowed.findall(self.expstr)

        if match_allowed:
            raise BoolSheetSymbolError(match_allowed)

        pattern_variable = re.compile(r'[a-z]', re.IGNORECASE)
        match_variable = pattern_variable.search(self.expstr)

        if not match_variable:
            raise BoolSheetVariableError()

    def _check_operands(self):
        """ Checks misused operands: ~+, ~), ++, +), (+
        """

        patterns = '|'.join([
                r'^\+',         # start with '+'
                r'[~\+]$',      # end with '~' or '+'
                r'\+{2,}',      # repetition '+'
                r'~[\+\)]',     # '~' followed by '+' or ')'
                r'\+\)',        # '+' followed by ')'
                r'\(\+'         # '+' after '('
                ])

        pattern_operand = re.compile(patterns, re.IGNORECASE)
        match_operand = pattern_operand.findall(self.expstr)

        if match_operand:
            raise BoolSheetOperandError(match_operand)

    def _check_parentheses(self):
        """ Checks for parentheses match
        """

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
        """ Checks allowed symbols, misused operands and parentheses match
            and return a list of symbols and operands
        """

        self._check_symbols()
        self._check_operands()
        self._check_parentheses()

        return list(self.expstr)

    def nest(self, symbols):
        """ Nests subexpressions as a nested lists
        """

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
        """ Returns the graph representation of the expression
        """

        symbols = self.to_lst()
        return self.nest(symbols)[1]

    def pick_vars(self):
        """ Returns an alphabetically ordered list of variables
        """

        pattern_vars = re.compile(r'[A-Z]', re.IGNORECASE)
        match_vars = pattern_vars.findall(self.expstr)

        return sorted(list(set(match_vars)))

    def get_inner(self, inner):
        for exp in inner:
            if isinstance(exp, list):
                inner = self.bool_table(exp)

        return inner

    def __str__(self):
        return self.expstr


def main():
    boolexp = input('Enter your boolsheet: ')
    boolsheet = BoolSheet(boolexp)

    if DEBUG:
        try:
            print(boolsheet.expstr, '==>', boolsheet.to_graph())
        except (
                BoolSheetSymbolError,
                BoolSheetOperandError,
                BoolSheetParenthesesError,
                BoolSheetVariableError) as err:
            print(err.msg)

        print('Variables: {}'.format(''.join(boolsheet.pick_vars())))
        print(boolsheet.bool_table(boolsheet.to_graph()))


if __name__ == '__main__':
    main()
