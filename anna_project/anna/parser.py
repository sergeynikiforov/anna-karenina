# here we combine parsers from primitives defined in combinators.py
# based on http://jayconrod.com/posts/40/a-simple-interpreter-from-scratch-in-python-part-4

from functools import reduce

from .lexer import *
from .combinators import *
from .ast import *


# binary operators precedence levels
word_exp_precedence_levels = [
    ['AND'],
    ['OR'],
]


def parse(tokens):
    """
    Top level parser for word expression

    Gets list of tokens from lexer as input, returns AST (Result obj) or None if there was a parsing error
    """
    ast = word_expression()(tokens, 0)
    return ast if ast and ast.pos == len(tokens) else None


def word_expression():
    """
    General word expression parser

    Wraps precedence() func
    """
    return precedence(word_expression_term(), word_exp_precedence_levels, process_binop)


def precedence(value_parser, precedence_levels, combine):
    """
    Combinator that handles precedence levels for word expressions

    value_parser: parser that can read basic parts of an expression (i.e. word) - `word_expression_term()`
    precedence_levels: list of lists of operators, the lower the index in the top list, the higher the op precedence level
    combine: `process_binop` - a function that takes an operator and returns a function that builds a larger expr from 2 smaller exprs
    """
    # we'll use op_parser as the right-hand operand of an Exp() call (`*`)
    def op_parser(precedence_level):
        # read any operator from the precedence_level list and apply (`^`) combine func to it
        return any_operator_in_list(precedence_level) ^ combine

    # call Exp (`*`) first with the highest precedence level
    parser = value_parser * op_parser(precedence_levels[0])

    # call `*` for other precedence levels
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser


def any_operator_in_list(ops):
    """
    Function that selects a parser that matches any operator from a given list of operators.
    Helper functions that's used in precedence function

    ops: list of operators with the same precedence level
    """
    op_parsers = [keyword(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser


def process_binop(op):
    """
    Function that constructs BinopWordExpression obj.
    Takes a reserved operator (OR, AND) and returns a function that combines expressions using this op.
    """
    return lambda l, r: BinopWordExpression(op, l, r)


# primitives
def keyword(kw):
    """Matches reserved tokens"""
    return Reserved(kw, RESERVED)


def word_expression_value():
    """
    Primitive word expression parser
    """
    return Tag(WORD) ^ (lambda i: WordExpression(i))


def process_group(parsed):
    """
    Helper function to process expr group
    """
    ((_, p), _) = parsed
    return p


def word_expression_not():
    """
    Parser for NOT expression

    Concats keyword and word_expression_term()
    Uses Lazy() to avoid infinite recursion
    """
    return keyword('NOT') + Lazy(word_expression_term) ^ (lambda parsed: NotWordExpression(parsed[1]))


def word_expression_group():
    """
    Parser for parentheses group.
    Uses overloaded `+` (which calls Concat combinator) to parse `(`, followed by word expression, followed by `)`
    Uses Lazy() to avoid infinite recursion
    """
    return keyword('(') + Lazy(word_expression) + keyword(')') ^ process_group


def word_expression_term():
    """
    word_expression_term is any basic self-contained word expression
    expression is flat in terms of precedence
    """
    return word_expression_not() | word_expression_value() | word_expression_group()
