#!/usr/bin/env python3

import unittest
from boolsheet import BoolSheet
from boolsheet import BoolSheetSymbolError, BoolSheetOperandError


class TestBoolSheet(unittest.TestCase):
    def test_to_lst_method(self):
        """ Testa o método to_lst
        """
        data = '~(A + B)C'
        bs = BoolSheet(data)
        self.assertEqual(bs.to_lst(), ['~', '(', 'A', '+', 'B', ')', 'C'])

    def test_symbol_error(self):
        """ Testa o método to_lst com erro de símbolo
        """
        data = '~(A + B)*C'
        bs = BoolSheet(data)
        with self.assertRaises(BoolSheetSymbolError):
            bs.to_lst()

    def test_operand_error(self):
        """ Testa o método to_lst com erros de operando
        """
        data = '~(A ~+ B)C'
        bs = BoolSheet(data)
        with self.assertRaises(BoolSheetOperandError):
            bs.to_lst()

        data = '~(A + B~)C'
        bs = BoolSheet(data)
        with self.assertRaises(BoolSheetOperandError):
            bs.to_lst()

        data = '~(A ++ B)C'
        bs = BoolSheet(data)
        with self.assertRaises(BoolSheetOperandError):
            bs.to_lst()

        data = '~(+A + B)C'
        bs = BoolSheet(data)
        with self.assertRaises(BoolSheetOperandError):
            bs.to_lst()

    def test_to_graph(self):
        """ Testa o método to_graph
        """
        data = '~(A + B (AB + ~C)) D'
        bs = BoolSheet(data)
        self.assertEqual(bs.to_graph()[1], ['~', ['A', '+', 'B', ['A',
                                            'B', '+', '~', 'C']], 'D'])


if __name__ == '__main__':
    unittest.main()
