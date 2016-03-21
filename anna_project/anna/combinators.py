# library of generic parsers that are used to write our parser for search queries
# heavily based on http://jayconrod.com/posts/38/a-simple-interpreter-from-scratch-in-python-part-2

class Result:
    """
    Every parser will return a Result object on success or None on failure.
    value: part of an abstact syntax tree
    pos: position on the next token in the input str
    """
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos

    def __repr__(self):
        return 'Result({val}, {pos})'.format(val=self.value, pos=self.pos)


class Parser:
    """
    Every parser will be a subclass of Parser and will override __call__()
    """
    def __add__(self, other):
        return Concat(self, other)

    def __mul__(self, other):
        return Exp(self, other)

    def __or__(self, other):
        return Alternate(self, other)

    def __xor__(self, function):
        return Process(self, function)


class Tag(Parser):
    """
    Primitive parser
    Matches any token which has a particular tag, i.e. Tag(WORD)
    """
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and tokens[pos][1] is self.tag:
            return Result(tokens[pos][0], pos + 1)
        else:
            return None


class Reserved(Parser):
    """
    Primitive parser
    Parses reserved words and operators, i.e. Reserved(')', RESERVED)
    """
    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and tokens[pos][0] == self.value and tokens[pos][1] is self.tag:
            return Result(tokens[pos][0], pos + 1)
        else:
            return None


class Concat(Parser):
    """
    Takes two parsers as input (left and right)
    Concat parser first applies the left parser, followed by the right parser.
    If both are successful, the result value will be a pair containing the left and right results.
    If either parser is unsuccessful, None is returned.
    example: 'word1 OR word2' -> Concat(Concat(Tag(WORD), Reserved('OR', RESERVED)), Tag(WORD))
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        # call left first
        left_result = self.left(tokens, pos)
        if left_result:
            # call right second
            right_result = self.right(tokens, left_result.pos)
            if right_result:
                # both parsers parsed successfully
                combined_value = (left_result.value, right_result.value)
                return Result(combined_value, right_result.pos)
        return None


class Alternate(Parser):
    """
    Takes two parsers as input (left and right).
    Concat parser first applies the left parser, if successfull returns the result, else tries to apply the right parser.
    If either parser is unsuccessful, None is returned.
    This parser is used when we need to decide which parser to choose from.
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        # call left, if ok return the result
        left_result = self.left(tokens, pos)
        if left_result:
            return left_result
        # left fails, try right
        else:
            right_result = self.right(tokens, pos)
            return right_result


class Exp(Parser):
    """
    Provides a workaround for the issue of infinite left-recursion for compound statements like `w1 OR w2`
    Exp takes two parsers as input.
    The first matches the actual elements of the list.
    The second matches the separators.
    On success, the separator parser must return a function which combines elements parsed on the left
    and right into a single value.
    This value is accumulated for the whole list, left to right, and is ultimately returned.
    """
    def __init__(self, parser, separator):
        self.parser = parser
        self.separator = separator

    def __call__(self, tokens, pos):
        # result stores what's been parsed so far
        result = self.parser(tokens, pos)

        def process_next(parsed):
            (sepfunc, right) = parsed
            return sepfunc(result.value, right)

        # applies `separator` first, followed by `parser`
        next_parser = self.separator + self.parser ^ process_next

        next_result = result
        while next_result:
            next_result = next_parser(tokens, result.pos)
            if next_result:
                result = next_result
        return result


class Process(Parser):
    """
    Input to Process is a parser and a function.
    When the parser is applied successfully, the result value is passed to the function.
    The return value from the function is returned instead of the original value.
    """
    def __init__(self, parser, function):
        self.parser = parser
        self.function = function

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            result.value = self.function(result.value)
            return result


class Lazy(Parser):
    """
    Lazy allows building recursive parsers
    Takes a zero-argument function which returns a parser.
    Lazy will not call the function to get the parser until it's applied.
    """
    def __init__(self, parser_func):
        self.parser = None
        self.parser_func = parser_func

    def __call__(self, tokens, pos):
        if not self.parser:
            self.parser = self.parser_func()
        return self.parser(tokens, pos)
