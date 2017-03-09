import unittest

from kimi.parser import parse
from kimi.environments import standard_env
from kimi.evaluator import evaluate
from kimi.tokenizer import tokenize
from kimi.exceptions import *


def execute(program):
    '''Take a Kimi program as a string. Tokenize the program, parse the tokens into a tree,
    then evaluate the tree. Return the result, or an error message.'''
    return evaluate(parse(tokenize(program)), standard_env())


class TestTokenize(unittest.TestCase):

    def test_numbers(self):
        # Valid number literals
        self.assertEqual(tokenize("3"), [('literal', 3)])
        self.assertEqual(tokenize("+3"), [('literal', 3)])
        self.assertEqual(tokenize("-4"), [('literal', -4)])
        # Not valid (considered symbols)
        self.assertEqual(tokenize("2.5"), [('symbol', '2.5')])
        self.assertEqual(tokenize("-2-4"), [('symbol', '-2-4')])

    def test_strings(self):
        # Valid string literals
        self.assertEqual(tokenize('"some string"'), [('literal', 'some string')])
        self.assertEqual(tokenize('"some (string)"'), [('literal', 'some (string)')])
        self.assertEqual(tokenize('''"some 'string'"'''), [('literal', "some 'string'")])
        # Not valid
        self.assertEqual(tokenize('"some \"string\""'), [('literal', 'some '), ('symbol', 'string'), ('literal', '')])

    def test_symbols(self):
        # Valid symbols
        self.assertEqual(tokenize("x"), [('symbol', 'x')])
        self.assertEqual(tokenize("123abc123"), [('symbol', '123abc123')])
        self.assertEqual(tokenize("--thing--"), [('symbol', '--thing--')])
        # Not valid
        self.assertEqual(tokenize("x y"), [('symbol', 'x'), ('symbol', 'y')])
        self.assertEqual(tokenize("z(x)"), [('symbol', 'z'), ('opening', None), ('symbol', 'x'), ('closing', None)])


    def test_apply(self):
        self.assertEqual(tokenize("(- 1 2)"), [('opening', None), ('symbol', '-'), ('literal', 1), ('literal', 2), ('closing', None)])
        self.assertEqual(tokenize("(define square (lambda x (* x x)))"),
            [('opening', None), ('symbol', 'define'), ('symbol', 'square'),
             ('opening', None), ('symbol', 'lambda'), ('symbol', 'x'),
             ('opening', None), ('symbol', '*'), ('symbol', 'x'), ('symbol', 'x'),
             ('closing', None), ('closing', None), ('closing', None)])

    def test_syntax_errors(self):
        self.assertRaises(KimiSyntaxError, tokenize, ("( + 1 2 )"))
        self.assertRaises(KimiSyntaxError, tokenize, ("(((+ 1 2)))"))
        self.assertRaises(KimiSyntaxError, tokenize, (")+ 1 2("))
        self.assertRaises(KimiSyntaxError, tokenize, ("+ 1 2()"))
        # self.assertEqual(tokenize("(+ 1 2) (+ 3 4)"),
        #     [('opening', None), ('symbol', '+'), ('literal', 1), ('literal', 2), ('closing', None),
        #      ('opening', None), ('symbol', '+'), ('literal', 3), ('literal', 4), ('closing', None)] )

class TestParse(unittest.TestCase):

    def test_parse(self):
        self.assertEqual(parse(tokenize("(+ 1 2)")),
             {'type': 'apply',
              'operator': {'type': 'symbol', 'value': '+'},
              'arguments': ({'type': 'literal', 'value': 1},
                            {'type': 'literal', 'value': 2})})
        self.assertEqual(parse(tokenize("(define square (lambda x (* x x)))")),
             {'type': 'apply',
              'operator': {'type': 'symbol', 'value': 'define'},
              'arguments': ({'type': 'symbol', 'value': 'square'},
                            {'type': 'apply',
                             'operator': {'type': 'symbol', 'value': 'lambda'},
                             'arguments': ({'type': 'symbol', 'value': 'x'},
                                           {'type': 'apply',
                                            'operator': {'type': 'symbol', 'value': '*'},
                                            'arguments': ({'type': 'symbol', 'value': 'x'},
                                                          {'type': 'symbol', 'value': 'x'})})})})


class TestExecute(unittest.TestCase):

    def test_atoms(self):
        self.assertEqual(execute("-10"), -10)
        self.assertEqual(execute("true"), True)
        self.assertEqual(execute('"string"'), "string")

    def test_nesting(self):
        self.assertEqual(execute("(| (& true false) (! true))"), False)
        self.assertEqual(execute("(+ (* 2 3) (- 4 2))"), 8)

    @unittest.expectedFailure
    def test_bad_program(self):
        self.assertRaises(SystemExit, execute, ("(+ (1) (2))"))
        self.assertEqual(execute("(+ 1 2) (+ 3 4)"), 7) #or throw error

