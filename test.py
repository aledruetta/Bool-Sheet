#!/usr/bin/env python3

import unittest
from boolsheet import BoolSheet
from boolsheet import BoolSheetSymbolError, BoolSheetOperandError


class TestBoolSheet(unittest.TestCase):
    def test_to_lst_method(self):
        """ Testa o método to_lst()
        """

        # Allowed expression
        result = BoolSheet('~(A + B)C').to_lst()
        self.assertEqual(result, ['~', '(', 'A', '+', 'B', ')', 'C'])

        # Not allowed symbol '*'
        result = BoolSheet('~(A + B)*C')
        with self.assertRaises(BoolSheetSymbolError):
            result.to_lst()

        # Not allowed operand '~+'
        result = BoolSheet('~(A ~+ B)C')
        with self.assertRaises(BoolSheetOperandError):
            result.to_lst()

        # Not allowed operand '~)'
        result = BoolSheet('~(A + B~)C')
        with self.assertRaises(BoolSheetOperandError):
            result.to_lst()

        # Not allowed operand '++'
        result = BoolSheet('~(A ++ B)C')
        with self.assertRaises(BoolSheetOperandError):
            result.to_lst()

        # Not allowed operand '(+'
        result = BoolSheet('~(+A + B)C')
        with self.assertRaises(BoolSheetOperandError):
            result.to_lst()

    def test_to_graph(self):
        """ Testa o método to_graph()
        """

        # Correct nested expressions
        result = BoolSheet('~(A + B (AB + ~C)) D').to_graph()[1]
        self.assertEqual(
                result, ['~', ['A', '+', 'B', ['A', 'B', '+', '~', 'C']], 'D'])


if __name__ == '__main__':
    unittest.main()