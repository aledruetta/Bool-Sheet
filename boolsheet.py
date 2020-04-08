#!/usr/bin/env python3

import re
from exceptions import (
        BoolSheetOperandError,
        BoolSheetSymbolError,
        BoolSheetVariableError,
        BoolSheetParenthesesError)

DEBUG = True


class BoolSheet:
    """ This class ofers a bunch of methods for manipulating a
        boolean expression and its true table
    """

    def __init__(self, expstr):
        """ Initialize class attributes: expstr
        """

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

    def nest_parentheses(self, symbols):
        """ Nests subexpressions enclosed in parentheses as lists
        """

        nested = []
        i = 0

        while i < len(symbols):
            if symbols[i] == '(':
                symbols, sub = self.nest_parentheses(symbols[i+1:])
                nested.append(sub)
                i = 0
            elif symbols[i] == ')':
                return symbols[i+1:], nested
            else:
                nested.append(symbols[i])
                i += 1

        return None, nested

    def complement_vars(self, symbols):
        """ Nests complemented variables as lists
        """

        i = 0

        while i < len(symbols):
            if isinstance(symbols[i], list):
                symbols[i] = self.complement_vars(symbols[i])
            elif symbols[i] == '~' \
                    and isinstance(symbols[i+1], str) \
                    and symbols[i+1].isalpha():
                symbols[i] = [symbols[i], symbols[i+1]]
                symbols.pop(i+1)

            i += 1

        return symbols

    def to_graph(self):
        """ Returns the graph representation of the expression
        """

        symbols = self.to_lst()
        pars = self.nest_parentheses(symbols)[1]
        comp = self.complement_vars(pars)

        return comp

    def pick_vars(self):
        """ Returns an alphabetically ordered list of variables
        """

        pattern_vars = re.compile(r'[A-Z]', re.IGNORECASE)
        match_vars = pattern_vars.findall(self.expstr)

        return sorted(list(set(match_vars)))

    def replace_var(self, term):
        """
        """
        pass

    def table(self):
        """
        """
        pass

    def get_inner(self, inner=None):
        """ Returns the last innermost subexpression
        """

        if inner is None:
            inner = self.to_graph()

        for exp in inner:
            if isinstance(exp, list):
                inner = self.get_inner(exp)

        return inner

    def __str__(self):
        return self.expstr


def main():
    boolexp = input('Enter your boolsheet: ')
    bs = BoolSheet(boolexp)

    if DEBUG:
        try:
            print(bs.expstr, '==>', bs.to_lst())
        except (
                BoolSheetSymbolError,
                BoolSheetOperandError,
                BoolSheetParenthesesError,
                BoolSheetVariableError) as err:
            print(err.msg)

        print('Variables: '
              '{}'.format(''.join(bs.pick_vars())))
        print(bs.to_graph())


if __name__ == '__main__':
    main()