class TestBuiltins(unittest.TestCase):

    def test_arithmetic(self):
        # Addition
        self.assertEqual(execute("(+ 1 2)"), 3)
        self.assertEqual(execute("(+ -1 2)"), 1)
        # Subtraction
        self.assertEqual(execute("(- 2 1)"), 1)
        self.assertEqual(execute("(- 1 -2)"), 3)
        # Multiplication
        self.assertEqual(execute("(* 2 4)"), 8)
        self.assertEqual(execute("(* 3 -2)"), -6)
        # Floor division
        self.assertEqual(execute("(/ 6 2)"), 3)
        self.assertEqual(execute("(/ 7 2)"), 3)
        self.assertEqual(execute("(/ 1 2)"), 0)
        self.assertEqual(execute("(/ 6 -2)"), -3)
        self.assertEqual(execute("(/ -3 -2)"), 1)
        # Modulo
        self.assertEqual(execute("(% 7 2)"), 1)
        self.assertEqual(execute("(% 6 -4)"), -2)
        self.assertEqual(execute("(% 2 3)"), 2)

    def test_logic(self):
        # And
        self.assertEqual(execute("(& true true)"), True)
        self.assertEqual(execute("(& true false)"), False)
        self.assertEqual(execute("(& false true)"), False)
        self.assertEqual(execute("(& false false)"), False)
        # Or
        self.assertEqual(execute("(| true true)"), True)
        self.assertEqual(execute("(| true false)"), True)
        self.assertEqual(execute("(| false true)"), True)
        self.assertEqual(execute("(| false false)"), False)
        # Not
        self.assertEqual(execute("(! true)"), False)
        self.assertEqual(execute("(! false)"), True)

    def test_equality(self):
        self.assertEqual(execute("(= 1 1)"), True)
        self.assertEqual(execute("(= 1 2)"), False)
        self.assertEqual(execute('(= "yes" "yes")'), True)
        self.assertEqual(execute('(= "yes" "no")'), False)
        self.assertEqual(execute("(= false false)"), True)
        self.assertEqual(execute("(= true false)"), False)

    def test_comparison(self):
        # Greater than
        self.assertEqual(execute("(> 2 1)"), True)
        self.assertEqual(execute("(> 2 2)"), False)
        self.assertEqual(execute("(> 1 2)"), False)
        # Less than
        self.assertEqual(execute("(< 2 1)"), False)
        self.assertEqual(execute("(< 2 2)"), False)
        self.assertEqual(execute("(< 1 2)"), True)
        # Greater or equal
        self.assertEqual(execute("(>= 2 1)"), True)
        self.assertEqual(execute("(>= 2 2)"), True)
        self.assertEqual(execute("(>= 1 2)"), False)
        # Less or equal
        self.assertEqual(execute("(<= 2 1)"), False)
        self.assertEqual(execute("(<= 2 2)"), True)
        self.assertEqual(execute("(<= 1 2)"), True)

    def test_lists(self):
        self.assertEqual(execute("(prepend 1 (prepend 2 nil))"), (1, (2, None)))
        self.assertEqual(execute("(list 1 2)"), (1, (2, None)))
        self.assertEqual(execute("(first (list 1 2))"), 1)
        self.assertEqual(execute("(rest (list 1 2))"), (2, None))


class TestSpecialForms(unittest.TestCase):

    def test_do(self):
        self.assertEqual(execute("(do (> 4 3))"), True)
        self.assertEqual(execute("(do (+ 1 2) (+ 3 4))"), 7)

    def test_lambda(self):
        self.assertTrue(callable(execute("(lambda x (* x x))")))
        self.assertEqual(execute("((lambda x (* x x)) 2)"), 4)
        self.assertEqual(execute("((lambda a b (! (& a b))) true false)"), True)
        self.assertEqual(execute("((lambda a ((lambda y (- a y)) 3)) 7)"), 4)
    #
    def test_define(self):
        self.assertEqual(execute("(do (define x 1) (+ x x))"), 2)

    def test_if(self):
        self.assertEqual(execute("(if true 1 2)"), 1)
        self.assertEqual(execute("(if false 1 2)"), 2)
        self.assertRaises(KimiTypeError, execute, "(if 1 2 3)")


if __name__ == '__main__':
    unittest.main()
