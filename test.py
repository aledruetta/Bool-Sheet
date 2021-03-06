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
        """ Test the method to_lst()
        """

        # Allowed expression
        result = BoolSheet('~(A + B)C').to_lst()
        self.assertEqual(result, ['~', '(', 'A', '+', 'B', ')', 'C'])

    def test_check_symbols(self):
        """ Test the method _check_symbols()
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
        """ Test the method _check_operands()
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
        """ Test the method _check_parentheses()
        """

        # Check parentheses nest misused
        result = BoolSheet('~(A ~+ B))C')
        with self.assertRaises(BoolSheetParenthesesError):
            result._check_parentheses()

        # Check parentheses nest misused
        result = BoolSheet('~)(A ~+ B)C(')
        with self.assertRaises(BoolSheetParenthesesError):
            result._check_parentheses()

    def test_to_lst(self):
        """ Test the method to_lst()
        """

        # Test string to list convertion
        result = BoolSheet('~(A + B)CA').to_lst()
        self.assertEqual(result, ['~', '(', 'A', '+', 'B', ')', 'C', 'A'])

    def test_nest_parentheses(self):
        """ Test the method nest_parentheses()
        """

        # Test correct nested parentheses
        bs = BoolSheet('~(A + B)(CA)')
        result = bs.nest_parentheses(bs.expstr)[1]
        self.assertEqual(result, ['~', ['A', '+', 'B'], ['C', 'A']])

    def test_complement(self):
        """ Test the method complement()
        """

        # Test complemented variables
        bs = BoolSheet('~(A + ~B) ~CA')
        result = bs.complement(bs.nest_parentheses(bs.to_lst())[1])
        self.assertEqual(
                result, [['~', ['A', '+', ['~', 'B']]], ['~', 'C'], 'A'])

    def test_to_graph(self):
        """ Test the method to_graph()
        """

        # Correct nested expressions
        result = BoolSheet('~(A + B (AB + ~C)(CD)) D').to_graph()
        self.assertEqual(
                result, [['~', ['A', '+', 'B', ['A', 'B', '+', ['~', 'C']],
                         ['C', 'D']]], 'D'])

    def test_pick_vars(self):
        """ Test the method pick_vars()
        """

        # Pick boolean variables
        result = BoolSheet('~(A + B)CA').pick_vars()
        self.assertEqual(result, ['A', 'B', 'C'])

    def test_get_inner(self):
        """ Test the method get_inner()
        """

        # Get the first innermost
        result = BoolSheet('~(A + B (AB + ~C)(CD)) D').get_inner()
        self.assertEqual(result, ['C', 'D'])


if __name__ == '__main__':
    unittest.main()
