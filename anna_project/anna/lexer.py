# heavily based on http://jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python-part-1

import sys
import re

RESERVED = 'RESERVED'
WORD     = 'WORD'

# list of tuples of regexes and corresponding tags for lex function
token_exprs = [
    (r'[\s]+',          None),     # ignore whitespace
    (r'\(',             RESERVED), # we need brackets for precedence
    (r'\)',             RESERVED), # we need brackets for precedence
    (r'AND',            RESERVED), # represents logical AND op
    (r'OR',             RESERVED), # represents logical OR op
    (r'NOT',            RESERVED), # represents logical NOT op
    (r'[^\s\(\)]+',     WORD),     # matches a single word for search
]


def lex(input_str, token_exprs=token_exprs):
    """
    Generic lexer that takes a list of regular expressions and their tags.
    For each expression, it will check whether the input text matches a token at the current position.
    If a match is found, the matching text is extracted into a token, along with the regular expression's tag.
    If the regular expression has no tag associated with it (the tag is None), the text is discarded.
    The process is repeated until there are no more chars left to match.

    Token is a tuple: a value (the string it represents) and a tag (to indicate what kind of token it is).
    The parser will use both to decide how to create the AST.
    """
    pos = 0
    tokens = []
    # scan the input by matched chunks
    while pos < len(input_str):
        match = None
        # try to match all tokens, the order DOES matter
        # we should put the most specific expressions first
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(input_str, pos)
            # we found a match
            if match:
                text = match.group(0)
                # add to list of tokens only if there's a tag associated with it
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        # no matched tokens found - illegal expression
        # else - get to the position past the matched chunk of input str
        if not match:
            sys.exit('Illegal character: {}'.format(input_str[pos]))
        else:
            pos = match.end(0)
    return tokens


def anna_lexer(input_str):
    """
    Wrapper function for the main lexer function
    """
    return lex(input_str, token_exprs)
