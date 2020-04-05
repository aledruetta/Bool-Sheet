#!/usr/bin/env python3

from boolsheet import BoolSheet, BoolSheetOperandError, BoolSheetSymbolError


def test():
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
    test()
