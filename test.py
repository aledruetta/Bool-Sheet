#!/usr/bin/env python3

""" Usage:

    python3 -m unittest -v test
"""

import unittest
from boolsheet import BoolSheet
from exceptions import (
        BoolSheetSymbolError,
        BoolSheetOperandError,
        BoolSheetParenthesesError,
        BoolSheetVariableError)


class TestBoolSheet(unittest.TestCase):
    def test_to_lst_method(self):
        """ Testa o método to_lst()
        """

        # Allowed expression
        result = BoolSheet('~(A + B)C').to_lst()
        self.assertEqual(result, ['~', '(', 'A', '+', 'B', ')', 'C'])

    def test_check_symbols(self):
        """ Testa o método _check_symbols()
        """

        # Check for variables
        result = BoolSheet('~(+)')
        with self.assertRaises(BoolSheetVariableError):
            result._check_symbols()

        # Not allowed symbol '*'
        result = BoolSheet('~(A + B)*C')
        with self.assertRaises(BoolSheetSymbolError):
            result._check_symbols()

    def test_check_operands(self):
        """ Testa o método _check_operands()
        """

        # Not allowed operand '~+'
        result = BoolSheet('~(A ~+ B)C')
        with self.assertRaises(BoolSheetOperandError):
            result._check_operands()

        # Not allowed operand '~)'
        result = BoolSheet('~(A + B~)C')
        with self.assertRaises(BoolSheetOperandError):
            result._check_operands()

        # Not allowed operand '++'
        result = BoolSheet('~(A ++ B)C')
        with self.assertRaises(BoolSheetOperandError):
            result._check_operands()

        # Not allowed operand '(+'
        result = BoolSheet('~(+A + B)C')
        with self.assertRaises(BoolSheetOperandError):
            result._check_operands()

        # Not allowed start with '+'
        result = BoolSheet('+~(A + B)C')
        with self.assertRaises(BoolSheetOperandError):
            result._check_operands()

        # Not allowed end with '+'
        result = BoolSheet('~(A + B)C+')
        with self.assertRaises(BoolSheetOperandError):
            result._check_operands()

        # Not allowed end with '~'
        result = BoolSheet('~(A + B)C~')
        with self.assertRaises(BoolSheetOperandError):
            result._check_operands()

    def test_check_parentheses(self):
        """ Testa o método _check_parentheses()
        """

        # Check parentheses nest misused
        result = BoolSheet('~(A ~+ B))C')
        with self.assertRaises(BoolSheetParenthesesError):
            result._check_parentheses()

        # Check parentheses nest misused
        result = BoolSheet('~)(A ~+ B)C(')
        with self.assertRaises(BoolSheetParenthesesError):
            result._check_parentheses()

    def test_to_graph(self):
        """ Testa o método to_graph()
        """

        # Correct nested expressions
        result = BoolSheet('~(A + B (AB + ~C)(CD)) D').to_graph()
        self.assertEqual(
                result, ['~', ['A', '+', 'B', ['A', 'B', '+', '~', 'C'],
                               ['C', 'D']], 'D'])


if __name__ == '__main__':
    unittest.main()
